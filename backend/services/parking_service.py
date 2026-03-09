"""
ARCHIVO: services/parking_service.py

SERVICIO DE ESTACIONAMIENTO

Encapsula toda la logica de negocio del sistema de estacionamiento:
consulta de espacios, reservas, ocupacion, liberacion y expiracion.

Extrae la logica pesada de app.py para mantener los endpoints limpios
y facilitar pruebas unitarias.
"""

import math
from datetime import datetime, timedelta
from models import db, ParkingSpace, ParkingSection, ParkingHistory


class ParkingService:
    """
    SERVICIO DE ESTACIONAMIENTO

    Gestiona el ciclo de vida completo de los espacios de estacionamiento:
    consulta, reserva, ocupacion, liberacion y verificacion de expiraciones.
    """

    # COORDENADAS GPS DE CADA SECCION DEL ESTACIONAMIENTO
    SECTION_COORDS = {
        'Seccion 1': {'lat': 19.329415, 'lng': -99.111664},
        'Seccion 2': {'lat': 19.329622, 'lng': -99.111354},
        'Seccion 3': {'lat': 19.329827, 'lng': -99.110991},
        'Seccion 4': {'lat': 19.329246, 'lng': -99.111603},
    }

    # DISTANCIA MAXIMA EN METROS PARA MARCAR COMO OCUPADO
    MAX_OCCUPY_DISTANCE = 50

    @staticmethod
    def _haversine(lat1, lng1, lat2, lng2):
        """
        CALCULAR DISTANCIA HAVERSINE

        Calcula la distancia en metros entre dos coordenadas GPS.
        """
        R = 6371000  # Radio de la Tierra en metros
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlam = math.radians(lng2 - lng1)

        a = math.sin(dphi / 2) ** 2 + \
            math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def validate_user_distance(self, user_lat, user_lng, section_name):
        """
        VALIDAR DISTANCIA DEL USUARIO A LA SECCION

        Verifica que el usuario este a menos de 50 metros de la seccion
        del estacionamiento correspondiente.

        Argumentos:
            user_lat: Latitud del usuario
            user_lng: Longitud del usuario
            section_name: Nombre de la seccion (ej. 'Seccion 1')

        Retorna:
            Tupla (valido: bool, mensaje: str, distancia: float)
        """
        coords = self.SECTION_COORDS.get(section_name)
        if not coords:
            return True, "Seccion sin coordenadas configuradas", 0

        distance = self._haversine(user_lat, user_lng, coords['lat'], coords['lng'])

        if distance > self.MAX_OCCUPY_DISTANCE:
            return False, (
                f"Debes estar a menos de 50 metros de {section_name} "
                f"para marcar este espacio como ocupado. "
                f"Distancia actual: {round(distance)}m."
            ), distance

        return True, "Distancia valida", distance

    def validate_user_active_space(self, user_boleta):
        """
        VALIDAR ESPACIO ACTIVO DEL USUARIO

        Verifica si el usuario ya tiene un espacio reservado u ocupado.

        Argumentos:
            user_boleta: Boleta del usuario

        Retorna:
            Tupla (tiene_activo: bool, mensaje: str, espacio: ParkingSpace o None)
        """
        active_space = ParkingSpace.query.filter(
            ((ParkingSpace.status == 'reserved') & (ParkingSpace.reserved_by == user_boleta)) |
            ((ParkingSpace.status == 'occupied') & (ParkingSpace.occupied_by == user_boleta))
        ).first()

        if active_space:
            tipo = "reserva activa" if active_space.status == 'reserved' else "coche estacionado"
            return True, (
                f"Solo puedes tener un lugar reservado u ocupado a la vez. "
                f"Ya tienes un(a) {tipo} en el espacio {active_space.space_number}."
            ), active_space

        return False, "Sin espacio activo", None

    def check_expired_reservations(self):
        """
        VERIFICAR RESERVAS VENCIDAS

        Libera automaticamente las reservas caducadas y registra
        la accion en el historial.
        """
        now = datetime.now()
        try:
            expired_spaces = ParkingSpace.query.filter(
                ParkingSpace.status == 'reserved',
                ParkingSpace.reservation_expires_at != None,
                ParkingSpace.reservation_expires_at < now
            ).all()

            for space in expired_spaces:
                history = ParkingHistory(
                    space_id=space.id,
                    user_boleta=space.reserved_by,
                    action='expire',
                    previous_status='reserved',
                    new_status='available',
                    timestamp=now
                )
                db.session.add(history)

                space.status = 'available'
                space.reserved_by = None
                space.reserved_at = None
                space.reservation_expires_at = None

            if expired_spaces:
                db.session.commit()

        except Exception as e:
            print(f"[PARKING] Error verificando expiraciones: {e}")

    def get_all_spaces(self):
        """
        OBTENER TODOS LOS ESPACIOS

        Devuelve todos los espacios agrupados por seccion con estadisticas.

        Retorna:
            Diccionario con totales globales y lista de secciones con sus espacios.
        """
        self.check_expired_reservations()

        sections = ParkingSection.query.order_by(ParkingSection.id).all()
        spaces = ParkingSpace.query.all()

        result_sections = []
        for sec in sections:
            sec_spaces = [s for s in spaces if s.section_id == sec.id]
            sec_spaces.sort(key=lambda x: x.id)

            sec_available = sum(1 for s in sec_spaces if s.status == 'available')
            sec_occupied = sum(1 for s in sec_spaces if s.status == 'occupied')
            sec_reserved = sum(1 for s in sec_spaces if s.status == 'reserved')

            result_sections.append({
                "id": sec.id,
                "name": sec.name,
                "total_spaces": sec.total_spaces,
                "map_image_url": sec.map_image_url,
                "stats": {
                    "available": sec_available,
                    "occupied": sec_occupied,
                    "reserved": sec_reserved
                },
                "spaces": [s.to_dict() for s in sec_spaces]
            })

        total_spaces = sum(s.total_spaces for s in sections)
        available = sum(1 for s in spaces if s.status == 'available')
        occupied = sum(1 for s in spaces if s.status == 'occupied')
        reserved = sum(1 for s in spaces if s.status == 'reserved')

        return {
            "total": total_spaces,
            "available": available,
            "occupied": occupied,
            "reserved": reserved,
            "sections": result_sections
        }

    def get_space(self, space_id):
        """
        OBTENER ESPACIO INDIVIDUAL

        Retorna los datos de un espacio especifico o None si no existe.
        """
        self.check_expired_reservations()
        return ParkingSpace.query.get(space_id)

    def update_space_status(self, space_id, new_status, user_boleta, user_lat=None, user_lng=None):
        """
        ACTUALIZAR ESTADO DE ESPACIO

        Cambia el estado de un cajon aplicando las reglas de negocio.

        Argumentos:
            space_id: ID del espacio
            new_status: Nuevo estado ('available', 'reserved', 'occupied')
            user_boleta: Boleta del usuario que realiza la accion
            user_lat: Latitud del usuario (requerida para 'occupied')
            user_lng: Longitud del usuario (requerida para 'occupied')

        Retorna:
            Tupla (exito: bool, resultado: dict o str, codigo_http: int)
        """
        self.check_expired_reservations()

        if not user_boleta:
            return False, "Falta la identificacion del usuario (user_boleta)", 400

        if new_status not in ['available', 'occupied', 'reserved']:
            return False, "Estado invalido", 400

        space = ParkingSpace.query.get(space_id)
        if not space:
            return False, "Espacio no encontrado", 404

        now = datetime.now()
        previous_status = space.status

        # REGLA 1: RESERVA DE ESPACIO
        if new_status == 'reserved':
            if space.status != 'available':
                return False, "El espacio no esta disponible", 400

            # Validar limite: solo un espacio activo por usuario
            has_active, msg, _ = self.validate_user_active_space(user_boleta)
            if has_active:
                return False, msg, 403

            # Validar cooldown post-cancelacion (1 hora)
            one_hour_ago = now - timedelta(hours=1)
            cooldown = ParkingHistory.query.filter(
                ParkingHistory.space_id == space_id,
                ParkingHistory.user_boleta == user_boleta,
                ParkingHistory.action == 'free',
                ParkingHistory.timestamp >= one_hour_ago
            ).first()
            if cooldown:
                return False, "Por politicas anti-monopolio, debes esperar 1 hora para reservar este mismo lugar nuevamente.", 403

            space.status = 'reserved'
            space.reserved_by = user_boleta
            space.reserved_at = now
            space.reservation_expires_at = now + timedelta(minutes=10)

            history = ParkingHistory(
                space_id=space.id, user_boleta=user_boleta,
                action='reserve', previous_status=previous_status,
                new_status=new_status, timestamp=now
            )
            db.session.add(history)

        # REGLA 2: OCUPACION
        elif new_status == 'occupied':
            if space.status == 'occupied':
                return False, "El espacio ya esta ocupado", 400
            if space.status == 'reserved' and space.reserved_by != user_boleta:
                return False, "El espacio esta reservado por alguien mas.", 403

            # Validar limite: solo un espacio activo por usuario
            # (excepto si esta convirtiendo su propia reserva en ocupado)
            if space.status != 'reserved' or space.reserved_by != user_boleta:
                has_active, msg, _ = self.validate_user_active_space(user_boleta)
                if has_active:
                    return False, msg, 403

            # Validar distancia: debe estar a menos de 50m de la seccion
            if user_lat is not None and user_lng is not None:
                section = ParkingSection.query.get(space.section_id)
                if section:
                    valid, msg, dist = self.validate_user_distance(user_lat, user_lng, section.name)
                    if not valid:
                        return False, msg, 403

            space.status = 'occupied'
            space.occupied_by = user_boleta
            space.occupied_at = now
            space.reserved_by = None
            space.reserved_at = None
            space.reservation_expires_at = None

            history = ParkingHistory(
                space_id=space.id, user_boleta=user_boleta,
                action='occupy', previous_status=previous_status,
                new_status=new_status, timestamp=now
            )
            db.session.add(history)

        # REGLA 3: LIBERACION
        elif new_status == 'available':
            if space.status == 'available':
                return False, "El espacio ya esta libre", 400
            if space.status == 'occupied' and space.occupied_by != user_boleta:
                return False, "No puedes liberar un espacio ajeno", 403
            if space.status == 'reserved' and space.reserved_by != user_boleta:
                return False, "No puedes liberar la reserva de alguien mas", 403

            space.status = 'available'
            space.occupied_by = None
            space.occupied_at = None
            space.reserved_by = None
            space.reserved_at = None
            space.reservation_expires_at = None

            history = ParkingHistory(
                space_id=space.id, user_boleta=user_boleta,
                action='free', previous_status=previous_status,
                new_status=new_status, timestamp=now
            )
            db.session.add(history)

        db.session.commit()
        return True, space.to_dict(), 200

    def get_stats(self):
        """
        OBTENER ESTADISTICAS

        Genera metricas globales y por seccion del estacionamiento.
        """
        total = ParkingSpace.query.count()
        available = ParkingSpace.query.filter_by(status='available').count()
        occupied = ParkingSpace.query.filter_by(status='occupied').count()
        reserved = ParkingSpace.query.filter_by(status='reserved').count()

        sections = {}
        all_sections = ParkingSection.query.all()
        for sec in all_sections:
            section_total = sec.total_spaces
            section_available = ParkingSpace.query.filter_by(section_id=sec.id, status='available').count()
            section_occupied = ParkingSpace.query.filter_by(section_id=sec.id, status='occupied').count()
            section_reserved = ParkingSpace.query.filter_by(section_id=sec.id, status='reserved').count()

            sections[sec.name] = {
                "total": section_total,
                "available": section_available,
                "occupied": section_occupied,
                "reserved": section_reserved,
                "occupancy_rate": round((section_occupied / section_total * 100), 1) if section_total > 0 else 0
            }

        return {
            "total": total,
            "available": available,
            "occupied": occupied,
            "reserved": reserved,
            "occupancy_rate": round((occupied / total * 100), 1) if total > 0 else 0,
            "sections": sections
        }

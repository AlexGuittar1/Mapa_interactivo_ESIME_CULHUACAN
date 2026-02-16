"""
Parking API Endpoints
Agregar estos endpoints al archivo app.py después de los endpoints existentes
"""

# ==================== PARKING ENDPOINTS ====================

@app.route("/api/parking/spaces", methods=["GET"])
def get_parking_spaces():
    """Obtener todos los espacios de estacionamiento con filtros opcionales"""
    try:
        # Parámetros de filtro
        section = request.args.get('section')  # A, B, C
        status = request.args.get('status')    # available, occupied, reserved
        sort_by = request.args.get('sort_by', 'space_number')  # space_number, distance_to_building_X
        
        # Query base
        query = ParkingSpace.query
        
        # Aplicar filtros
        if section:
            query = query.filter_by(section=section.upper())
        if status:
            query = query.filter_by(status=status)
        
        # Ordenar
        if sort_by == 'space_number':
            query = query.order_by(ParkingSpace.space_number)
        elif sort_by.startswith('distance_to_building_'):
            building_num = sort_by.split('_')[-1]
            if building_num in ['1', '2', '3']:
                query = query.order_by(getattr(ParkingSpace, f'distance_to_building_{building_num}'))
        
        spaces = query.all()
        
        # Calcular estadísticas
        total = len(spaces)
        available = sum(1 for s in spaces if s.status == 'available')
        occupied = sum(1 for s in spaces if s.status == 'occupied')
        reserved = sum(1 for s in spaces if s.status == 'reserved')
        
        return jsonify({
            "total": total,
            "available": available,
            "occupied": occupied,
            "reserved": reserved,
            "spaces": [space.to_dict() for space in spaces]
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/parking/spaces/<int:space_id>", methods=["GET"])
def get_parking_space(space_id):
    """Obtener detalles de un espacio específico"""
    try:
        space = ParkingSpace.query.get(space_id)
        if not space:
            return jsonify({"error": "Espacio no encontrado"}), 404
        
        return jsonify(space.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/parking/reserve", methods=["POST"])
def reserve_parking():
    """Reservar un espacio de estacionamiento"""
    try:
        data = request.get_json()
        space_id = data.get('space_id')
        user_boleta = data.get('user_boleta')
        duration_minutes = data.get('duration_minutes', 15)  # Default 15 minutos
        
        if not space_id or not user_boleta:
            return jsonify({"error": "Faltan parámetros requeridos"}), 400
        
        # Verificar que el espacio existe y está disponible
        space = ParkingSpace.query.get(space_id)
        if not space:
            return jsonify({"error": "Espacio no encontrado"}), 404
        
        if space.status != 'available':
            return jsonify({"error": f"Espacio no disponible (estado: {space.status})"}), 400
        
        # Verificar que el usuario existe
        user = Alumno.query.filter_by(boleta=user_boleta).first()
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        # Calcular tiempo de expiración
        from datetime import datetime, timedelta
        now = datetime.now()
        expires_at = now + timedelta(minutes=duration_minutes)
        
        # Actualizar espacio
        space.status = 'reserved'
        space.reserved_by = user_boleta
        space.reserved_at = now
        space.reservation_expires_at = expires_at
        
        # Crear registro de reserva
        reservation = ParkingReservation(
            space_id=space_id,
            user_boleta=user_boleta,
            expires_at=expires_at,
            status='active'
        )
        
        # Crear registro en historial
        history = ParkingHistory(
            space_id=space_id,
            user_boleta=user_boleta,
            action='reserve'
        )
        
        db.session.add(reservation)
        db.session.add(history)
        db.session.commit()
        
        return jsonify({
            "message": "Reserva exitosa",
            "reservation": reservation.to_dict(),
            "space": space.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/api/parking/occupy", methods=["POST"])
def occupy_parking():
    """Marcar un espacio como ocupado"""
    try:
        data = request.get_json()
        space_id = data.get('space_id')
        user_boleta = data.get('user_boleta')
        
        if not space_id or not user_boleta:
            return jsonify({"error": "Faltan parámetros requeridos"}), 400
        
        space = ParkingSpace.query.get(space_id)
        if not space:
            return jsonify({"error": "Espacio no encontrado"}), 404
        
        # Verificar que el espacio está disponible o reservado por este usuario
        if space.status == 'occupied':
            return jsonify({"error": "Espacio ya ocupado"}), 400
        
        if space.status == 'reserved' and space.reserved_by != user_boleta:
            return jsonify({"error": "Espacio reservado por otro usuario"}), 400
        
        # Si había una reserva activa, marcarla como completada
        if space.status == 'reserved':
            active_reservation = ParkingReservation.query.filter_by(
                space_id=space_id,
                user_boleta=user_boleta,
                status='active'
            ).first()
            if active_reservation:
                active_reservation.status = 'completed'
        
        # Actualizar espacio
        from datetime import datetime
        space.status = 'occupied'
        space.occupied_by = user_boleta
        space.occupied_at = datetime.now()
        space.reserved_by = None
        space.reserved_at = None
        space.reservation_expires_at = None
        
        # Crear registro en historial
        history = ParkingHistory(
            space_id=space_id,
            user_boleta=user_boleta,
            action='occupy'
        )
        
        db.session.add(history)
        db.session.commit()
        
        return jsonify({
            "message": "Espacio ocupado exitosamente",
            "space": space.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/api/parking/vacate", methods=["POST"])
def vacate_parking():
    """Liberar un espacio ocupado"""
    try:
        data = request.get_json()
        space_id = data.get('space_id')
        user_boleta = data.get('user_boleta')  # Opcional, para verificación
        
        if not space_id:
            return jsonify({"error": "Falta space_id"}), 400
        
        space = ParkingSpace.query.get(space_id)
        if not space:
            return jsonify({"error": "Espacio no encontrado"}), 404
        
        if space.status != 'occupied':
            return jsonify({"error": "Espacio no está ocupado"}), 400
        
        # Verificar que el usuario que libera es el que ocupó (opcional)
        if user_boleta and space.occupied_by != user_boleta:
            return jsonify({"error": "No tienes permiso para liberar este espacio"}), 403
        
        # Guardar boleta para historial
        previous_occupant = space.occupied_by
        
        # Liberar espacio
        space.status = 'available'
        space.occupied_by = None
        space.occupied_at = None
        
        # Crear registro en historial
        history = ParkingHistory(
            space_id=space_id,
            user_boleta=previous_occupant,
            action='vacate'
        )
        
        db.session.add(history)
        db.session.commit()
        
        return jsonify({
            "message": "Espacio liberado exitosamente",
            "space": space.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/api/parking/cancel-reservation", methods=["POST"])
def cancel_reservation():
    """Cancelar una reserva activa"""
    try:
        data = request.get_json()
        space_id = data.get('space_id')
        user_boleta = data.get('user_boleta')
        
        if not space_id or not user_boleta:
            return jsonify({"error": "Faltan parámetros requeridos"}), 400
        
        space = ParkingSpace.query.get(space_id)
        if not space:
            return jsonify({"error": "Espacio no encontrado"}), 404
        
        if space.status != 'reserved' or space.reserved_by != user_boleta:
            return jsonify({"error": "No tienes una reserva activa en este espacio"}), 400
        
        # Marcar reserva como cancelada
        active_reservation = ParkingReservation.query.filter_by(
            space_id=space_id,
            user_boleta=user_boleta,
            status='active'
        ).first()
        if active_reservation:
            active_reservation.status = 'cancelled'
        
        # Liberar espacio
        space.status = 'available'
        space.reserved_by = None
        space.reserved_at = None
        space.reservation_expires_at = None
        
        # Crear registro en historial
        history = ParkingHistory(
            space_id=space_id,
            user_boleta=user_boleta,
            action='cancel'
        )
        
        db.session.add(history)
        db.session.commit()
        
        return jsonify({
            "message": "Reserva cancelada exitosamente",
            "space": space.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/api/parking/nearby", methods=["GET"])
def get_nearby_parking():
    """Obtener espacios cercanos a una ubicación"""
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        radius = float(request.args.get('radius', 100))  # metros
        status = request.args.get('status', 'available')
        
        # Importar función de distancia
        from kml_router import haversine_distance
        
        # Obtener espacios con el estado solicitado
        spaces = ParkingSpace.query.filter_by(status=status).all()
        
        # Calcular distancias y filtrar
        nearby_spaces = []
        for space in spaces:
            distance = haversine_distance((lat, lon), (space.lat, space.lon))
            if distance <= radius:
                space_dict = space.to_dict()
                space_dict['distance_to_user'] = round(distance, 1)
                nearby_spaces.append(space_dict)
        
        # Ordenar por distancia
        nearby_spaces.sort(key=lambda x: x['distance_to_user'])
        
        return jsonify({
            "count": len(nearby_spaces),
            "spaces": nearby_spaces
        }), 200
        
    except ValueError:
        return jsonify({"error": "Parámetros inválidos"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/parking/stats", methods=["GET"])
def get_parking_stats():
    """Obtener estadísticas generales del estacionamiento"""
    try:
        total = ParkingSpace.query.count()
        available = ParkingSpace.query.filter_by(status='available').count()
        occupied = ParkingSpace.query.filter_by(status='occupied').count()
        reserved = ParkingSpace.query.filter_by(status='reserved').count()
        
        # Estadísticas por sección
        sections = {}
        for section in ['A', 'B', 'C']:
            section_total = ParkingSpace.query.filter_by(section=section).count()
            section_available = ParkingSpace.query.filter_by(section=section, status='available').count()
            section_occupied = ParkingSpace.query.filter_by(section=section, status='occupied').count()
            section_reserved = ParkingSpace.query.filter_by(section=section, status='reserved').count()
            
            sections[section] = {
                "total": section_total,
                "available": section_available,
                "occupied": section_occupied,
                "reserved": section_reserved,
                "occupancy_rate": round((section_occupied / section_total * 100), 1) if section_total > 0 else 0
            }
        
        return jsonify({
            "total": total,
            "available": available,
            "occupied": occupied,
            "reserved": reserved,
            "occupancy_rate": round((occupied / total * 100), 1) if total > 0 else 0,
            "sections": sections
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/parking/my-reservations", methods=["GET"])
def get_my_reservations():
    """Obtener reservas del usuario autenticado"""
    try:
        user_boleta = request.args.get('boleta')
        if not user_boleta:
            return jsonify({"error": "Falta parámetro boleta"}), 400
        
        # Obtener reservas activas
        active_reservations = ParkingReservation.query.filter_by(
            user_boleta=user_boleta,
            status='active'
        ).all()
        
        # Obtener historial reciente
        recent_history = ParkingHistory.query.filter_by(
            user_boleta=user_boleta
        ).order_by(ParkingHistory.timestamp.desc()).limit(10).all()
        
        return jsonify({
            "active_reservations": [r.to_dict() for r in active_reservations],
            "recent_history": [h.to_dict() for h in recent_history]
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

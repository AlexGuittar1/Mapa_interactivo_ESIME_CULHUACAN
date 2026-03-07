"""
ARCHIVO: services/schedule_service.py

SERVICIO DE HORARIOS ACADEMICOS

Abstracción centralizada para manipular, obtener o sintetizar
rutinas y bloques de planeación escolar desde los repositorios de información aislados.
"""


class ScheduleService:
    """
    CLASE DE SERVICIO DE CALENDARIZACION ACADEMICA
    """

    DIAS_SEMANA = {
        0: 'Lunes', 1: 'Martes', 2: 'Miércoles',
        3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'
    }

    def __init__(self, schedule_repo, user_repo):
        self.schedule_repo = schedule_repo
        self.user_repo = user_repo

    def get_student_schedule(self, boleta, dia=None):
        """
        OBTENER CRONOGRAMA DE ESTUDIANTE
        
        Determina y recupera todo el panel formativo asignado al índice o boleta ingresada,
        opcionalmente cribado bajo un ciclo diario en específico.

        Retorna:
            tupla binaria: (Listado horario o Nulo, String de error formateado o Nulo)
        """
        user = self.user_repo.find_by_boleta(boleta)
        if not user:
            return None, "Usuario no encontrado"

        horarios = self.schedule_repo.get_schedule_by_boleta(boleta, dia)
        return horarios, None

    def get_today_schedule(self, boleta):
        """
        OBTENER HORARIO DEL DIA ACTUAL
        
        Devuelve las asignaturas cursadas relativas a la franja temporal del servidor para el estudiante seleccionado.
        """
        from datetime import datetime
        dia_actual = self.DIAS_SEMANA.get(datetime.now().weekday(), 'Lunes')
        return self.get_student_schedule(boleta, dia_actual)

    def get_group_schedule(self, grupo_clave, dia=None):
        """
        OBTENER HORARIO DEL GRUPO
        
        Exporta el bloque cronológico íntegro asimilado de un núcleo formativo base (ejemplo: 1CV1 o 5CM12).
        """
        horarios = self.schedule_repo.get_schedule_by_grupo(grupo_clave, dia)
        return horarios, None

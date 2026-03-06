"""
ScheduleService — Lógica de horarios desacoplada.
"""


class ScheduleService:
    """Servicio de horarios académicos."""

    DIAS_SEMANA = {
        0: 'Lunes', 1: 'Martes', 2: 'Miércoles',
        3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'
    }

    def __init__(self, schedule_repo, user_repo):
        self.schedule_repo = schedule_repo
        self.user_repo = user_repo

    def get_student_schedule(self, boleta, dia=None):
        """Obtener horario de un alumno.

        Returns:
            tuple: (schedule_list, error_message or None)
        """
        user = self.user_repo.find_by_boleta(boleta)
        if not user:
            return None, "Usuario no encontrado"

        horarios = self.schedule_repo.get_schedule_by_boleta(boleta, dia)
        return horarios, None

    def get_today_schedule(self, boleta):
        """Obtener horario del día actual para un alumno."""
        from datetime import datetime
        dia_actual = self.DIAS_SEMANA.get(datetime.now().weekday(), 'Lunes')
        return self.get_student_schedule(boleta, dia_actual)

    def get_group_schedule(self, grupo_clave, dia=None):
        """Obtener horario de un grupo académico."""
        horarios = self.schedule_repo.get_schedule_by_grupo(grupo_clave, dia)
        return horarios, None

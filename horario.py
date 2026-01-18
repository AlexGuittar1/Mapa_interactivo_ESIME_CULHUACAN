class Horario:
    def __init__(self, dia, hora_inicio, hora_fin, materia, grupo, docente):
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.materia = materia
        self.grupo = grupo
        self.docente = docente

    def __str__(self):
        return f"{self.dia} {self.hora_inicio}-{self.hora_fin} | {self.materia} ({self.grupo})"


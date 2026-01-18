from lista_doble import ListaDoblementeLigada
from salon import Salon

class Edificio:
    def __init__(self, nombre):
        self.nombre = nombre
        self.salones = ListaDoblementeLigada()

    def agregar_salon(self, numero_salon):
        salon = Salon(numero_salon)
        self.salones.insertar_al_final(salon)

    def eliminar_salon(self, numero_salon):
        self.salones.eliminar(numero_salon)

    def mostrar_salones(self):
        self.salones.recorrer_adelante()

    def __str__(self):
        return f"Edificio {self.nombre}"


    def buscar_salon(self, numero_salon):
        actual = self.salones.cabeza

        while actual is not None:
            if actual.dato.numero == numero_salon:
                return actual.dato
            actual = actual.siguiente

        return None

    def clases_del_dia(self, dia):
        resultado = []

        actual_salon = self.salones.cabeza
        while actual_salon is not None:
            salon = actual_salon.dato

            horarios = salon.horarios.cabeza
            if horarios is not None:
                actual_horario = horarios
                while True:
                    if actual_horario.dato.dia == dia:
                        resultado.append((salon.numero, actual_horario.dato))

                    actual_horario = actual_horario.siguiente
                    if actual_horario == horarios:
                        break

            actual_salon = actual_salon.siguiente

        return resultado

    def buscar_materia(self, nombre_materia):
        resultado = []

        actual_salon = self.salones.cabeza
        while actual_salon is not None:
            salon = actual_salon.dato
            horarios = salon.horarios.cabeza

            if horarios is not None:
                actual_horario = horarios
                while True:
                    if actual_horario.dato.materia == nombre_materia:
                        resultado.append((salon.numero, actual_horario.dato))

                    actual_horario = actual_horario.siguiente
                    if actual_horario == horarios:
                        break

            actual_salon = actual_salon.siguiente

        return resultado

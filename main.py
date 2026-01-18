from arbol_edificios import ArbolAVL
from lista_doble import ListaDoblementeLigada
from lista_circular import ListaCircular
from edificio import Edificio
from horario import Horario

# Crear edificio
edificio_a = Edificio("1")

# Agregar salones
edificio_a.agregar_salon("1205")
edificio_a.agregar_salon("1206")

# Crear horarios
h1 = Horario("Lunes", "20:30", "22:00", "Estructura de Datos", "3CV15", "Gonzalez")
h2 = Horario("Miercoles", "20:30", "22:00", "Estructura de Datos", "3CV15", "Gonzalez")

# Agregar horarios al salon 1205
salon_1205 = edificio_a.salones.cabeza.dato
salon_1205.agregar_horario(h1)
salon_1205.agregar_horario(h2)

# Mostrar todo
print(edificio_a)
edificio_a.mostrar_salones()
print("Horarios del salon 1205:")
salon_1205.mostrar_horarios()

clases_hoy = edificio_a.clases_del_dia("Lunes")
for salon, horario in clases_hoy:
    print(salon, horario)

salon_1205 = edificio_a.buscar_salon("1205")
clase = salon_1205.clase_actual()
if clase:
    print("Clase actual:", clase)

arbol = ArbolAVL()

edificio_a = Edificio("A")
edificio_b = Edificio("B")

arbol.insertar("A", edificio_a)
arbol.insertar("B", edificio_b)
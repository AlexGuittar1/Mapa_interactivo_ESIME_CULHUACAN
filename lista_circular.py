class NodoCircular:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

class ListaCircular:
    def __init__(self):
        self.cabeza = None
        self.tamano = 0

    def insertar(self, dato):
        nuevo = NodoCircular(dato)

        if self.cabeza is None:
            nuevo.siguiente = nuevo
            nuevo.anterior = nuevo
            self.cabeza = nuevo
        else:
            ultimo = self.cabeza.anterior

            nuevo.siguiente = self.cabeza
            nuevo.anterior = ultimo

            ultimo.siguiente = nuevo
            self.cabeza.anterior = nuevo

        self.tamano += 1

    def recorrer(self):
        if self.cabeza is None:
            return

        actual = self.cabeza
        while True:
            print(actual.dato)
            actual = actual.siguiente
            if actual == self.cabeza:
                break

    def insertar_despues(self, referencia, dato):
        if self.cabeza is None:
            return False

        actual = self.cabeza

        while True:
            if actual.dato == referencia:
                nuevo = NodoCircular(dato)

                nuevo.siguiente = actual.siguiente
                nuevo.anterior = actual

                actual.siguiente.anterior = nuevo
                actual.siguiente = nuevo

                self.tamano += 1
                return True

            actual = actual.siguiente
            if actual == self.cabeza:
                break

        return False

    def eliminar(self, dato):
        if self.cabeza is None:
            return False

        actual = self.cabeza

        while True:
            if actual.dato == dato:
                if actual.siguiente == actual:
                    self.cabeza = None
                else:
                    actual.anterior.siguiente = actual.siguiente
                    actual.siguiente.anterior = actual.anterior

                    if actual == self.cabeza:
                        self.cabeza = actual.siguiente

                self.tamano -= 1
                return True

            actual = actual.siguiente
            if actual == self.cabeza:
                break

        return False


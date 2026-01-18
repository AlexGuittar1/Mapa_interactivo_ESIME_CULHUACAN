class NodoListaDoble:
    def __init__(self, dato):
        self.dato = dato
        self.anterior = None
        self.siguiente = None

class ListaDoblementeLigada:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamano = 0

    def insertar_al_final(self, dato):
        nuevo_nodo = NodoListaDoble(dato)

        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo

        self.tamano += 1

    def recorrer_adelante(self):
        actual = self.cabeza
        while actual is not None:
            print(actual.dato)
            actual = actual.siguiente

    def insertar_despues(self, referencia, dato):
        actual = self.cabeza

        while actual is not None:
            if actual.dato == referencia:
                nuevo = NodoListaDoble(dato)

                nuevo.anterior = actual
                nuevo.siguiente = actual.siguiente

                if actual.siguiente is not None:
                    actual.siguiente.anterior = nuevo
                else:
                    self.cola = nuevo

                actual.siguiente = nuevo
                self.tamano += 1
                return True

            actual = actual.siguiente

        return False

    def insertar_antes(self, referencia, dato):
        actual = self.cabeza

        while actual is not None:
            if actual.dato == referencia:
                nuevo = NodoListaDoble(dato)

                nuevo.siguiente = actual
                nuevo.anterior = actual.anterior

                if actual.anterior is not None:
                    actual.anterior.siguiente = nuevo
                else:
                    self.cabeza = nuevo

                actual.anterior = nuevo
                self.tamano += 1
                return True

            actual = actual.siguiente

        return False

    def eliminar(self, dato):
        actual = self.cabeza

        while actual is not None:
            if actual.dato == dato:
                if actual.anterior is not None:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente

                if actual.siguiente is not None:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.cola = actual.anterior

                self.tamano -= 1
                return True

            actual = actual.siguiente

        return False

    def recorrer_atras(self):
        actual = self.cola
        while actual is not None:
            print(actual.dato)
            actual = actual.anterior

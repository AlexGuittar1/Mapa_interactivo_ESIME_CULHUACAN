
# Nodo del Árbol AVL

class NodoAVL:
    def __init__(self, clave, edificio):
        self.clave = clave              # Nombre o ID del edificio
        self.edificio = edificio        # Objeto Edificio
        self.izquierda = None
        self.derecha = None
        self.altura = 1

# Árbol AVL

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    # Funciones auxiliares

    def obtener_altura(self, nodo):
        if nodo is None:
            return 0
        return nodo.altura

    def obtener_balance(self, nodo):
        if nodo is None:
            return 0
        return self.obtener_altura(nodo.izquierda) - self.obtener_altura(nodo.derecha)

    # Rotaciones

    def rotacion_derecha(self, y):
        x = y.izquierda
        T2 = x.derecha

        x.derecha = y
        y.izquierda = T2

        y.altura = 1 + max(self.obtener_altura(y.izquierda),
                        self.obtener_altura(y.derecha))
        x.altura = 1 + max(self.obtener_altura(x.izquierda),
                        self.obtener_altura(x.derecha))

        return x

    def rotacion_izquierda(self, x):
        y = x.derecha
        T2 = y.izquierda

        y.izquierda = x
        x.derecha = T2

        x.altura = 1 + max(self.obtener_altura(x.izquierda),
                        self.obtener_altura(x.derecha))
        y.altura = 1 + max(self.obtener_altura(y.izquierda),
                        self.obtener_altura(y.derecha))

        return y

    # Inserción

    def insertar(self, nodo, clave, edificio):
        if nodo is None:
            return NodoAVL(clave, edificio)

        if clave < nodo.clave:
            nodo.izquierda = self.insertar(nodo.izquierda, clave, edificio)
        elif clave > nodo.clave:
            nodo.derecha = self.insertar(nodo.derecha, clave, edificio)
        else:
            # Sustitución del edificio
            nodo.edificio = edificio
            return nodo

        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierda),
                            self.obtener_altura(nodo.derecha))

        balance = self.obtener_balance(nodo)

        # Casos de balanceo
        if balance > 1 and clave < nodo.izquierda.clave:
            return self.rotacion_derecha(nodo)

        if balance < -1 and clave > nodo.derecha.clave:
            return self.rotacion_izquierda(nodo)

        if balance > 1 and clave > nodo.izquierda.clave:
            nodo.izquierda = self.rotacion_izquierda(nodo.izquierda)
            return self.rotacion_derecha(nodo)

        if balance < -1 and clave < nodo.derecha.clave:
            nodo.derecha = self.rotacion_derecha(nodo.derecha)
            return self.rotacion_izquierda(nodo)

        return nodo

    def insertar_edificio(self, clave, edificio):
        self.raiz = self.insertar(self.raiz, clave, edificio)

    # Búsqueda

    def buscar(self, clave):
        return self._buscar_recursivo(self.raiz, clave)

    def _buscar_recursivo(self, nodo, clave):
        if nodo is None:
            return None

        if clave == nodo.clave:
            return nodo.edificio
        elif clave < nodo.clave:
            return self._buscar_recursivo(nodo.izquierda, clave)
        else:
            return self._buscar_recursivo(nodo.derecha, clave)

    # Eliminación

    def obtener_minimo(self, nodo):
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual

    def eliminar(self, nodo, clave):
        if nodo is None:
            return nodo

        if clave < nodo.clave:
            nodo.izquierda = self.eliminar(nodo.izquierda, clave)
        elif clave > nodo.clave:
            nodo.derecha = self.eliminar(nodo.derecha, clave)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda

            temp = self.obtener_minimo(nodo.derecha)
            nodo.clave = temp.clave
            nodo.edificio = temp.edificio
            nodo.derecha = self.eliminar(nodo.derecha, temp.clave)

        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierda),
                            self.obtener_altura(nodo.derecha))

        balance = self.obtener_balance(nodo)

        if balance > 1 and self.obtener_balance(nodo.izquierda) >= 0:
            return self.rotacion_derecha(nodo)

        if balance > 1 and self.obtener_balance(nodo.izquierda) < 0:
            nodo.izquierda = self.rotacion_izquierda(nodo.izquierda)
            return self.rotacion_derecha(nodo)

        if balance < -1 and self.obtener_balance(nodo.derecha) <= 0:
            return self.rotacion_izquierda(nodo)

        if balance < -1 and self.obtener_balance(nodo.derecha) > 0:
            nodo.derecha = self.rotacion_derecha(nodo.derecha)
            return self.rotacion_izquierda(nodo)

        return nodo

    def eliminar_edificio(self, clave):
        self.raiz = self.eliminar(self.raiz, clave)

    # Recorridos

    def inorden(self):
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, lista):
        if nodo:
            self._inorden(nodo.izquierda, lista)
            lista.append(nodo.edificio)
            self._inorden(nodo.derecha, lista)

    def preorden(self):
        resultado = []
        self._preorden(self.raiz, resultado)
        return resultado

    def _preorden(self, nodo, lista):
        if nodo:
            lista.append(nodo.edificio)
            self._preorden(nodo.izquierda, lista)
            self._preorden(nodo.derecha, lista)

    def postorden(self):
        resultado = []
        self._postorden(self.raiz, resultado)
        return resultado

    def _postorden(self, nodo, lista):
        if nodo:
            self._postorden(nodo.izquierda, lista)
            self._postorden(nodo.derecha, lista)
            lista.append(nodo.edificio)

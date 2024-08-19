from random import randint
from itertools import combinations
from random import randint, choice
from itertools import combinations
from math import sqrt



class GruposVertices:
    def __init__(self, n_bloques) -> None:
        self.num_bloques = n_bloques
        self._grupos_vertices = []

    @property
    def grupos_vertices(self):
        
        grupos = self._agrupar()
        for grp in grupos:

            self._grupos_vertices.extend(grp)
        
        return self._grupos_vertices
    
    def _agrupar(self):

        filas = [[i for i in range(j, j+self.num_bloques)] for j in range(0, self.num_bloques**2, self.num_bloques)]

        columnas = [[i[j] for i in filas] for j in range(self.num_bloques)]

        regiones = []

        n = int(sqrt(self.num_bloques))

        for i in range(n):

            banda = filas[i*n:i*n+n]
            lista_temp =[[] for _ in range(n)]

            for fila in banda:

                for j in range(n):

                    lista_temp[j].extend(fila[n*j:n*j+n])
            
            regiones.extend(lista_temp)
            lista_temp.clear()

        return filas, columnas, regiones
    

class SudokuGraph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]
        self.digits = int(sqrt(self.V))

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def greedy_coloring(self):

        result = [-1] * self.V  
        
        result[0] = randint(0,self.digits-1)

        for u in range(1, self.V):
            
            available = [False] * self.digits
            
           
            for v in self.graph[u]:
                if result[v] != -1:
                    available[result[v]] = True

            colores_disponibles = [i for i,a in enumerate(available) if a is False]
            if not colores_disponibles:
                break 
            color = choice(colores_disponibles)

            result[u] = color

        return result


class SudokuGreed:
    def __init__(self):
        self.graph = SudokuGraph(81)
        self._greed_sin_resolver = None
        self._greed_solucion = None
        self._initialize_graph()

    def _initialize_graph(self):
        grupo = GruposVertices(9)
        grupo_vertices = grupo.grupos_vertices

        aristas = []
        for grupo in grupo_vertices:
            adyacentes = combinations(grupo, 2)
            for v in list(adyacentes):
                if not (v[0], v[1]) in aristas:
                    self.graph.add_edge(v[0], v[1])

    def _compute__greed_solucion(self):
        while True:
            s = self.graph.greedy_coloring()
            if not -1 in s:
                resultado = list(map(lambda x: x + 1, s))
                break

        self._greed_solucion = [resultado[9*i:9*i+9] for i in range(9)]
        return self._greed_solucion

    def _compute__greed_sin_resolver(self):
        if self._greed_solucion is None:
            self._compute__greed_solucion()

        resultado = [num for fila in self._greed_solucion for num in fila]
        
        missing_digits_pos = set()
        while True:
            while True:
                n = randint(0, 39)
                missing_digits_pos.add(n)
                if len(missing_digits_pos) > 26:
                    break

            x = list(missing_digits_pos)
            y = list(map(lambda i: 80-i, x))
            missing_digits_pos = x + y

            for i in missing_digits_pos:
                resultado[i] = -1

            if (1 in resultado and 2 in resultado and 3 in resultado and
                4 in resultado and 5 in resultado and 6 in resultado and
                7 in resultado and 8 in resultado and 9 in resultado):
                break

        self._greed_sin_resolver = [resultado[9*i:9*i+9] for i in range(9)]
        return self._greed_sin_resolver

    @property
    def greed_solucion(self):
        if self._greed_solucion is None:
            self._compute__greed_solucion()
        return self._greed_solucion
    
    @property
    def greed_sin_resolver(self):
        if self._greed_sin_resolver is None:
            self._compute__greed_sin_resolver()
        return self._greed_sin_resolver
    
if __name__ == '__main__':
    sudoku_greed = SudokuGreed()
    print(sudoku_greed.greed_sin_resolver)
    print(sudoku_greed.greed_solucion)

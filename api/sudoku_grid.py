from itertools import combinations
from random import randint, choice, shuffle
from math import sqrt
from copy import deepcopy


def duplicados_en_conjuntos(lst):
    vistos = set()
    duplicados = set()
    
    lst_tuplas = [tuple(sorted(conjunto)) for conjunto in lst]
    
    for tupla in lst_tuplas:
        if tupla in vistos:
            duplicados.add(tupla)
        else:
            vistos.add(tupla)
    
    # Convertir las tuplas de vuelta a conjuntos
    duplicados_conjuntos = [set(tupla) for tupla in duplicados]
    
    return duplicados_conjuntos if duplicados_conjuntos else False



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


class SudokuGrid:
    def __init__(self):
        self.graph = SudokuGraph(81)
        self._grid_sin_resolver = None
        self._grid_solucion = None
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

    def _compute_grid_solucion(self):
        while True:
            s = self.graph.greedy_coloring()
            if not -1 in s:
                resultado = list(map(lambda x: x + 1, s))
                break

        self._grid_solucion = [resultado[9*i:9*i+9] for i in range(9)]
        return self._grid_solucion

    def _compute_grid_sin_resolver(self):
        if self._grid_solucion is None:
            self._compute_grid_solucion()

        resultado = [num for fila in self._grid_solucion for num in fila]

        # Generar una lista de posiciones y mezclarla
        posiciones = list(range(81))
        shuffle(posiciones)

        # Seleccionar las primeras 23 posiciones para vaciar
        celdas_vacias = set(posiciones[:25])

        # Genera posiciones simétricas
        x = list(celdas_vacias)
        y = [80 - i for i in x]
        celdas_vacias = set(x + y)

        # Reemplaza los valores en resultado
        resultado = [num if i not in celdas_vacias else -1 for i, num in enumerate(resultado)]

        self._grid_sin_resolver = [resultado[9*i:9*i+9] for i in range(9)]  
        return self._grid_sin_resolver


    @property
    def grid_solucion(self):
        if self._grid_solucion is None:
            self._compute_grid_solucion()
        return self._grid_solucion
    
    @property
    def grid_sin_resolver(self):
        if self._grid_sin_resolver is None:
            self._compute_grid_sin_resolver()
        return self._grid_sin_resolver
    
class SudokuValid():

    N = 9
    def __init__(self):
        self.soluciones = []
    def sudoku(self):
        
        sudoku = SudokuGrid()
        valores = sudoku.grid_sin_resolver
        grid = deepcopy(valores)
        self.soluciones = []
        solucion = sudoku.grid_solucion
        self._resuelve_sudoku(grid, 0, 0)

        if len(self.soluciones) == 1:
            return valores, solucion
        else:
            return self.sudoku()


    def _es_candidato(self, grid, row, col, num):
    
        for x in range(9):
            if grid[row][x] == num:
                return False

        for x in range(9):
            if grid[x][col] == num:
                return False

        startRow = row - row % 3
        startCol = col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + startRow][j + startCol] == num:
                    return False
        return True

    def _resuelve_sudoku(self,grid, row, col):
        # Comprueba que la grid tenga más de una solucion posible para descartarla
        if len(self.soluciones) > 1:
            return
        # Comprueba si la última celda (row=8, col=9) está completa para salir del método
        if row == self.N - 1 and col == self.N:
            self.soluciones.append(deepcopy(grid))
            return
        
        # Comprueba si la última celda de la columna está llena para pasar a la siguiente
        if col == self.N:
            row += 1
            col = 0

        # Comprueba si la celda ya está ocupada, en caso de ser así avanza a la próxima celda
        if grid[row][col] > 0:
            self._resuelve_sudoku(grid, row, col + 1)

        else:
            for num in range(1, self.N + 1):
                if self._es_candidato(grid, row, col, num):
                    grid[row][col] = num
                    self._resuelve_sudoku(grid, row, col + 1)
                    grid[row][col] = 0
         
if __name__ == '__main__':
    sudoku = SudokuValid()
    print(sudoku.sudoku())

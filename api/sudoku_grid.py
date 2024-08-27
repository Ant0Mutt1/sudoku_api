from itertools import combinations
from random import randint, choice
from math import sqrt

def duplicados_en_conjuntos(lst):
    vistos = set()
    duplicados = set()
    
    # Convertir conjuntos a tuplas (ya que los conjuntos no son hashables y no se pueden añadir a otro conjunto)
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
        
        while True:
            missing_digits_pos = set()
            while True:
                n = randint(0, 39)
                missing_digits_pos.add(n)
                if len(missing_digits_pos) > 22:
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

        self._grid_sin_resolver = [resultado[9*i:9*i+9] for i in range(9)]
        return self._grid_sin_resolver
    
    def _obtener_adyacencias(self,grid):
    
        adyacencias = []
        for fila in grid:

            adyacentes = list(combinations(fila, 2))

            #Las combinaciones posible de una fila son convertidas en 'set' para poder compararlos con otras 
            #combinaciones sin importar el orden. Por ejemplo {1,2} == {2,1}        
            adyacencias.append(
                list(
                    map(set, adyacentes)
                )                    
            )
        return adyacencias

    def _encontrar_valores_claves(self,grid):

        '''    
        Busca valores que deben estar presentes como pistas para que no 
        existan 'bloques ilegales' (Una casilla con dos soluciones válidas).

        '''        
        adyacencias = self._obtener_adyacencias(grid)
        agrupaciones_por_indice = list(zip(*adyacencias)) 
        valor_posicion = []
            
        for grupo in agrupaciones_por_indice:          
    
            print(grupo)
            conjuntos_identicos = duplicados_en_conjuntos(grupo)
            print(type(conjuntos_identicos))

            if conjuntos_identicos:
                #Informa en qué fila aparece por primera ver el valor que debe estar 
                # presente para evitar un bloque ilegal.
                for conjuntos in conjuntos_identicos:
                
                    fila_a_modif = (list(grupo).index(conjuntos))
                    print(fila_a_modif, conjuntos)
                    pista_obligatoria = conjuntos.pop()
                
                    valor_posicion.append((fila_a_modif, pista_obligatoria))                                                    
            # except ValueError as e:
            #     pass   
        return valor_posicion 
    @property
    def grid_solucion(self):
        if self._grid_solucion is None:
            self._compute_grid_solucion()
        return self._grid_solucion
    
    @property
    def grid_sin_resolver(self):
        if self._grid_sin_resolver is None:
            self._compute_grid_sin_resolver()
            valores_claves = self._encontrar_valores_claves(self.grid_solucion)

            for pos, valor in valores_claves:
                indice = self.grid_solucion[pos].index(valor)
                self._grid_sin_resolver[pos][indice] = valor
        return self._grid_sin_resolver
    
if __name__ == '__main__':
    sudoku_grid = SudokuGrid()
    print(sudoku_grid.grid_sin_resolver)
    print(sudoku_grid.grid_solucion)

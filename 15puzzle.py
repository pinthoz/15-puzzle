from copy import deepcopy
import heapq
import time
import sys
#import random


# definition of the problem
class GameBoard:

    def __init__(self, board, move_directions=[],move_history=[]):
        # board representa a matriz do estado do puzzle
        # move_directions guarda a sequencia de movimentos feitos ate ao estado atual
        # move_history guarda o historico de boards ate ao estado atual
        self.board = deepcopy(board)
        (self.blank_row, self.blank_col) = self.find_blank()
        self.move_directions = [] + move_directions
        self.move_history = [] + move_history + [self.board]

    def find_blank(self):
        # encontra a posicao do espaco vazio
        for row in range(4):
            for col in range(4):
                if self.board[row][col] == 0:
                    return (row, col)
                

    def children(self):
        # faz os movimentos possiveis
        possible_moves = [self.up, self.down, self.left, self.right]
        # para os movimentos serem escolhidos de forma aleatoria
        # random.shuffle(possible_moves)
        children = []
        
        for func in possible_moves:
            child = func()
            if child:
                children.append(child)
        return children

 
 #####################################################################################################
 
    def make_move(func):
        # a funcao make_move recebe como argumentos o up,down,left,right
        # a funcao so devolve os movimentos validos, que depois vao ser incluidos na lista dos filhos
        # tambem adiciona os movimentos ao historico de jogadas respetivo
        def wrapper(self):
            state = GameBoard(self.board, self.move_directions + [func.__name__],self.move_history)
            value = func(state)
            if value:
                return state
            else:
                return None

        return wrapper

    @make_move
    def up(self):
        # move o espaco vazio para cima se nao estiver na primeira linha
        if self.blank_row == 0:
            return False
        else:
            self.board[self.blank_row][self.blank_col] = self.board[self.blank_row - 1][self.blank_col]
            self.board[self.blank_row - 1][self.blank_col] = 0
            self.blank_row -= 1
            return True

    @make_move
    def down(self):
        # move o espaco vazio para baixo se nao estiver na ultima linha
        if self.blank_row == 3:
            return False
        else:
            self.board[self.blank_row][self.blank_col] = self.board[self.blank_row + 1][self.blank_col]
            self.board[self.blank_row + 1][self.blank_col] = 0
            self.blank_row += 1
            return True

    @make_move
    def left(self):
        # move o espaco vazio para a esquerda se nao estiver na primeira coluna
        if self.blank_col == 0:
            return False
        else:
            self.board[self.blank_row][self.blank_col] = self.board[self.blank_row][self.blank_col - 1]
            self.board[self.blank_row][self.blank_col - 1] = 0
            self.blank_col -= 1
            return True

    @make_move
    def right(self):
        # move o espaco vazio para a direita se nao estiver na ultima coluna
        if self.blank_col == 3:
            return False
        else:
            self.board[self.blank_row][self.blank_col] = self.board[self.blank_row][self.blank_col + 1]
            self.board[self.blank_row][self.blank_col + 1] = 0
            self.blank_col += 1
            return True

#####################################################################################################

    # para o set funcionar tem de ser possivel comparar os estados
    # para tal,duas instancias sao iguais se o seu hash value for igual
    # o hash value e calculado a partir da matriz do estado
    
    def __hash__(self):
        
        return hash(str([item for sublist in self.board for item in sublist]))

    def __eq__(self, other):
        #compara duas matrizes para ver se sao iguais
        #transforma a matriz numa lista e compara as lista do self e do other
        return [item for sublist in self.board for item in sublist] == [item for sublist in other.board for item in sublist]


#####################################################################################################

def dfs(first_board,final_board):
    # depth first search
    # o dfs usa uma stack para guardar os estados 
    # vai dando pop ao topo da pilha e adiciona os filhos a stack
    global max_nodes
    stack = [first_board]
    visited = set() # para na visitar o mesmo no mais do que uma vez

    while stack:
        
        if len(stack) > max_nodes:
            max_nodes = len(stack)
            
        state = stack.pop()
        visited.add(state)

        if state == final_board:
            return (state.move_directions,state.move_history)

        for child in state.children():
            if child not in visited:
                stack.append(child)
 
    return None

#####################################################################################################

def bfs(first_board,final_board):
    # breadth first search
    # o bfs usa uma queue para guardar os estados
    # vai dando pop ao estado que esta no inicio da fila e adiciona os filhos a queue
    global max_nodes
    queue = [first_board]
    visited = set() # para na visitar o mesmo no mais do que uma vez

    while queue:
        
        if len(queue) > max_nodes:
            max_nodes = len(queue)
            
        state = queue.pop(0)
        visited.add(state)

        if state == final_board:
            return (state.move_directions,state.move_history)

        for child in state.children():
            if child not in visited:
                queue.append(child)

    return None

#####################################################################################################

def idfs(first_board,final_board):
    # comeca com uma profundidade de 0 e vai aumentando ate encontrar uma solucao
    
    d = 0
    while True:
        result = dls(first_board,final_board,d)
        if result != None:
            return result
        d += 1


def dls(first_board,final_board,depth):
    
    global max_nodes
    stack = [first_board]
    
    while stack:
        
        if len(stack) > max_nodes:
            max_nodes = len(stack)
            
        state = stack.pop()

        if state == final_board:
            return (state.move_directions,state.move_history)

        if len(state.move_directions) < depth:
            for child in state.children():
                stack.append(child)
    
    return None

#####################################################################################################
        
def get_final_pos(final_matrix):
    # devolve uma lista de tuplos com as posicoes finais de cada peca
    # o indice da lista corresponde ao numero da peca
    positions = [0]*16
    
    for row in range(4):
            for col in range(4):
                positions[final_matrix[row][col]] = (row,col)
    
    return positions

# as duas heuristicas que vao ser usadas
# o misplaced conta o numero de pecas fora do sitio
# o manhattan calcula a distancia de cada peca para o sitio certo

def h_misplaced(board_state,final_matrix_pos):
     
    board = board_state.board
    cost = 0
    
    for row in range(4):
        for col in range(4):
            if board[row][col] != 0 and (row,col) != final_matrix_pos[board[row][col]]:
                cost += 1

    return cost


def h_manhattan(board_state,final_matrix_pos):

    board = board_state.board
    cost = 0
    
    for row in range(4):
        for col in range(4):
            if board[row][col] != 0 and (row,col) != final_matrix_pos[board[row][col]]:
                
                cost += abs(row - final_matrix_pos[board[row][col]][0]) + abs(col - final_matrix_pos[board[row][col]][1])

    return cost

#####################################################################################################

def greedy(first_board, heuristic, final_board,final_matrix):
    
    # o greedy vai escolher sempre o caminho com a menor valor de heuristica
    # o setattr cria um atributo novo na classe GameBoard, o __lt__ (less than)
    # o novo atributo tem como valor uma funcao lambda que compara o valor da heuristica de dois estados
    # desta forma, a priority queue vai ordenar os estados por ordem crescente do valor de heuristica
    
    global max_nodes
    
    final_matrix_pos = get_final_pos(final_matrix) # lista de tuplos com a posicao de cada peca no estado final
    
    setattr(GameBoard, "__lt__", lambda self, other: heuristic(self,final_matrix_pos) < heuristic(other,final_matrix_pos))
    
    states = [first_board]
    visited = set() 
    
    while states:
        
        if len(states) > max_nodes:
            max_nodes = len(states)
        
        state = heapq.heappop(states)
        visited.add(state)
        
        if state == final_board:
            return (state.move_directions,state.move_history)

        for child in state.children():
            if child not in visited:
                heapq.heappush(states, child)
        
    return None

#####################################################################################################

def a_star(first_board, heuristic, final_board,final_matrix):
    # o a star funciona como o greedy search, mas tambem tem em conta o fator profundidade
    
    global max_nodes
    
    final_matrix_pos = get_final_pos(final_matrix) # lista de tuplos com a posicao de cada peca no estado final
    
    setattr(GameBoard, "__lt__", lambda self, other: heuristic(self,final_matrix_pos) + len(self.move_directions) < heuristic(other,final_matrix_pos) + len(other.move_directions))
    
    states = [first_board]
    visited = set() 

    while states:
            
            if len(states) > max_nodes:
                max_nodes = len(states)
                
            state = heapq.heappop(states)
            visited.add(state)
            
            if state == final_board:
                return (state.move_directions,state.move_history)
    
            for child in state.children():
                if child not in visited:
                    heapq.heappush(states, child)

    return None

#####################################################################################################

def print_board(board):
    
    print("+--+--+--+--+")
    for row in range(4):
        line = "|"
        for col in range(4):
            if board[row][col] == 0: # espaco vazio
                line +=  "  |"
            elif board[row][col] < 10: # para ficar alinhado
                line += str(board[row][col]) +   " |"
            else:
                line += str(board[row][col]) + "|"
                     
        print(line)
        print("+--+--+--+--+")
        
    print()
        
def print_sequence(move_sequence):
    # imprime a direcao dos movimentos e o estado do tabuleiro apos cada movimento
    dirs = move_sequence[0]
    boards = move_sequence[1]
    
    first_config = boards.pop(0)
    print_board(first_config)
    i = 0
    for board in boards:
        print("%s:" % dirs[i].capitalize())
        print_board(board)
        i+=1
    
    print(f"Steps: {len(dirs)}")
    print(f"Max nodes stored: {max_nodes}" )
    
#####################################################################################################

def reshape_to_matrix(num):
    #transforma a lista dada numa matriz 4x4
    matrix = []
    for i in range(4):
        matrix.append(num[i*4:(i+1)*4])
    return matrix

#####################################################################################################

def count_inversions(num):
    #conta o numero de inversoes na lista dada
    count = 0
    for i in range(15):
        for j in range(i+1, 16):
            if num[i] > num[j] and num[i] != 0 and num[j] != 0:
                count+=1

    return count
     

def check_possible(n_board,final_board):
    #verifica se o tabuleiro tem solucao
    
    first_arr = [item for sublist in n_board.board for item in sublist]
    final_arr = [item for sublist in final_board.board for item in sublist]
    
    first_inversions = count_inversions(first_arr)
    final_inversions = count_inversions(final_arr)
    
    first_row_blank = 4 - n_board.find_blank()[0]
    final_row_blank = 4 - final_board.find_blank()[0]
    
    cond_i = (first_inversions%2 == 0) == (first_row_blank%2==1)
    cond_f = (final_inversions%2 == 0) == (final_row_blank%2==1)
    return cond_i == cond_f

#####################################################################################################
 

max_nodes = 0

if __name__ == "__main__":
    
    ALG = sys.argv[1] # algoritmo a usar
    start = list(map(int,input().split())) # lista com os numeros do tabuleiro inicial
    final = list(map(int,input().split())) # lista com os numeros do tabuleiro final
    
    start_matrix = reshape_to_matrix(start) # matriz 4x4 do tabuleiro final
    final_matrix = reshape_to_matrix(final) # matriz 4x4 do tabuleiro final
    
    num_board = GameBoard(start_matrix) # tabuleiro inicial
    final_board =  GameBoard(final_matrix) # tabuleiro final
    
    
    
    # verifica se o tabuleiro tem solucao
    if check_possible(num_board,final_board) == False:
        print("Not solvable")
    
    else:
        start = time.time()
        
        if ALG == "DFS":
            print_sequence(dfs(num_board,final_board))
        elif ALG == "BFS":
            print_sequence(bfs(num_board,final_board))
        elif ALG == "IDFS":
            print_sequence(idfs(num_board,final_board))
        elif ALG == "A*-misplaced":
            print_sequence(a_star(num_board,h_misplaced,final_board,final_matrix))
        elif ALG == "A*-Manhattan":
            print_sequence(a_star(num_board,h_manhattan,final_board,final_matrix))
        elif ALG == "Greedy-misplaced":
            print_sequence(greedy(num_board,h_misplaced,final_board,final_matrix))
        elif ALG == "Greedy-Manhattan":
            print_sequence(greedy(num_board,h_manhattan,final_board,final_matrix))
        else:    
            print("Invalid Input")
            
        end = time.time()
        print("Execution time: %f seconds" % (end - start))
        

# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    visit = {} # armazenar os nó já visitado
    sol = [] # armazenar os movimentos para a solução
    pai = {} # armazenar os pai dos nó
    com = problem.getStartState() # obter a posição inicial
    
    pilha = util.Stack() #pilha LIFO para armazenar os nos
    #se ficar sem elemento quer dizer que todos os nos já foram visitados
    
    pilha.push((com, "undefined", 0)) # mandar para a pilha o elemento da posição inicial
    
    goal = False
    while (pilha.isEmpty() != True or goal != True):
        no = pilha.pop() # ((coordenadas), nome, custo)
        visit[no[0]] = no[1]
        
        #Verificar se o NO é o goalstate
        if (problem.isGoalState(no[0])):
            goal = True
            no_sol = no[0]
           # print("encontrou o goal state")
            break
        
        for e in problem.getSuccessors(no[0]):
            if (e[0] not in visit.keys()): #verificar se o nó não foi visitado posteriormente
                pilha.push(e)
                pai[e[0]] = no[0]
                
    
            
    while (no_sol in pai.keys()):
        # rastrear a origem do no, partindo do no solução até o inicio
        no_sol_antes = pai[no_sol] 
        
        #inserir na lista SOluçao os passos para o pacman chegar ao destino
        sol.insert(0, visit[no_sol])
        no_sol = no_sol_antes
        
    return sol

        
def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    visit = {} # armazenar os nó já visitado
    sol = [] # armazenar os movimentos para a solução
    pai = {} # armazenar os pai dos nó
    com = problem.getStartState() # obter a posição inicial
    
    fila = util.Queue() #fila FIFO para armazenar os nos
    #se ficar sem elemento quer dizer que todos os nos já foram visitados
    
    fila.push((com, "undefined", 0)) # mandar para a fila o elemento da posição inicial
    
    goal = False
    while (fila.isEmpty() != True or goal != True):
        no = fila.pop() # ((coordenadas), nome, custo)
        
        visit[no[0]] = no[1]
    
        #Verificar se o NO é o goalstate
        if (problem.isGoalState(no[0])):
            goal = True
            no_sol = no[0]
            break
        
        for e in problem.getSuccessors(no[0]):
            # verificar se o no não foi visitado anteriormente e se não foi expandido
            if (e[0] not in visit.keys() and e[0] not in pai.keys()): 
                fila.push(e)
                pai[e[0]] = no[0]
            
        
            
    while (no_sol in pai.keys()):
        # rastrear a origem do no, partindo do no solução até o inicio
        no_sol_antes = pai[no_sol] 
        
        #inserir na lista SOluçao os passos para o pacman chegar ao destino
        sol.insert(0, visit[no_sol])
        no_sol = no_sol_antes
        
    return sol
    # codico semelhante ao DFS, mas inves de utilizar um estrutura
    # LIFO, utiliza-se uma estrutura FIFO ...   


    
def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    comeco = problem.getStartState() #obter estado inicial do pacman
    visitados = {} # armazenar cordenadas e direções já exploradas
    
    # priorityQueue é uma estrutura FIFO, mas com uma diferença que remove os elementos tendo em base sua prioridade
    fila = util.PriorityQueue() #fila contendo (coordenadas, direção, custo) e prioridade
    #adicionar no inicial na fila com direção indefinida, custo e prioridade 0
    fila.push((comeco, 'Undefined', 0), 0) 
    
    parents = {} #armazenar os nos e seu no pai
    
    custo = {} # contendo a coordenada do no e seu respetivo custo até chegar nele
    custo[comeco] = 0 # adicionando o no de comeco com custo 0
    
    goal = False

    while(fila.isEmpty() != True and goal != True):
        """
        este loop de reptição é diferente do DFS e BFS, que enquanto nos outros
        a condição é a fila estar vazia ou ter chegado ao goal, no cost-sensitive search 
        para sair do loop para além de ter chegado no goal é necessario que não haja mais nos para explorar
        """
        #Retirar elemento da frente da pilha
        no=fila.pop()
        
        #O no ja foi visitado
        visitados[no[0]]=no[1]
        #Verificar se o elemento é o goal
        if problem.isGoalState(no[0]):
            no_sol = no[0]
            goal = True
           # print("goal State encontrado")
            break
        
        #expandir no
        for elem in problem.getSuccessors(no[0]):
            # verificar se o no nao foi visitado anteriormente
            if elem[0] not in visitados.keys():
                priority = no[2] + elem[2]
                
                
                if elem[0]  in custo.keys():
                    #verificar se o custo atual é maior que anterior
                    if custo[elem[0]] <= priority:
                        continue #se é verdadeiro avançar para proxima iteração
                    # se o novo custo for menor que o custo antigo, coloque na fila e altere o custo e o pai 
                fila.push((elem[0], elem[1], priority), priority)
                custo[elem[0]] = priority #Armazenar custo do elemento
                   
                parents[elem[0]] = no[0]  # Armazenar o seu no filho
    
    
    solucao=[]    #armazenar os movimentos ate chegar no goal State      
    # encontrando e armazenando o caminho
    while(no_sol in parents.keys()):
        #encontre o pai
        no_sol_prev=parents[no_sol]
        # acrescenta a direção à solução
        solucao.insert(0, visitados[no_sol])
        # Ir para o nó anterior
        no_sol= no_sol_prev
        
    return solucao
      

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    comeco = problem.getStartState() #obter estado inicial do pacman
    visitados = {} # armazenar cordenadas e direções já exploradas
    
    # priorityQueue é uma estrutura FIFO, mas com uma diferença que remove os elementos tendo em base sua prioridade
    fila = util.PriorityQueue() #fila contendo (coordenadas, direção, custo) e prioridade
    #adicionar no inicial na fila com direção indefinida, custo e prioridade 0
    fila.push((comeco, 'Undefined', 0), 0) 
    
    parents = {} #armazenar os nos e seu no pai
    
    custo = {} # contendo a coordenada do no e seu respetivo custo até chegar nele
    custo[comeco] = 0 # adicionando o no de comeco com custo 0
    
    goal = False

    while(fila.isEmpty() != True and goal != True):
        """
        o codigo é igual a uniformedcostSearch com adiçao da Heuristica no calculo da prioridade do no
        """
        #Retirar elemento da frente da pilha
        no=fila.pop()
        
        #O no ja foi visitado
        visitados[no[0]]=no[1]
        #Verificar se o elemento é o goal
        if problem.isGoalState(no[0]):
            no_sol = no[0]
            goal = True
            break
        
        #expandir no
        for elem in problem.getSuccessors(no[0]):
            # verificar se o no nao foi visitado anteriormente
            if elem[0] not in visitados.keys():
                #função heurística que estima o custo restante para atingir o objetivo a partir do nó 
                priority = no[2] + elem[2] + heuristic(elem[0],problem) 
                
                
                if elem[0]  in custo.keys():
                    #verificar se o custo atual é maior que anterior
                    if custo[elem[0]] <= priority:
                        continue #se é verdadeiro avançar para proxima iteração
                    # se o novo custo for menor que o custo antigo, coloque na fila e altere o custo e o pai 
                fila.push((elem[0], elem[1],no[2]+elem[2]), priority)
                custo[elem[0]] = priority #Armazenar custo do elemento
                   
                parents[elem[0]] = no[0]  # Armazenar o seu no filho
    
    
    solucao=[]    #armazenar os movimentos ate chegar no goal State      
    # encontrando e armazenando o caminho
    while(no_sol in parents.keys()):
        #encontre o pai
        no_sol_prev=parents[no_sol]
        # acrescenta a direção à solução
        solucao.insert(0, visitados[no_sol])
        # Ir para o nó anterior
        no_sol= no_sol_prev
        
    return solucao


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


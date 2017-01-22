#BFS working.
#Program prints node numbers of the nodes along the path from start to goal node.
#Snake follows the path dictated by BFS algorithm
#Snake follows path to one apple after another
#Imported A* code from Dipesh and fixed PriorityQueue unorderable objects error
#Snake works with A* algorithm
#PriorityQueue implementation was incorrect
#Used heap to implement priority queue and made Node object orderable by defining __lt__ method
#nodeVisitCount records incorrect node visit count. Printed the nodes visited and found that the logic used in AStar search was incorrect. Fixed the logic
#Verified generate_h_values generates correct heuristic map
#Fixed further issues with calculation of gValue = hValue + 10
#Now the program prints correct number of nodes visited and the snake follows correct path. We can clearly see that AStar is more efficient than BFS

import random, pygame, sys
from pygame.locals import *
from queue import *
from heapq import heappush, heappop, heapify

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

nodeVisitCount = 0

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
GRAY      = (175, 175, 175)
SKYBLUE   = (  0, 145, 255)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

# Node Class
class Node:
    xCoord = 0
    yCoord = 0
    nodeNum = 0
    parent = None
    hValue = 0
    gValue = 0
    status = ''
    color = ''

    #To make node objects orderable. Since we are passing objects to heap, we have to make obects orderable.
    def __lt__(self, other):
        return(self.gValue < other.gValue)
    

class Worm:
    xCoord = 0
    yCoord = 0
    

#Function to generate empty node map
def genEmptyNodeMap():
    nodeMap = list()
    mapSize = CELLWIDTH * CELLHEIGHT
    yCounter = 0
    for i in range(mapSize):
        node = Node()
        node.xCoord = i % CELLWIDTH
        node.yCoord = yCounter
        if int(i % CELLWIDTH) == CELLWIDTH-1 and i > CELLWIDTH-2:
            yCounter+=1
        node.nodeNum = i
        node.status = 'notvisited'
        node.color = BLACK
        nodeMap.append(node)
    return nodeMap


#Function to trace the shortest path found
def tracePath(start, goal, nodeMap):
    path = list()
    currNode = goal
    while(currNode.nodeNum != start.nodeNum):
        path.append(currNode)
        currNode.color = WHITE
        currNode = currNode.parent
    path.append(start)
    path.reverse()
    return path


def generate_h_value(goal, nodeMap):
    for node in nodeMap:
        node.hValue = abs(goal.xCoord - node.xCoord) + abs(goal.yCoord - node.yCoord)
    

#Breadth First Search in 2D Grid
def BFS(start, goal, nodeMap):
    #Initialize
    q = Queue()
    bottomNode = rightNode = topNode = leftNode = None
    global nodeVisitCount
    nodeVisitCount = 0
    
    #Insert start node into queue
    start.color = WHITE
    q.put(start)
    while(not q.empty()):
        popNode = q.get()
        bottomNode = rightNode = topNode = leftNode = None
        if (popNode.nodeNum != goal.nodeNum):
            #Check if bottom node exits and status = notvisited
            if (popNode.nodeNum < CELLWIDTH*(CELLHEIGHT-1)):
                bottomNode = nodeMap[popNode.nodeNum + CELLWIDTH]
                if(bottomNode.status == 'notvisited'):
                    bottomNode.status = 'visited'
                    bottomNode.parent = popNode
                    bottomNode.color = GRAY
                    nodeVisitCount += 1
                    q.put(bottomNode)
            #Check if right node exists and status = notvisited
            if (popNode.nodeNum % CELLWIDTH < CELLWIDTH-1):
                rightNode = nodeMap[popNode.nodeNum + 1]
                if(rightNode.status == 'notvisited'):
                    rightNode.status = 'visited'
                    rightNode.parent = popNode
                    rightNode.color = GRAY
                    nodeVisitCount += 1
                    q.put(rightNode)
            #Check if top node exists and status = notvisited
            if (popNode.nodeNum >= CELLWIDTH):
                topNode = nodeMap[popNode.nodeNum - CELLWIDTH]
                if(topNode.status == 'notvisited'):
                    topNode.status = 'visited'
                    topNode.parent = popNode
                    topNode.color = GRAY
                    nodeVisitCount += 1
                    q.put(topNode)
            #Check if left node exists and status = notvisited
            if (popNode.nodeNum % CELLWIDTH) > 0:
                leftNode = nodeMap[popNode.nodeNum - 1]
                if(leftNode.status == 'notvisited'):
                    leftNode.status = 'visited'
                    leftNode.parent = popNode
                    leftNode.color = GRAY
                    nodeVisitCount += 1
                    q.put(leftNode)
        else:
            break
    print('Number of nodes visited = %d' %nodeVisitCount)
    return(tracePath(start, goal, nodeMap))
    

#A* Search in 2D Grid
def AStar(start, goal, nodeMap):
    #Init
    heap = []
    bottomNode = rightNode = topNode = leftNode = None
    global nodeVisitCount
    nodeVisitCount = 0
    
    #Genereate Heuristic Table
    generate_h_value(goal, nodeMap)

    #Initialize and insert start node into heap
    start.status = 'visited'
    start.color = WHITE
    heappush(heap, start)

    #Get items from heap and isert neighbor nodes into heap; stop on reaching goal node
    while heap:
        heapify(heap)
        current = heappop(heap)
        #print('Current = %d' %current.nodeNum)
        if current.nodeNum == goal.nodeNum:
            break

        bottomNode = rightNode = topNode = leftNode = None
        
        #Check if bottom node exits and status = notvisited
        if (current.nodeNum < CELLWIDTH*(CELLHEIGHT-1)):
            bottomNode = nodeMap[current.nodeNum + CELLWIDTH]
            if(bottomNode.status == 'notvisited'):
                bottomNode.status = 'visited'
                bottomNode.parent = current
                bottomNode.gValue = bottomNode.hValue + 10
                bottomNode.color = GRAY
                nodeVisitCount += 1
                heappush(heap,bottomNode)
            elif(bottomNode.gValue > current.gValue + 10):
                bottomNode.parent = current
                bottomNode.gValue = current.gValue + 10
                    
        #Check if right node exists and status = notvisited
        if (current.nodeNum % CELLWIDTH < CELLWIDTH-1):
            rightNode = nodeMap[current.nodeNum + 1]
            if(rightNode.status == 'notvisited'):
                rightNode.status = 'visited'
                rightNode.parent = current
                rightNode.gValue = rightNode.hValue + 10
                rightNode.color = GRAY
                nodeVisitCount += 1
                heappush(heap,rightNode)
            elif(rightNode.gValue > current.gValue + 10):
                rightNode.parent = current
                rightNode.gValue = current.gValue + 10
                    
        #Check if top node exists and status = notvisited
        if (current.nodeNum >= CELLWIDTH):
            topNode = nodeMap[current.nodeNum - CELLWIDTH]
            if(topNode.status == 'notvisited'):
                topNode.status = 'visited'
                topNode.parent = current
                topNode.gValue = topNode.hValue + 10
                topNode.color = GRAY
                nodeVisitCount += 1
                heappush(heap,topNode)
            elif(topNode.gValue > current.gValue + 10):
                topNode.parent = current
                topNode.gValue = current.gValue + 10
                    
        #Check if left node exists and status = notvisited
        if (current.nodeNum % CELLWIDTH) > 0:
            leftNode = nodeMap[current.nodeNum - 1]
            if(leftNode.status == 'notvisited'):
                leftNode.status = 'visited'
                leftNode.parent =  current
                leftNode.gValue = leftNode.hValue + 10
                leftNode.color = GRAY
                nodeVisitCount += 1
                heappush(heap,leftNode)
            elif(leftNode.gValue > current.gValue + 10):
                leftNode.parent = current
                leftNode.gValue = current.gValue + 10

    print('Number of nodes visited = %d' %nodeVisitCount)
    return(tracePath(start, goal, nodeMap))

#Main method
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake')
    runGame()
        #showGameOverScreen()


def runGame():
    #Generate Node Map
    nodeMap = genEmptyNodeMap()

    global nodeVisitCount
    
    #Create worm
    worm = Worm()
    #Set random start point
    startNodeNum = random.randint(5, (CELLWIDTH * CELLHEIGHT)-1)
    startNode = nodeMap[startNodeNum]
    #Set worm intial coordinates
    worm.xCoord = startNode.xCoord
    worm.yCoord = startNode.yCoord
    
    while True:
        #Reset Map
        nodeMap = genEmptyNodeMap()
        #Set random goal point
        goalNodeNum = random.randint(0, (CELLWIDTH * CELLHEIGHT)-1)
        goalNode = nodeMap[goalNodeNum]

        #Set startNode to snake's head
        startNode = nodeMap[worm.yCoord * CELLWIDTH + worm.xCoord]
        #print('Snake Node Number = %d' %(worm.yCoord * CELLWIDTH + worm.xCoord))
        #Get shortest path from BFS
        print('StartNode = %d' %startNode.nodeNum)
        print('GoalNode = %d' %goalNode.nodeNum)
        path = AStar(startNode, goalNode, nodeMap)

        #for node in path:
        #   print(node.nodeNum)

        #Generate list of directions    
        directions = list()
        lastNode = path[0]
        path = path[1:]
        for node in path:
            currNode =  node
            if(currNode.yCoord==lastNode.yCoord and currNode.xCoord == lastNode.xCoord+1):
                directions.append('right')
            elif(currNode.yCoord==lastNode.yCoord and currNode.xCoord == lastNode.xCoord-1):
                directions.append('left')
            elif(currNode.xCoord==lastNode.xCoord and currNode.yCoord == lastNode.yCoord+1):
                directions.append('down')
            elif(currNode.xCoord==lastNode.xCoord and currNode.yCoord == lastNode.yCoord-1):
                directions.append('up')
            lastNode = currNode
        #print(directions)
        
        DISPLAYSURF.fill(BGCOLOR)
        colorPath(nodeMap)
        drawGrid()
        drawGoal(goalNode)
        drawWorm(worm)
        drawNodeVisitCount(nodeVisitCount)
        
        for direction in directions:
            if direction == 'up':
                worm.yCoord = worm.yCoord - 1
            elif direction == 'down':
                worm.yCoord = worm.yCoord + 1
            elif direction == 'left':
                worm.xCoord = worm.xCoord - 1  
            elif direction == 'right':
                worm.xCoord = worm.xCoord + 1
               
            DISPLAYSURF.fill(BGCOLOR)
            colorPath(nodeMap)
            drawGrid()
            drawGoal(goalNode)
            drawWorm(worm)
            drawNodeVisitCount(nodeVisitCount)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            pygame.time.delay(200)
            #Display worm initial coordinates
         

def colorPath(nodeMap):
    for node in nodeMap:
        nodeRect = pygame.Rect(node.xCoord*CELLSIZE, node.yCoord*CELLSIZE, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, node.color, nodeRect)


def drawNodeVisitCount(nodeVisitCount):
    nvcSurf = BASICFONT.render('Nodes Visited: %s' % (nodeVisitCount), True, RED)
    nvcRect = nvcSurf.get_rect()
    nvcRect.topleft = (WINDOWWIDTH - 180, 10)
    DISPLAYSURF.blit(nvcSurf, nvcRect)


def drawWorm(worm):
    x = worm.xCoord * CELLSIZE
    y = worm.yCoord * CELLSIZE
    wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
    wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
    pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawGoal(goal):
    x = goal.xCoord * CELLSIZE
    y = goal.yCoord * CELLSIZE
    goalRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, goalRect)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))
        

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return


if __name__ == '__main__':
    main()

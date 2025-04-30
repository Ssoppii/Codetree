MAX_CONTAINER = 20
MAX_MICRO = 55

dr = [-1, 0, 1, 0]
dc = [0, -1, 0, 1]

containerSize = 0
experimentCount = 0

cultureBoard = [[0 for _ in range(MAX_CONTAINER)] for _ in range(MAX_CONTAINER)]
newCultureBoard = [[0 for _ in range(MAX_CONTAINER)] for _ in range(MAX_CONTAINER)]
visited = [[False for _ in range(MAX_CONTAINER)] for _ in range(MAX_CONTAINER)]

connectedComponentCount = [0 for _ in range(MAX_MICRO)]

microSize = [0 for _ in range(MAX_MICRO)]
microBoundingStart = [(0,0) for _ in range(MAX_MICRO)]
microBoundingEnd = [(0,0) for _ in range(MAX_MICRO)]

def dfsMarkComponent(row, col, microId):
    visited[row][col] = True
    for dir in range(4):
        newRow = row + dr[dir]
        newCol = col + dc[dir]
        if not (0 <= newRow < containerSize and 0 <= newCol < containerSize):
            continue
        if visited[newRow][newCol]:
            continue
        if cultureBoard[newRow][newCol] != microId:
            continue
        dfsMarkComponent(newRow, newCol, microId)

def removeMicroorganism(microId):
    for row in range(containerSize):
        for col in range(containerSize):
            if cultureBoard[row][col] == microId:
                cultureBoard[row][col] = 0

def arrangeMicroorganisms(microId, injectionRow1, injectionCol1, injectionRow2, injectionCol2):
    for row in range(containerSize):
        for col in range(containerSize):
            visited[row][col] = False
    for id in range(1, microId + 1):
        connectedComponentCount[id] = 0

    for row in range(injectionRow1, injectionRow2):
        for col in range(injectionCol1, injectionCol2):
            cultureBoard[row][col] = microId

    for row in range(containerSize):
        for col in range(containerSize):
            if cultureBoard[row][col] == 0:
                continue
            if visited[row][col]:
                continue
            currentMicroId = cultureBoard[row][col]
            connectedComponentCount[currentMicroId] += 1
            dfsMarkComponent(row, col, currentMicroId)

    for id in range(1, microId + 1):
        if connectedComponentCount[id] >= 2:
            removeMicroorganism(id)

def relocateMicroorganisms(microCount):
    for row in range(containerSize):
        for col in range(containerSize):
            newCultureBoard[row][col] = 0
    for id in range(1, microCount + 1):
        microSize[id] = 0
        microBoundingStart[id] = (10**9, 10**9)
        microBoundingEnd[id] = (0, 0)

    for row in range(containerSize):
        for col in range(containerSize):
            currentMicroId = cultureBoard[row][col]
            if currentMicroId == 0:
                continue
            microSize[currentMicroId] += 1
            microBoundingStart[currentMicroId] = (min(microBoundingStart[currentMicroId][0], row), min(microBoundingStart[currentMicroId][1], col))
            microBoundingEnd[currentMicroId] = (max(microBoundingEnd[currentMicroId][0], row), max(microBoundingEnd[currentMicroId][1], col))

    relocationOrder = []
    for id in range(1, microCount + 1):
        if microSize[id] == 0:
            continue
        relocationOrder.append((-microSize[id], id))
    relocationOrder.sort()

    for orderPair in relocationOrder:
        currentMicroId = orderPair[1]
        boundingStart = microBoundingStart[currentMicroId]
        boundingEnd = microBoundingEnd[currentMicroId]
        clusterRowCount = boundingEnd[0] - boundingStart[0] + 1
        clusterColCount = boundingEnd[1] - boundingStart[1] + 1

        for newRow in range(containerSize - clusterRowCount + 1):
            placedForThisRow = False
            for newCol in range(containerSize - clusterColCount + 1):
                canPlace = True
                for dr in range(clusterRowCount):
                    for dc in range(clusterColCount):
                        originalRow = boundingStart[0] + dr
                        originalCol = boundingStart[1] + dc
                        if cultureBoard[originalRow][originalCol] != currentMicroId:
                            continue
                        if newCultureBoard[newRow + dr][newCol + dc] != 0:
                            canPlace = False
                            break
                    if not canPlace:
                        break
                if canPlace:
                    for dr in range(clusterRowCount):
                        for dc in range(clusterColCount):
                            originalRow = boundingStart[0] + dr
                            originalCol = boundingStart[1] + dc
                            if cultureBoard[originalRow][originalCol] != currentMicroId:
                                continue
                            newCultureBoard[newRow + dr][newCol + dc] = currentMicroId
                    placedForThisRow = True
                    break
            if placedForThisRow:
                break

    for row in range(containerSize):
        for col in range(containerSize):
            cultureBoard[row][col] = newCultureBoard[row][col]

def calculateExperimentResult(microCount):
    isAdjacent = [[False for _ in range(MAX_MICRO)] for _ in range(MAX_MICRO)]

    for row in range(containerSize):
        for col in range(containerSize):
            if cultureBoard[row][col] == 0:
                continue
            for dir in range(4):
                adjRow = row + dr[dir]
                adjCol = col + dc[dir]
                if not (0 <= adjRow < containerSize and 0 <= adjCol < containerSize):
                    continue
                if cultureBoard[adjRow][adjCol] == 0:
                    continue
                if cultureBoard[row][col] != cultureBoard[adjRow][adjCol]:
                    idA = cultureBoard[row][col]
                    idB = cultureBoard[adjRow][adjCol]
                    isAdjacent[idA][idB] = True
                    isAdjacent[idB][idA] = True

    experimentScore = 0
    for idA in range(1, microCount + 1):
        for idB in range(idA + 1, microCount + 1):
            if isAdjacent[idA][idB]:
                experimentScore += microSize[idA] * microSize[idB]
    print(experimentScore)

containerSize, experimentCount = map(int, input().split())

for row in range(containerSize):
    for col in range(containerSize):
        cultureBoard[row][col] = 0

for experimentId in range(1, experimentCount + 1):
    r1, c1, r2, c2 = map(int, input().split())
    arrangeMicroorganisms(experimentId, r1, c1, r2, c2)
    relocateMicroorganisms(experimentId)
    calculateExperimentResult(experimentId)
#region Import libraries
import sys
import csv
import random
import math
import config
from tkinter import *
from tkinter import ttk
#endregion

#region Initialisation

GRID_X = 18
GRID_Y = 18
GRID_CHAR_SIZE  = 8
naturalTypes = []
builtTypes = []
setupArraysPointer = 0
file = open('tileSetup.csv')
csvreader = csv.reader(file)
naturalTypes = next(csvreader)
for row in csvreader:
    builtTypes.append(row)

def checkTileValid(naturalType, builtType):  
    builtTypesNames = [builtType[0] for builtType in builtTypes]
    builtTypesIndex = builtTypesNames.index(builtType)
    naturalTypeIndex = naturalTypes.index(naturalType)
    temp = builtTypes[builtTypesIndex][naturalTypeIndex]
    if int(builtTypes[builtTypesIndex][naturalTypeIndex]) == 1:
        return True
    else:
        return False

class gameWindow():
    
    def __init__(self):
        root = Tk()
        root.resizable(0, 0)
        root.geometry(str(config.GameWindowX) + "x" + str(config.GameWindowY))
        gameFrame = ttk.Frame(root, padding = 10)
        gameFrame.grid()
        ttk.Label(gameFrame, text="Hello World!").grid(column=0, row=0)
        ttk.Button(gameFrame, text="Quit", command=root.destroy).grid(column=1, row=0)
        root.mainloop()
        

class tileMap():
    
    def __init__(self):
        super().__init__()
        self.map = []
        for y in range(GRID_Y):
            for x in range(GRID_X):
                self.map.append([x, y])
        self.mapTiles = []
        for i in self.map:
            self.mapTiles.append(tileTemplate())
        self.generateRivers()
        self.generateRoads()
        
    
    def generateRivers(self):
        for i in range(config.RiverCount):
            RiverPointer = [random.randint(config.RiverFromEdge, GRID_X - config.RiverFromEdge), random.randint(config.RiverFromEdge, GRID_Y - config.RiverFromEdge)]
            NewRiverTileIndex = self.map.index(RiverPointer)
            self.mapTiles[NewRiverTileIndex].naturalType = "river"
            RiverDirectionA = math.radians(random.randint(0, 359))
            RiverDirectionB = RiverDirectionA + math.radians(180)
            endedEarly = self.generateRiverLine(RiverPointer, RiverDirectionA, False)
            self.generateRiverLine(RiverPointer, RiverDirectionB, endedEarly)
                
    def generateRiverLine(self, startTile, angle, canEndEarly):
        hypotenuse = 0
        exitLoops = False
        while not exitLoops:
            for i in range(config.RiverSegmentSize):
                hypotenuse += config.RiverCheckInterval
                XAxis = math.floor(startTile[0] + math.sin(angle) * hypotenuse)
                YAxis = math.floor(startTile[1] + math.cos(angle) * hypotenuse)
                if XAxis > GRID_X - 1 or XAxis < 0:
                    exitLoops = True
                    break
                elif YAxis > GRID_Y - 1 or YAxis < 0:
                    exitLoops = True
                    break
                tileIndex = self.map.index([XAxis, YAxis])
                self.mapTiles[tileIndex].naturalType = "river"
            angle += math.radians(random.randint(-config.RiverWobble, config.RiverWobble))
            if canEndEarly == True and random.random() < config.RiverEndingChange:
                return True
        return False

    def generateRoads(self):
        for i in range(config.RoadMapCount):
            startingTile = random.choice(self.mapTiles)
            startingTileCoords = self.map[self.mapTiles.index(startingTile)]
            while not ((startingTileCoords[0] > config.RoadStartingBoundaries) and (startingTileCoords[0] < (GRID_X - config.RoadStartingBoundaries)) and (startingTileCoords[1] > config.RoadStartingBoundaries) and (startingTileCoords[1] < (GRID_Y - config.RoadStartingBoundaries))):   
                startingTile = random.choice(self.mapTiles)
                startingTileCoords = self.map[self.mapTiles.index(startingTile)]
                while not checkTileValid(startingTile.naturalType, "road"):
                    startingTile = random.choice(self.mapTiles)
                    startingTileCoords = self.map[self.mapTiles.index(startingTile)]
                    
            startingTile.builtType = "road"
            self.layRoadMap(startingTile)
    
    def layRoadMap(self, startingTile):
        lastTileCoords = self.map[self.mapTiles.index(startingTile)]
        segmentsLayed = 0
        isFinishedRoad = False
        exitingMapSpace = False
        # Setting random early avoids direction selection bias for 1st pick in the while statement
        isX = bool(random.getrandbits(1))
        isPositiveDirection = bool(random.getrandbits(1))
        while not isFinishedRoad:
            if segmentsLayed >= config.MinRoadSegments and config.RoadSegmentEndChance < random.random():
                isFinishedRoad = True
                break
            previousX = isX
            previousPositiveDirection = isPositiveDirection
            if self.mapTiles[self.map.index(lastTileCoords)].builtType != "bridge":
                if random.random() < config.RoadSegmentDirectionChangeChance:
                    isX = bool(random.getrandbits(1))
                    isPositiveDirection = bool(random.getrandbits(1))
            while previousX == isX and previousPositiveDirection != isPositiveDirection:
                isX = bool(random.getrandbits(1))
                isPositiveDirection = bool(random.getrandbits(1))                
            for i in range(config.RoadSegmentSize):
                if isFinishedRoad == True:
                    break
                if isX:
                    deltaX = 1 if isPositiveDirection else -1
                    newCoords = [lastTileCoords[0] + deltaX, lastTileCoords[1]]
                else:
                    deltaY = 1 if isPositiveDirection else -1
                    newCoords = [lastTileCoords[0], lastTileCoords[1] + deltaY]
                try:
                    newTile = self.mapTiles[self.map.index(newCoords)]
                except ValueError:
                    exitingMapSpace = True
                else:
                    if checkTileValid(newTile.naturalType, "road"):
                        newTile.builtType = "road"
                    elif checkTileValid(newTile.naturalType, "bridge"):
                        newTile.builtType = "bridge"
                if exitingMapSpace == True:
                    #Change axis and travel random direction, if not go the other one, if not cancel layout and roadFinished = True
                    oldPositiveDirection = isPositiveDirection
                    isX = not isX
                    isPositiveDirection = bool(random.getrandbits(1))
                    hasFailedBefore = False
                    for isReverseDirection in [1, -1]:
                        try:
                            if isX:
                                deltaX = config.RoadSegmentSize if isPositiveDirection else -config.RoadSegmentSize
                                newCoords = [lastTileCoords[0] + deltaX * isReverseDirection, lastTileCoords[1]]
                            else:
                                deltaY = config.RoadSegmentSize if isPositiveDirection else -config.RoadSegmentSize
                                newCoords = [lastTileCoords[0], lastTileCoords[1] + deltaY * isReverseDirection]
                            newTile = self.mapTiles[self.map.index(newCoords)]
                            if checkTileValid(newTile.naturalType, "road"):
                                newTile.builtType = "road"
                            elif checkTileValid(newTile.naturalType, "bridge"):
                                newTile.builtType = "bridge"    
                        except ValueError:
                            if hasFailedBefore == False:
                                hasFailedBefore = True
                            else:
                                isFinishedRoad = True
                                break
                        else:
                            #Flipping directions to opposite of original map ending
                            isX = not isX
                            isPositiveDirection = not oldPositiveDirection
                            for i2 in range(i):
                                if isFinishedRoad == True:
                                    break
                                if isX:
                                    deltaX = 1 if isPositiveDirection else -1
                                    newCoords = [lastTileCoords[0] + deltaX, lastTileCoords[1]]
                                else:
                                    deltaY = 1 if isPositiveDirection else -1
                                    newCoords = [lastTileCoords[0], lastTileCoords[1] + deltaY]
                                try:
                                    newTile = self.mapTiles[self.map.index(newCoords)]
                                except ValueError:
                                    # The map would have to be smaller than segment size to get here
                                    isFinishedRoad = True
                                    break
                                else:
                                    if checkTileValid(newTile.naturalType, "road"):
                                        newTile.builtType = "road"
                                    elif checkTileValid(newTile.naturalType, "bridge"):
                                        newTile.builtType = "bridge"
                                lastTileCoords = self.map[self.mapTiles.index(newTile)]
                        exitingMapSpace = False
                lastTileCoords = self.map[self.mapTiles.index(newTile)]
            segmentsLayed += 1
            
                                        
    def printMap(self):
        xHeader = '    '
        for x in range(GRID_X):
            xHeader += str(x) + ' ' * (GRID_CHAR_SIZE - len(str(x)) + 1)
        print(xHeader)
        for y in range(GRID_Y):
            xLine = str(y) + '   '
            if len(xLine) > 4:
                xLine = xLine[:4]
            for x in range(GRID_X):
                pointer = x + y * GRID_X
                text = self.mapTiles[pointer].builtType
                if text is None:
                    text = self.mapTiles[pointer].naturalType
                # try:
                #     text += ' ' + str(self.mapTiles[pointer].builtType)[0]
                # except ValueError:
                #     return
                if len(text) > GRID_CHAR_SIZE:
                    text = text[:GRID_CHAR_SIZE]
                else:
                    text = text + ' ' * (GRID_CHAR_SIZE - len(text))
                xLine += text + '|'
            xLine = xLine[:-1]
            print(xLine)

    def processInput(self, mapIndex, command):
        tilePointer = self.mapTiles[mapIndex]
        match command:
            case 'build': 
                buildingName = input('What building would you like to place? ').lower()
                tilePointer.build(buildingName)
            case _: 
                print('Not defined yet')
           
class tileTemplate():

    def __init__(self):
        super().__init__()
        self.naturalType = naturalTypes[1]
        self.builtType = None

    def __str__(self):
        return f'tile({self.naturalType},{self.builtType})'
    
    def build(self, building):
        match building:
            case 'farm':
                if self.naturalType == 'Plain' or self.naturalType == 'Hill':
                    self.builtType = 'Farm'
                else:
                    print(f'A {building} cannot be placed on a {self.naturalType} tile.')
            case 'mine':
                if self.naturalType == 'Plain' or self.naturalType == 'Hill' or self.naturalType == 'Mountain':
                    self.builtType = 'Mine'
                else:
                    print(f'A {building} cannot be placed on a {self.naturalType} tile.')
            case 'coal powered turbine':
                if self.naturalType == 'Plain' or self.naturalType == 'Hill':
                    self.builtType = 'Coal Powered Turbine'
                else:
                    print(f'A {building} cannot be placed on a {self.naturalType} tile.')
            case _:
                print('Error - Building input is not valid')

#endregion

#region Main
def main():
    window = gameWindow()
    #main_menu.main()
    econGame = tileMap()
    while True:
        econGame.printMap()
        try:
            x = int(input('x? '))
        except:
            print('x - bad input')
        try:
            y = int(input('y? '))
        except:
            print('y - bad input')
        command = input('What would you like to do? ').lower()

        mapIndex = (econGame.map.index([x, y]))
        if command == 'quit':
            sys.exit()
        else:
            econGame.processInput(mapIndex, command)
#endregion

# Start
if __name__ == '__main__':
    main()

#region Import libraries
import sys
import random
import main_menu
#endregion

#region Initialisation

#region Establish types
GRID_X = 5
GRID_Y = 8
GRID_CHAR_SIZE  = 12
naturalTypes = []
builtTypes = []
setupArraysPointer = 0
with open('tileSetup.txt', 'r') as tileSetup:
    for line in tileSetup:
        line = line.strip()
        if line == '':
            break
        elif line.startswith('#'):
            continue
        elif line.startswith('`'):
            setupArraysPointer += 1
        else: 
            if setupArraysPointer == 0:
                naturalTypes.append(line)
            elif setupArraysPointer == 1:
                builtTypes.append(line) 
#endregion

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

    def printMap(self):
        xHeader = '  '
        for x in range(GRID_X):
            xHeader += str(x) + '          '
        print(xHeader)
        for y in range(GRID_Y):
            xLine = str(y) + ' '
            for x in range(GRID_X):
                pointer = x + y * GRID_X
                text = self.mapTiles[pointer].naturalType
                try:
                    text += ' ' + str(self.mapTiles[pointer].builtType)[0]
                except:
                    return
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
        self.naturalType = naturalTypes[random.randint(0, 4)]
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

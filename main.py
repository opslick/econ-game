# Import libraries
import sys
import random
import main_menu


#region Initialisation

GRID_X = 4
GRID_Y = 3
# tileSetup.txt
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

class tileMap():
    
    def __init__(self):
        super().__init__()
        self.map = []
        for y in range(GRID_Y):
            for x in range(GRID_X):
                self.map.append([x, y])
        self.mapTiles = []
        for i in self.map:
            self.mapTiles.append([i, tileTemplate()])

    def processInput(self, mapIndex, command):
        tilePointer = self.mapTiles.index(mapIndex)
        match command:
            case 'Build': 
                buildingName = input('What building would you like to place? ')
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
            case 'Farm':
                if self.naturalType == 'Plain' or self.naturalType == 'Hill':
                    return
                else:
                    return f'{building} cannot be placed on a {self.naturalType} tile.'
            case 'Mine':
                if self.naturalType == 'Plain' or self.naturalType == 'Hill' or self.naturalType == 'Mountain':
                    return
                else:
                    return f'{building} cannot be placed on a {self.naturalType} tile.'
            case 'Coal Powered Turbine':
                if self.naturalType == 'Plain' or self.naturalType == 'Hill':
                    return
                else:
                    return f'{building} cannot be placed on a {self.naturalType} tile.'
            case _:
                print('Error - Building input is not valid')


#endregion

# Main
def main():
    #main_menu.main()
    econGame = tileMap()
    while True:
        for y in range(GRID_Y):
            xLine = ''
            for x in range(GRID_X):
                xLine += str(econGame.map[x + y * GRID_X]) + '|'
            xLine = xLine[:-1]
            print(xLine)
        try:
            x = int(input('x? '))
        except:
            print('x - bad input')
        try:
            y = int(input('y? '))
        except:
            print('y - bad input')
        command = input('What would you like to do? ')

        mapIndex = (econGame.map.index([x, y]))
        if command == 'quit':
            sys.exit()
        else:
            econGame.processInput(mapIndex, command)

# Start
if __name__ == '__main__':
    main()










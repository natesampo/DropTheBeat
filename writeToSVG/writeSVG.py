import svgwrite
from svgwrite import mm, cm
import numpy as np
import convertMidi



strokeColor = "red" #
svgname = 'testHoney.svg'#file to load
# mm = 3.543 #simple conversions between px and other formats
# cm = 35.43
# inch = 90
sw = str(0.1)#width of drawn lines
sysMult = 1 # chosen multiplier for all inputs
# sysDict = {3.543:'mm',35.43:'cm',90:'inches'}
print(sysMult)
honeyComb = 0
def convertIn(unit):
    return str(unit)

class svgCut:
    '''This is the object that controls most of the operations of writing to the
    svg'''
    def __init__(self,numHoles,holeRadius,holeSpace,borderSpace):
        self.numHoles = numHoles
        self.holeRadius = holeRadius
        self.holeSpacex = holeSpace[0] #x distance between holes.. should be at least radius * 2
        self.holeSpacey = holeSpace[1]
        self.borderSpacex = borderSpace[0]
        self.borderSpacey =  borderSpace[1]#extra space on the sides where no holes will be drawn
        self.borderSpaceEnd = borderSpace[2]
        if honeyComb:
            self.pagex = self.borderSpacex * 2 + (self.numHoles-.5) * self.holeSpacex + 2 * self.holeRadius
        else:
            self.pagex = self.borderSpacex * 2 + (self.numHoles - 1) * self.holeSpacex + self.holeRadius * 2 #from what we are already given we can calculate width of page

    def drawRectangle(self,dwg,origin = (0,0), end = None):
        '''This will draw a rectangle around the border so it can be properly cut'''
        if end is None:
            end = (self.pagex,self.pagey)
        lines = [[origin, (origin[0],end[1])], [origin, (end[0],origin[1])],[end, (origin[0],end[1])], [end,  (end[0],origin[1])]]
        for line in lines:
            dwg.add(dwg.line(start = (convertIn(line[0][0]),convertIn(line[0][1])),end = (convertIn(line[1][0]),convertIn(line[1][1])),stroke=strokeColor,stroke_width=sw))
        pass


    def drawHole(self, dwg, point):
        '''quick code to add a hold to the previous specifications'''

        if honeyComb:
            if point[1] % 2:
                centerx = self.borderSpacex + self.holeSpacex * (point[0]+.5) + self.holeRadius
                centery = self.holeSpacey * (point[1]//2+.5) + self.holeRadius

            else:
                centerx = self.borderSpacex + self.holeSpacex * (point[0]) + self.holeRadius
                centery = self.holeSpacey * (point[1]//2) + self.holeRadius
        else:
            centerx = self.borderSpacex + self.holeSpacex * point[0] + self.holeRadius
            centery = self.holeSpacey * point[1] + self.holeRadius
        dwg.add(dwg.circle(center=(convertIn(centerx),convertIn(self.borderSpacey + centery)),
                        r=convertIn(self.holeRadius),fill_opacity = 0.0,stroke=strokeColor,stroke_width=sw))

    def drawHoles(self,holeArray):
        '''draw all holes given an array of positions'''
        if(len(holeArray[0]) != self.numHoles):#check to make sure size of  array is correct
            print('DIMENSION MISMATCH')
            return 0
        if honeyComb:
            self.pagey = (len(holeArray)//2 + 1) * self.holeSpacey +  self.borderSpacey + self.borderSpaceEnd
        else:
            self.pagey = (len(holeArray) + 1) * self.holeSpacey  +  self.borderSpacey + self.borderSpaceEnd#calculate pag length
        xString = str(self.pagex) + 'in' #string stuff
        yString = str(self.pagey) + 'in'
        print('Width in inches: ',str(self.pagex))
        print('Height in inches: ',str(self.pagey))
        dwg = svgwrite.Drawing(svgname, size = (xString, yString))
        dwg.defs
        dwg.viewbox(0,0,width = self.pagex, height = self.pagey)
        for i,line in enumerate(holeArray): #cut holes in array where element  != 0
            [self.drawHole(dwg,(j,i)) for j,v in enumerate(line) if v]
        self.drawRectangle(dwg)
        dwg.save()

def addHoles(timeArr, cutArr, minTime = 0):

    unit = min(timeArr)
    timeArr[0] = 0
    if unit >= minTime:
        minTime = unit
    plus = 0
    empty = [0] * len(cutArr[0])
    for i,v in enumerate(timeArr):
        extra = round(v/minTime)-1
        for j in range(extra):
            print('Done')

            cutArr = np.insert(cutArr,i+ plus, empty, axis = 0)
            plus += 1
    print(cutArr)
    return cutArr




if __name__ == "__main__":
    print("WHAT")
    svgname = 'doctor.svg'
    # dictN = {60:0 ,62:1,64:2 ,65:3, 67:4}
    cutObj = svgCut(numHoles = 30,holeRadius = .265/2,holeSpace = [2*(.265 + 0.0751011),.265], borderSpace= [.251,1,1])
    convertMidi.printTracks('doctor.mid')
    times, cutArr = convertMidi.readMidi('doctor.mid', trackNumbers = list(range(0,14)), baseNote = 40, noteRange = 30, noteLim = 60,offset = 0)
    print(times)
    cutArr = addHoles(times, cutArr)
    cutObj.drawHoles(cutArr)
    # svgname = 'pushStick.svg'
    # cutObj.drawHoles([[0,0,0,0,0]])

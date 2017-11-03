import svgwrite
from svgwrite import mm, cm
import numpy as np
import convertMidi



strokeColor = "red" #
svgname = 'testHoney.svg'#file to load
mm = 3.543 #simple conversions between px and other formats
cm = 35.43
inch = 90
sw = 0.1 * inch #width of drawn lines
sysMult = inch # chosen multiplier for all inputs
sysDict = {3.543:'mm',35.43:'cm',90:'inches'}
print(sysMult)
honeyComb = 1
class svgCut:
    '''This is the object that controls most of the operations of writing to the
    svg'''
    def __init__(self,numHoles,holeRadius,holeSpace,borderSpace):
        self.numHoles = numHoles
        self.holeRadius = holeRadius * sysMult
        self.holeSpacex = holeSpace[0] * sysMult #x distance between holes.. should be at least radius * 2
        self.holeSpacey = holeSpace[1] * sysMult
        self.borderSpace = borderSpace * sysMult #extra space on the sides where no holes will be drawn
        if honeyComb:
            self.pagex = self.borderSpace * 2 + (self.numHoles) * self.holeSpacex + self.holeRadius * 2
        else:
            self.pagex = self.borderSpace * 2 + (self.numHoles - 1) * self.holeSpacex + self.holeRadius * 2 #from what we are already given we can calculate width of page

    def drawRectangle(self,dwg,origin = (0,0), end = None):
        '''This will draw a rectangle around the border so it can be properly cut'''
        if end is None:
            end = (self.pagex,self.pagey)
        lines = [[origin, (origin[0],end[1])], [origin, (end[0],origin[1])],[end, (origin[0],end[1])], [end,  (end[0],origin[1])]]
        for line in lines:
            dwg.add(dwg.line(start = line[0],end = line[1],stroke=strokeColor,stroke_width=sw))
        pass

    def drawHole(self, dwg, point):
        '''quick code to add a hold to the previous specifications'''

        if honeyComb:
            if point[1] % 2:
                centerx = self.borderSpace + self.holeSpacex * (point[0]+.5) + self.holeRadius
                centery = self.holeSpacey * (point[1]//2+.5) + self.holeRadius

            else:
                centerx = self.borderSpace + self.holeSpacex * (point[0]) + self.holeRadius
                centery = self.holeSpacey * (point[1]//2) + self.holeRadius
        else:
            centerx = self.borderSpace + self.holeSpacex * point[0] + self.holeRadius
            centery = self.holeSpacey * point[1] + self.holeRadius
        dwg.add(dwg.circle(center=(centerx,centery),
                        r=self.holeRadius,fill_opacity = 0.0,stroke=strokeColor,stroke_width=sw))

    def drawHoles(self,holeArray):
        '''draw all holes given an array of positions'''
        if(len(holeArray[0]) != self.numHoles):#check to make sure size of  array is correct
            print('DIMENSION MISMATCH')
            return 0
        self.pagey = (len(holeArray) + 1) * self.holeSpacey #calculate pag length
        xString = str(int(self.pagex)) + 'px' #string stuff
        yString = str(int(self.pagey)) + 'px'
        print('Width in',sysDict[sysMult], ': ',str(self.pagex / sysMult))
        print('Height in',sysDict[sysMult], ': ',str(self.pagey / sysMult))
        dwg = svgwrite.Drawing(svgname, size = (xString, yString))
        for i,line in enumerate(holeArray): #cut holes in array where element  != 0
            [self.drawHole(dwg,(j,i)) for j,v in enumerate(line) if v]
        self.drawRectangle(dwg)
        dwg.save()




if __name__ == "__main__":
    cutObj = svgCut(numHoles = 10,holeRadius = .125,holeSpace = [2*(.265 + 0.0751011),.265], borderSpace= .25)
    convertMidi.printTracks('doctor.mid')
    times, cutArr = convertMidi.readMidi('doctor.mid', trackNumbers = [0,1], baseNote = 64, noteRange = 10, noteLim = 120,offset = 0)
    cutObj.drawHoles(cutArr)

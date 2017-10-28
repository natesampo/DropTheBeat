import svgwrite
from svgwrite import mm, cm
import numpy as np
import testMidi



strokeColor = "red" #
svgname = 'test.svg'#file to load
mm = 3.543 #simple conversions between px and other formats
cm = 35.43
inch = 90
sw = 0.001 * inch #width of drawn lines
sysMult = inch # chosen multiplier for all inputs

print(sysMult)
class svgCut:
    '''This is the object that controls most of the operations of writing to the
    svg'''
    def __init__(self,numHoles,holeRadius,holeSpace,borderSpace):
        self.numHoles = numHoles
        self.holeRadius = holeRadius * sysMult
        self.holeSpacex = holeSpace[0] * sysMult #x distance between holes.. should be at least radius * 2
        self.holeSpacey = holeSpace[1] * sysMult
        self.borderSpace = borderSpace * sysMult #extra space on the sides where no holes will be drawn
        self.pagex = self.borderSpace * 2 + (self.numHoles - 1) * self.holeSpacex + self.holeRadius * 2 #from what we are already given we can calculate width of page

    def drawRectangle():
        '''This will draw a rectangle around the border so it can be properly cut'''
        #TODO
        pass

    def drawHole(self, dwg, point):
        '''quick code to add a hold to the previous specifications'''
        dwg.add(dwg.circle(center=(self.borderSpace + self.holeSpacex * point[0] + self.holeRadius, self.holeSpacey * point[1] + self.holeRadius),
                            r=self.holeRadius,fill_opacity = 0.0,stroke=strokeColor,stroke_width=sw))

    def drawHoles(self,holeArray):
        '''draw all holes given an array of positions'''
        if(len(holeArray[0]) != self.numHoles):#check to make sure size of  array is correct
            return 0
        self.pagey = (len(holeArray) + 1) * self.holeSpacey #calculate pag length
        xString = str(int(self.pagex)) + 'px' #string stuff
        yString = str(int(self.pagey)) + 'px'
        dwg = svgwrite.Drawing(svgname, size = (xString, yString))
        for i,line in enumerate(holeArray): #cut holes in array where element  != 0
            [self.drawHole(dwg,(j,i)) for j,v in enumerate(line) if v]
        dwg.save()




if __name__ == "__main__":
    cutObj = svgCut(numHoles = 36,holeRadius = .125,holeSpace = [.25,.25], borderSpace= 1)
    testMidi.printTracks('chopstik.mid')
    times, cutArr = testMidi.readMidi('chopstik.mid', trackNumbers = [1,2,3,4,5], baseNote = 36, noteRange = 36, noteLim = 100)
    cutObj.drawHoles(cutArr)

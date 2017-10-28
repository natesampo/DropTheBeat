import svgwrite
from svgwrite import mm, cm
import numpy as np
import testMidi



strokeColor = "red"
svgname = 'test.svg'
mm = 3.543
cm = 35.43
inch = 90
sw = 0.001
sysMult = inch

print(sysMult)
class svgCut:
    def __init__(self,numHoles,holeRadius,holeSpace,borderSpace):
        self.numHoles = numHoles
        self.holeRadius = holeRadius * sysMult
        self.holeSpacex = holeSpace[0] * sysMult
        self.holeSpacey = holeSpace[1] * sysMult
        self.borderSpace = borderSpace * sysMult
        self.pagex = self.borderSpace * 2 + (self.numHoles - 1) * self.holeSpacex + self.holeRadius * 2

    def drawRectangle():
        #TODO
        pass

    def drawHole(self, dwg, point):
        dwg.add(dwg.circle(center=(self.borderSpace + self.holeSpacex * point[0] + self.holeRadius, self.holeSpacey * point[1] + self.holeRadius),
                            r=self.holeRadius,fill_opacity = 0.0,stroke=strokeColor,stroke_width=sw))

    def drawHoles(self,holeArray):
        if(len(holeArray[0]) != self.numHoles):
            return 0
        self.pagey = (len(holeArray) + 1) * self.holeSpacey
        xString = str(int(self.pagex)) + 'px'
        yString = str(int(self.pagey)) + 'px'
        print(xString)
        dwg = svgwrite.Drawing(svgname, size = (xString, yString))
        for i,line in enumerate(holeArray):
            [self.drawHole(dwg,(j,i)) for j,v in enumerate(line) if v]
        dwg.save()




if __name__ == "__main__":
    cutObj = svgCut(numHoles = 9,holeRadius = .125,holeSpace = [.25,.25], borderSpace= 1)
    times, cutArr = testMidi.readMidi('bach_bourree.mid', trackNumber = 1, baseNote = 71, noteRange = 9)
    cutObj.drawHoles(cutArr)

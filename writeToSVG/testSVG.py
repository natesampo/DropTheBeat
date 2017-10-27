import svgwrite
from svgwrite import mm, cm
import numpy as np


sw = 5
svgname = 'test.svg'
class svgCut:
    def __init__(self,numHoles,holeSize,holeSpace,borderSpace):
        self.numHoles = numHoles
        self.holeSize = holeSize
        self.holeSpace = holeSpace
        self.borderSpace = borderSpace
        self.pagex = self.borderSpace * 2 + (self.numHoles + 1) * self.holeSpace

    def drawBorders():
        #TODO
        pass

    def drawHole(self, dwg, point):
        dwg.add(dwg.circle(center=(self.borderSpace + self.holeSpace * point[0], self.holeSpace * point[1]),
                            r=self.holeSize,fill_opacity = 0.0,stroke="black",stroke_width=sw))

    def drawHoles(self,holeArray):
        if(len(holeArray[0]) != self.numHoles):
            return 0
        self.pagey = (self.numHoles + 1) * self.holeSpace
        xString = str(int(self.pagex)) + 'px'
        yString = str(int(self.pagey)) + 'px'
        print(xString)
        dwg = svgwrite.Drawing(svgname, size = (xString, yString))
        for i,line in enumerate(holeArray):
            [self.drawHole(dwg,(j+1,i+1)) for j,v in enumerate(line) if v]
        dwg.save()




if __name__ == "__main__":
    cutObj = svgCut(numHoles = 5,holeSize = 30,holeSpace = 60, borderSpace= 50)
    k = np.array([
                [0,0,0,0,0],
                [0,1,1,0,0],
                [1,1,0,0,1],
                [0,0,1,0,0],
                [0,0,1,0,0]
                ],dtype = "uint8")
    cutObj.drawHoles(k)

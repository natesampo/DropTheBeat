import svgwrite
from svgwrite import mm, cm
dwg = svgwrite.Drawing('test.svg', size = ("800px", "600px"))
dwg.add(dwg.line((0, 0), (100, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))

dwg.add(dwg.circle(center=(100, 100), r=100,fill_opacity = 0.0,stroke="black",stroke_width=5))
dwg.add(dwg.text('Test', insert=(0, 20), fill='red'))
print(dwg.circle(center=(100, 100), r=100).attribs)
dwg.save()


sw = 5
class svgCut:
    def __init__(self,numHoles,holeSize,holeSpace,borderSpace):
        self.numHoles = numHoles
        self.holeSize = holeSize
        self.holeSpace = holeSpace
        self.borderSpace = borderSpace
        self.pagex = self.borderSpace * 2 + (self.numHoles + 1) * self.holeSpace

    def drawBorders():
        //TODO
        pass

    def drawHoles(self,holeArray):
        if(len(holeArray[0]) != self.numHoles):
            return 0
        self.pagey = (self.numHoles + 1) * self.holeSpace
        pass

    def drawHole(self, dwg, point):
        dwg.add(dwg.circle(center=(self.borderSpace + cm * self.holeSpace * point[0], cm * self.holeSpace * point[1]),
                            r=self.holeSize,fill_opacity = 0.0,stroke="black",stroke_width=sw))

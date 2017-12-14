#Author: Nick Steelman
#Last Revised Date: 12/14/17
#Contact: steelman@students.olin.edu

import svgwrite
from svgwrite import mm, cm
import numpy as np
import convertMidi


def convertIn(unit):
    return str(unit)#this is unnecessary code that could be implemented to convert units
class svgCut:
    '''This is the object that controls most of the operations of writing to the
    svg'''
    maxTime=None
    minTime=None
    def __init__(self,numHoles,holeRadius,holeSpace,borderSpace):
        self.numHoles = numHoles
        self.holeRadius = holeRadius
        self.holeSpacex = holeSpace[0] #x distance between holes.. should be at least radius * 2
        self.holeSpacey = holeSpace[1]
        self.borderSpacex = borderSpace[0]#extra space at beginning of the song
        self.borderSpacey =  borderSpace[1]#extra space at the end of the song
        self.borderSpaceEnd = borderSpace[2]#extra space on the sides where no holes will be drawn
        if honeyComb:#determine the sheet width based on number of holes, spacebetween holes,
        #and whether we are using a honeycomb pattern in hole drawing
            self.pagex = self.borderSpacex * 2 + (self.numHoles-0.5) * self.holeSpacex + 2*holeRadius
        else:
            self.pagex = self.borderSpacex * 2 + (self.numHoles - 1) * self.holeSpacex + self.holeRadius * 2 #from what we are already given we can calculate width of page

    def drawRectangle(self,dwg,origin = (0,0), end = None):
        '''This will draw a rectangle around the border so it can be properly cut'''
        if end is None:
            end = (self.pagex,self.pagey)

        #define a list of lines that need to be draw
        lines = [[origin, (origin[0],end[1])], [origin, (end[0],origin[1])],[end, (origin[0],end[1])], [end,  (end[0],origin[1])]]
        for line in lines:#draw each line in the list
            dwg.add(dwg.line(start = (convertIn(line[0][0]),convertIn(line[0][1])),end = (convertIn(line[1][0]),convertIn(line[1][1])),stroke=strokeColor,stroke_width=sw))
        pass
    def setSpeeds(self,slow, fast):
        '''If you want to encode time into the sheet, input the min and max
        speed the sheet can go (not used in final project)'''
        #in inches per second
        if honeyComb:
            vSpace = self.holeSpacey / 2
        else:
            vSpace = self.holeSpacey

        self.maxTime = convertToBeats(vSpace / slow)
        self.minTime = convertToBeats(vSpace / fast)


    def getProportion(self, time):
        '''math to calculate how to encode time into sheet (also not used)'''
        return (time - self.minTime)  / (self.maxTime - self.minTime)


    def encodeTimes(self,timeArr):
        '''deprecated code calculating the size of squares to make to encode time into
        the sheet'''
        lengthArr = []
        if honeyComb:
            vSpace = self.holeSpacey / 2
        else:
            vSpace = self.holeSpacey

        for i in timeArr:#
            if i > self.maxTime:
                print("TOO LONG")
                i = self.maxTime
            elif i < self.minTime:
                print("TOO SHORT")
                i = self.minTime
            lengthArr.append(self.getProportion(i) * vSpace)

        return lengthArr

    def drawTimes(self,lengthArr,dwg,width = 1,topLeft = (0,0)):
        '''deprecated code that would draw the rectangles found by encode times'''
        if honeyComb:
            vSpace = self.holeSpacey / 2
        else:
            vSpace = self.holeSpacey

        for j,v in enumerate(lengthArr):
            if v and v < vSpace:
                insert = (topLeft[0],topLeft[1] + j * vSpace - v)
                size = (width, v)
                dwg.add(dwg.rect(insert=insert,size = size,fill_opacity = 0.0,stroke=strokeColor,stroke_width=sw))



    def drawHole(self, dwg, point):
        '''quick code to add a hold to the previous specifications'''

        if honeyComb:
            if point[1] % 2:
                centerx = self.borderSpacex + self.holeSpacex * (point[0]+.5) + self.holeRadius
                centery = self.holeSpacey * (point[1]//2+.5) + self.holeRadius + self.borderSpacey

            else:
                centerx = self.borderSpacex + self.holeSpacex * (point[0]) + self.holeRadius
                centery = self.holeSpacey * (point[1]//2) + self.holeRadius + self.borderSpacey
        else:
            centerx = self.borderSpacex + self.holeSpacex * point[0] + self.holeRadius
            centery = self.holeSpacey * point[1] + self.holeRadius + self.borderSpacey
        dwg.add(dwg.circle(center=(convertIn(centerx),convertIn(centery)),
                        r=convertIn(self.holeRadius),fill_opacity = 0.0,stroke=strokeColor,stroke_width=sw))

    def drawHoles(self,holeArray, timeArr = None):
        '''draw all holes given an array of positions'''
        if(len(holeArray[0]) != self.numHoles):#check to make sure size of  array is correct
            print('DIMENSION MISMATCH')
            return 0
        if honeyComb:#calculate length of the sheet using number of final notes and sizing of sheet
            self.pagey = (len(holeArray)//2 + 1) * self.holeSpacey +  self.borderSpacey + self.borderSpaceEnd
        else:
            self.pagey = (len(holeArray) + 1) * self.holeSpacey  +  self.borderSpacey + self.borderSpaceEnd#calculate pag length
        xString = str(self.pagex) + 'in' #string stuff
        yString = str(self.pagey) + 'in'
        print('Width in inches: ',str(self.pagex))#check length
        print('Height in inches: ',str(self.pagey))
        dwg = svgwrite.Drawing(svgname, size = (xString, yString))#make a new drawing
        dwg.viewbox(0,0,width = self.pagex, height = self.pagey)#set a viewbox in the drawing,
        #this allows our our number to automatically be converted to inches
        for i,line in enumerate(holeArray): #cut holes in array where element  != 0
            [self.drawHole(dwg,(j,i)) for j,v in enumerate(line) if v]
        self.drawRectangle(dwg)
        if timeArr is not None:#incode times into the sheet if so desired
            lengthArr = cutObj.encodeTimes(timeArr)
            cutObj.drawTimes(lengthArr,dwg,width = self.borderSpacex,topLeft = (self.pagex - self.borderSpacex,self.borderSpacey + self.holeRadius))
        return dwg

    def addHoles(self, timeArr, cutArr, minTime = 0):
        '''This will take an array representing all the notes and what times they
        were played and turn it into a larger array with whitespace to include the
        notes of longer duration'''
        unit = min(timeArr)
        # timeArr[0] = 0
        if unit >= minTime:
            minTime = unit
        if self.minTime and minTime < self.minTime:
            raise NameError('NOT FAST ENOUGH')#check to make sure quickest not is not too quick
        plus = 1
        empty = [0] * len(cutArr[0])
        for i,v in enumerate(timeArr):#go through the cut array and inser zeros where appropriate
            extra = round(v/minTime)-1
            # print(extra)
            for j in range(extra):
                print('Done')
                cutArr = np.insert(cutArr,i+ plus, empty, axis = 0)
                plus += 1
        # print(cutArr)
        return cutArr

def convertToBeats(s):
    '''function that would potentially convert times to beats but was not used'''
    return s


strokeColor = "red" #
svgname = 'MountainKing.svg'#file to load
sw = str(0.1)#width of drawn lines
sysMult = 1 # chosen multiplier for all inputs, not needed
honeyComb = 0

if __name__ == "__main__":
    svgname = 'test2.svg'
    #define a dictionary mapping notes to where they should go on the songsheet
    dictN = {64:0, 65:2, 66:4,67:6,68:8,69:10,70:12,71:1,72:3,73:5,74:7,75:9,76:11}
    #define a svg cutter object with appropriate dimensions, gotten from the CAD
    cutObj = svgCut(numHoles = 5,holeRadius = .265/2,holeSpace = [.265,.265], borderSpace= [.5,.5,.5])
    #print the tracks from a desired MIDI file to see which ones to select
    convertMidi.printTracks('MountainKing.mid')
    #read the midi file and convert it into a cut array representing the order in
    #which all notes are played and a time array representing how long each not lasts.
    times, cutArr = convertMidi.readMidi('MountainKing.mid', trackNumbers = list(range(0,2)), baseNote = 64, noteRange = 13, noteLim = 105,offset = 0,dictN = dictN)
    #add white space for longer notes
    cutArr = cutObj.addHoles(times, cutArr)
    #add holes to the sheet
    dwg = cutObj.drawHoles(cutArr)
    #save the svg
    dwg.save()

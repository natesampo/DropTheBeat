import mido
import numpy as np

def printTracks(fileName):
    #print all the instuments in the midi file
    mid = mido.MidiFile(fileName)
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))


def readMidi(fileName, trackNumbers = [1], baseNote = 0, noteRange = 5, noteLim = 30,offset = 0, dictN =None,space= False):
    '''This will read a midi file and return an array of notes in the given range (x size )
    and up to the given length  (y size). The trackNumbers dictates which tracks to accept notes from
    it will also return an array of times dictating how long to wait before droping the current set.'''
    mid = mido.MidiFile(fileName) #get midi object
    emptyNotes = np.zeros(noteRange) #empty range
    currentNotes = emptyNotes.copy()
    timeTracker = []
    notesList = []
    elapsedTime = 0
    for msg in mid: # run through all messages
        print(msg)
        if msg.time != 0: # if there is a time associated with the message add it to time tracker
            elapsedTime += msg.time
            if max(currentNotes) and offset:
                offset -= 1
                currentNotes = emptyNotes.copy()
            elif max(currentNotes): #if there is a note played, index current states and move on to next row
                timeTracker.append(elapsedTime)
                notesList.append(currentNotes)
                currentNotes = emptyNotes.copy()
                elapsedTime = 0

        if (not msg.is_meta) and  msg.channel in trackNumbers and msg.type == 'note_on':

            #if its a valid message and track in the key range, write 1 in the corresponding index.
            if dictN and msg.note in dictN.keys():
                currentNotes[dictN[msg.note]] = 1
            elif not dictN and baseNote <= msg.note < baseNote + noteRange:
                currentNotes[msg.note - baseNote] = 1

        if len(timeTracker) > noteLim:#if we get too long, break
            break
    return timeTracker, np.array(notesList)

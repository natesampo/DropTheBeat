import mido
import numpy as np

def printTracks(fileName):
    mid = mido.MidiFile(fileName)
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))


def readMidi(fileName, trackNumber = 1, baseNote = 0, noteRange = 5):
    mid = mido.MidiFile(fileName)
    emptyNotes = np.zeros(noteRange)
    currentNotes = emptyNotes.copy()
    timeTracker = []
    notesList = []
    elapsedTime = 0
    for msg in mid.tracks[1]:
        if msg.time != 0:
            elapsedTime += msg.time
            if max(currentNotes):
                timeTracker.append(elapsedTime)
                notesList.append(currentNotes)
                currentNotes = emptyNotes.copy()
                elapsedTime = 0
        if msg.type == 'note_on' and baseNote <= msg.note < baseNote + noteRange:
            currentNotes[msg.note - baseNote] = 1
    return timeTracker, np.array(notesList)

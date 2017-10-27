import mido
import numpy as np
mid = mido.MidiFile('bach_bourree.mid')
#messages go from c to b
baseNote = 70
noterange = 5
for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    # for msg in track:
    #     print(msg)
emptyNotes = np.zeros(noterange)
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

    if msg.type == 'note_on' and baseNote <= msg.note < baseNote + noterange:
        currentNotes[msg.note - baseNote] = 1
    print(msg)

print(notesList)

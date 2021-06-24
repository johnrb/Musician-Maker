
# Whitekeys and whitemidi are lists of the names and midi note numbers for all the white notes
whitekeys = ('C2','D2','E2','F2','G2','A2','B2','C3','D3','E3','F3','G3','A3','B3',\
             'C4','D4','E4','F4','G4','A4','B4','C5','D5','E5','F5','G5','A5','B5',\
             'C6','D6','E6','F6','G6','A7','B6','C7')
whitemidi = (36,38,40,41,43,45,47,48,50,52,53,55,57,59,\
             60,62,64,65,67,69,71,72,74,76,77,79,81,83,\
             84,86,88,89,91,93,95,96)


# rangekeys and rangemidi are lists of text descriptions and midi numbers for useful instrument ranges
rangekeys = ('1 Octave', '1 Oct + 3rd','1 Oct + 5th', \
             '2 Octaves','2 Oct + 3rd','2 Oct + 5th', \
             '3 Octaves','3 Oct + 3rd','3 Oct + 5th', \
             '4 Octaves')
rangemidi = (12,16,19, 24,28,31, 36,40,43, 48)

def rangeToMidi(rangetext):
    i = rangekeys.index(rangetext)
    return rangemidi[i]
    
# midinames is a list of all the general midi instruments and their numbers
midiname = ('0 Acoustic Grand Piano','1 Bright Acoustic Piano','2 Electric Grand Piano','3 Honky-tonk Piano','4 Electric Piano 1','5 Electric Piano 2','6 Harpsicord','7 Clavi','8 Celesta','9 Glockenspiel',\
            '10 Music Box','11 Vibraphone','12 Marimba','13 Xylophone','14 Tubular Bells','15 Dulcimer','16 Drawbar Organ','17 Percussive Organ','18 Rock Organ','19 Church Organ',\
            '20 Reed Organ','21 Accordion','22 Harmonica','23 Tango Accordion','24 Acoustic Guitar (nylon)','25 Acoustic Guitar (steel)','26 Electric Guitar (jazz)','27 Electric Guitar (clean)','28 Electric Guitar (muted)','29 Overdriven Guitar',\
            '30 Distortion Guitar','31 Guitar Harmonics','32 Acoustic Bass','33 Electric Bass (finger)','34 Electric Bass (pick)','35 Fretless Bass','36 Slap Bass 1','37 Slap Bass 2','38 Synth Bass 1','39 Synth Bass 2',\
            '40 Violin','41 Viola','42 Cello','43 Contrabass','44 Tremolo Strings','45 Pizzicato Strings','46 Orchestral Harp','47 Timpani','48 String Ensemble 1','49 String Ensemble 2',\
            '50 Synth Strings 1','51 Synth Strings 2','52 Choir Aahs','53 Voice Oohs','54 Synth Voice','55 Orchestra Hit','56 Trumpet','57 Trombone','58 Tuba','59 Muted Trumpet',\
            '60 French Horn','61 Brass Section','62 Synth Brass 1','63 Synth Brass 2','64 Soprano Sax','65 Alto Sax','66 Tenor Sax','67 Baritone Sax','68 Oboe','69 English Horn',\
            '70 Bassoon','71 Clarinet','72 Piccolo','73 Flute','74 Recorder','75 Pan Flute','76 Blown Bottle','77 Shakuhachi','78 Whistle','79 Ocarina',\
            '80 Lead 1 (square)','81 Lead 2 (sawtooth)','82 Lead 3 (calliope)','83 Lead 4 (chiff)','84 Lead 5 (charang)','85 Lead 6 (voice)','86 Lead 7 (fifths)','87 Lead 8 (bass+lead)','88 Pad 1 (new age)','89 Pad 2 (warm)',\
            '90 Pad 3 (polysynth)','91 Pad 4 (choir)','92 Pad 5 (bowed)','93 Pad 6 (metallic)','94 Pad 7 (halo)','95 Pad 8 (sweep)','96 FX 1 (rain)','97 FX 2 (soundtrack)','98 FX 3 (crystal)','99 FX 4 (atmosphere)',\
            '100 FX 5 (brightness)','101 FX 6 (goblins)','102 FX 7 (echoes)','103 FX 8 (sci-fi)','104 Sitar','105 Banjo','106 Shamisen','107 Koto','108 Kalimba','109 Bagpipe',\
            '110 Fiddle','111 Shanai','112 Tinkle Bell','113 Agogo','114 Steel Drums','115 Woodblock','116 Taiko Drum','117 Melodic Tom','118 Synth Drum','119 Reverse Cymbal',\
            '120 Guitar Fret Noise','121 Breath Noise','122 Seashore','123 Bird Tweet','124 Telephone Ring','125 Helicopter','126 Applause','127 Gunshot')

mididrum = ('27 High Q', '28 Slap', '29 Scratch', '30 Scratch', '31 Sticks', '32 Square', '33 Metronome', '34 Metronome', '35 Bass Drum 2', '36 Bass Drum 1', '37 Side Stick/Rimshot', '38 Snare Drum 1', '39 Hand Clap',\
            '40 Snare Drum 2', '41 Low Tom 2', '42 Closed Hi-hat', '43 Low Tom 1', '44 Pedal Hi-hat', '45 Mid Tom 2', '46 Open Hi-hat', '47 Mid Tom 1', '48 High Tom 2', '49 Crash Cymbal 1',\
            '50 High Tom 1', '51 Ride Cymbal 1', '52 Chinese Cymbal', '53 Ride Bell', '54 Tambourine', '55 Splash Cymbal', '56 Cowbell', '57 Crash Cymbal 2', '58 Vibra Slap', '59 Ride Cymbal 2',\
            '60 High Bongo', '61 Low Bongo', '62 Mute High Conga', '63 Open High Conga', '64 Low Conga', '65 High Timbale', '66 Low Timbale', '67 High Agogo', '68 Low Agogo', '69 Cabasa',\
            '70 Maracas', '71 Short Whistle', '72 Long Whistle', '73 Short Guiro', '74 Long Guiro', '75 Claves', '76 High Wood Block', '77 Low Wood Block', '78 Mute Cuica', '79 Open Cuica',\
            '80 Mute Triangle', '81 Open Triangle', '82 Shaker', '83 Jingle Bell', '84 Belltree', '85 Castanets', '86 Mute Surdo', '87 Open Surdo')


# romanToChord : Converts a roman numeral from song file to array of note numbers
def romanToChord(chord, tonality):
#Returns the list of note numbers, the type (major or minor), and the inversion of the chord.
# chord can be 'IV', 'iiidim', 'V7/V', 'I64', 'V6'
# tonality is "major", "harmonic", or "natural" (minors). This is the tonality of the key (not the chord)
# major and minor chords are controlled by case. iv is minor IV is major
# returns notelist, type, inversion

#    if chord is "I" then notelist is [0,4,7]      type is "triad"   inversion is 0
#    if chord is "I6" then notelist is [0,4,7]     type is "triad"   inversion is 1
#    if chord is "I64" then notelist is [0,4,7]    type is "triad"   inversion is 2
#    if chord is "ii" then notelist is [2,5,9]     type is "triad"   inversion is 0
#    if chord is "V7" then notelist is [4,8,11,14] type is "seven"   inversion is 0

    #Set variables that need to be initalized
    global noteset
    seven = inversion = dim = aug = major = 0
    letters = ''
    
    # chord variable is a string ex: I , or iv or whatever
    if chord[-1] == ('7' or '5' or '3' or '2'): seven = 1
    
    noteset = scaleNotes(tonality)
    
    #TRIADS
    #Set diminished and augmented variables, as well as the inversion of the chord
    #Once that information has been set, take it out of "chord"
    if not seven:
        if chord.find('dim') != -1: dim = 1
        chord = chord.replace('dim', '')
        if chord.find('+') != -1: aug = 1
        chord = chord.replace('+', '')
        if chord[-1] == '6':
            inversion = 1
            chord = chord.replace("6", "")
        elif chord[-1] == '4':
            inversion = 2
            chord = chord.replace("64", "")
    
    #SEVENTH CHORDS
    #Set diminished and augmented variables, as well as the inversion of the chord
    #Once that information has been set, take it out of "chord"
    elif seven:
        if chord.find('7') != -1:
            seven = 2
            chord = chord.replace('7', '')
        elif chord.find('65') != -1:
            seven = 2
            inversion = 1
            chord = chord.replace('65', '')
        elif chord.find('43') != -1:
            seven = 2
            inversion = 2
            chord = chord.replace('43', '')
        elif chord.find('2') != -1:
            seven = 2
            inversion = 3
            chord = chord.replace('4', '')
            chord = chord.replace('2', '')
        if chord.find('dim') != -1:
            if chord.find('h') != -1:
                dim = 1
                chord = chord.replace('h', '')
            else: dim = 2
            chord = chord.replace('f', '')
            chord = chord.replace('dim', '')
        if chord.find('m') != -1:
            seven = 2
            chord = chord.replace('m', '')
        elif chord.find('M') != -1:
            seven = 3
            chord = chord.replace('M', '')
    
    #The variable "chord" should now be a roman numeral - i, ii, ..., vii
    
    #If the letters are uppercase, the chord is major. Otherwise, it's minor
    #Set "chord" to lowercase after that information has been obtained
    if chord.isupper(): major = 1
    chord = chord.lower()
    
    #Set the index based on what roman numeral "chord" is
    if   chord == "i":   index = 0
    elif chord == "ii":  index = 1
    elif chord == "iii": index = 2
    elif chord == "iv":  index = 3
    elif chord == "v":   index = 4
    elif chord == "vi":  index = 5
    elif chord == "vii": index = 6
    
    #Set the root of the chord based on the index
    root = noteset[index]
    
    #Determine what notes to pass back based on the variables set earlier (diminished, augmented, major_boolean, and inversion)
    #Then return the appropriate variables
    #The chordScale statements determine the notes the instruments can play, not the accompaniment chords
    #print "chord2:", chord
    if not seven:
        type = 'triad'
        if dim:
            notelist = [root, root + 3, root + 6]
        elif aug:
            notelist = notelist = [root, root + 4, root + 8]
        elif major:
            notelist = [root, root + 4, root + 7]
        else:
            notelist = [root, root + 3, root + 7]
    elif seven:
        type = 'seven'
        if dim:
            if dim == 1:
                notelist = [root, root + 3, root + 6, root + 10]
            elif dim == 2: notelist = [root, root + 3, root + 6, root + 9]
        else:
            if major:
                notelist = [root, root + 4, root + 7]
            else:
                notelist = [root, root + 3, root + 7]
            if seven == 2:
                notelist.append(root + 10)
            elif seven == 3:
                notelist.append(root + 11)
    return notelist, type, inversion

# NameToNumber Class: Takes in a name like D#3 and returns a Midi note number
#class nameToNumber():
#This class was originally a function, but needed to be used in other classes, so it was updated to become a self-contained class
#At this point is called in the MakeWindow class, MakeMusic class, and the Demonstrate class.
#Inside the class where it is called, a new object has to be created before the getSig or getNote methods can be called.
#The convention is to create a new nameToNumber object called Converter ( Converter = nameToNumber() )
#One can then access the getSig or getNote methods by calling Converter.getSig(key_letter) or Converter.getNote(note_name), respectvely.
    
#Define global variables
#global scale
scale = ['C', '', 'D', '', 'E', 'F', '', 'G', '', 'A', '', 'B']   # Array of the chromatic scale for note numbers



# scaleNotes : Set the list of relative note numbers in the scale, based on what the tonality is
def scaleNotes(tonality):
    if   tonality == "major":    noteset = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17]
    elif tonality == "natural":  noteset = [0, 2, 3, 5, 7, 8, 10, 12, 14, 15, 17]
    elif tonality == "harmonic": noteset = [0, 2, 3, 5, 7, 8, 11, 12, 14, 15, 17]
    return noteset

# getSig : Takes a letter passed in (C, D#, Ab) and returns the midi offset number (from C) with that key. 
def getSig(key_letter):
#  For example, D would return 2, while Ab would return 8

    letter = key_letter[0]                                                  # Get note letter
    playnote = scale.index(key_letter[0])                                   # Find the number of the note in the chromatic scale
    acc = key_letter.strip('ABCDEFG0123456789')                             # Get rid of everything but an accidental
    if acc == '#': playnote += 1                                            # Move up one spot in the chromatic array for a sharp
    if acc == 'b': playnote -= 1                                            # Move down one spot in the chromatic array for a flat
    return playnote                                                         # Return just playnote


# getNote : #Takes a note "C3", "D5", or "Ab4" and returns the midi number of that note.
def getNote(note_name):
#For example, C4 would return 60, while D5 would return 74


    letter = note_name[0]                                                   # Get note letter
    playnote = scale.index(note_name[0])                                    # Find the number of the note in the chromatic scale
    acc = note_name.strip('ABCDEFG0123456789')                              # Get rid of everything but an accidental
    if acc == '#': playnote += 1                                            # Move up one spot in the chromatic array for a sharp
    if acc == 'b': playnote -= 1                                            # Move down one spot in the chromatic array for a flat
    octave = int(note_name[-1])                                             # Get note octave
    return playnote + (12 * (octave + 1))                                   # Do the final math to find note number

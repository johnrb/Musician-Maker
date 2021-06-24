# Musician Maker  
# Original version written by Ben Toews, Zach Yordy in 2010
# Additions by John Miller in 2011
# Rewritten by John Buschert Feb 2012
# Updated to Python 3 Dec 2020
#
# Needs pygame and wxpython
# Needs serial which comes from pyserial
# Looks for USB connection to Roland SD-50 sound module, if not found it uses default sound card
# Looksfor USB connection to Eobody A/D (Midi) unit, if not found it creates a virtual instrument 
# If any BT instruments are selected, it looks for a serial connection to a bluetooth device
# Looks for default.mcf in same directory as program to get starting settings, if none it starts with defaults

import pickle, re, queue, threading # these are standard modules in python
import wx, pygame.midi, pygame.time  # wx and pygame must be downloaded
import serial    # serial is from pyserial (for serial connection to bluetooth)
import mmref     # mmref is our own module of functions and lists to convert notes, names, noteRanges
verbose = False

# ==========================   Functions   ========================================

def fileOpen(event):   # File|Open menu item.  File browser for config files
    opendlg = wx.FileDialog(None, "Open a config file", style = wx.OPEN)
    opendlg.SetWildcard("Config files (.mcf) |*.mcf")
    if opendlg.ShowModal() == wx.ID_OK:
        readConfig(opendlg.GetPath())
    
def readConfig(file):   # Read config file. Called by fileOpen and at startup 
    try:
        cfgfile = open(file, 'rb')
    except:
        print ("can't open cfg file:", file)
        return
    config = pickle.load(cfgfile)
    for pname,pref in Part.partlist:
        for attname,attref in pref.attlist:
            if pname+" "+attname in config:
                attref.SetValue(config[pname+" "+attname])
            attref.Refresh()
        pref.partrefresh(1)
    cfgfile.close()
        
def fileSave(event):   # File|Save menu item.  Save most instrument panel settings as a .mcf file
    savedlg = wx.FileDialog(None, "Save configuration", style = wx.SAVE)  
    savedlg.SetWildcard("*.mcf")                                          # saves in .mcf file extension
    if savedlg.ShowModal() == wx.ID_OK:
        cfgfile = open(savedlg.GetPath(), 'wb')
        saveConfig(cfgfile)
    
def saveConfig(cfgfile):  # Save Configuration.  Called by fileSave and fileSaveDefault
    config = {}
    for pname,pref in Part.partlist:
        for attname,attref in pref.attlist:
            config[pname+" "+attname]=attref.GetValue() 
    pickle.dump(config, cfgfile)
    cfgfile.close()   

def fileSaveDefault(event):   # Save as Default so program starts up with these settings
    cfgfile = open("default.mcf",'wb')  # this puts the default file in whatever is current directory. Should be one place.
    print ("saving:", cfgfile)
    saveConfig(cfgfile)
 
def fileQuit(event):    # File|Quit menu item.  Intended to Quit the program gracefully.  Does not succeed.
    global threadsAlive, active, playing
    active = playing = threadsAlive = False
    print ("quitting program ..............")
    #pygame.time.wait(500)
    #win.Destroy()
    if byteReader.is_alive():
        byteReader.join()
        print ("joined br")
    if accomp.is_alive():
        accomp.join()
        print ("joined acc")
    if sway1.is_alive():
        sway1.join()
        print ("joined swa")
    if obloe1.is_alive():
        obloe1.join()
        print ("joined obl")
    if baron1.is_alive():
        baron1.join()
        print ("joined bar")
    if pluck1.is_alive():
        pluck1.join()
        print ("joined plu")
    if marim1.is_alive():
        marim1.join()
        print ("joined mar")
    if blue1.is_alive():
        blue1.join()
   
    print ("joined all")
    
    print (" myapp is", myapp.IsActive())
    myapp.Destroy()   # not working correctly.  Has no effect!
       #Doesn't actually halt until I click on another button.
       #Then says it was terminated in an unusaul way.
       #Also don't know how to catch a click on the close button
       #would be nice to save default values in default.mcf
       #maybe at end of program after Loop??
    print ("destroyed")
    pass
    raise SystemExit() 
    
def play(event):  # Start instruments and begins the accompaniment song
    global active, playing, verbose
    toppan.SetBackgroundColour(COL_PLAY)
    toppan.Refresh()
    playbutton.SetValue(1)
    practicebutton.SetValue(0)
    stopbutton.SetValue(0)
    # initialize instruments and then start them   
    byteReader.newEobChanArray()
    readControls(1)
    active = True
    # start the song
    playing = True
    if verbose: print ("Play is executed")
    
def practice(event):  # Start instruments without accompaniment song
    global active, verbose
    # Update the display pane and control buttons
    toppan.SetBackgroundColour(COL_PRACTICE)
    toppan.Refresh()
    practicebutton.SetValue(1)
    playbutton.SetValue(0)
    stopbutton.SetValue(0)
    # initialize instruments and then start them   
    byteReader.newEobChanArray()
    readControls(1)
    active = True
    if verbose: print ("Practice is executed")

def stop(event):   # Stop instruments and song
    # Update the display pane and control buttons
    global active, playing, verbose
    toppan.SetBackgroundColour(COL_STOP)
    toppan.Refresh()
    playbutton.SetValue(0)
    practicebutton.SetValue(0)
    stopbutton.SetValue(1)
    playing = False   # stop the song
    active = False    # Stop the instruments
    pygame.time.wait(450)   # Wait to let notes stop gently
    for ichan in range(0,16):
        statusbyte = 0xB0 + ichan
        midout.write([[[statusbyte, 123, 0],pygame.midi.time()]]) # Turn all notes off
    if verbose: print ("Stopped")
    
def chordC(event):  # Set instruments to C chord
    setChordButtonsOff()
    Constraint.setChord(0,[0,4,7])
    chordCbutton.SetValue(1)

def chordDm(event):  # Set instruments to Dm chord
    setChordButtonsOff()
    Constraint.setChord(2,[0,3,7])
    chordDmbutton.SetValue(1)

def chordG(event):  # Set instruments to G chord
    setChordButtonsOff()
    Constraint.setChord(7,[0,4,7])
    chordGbutton.SetValue(1)

def chordScale(event):  # Set instruments to scale mode
    setChordButtonsOff()
    chordScalebutton.SetValue(1)
    Constraint.setAllModes("scale")

def setChordButtonsOff():  # Reset the chord buttons
    chordCbutton.SetValue(0)
    chordDmbutton.SetValue(0)
    chordGbutton.SetValue(0)
    chordScalebutton.SetValue(0)
    Constraint.setAllModes("chord")

def songBrowser(win):    # Open browser for accompaniment songfiles
    global songpicked,songfilename,verbose
    dlg = wx.FileDialog(None, "Open a song file", style = wx.FD_OPEN)
    dlg.SetWildcard("Song files (.sng) |*.sng")
    if dlg.ShowModal() == wx.ID_OK:
        songfilename = dlg.GetPath()
        songFileCtrl.SetValue(songfilename[songfilename.rfind('\\') + 1:-4])
        songpicked = True
    if verbose: print (songfilename)    

def readControls(event):  # Read the GUI controls of each instrument and put those values into the internal variables
    
    
    def setPan(instrument):
        Bn = 0xB0 + instrument.midich.GetValue()
        left = instrument.outchanL.GetValue()
        right = instrument.outchanR.GetValue()
        balance = 64
        if left and not right: balance = 0
        if right and not left: balance = 127
        midout.write([[[Bn,0x0A,balance],pygame.midi.time()]])
        
    for name,instrument in Instrument.iArray: 
        instrument.lowend = mmref.getNote( instrument.lowendbox.GetValue() ) 
        instrument.noteRange = mmref.rangeToMidi( instrument.noteRangebox.GetValue() )
        midi_instrument = int(re.split(" ",instrument.midinst.GetValue())[0])
        midout.set_instrument(midi_instrument, instrument.midich.GetValue())
        setPan(instrument)
        #print name, instrument.midinst.GetValue(), instrument.midich.GetValue()
    
    # could do pan for the accompaniment here but it's on two channels and does not use midich
    
   #print Instrument.iArray
    
    Constraint.updateAllChordNotes()
    
    
# =========================  Classes  ================================

# Part class --  Creates a control pane for accompaniment or instrument
class Part:
    partid = 0  # counts Parts
    partlist = []   # list of all instances of Part
    
    def __init__(self,name):
        vheight = ()
        Part.partid += 1  # counts instances of Part
        Part.partlist.append([name,self])
        self.attlist = []  # list of attributes to save
        
        # Create panel for part controls
        if self.__class__.partid == 1:
            vpos = 80 + 5
            height = 110
        else:
            height=55
            vpos= 80 + 5 + 110 + 5 + (Part.partid-2)*(height+5)
        self.partpan = wx.Panel(pan,-1,(5,vpos),(774,height))
        self.partpan.SetBackgroundColour(COL_DISABLED)  #disabled by default
            
        # Create checkbox to select this part 
        self.partcb = wx.CheckBox(self.partpan, -1, name, (10,5))
        self.partrefresh(1)
        self.partcb.Bind(wx.EVT_CHECKBOX, self.partrefresh)
        self.attlist.append(["partcb",self.partcb])
        
        # Create output channel buttons 
        wx.StaticText(self.partpan, -1, "Output Channel", pos=(545,5))
        self.outchanL = wx.ToggleButton(self.partpan, -1, 'L', pos=(545,25), size=(30,20))
        self.outchanL.SetValue(1)
        self.outchanL.Bind(wx.EVT_TOGGLEBUTTON,readControls)             #####################################
        self.attlist.append(["outchanL",self.outchanL])
        self.outchanR = wx.ToggleButton(self.partpan, -1, 'R', pos=(585,25), size=(30,20))
        self.outchanR.Bind(wx.EVT_TOGGLEBUTTON,readControls)             #####################################
        self.attlist.append(["outchanR",self.outchanR])
            
        # Create volume slider
        self.outvol = wx.Slider(self.partpan, -1, 50, 0, 100, pos=(630,5), size=(120,-1), style=wx.SL_LABELS)
        self.attlist.append(["outvol",self.outvol])
        
        # Create trace text
        self.trace = wx.StaticText(self.partpan, -1, "", pos=(10,40))
        
         # if Part.tracing: self.trace.SetLabel("")
        
        
    def turnon(self):  # Turn on part (to set it on by default at startup)  ## maybe unnec ##
        self.partcb.SetValue(1)
        self.partrefresh(1)
        
    def partrefresh(self,event):  # refresh pane color and enable according to checkbox
        #print self.name,   "partrefresh"
        if self.partcb.GetValue():
            # Turn on part
            self.partpan.SetBackgroundColour(COL_ENABLED)
            self.partpan.Refresh()
            #print self.name, "Set to ON"
        else:
            # Turn Off part
            self.partpan.SetBackgroundColour(COL_DISABLED)
            self.partpan.Refresh()
            #print self.name, "Set to OFF"
            pass
   
# InPart class -- Creates extra controls within part pane for an instrument
class InPart(Part):
    
    def __init__(self,name,comtype):
        Part.__init__(self,name)        
              
        # Create input channel selectors
        if comtype == "EOB":
            wx.StaticText(self.partpan, -1, "Pitch Eobody  Vol", pos=(90,5))
            self.eobpitch = wx.SpinCtrl(self.partpan, -1,  '', (90,25), (40, -1))
            self.eobvolch = wx.SpinCtrl(self.partpan, -1,  '', (140,25), (40, -1))
            self.attlist.append(["eobpitch",self.eobpitch])
            self.attlist.append(["eobvolch",self.eobvolch])
        elif comtype == "BT":
            wx.StaticText(self.partpan, -1, "BT COM port", pos=(120,5))
            
            self.blueChanCtrl = wx.SpinCtrl(self.partpan, -1,  '', (140,25), (40, -1))
            self.attlist.append(["blueCOM",self.blueChanCtrl])
            
            self.blueStatus = wx.StaticText(self.partpan, -1, "--     ", pos=(100,28))
            
            
        else:
            wx.StaticText(self.partpan, -1, "Unknown Type", pos=(90,5))
            
        # Create noteRange selectors
        wx.StaticText(self.partpan, -1, "Low end       Range", pos=(200,5))
        self.lowendbox = wx.ComboBox(self.partpan, -1, choices=mmref.whitekeys, pos=(200, 25), size=(40, -1), style=wx.CB_READONLY)
        self.lowendbox.SetValue('C3')
        self.lowendbox.Bind(wx.EVT_COMBOBOX , readControls) 
        self.attlist.append(["lowend",self.lowendbox])
        self.noteRangebox = wx.ComboBox(self.partpan, -1, choices=mmref.rangekeys, pos=(245, 25), size=(80, -1), style=wx.CB_READONLY)
        self.noteRangebox.SetValue('2 Octaves')
        self.noteRangebox.Bind(wx.EVT_COMBOBOX, readControls)
        self.attlist.append(["range",self.noteRangebox])
        
        # Create Midi Channel Selector
        wx.StaticText(self.partpan, -1, "Midi Ch", pos=(340,5))
        self.midich = wx.SpinCtrl(self.partpan, -1, '', (340,25), (40,-1))
        self.midich.Bind(wx.EVT_SPINCTRL, readControls) 
        self.attlist.append(["MidiChan", self.midich])
        
        # Create Midi Instrument Selector
        wx.StaticText(self.partpan, -1, "Midi Instrument", pos=(390,5))
        self.midinst = wx.ComboBox(self.partpan, -1, choices=mmref.midiname, pos=(390,25), size=(135,-1), style=wx.CB_READONLY)
        self.midinst.SetValue(mmref.midiname[0])
        self.midinst.Bind(wx.EVT_COMBOBOX, readControls)
        self.attlist.append(["midinst",self.midinst])

# ByteReader class -- reads incoming midi bytes from eobody and puts them in the instrument queues
class ByteReader(threading.Thread):
    
    # Initiates the thread, but doesn't actually start running it yet
    def __init__(self):
        threading.Thread.__init__(self)
        self.eobChanArray = ['','','', '','','', '','','']
        #print 'bytereader init'
    
    # Called by start() to a bytereader instance, calls this run method that runs forever
    def run(self):
        global threadsAlive, active
        midinpoll = midin.poll
        midinread = midin.read
        eobChanArray = self.eobChanArray
        
        while threadsAlive:
            while active:                      # Run in this loop while active
                if midinpoll():                # Check for incoming byte from Eobody
                    #print "poll"
                    byte = midinread(1)        # Assign the incoming byte of information
                    bytechan = byte[0][0][1]   # this part of the byte has the eobody channel 
                    bytevalue = byte[0][0][2]  # this part of the byte has the value (voltage)
                                        
                    if bytechan > 0:           # just to be sure we got something
                        queue = eobChanArray[bytechan]  # get the queue ptr  
                        if queue:              # be sure a queue is assigned
                            queue.put(bytevalue)   # put the value in the proper queue
                            #print bytevalue, "put in q", bytechan
            while midin.poll() and not active:   # while not active, keep flushing midi buffer # *****
                throwaway = midin.read(1)
    
    # Create the eobChanArray list of Eobody channel number and instrument queues
    def newEobChanArray(self):
        # each array element is associated with an eobody channel (1-8)
        # each stores the pointer to the queue assigned to that channel
        # [<blowqueue>, <turnqueue>, <aqueue>, <bqueue>, '', '', '', '', '']
        #print "begin newEobChanArray"
        for name,instrument in Instrument.iArray:
            if instrument.comtype == "EOB" and instrument.partcb.GetValue() == True:  #only put in instruments that are enabled
                chan = instrument.eobpitch.GetValue()
                self.eobChanArray[chan] = instrument.aqueue
                chan = instrument.eobvolch.GetValue()
                self.eobChanArray[chan] = instrument.bqueue
        #print "newEobChanArray", self.eobChanArray
        pass
    
# Constraint class -- A set of routines to constrain instrument notes.  This is a non-instantiated class
class Constraint:
    root = 0
    chord = [0,4,7]
    advancedInstruments = ["Marimbar","Baronium","Pluck n Play"]
    
    @staticmethod   # has no self parameter     
    def setAllScaleNotes(keyletter, tonality): # sends root and scalenotes to all instruments
                # Called by Run method of Accomp just after reading songfile, and called at program startup
                # In both cases its just to set things to a basic starting key
        # keyletter looks like "C" or "D#" or "Bb"
        # tonality is "major", or "relative", or "harmonic" (minor)
        midistart = 12 + mmref.getSig(keyletter)
        onescalenotes = mmref.scaleNotes(tonality)
        #print "beginning setAllScaleNotes", onescalenotes
        #print Instrument.iArray
        for name,instrument in Instrument.iArray:
            if instrument.partcb.GetValue():
                #print name, "is on "
                instrument.setMyScaleNotes(midistart,onescalenotes)
    
    @staticmethod    
    def setChord(newroot, newchord):  # sets the new chord then sets array for all instruments
                                      # called by accomp while playing song
        # newroot is a midi number fo the root chord, newchord is an array like [1,4,7]
        Constraint.root = newroot
        Constraint.chord = newchord
        for name,instrument in Instrument.iArray:
            if instrument.partcb.GetValue():
                instrument.setMyChordNotes(Constraint.root,Constraint.chord)
                instrument.chordchanged = True
    
    @staticmethod    
    def setAdvancedChord(newroot, newchord):  # for each "advanced inst.", sets array for that instrument
                                        # called by accomp just ahead of the usual setChord while playing song
        for name,instrument in Instrument.iArray:
            if instrument.partcb.GetValue() and name in Constraint.advancedInstruments:
                instrument.setMyChordNotes(newroot,newchord)
                instrument.chordchanged = True
    
    @staticmethod    
    def updateAllChordNotes():  # just updates chord array of all instruments (assumes root and chord are already set)
                                # called only by readcontrols                       
        for name,instrument in Instrument.iArray:
            if instrument.partcb.GetValue():
                instrument.setMyChordNotes(Constraint.root,Constraint.chord)
                
    @staticmethod
    def setAllModes(mode):  # sets all instruments to "chord" or "scale" mode
                            # called by chordScale and setChordButtonsOff
        for name,instrument in Instrument.iArray:
            if instrument.partcb.GetValue():
                instrument.setMyMode(mode)
    
# Accomp class -- Accompaniment class  This does everything related to the accompaniment.  Much of the action happens here.
class Accomp(threading.Thread,Part):
    
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
        Part.__init__(self,name)
        self.chordchannel = 10
        self.perc1channel = 9
        self.perc2channel = 9
        self.perc3channel = 9
        
        # set default values for parameters that come from the songfile
        self.tonality = "major"
        self.keyletter = "C"
        self.tempo = 120
        self.style = 0

        # set default voices for the chords and percussion
        self.chordvoice = 3 # default is piano for the chords
        self.perc1inst = 36  # 
        self.perc2inst = 57  #
        self.perc3inst = 38  # 
        
        # set default percussion patterns
        self.chordpattern = 'x-------'  # deault chord patterns
        self.perc1pattern = 'x-x-x-x-'
        self.perc2pattern = '--------'
        self.perc3pattern = '--------'
        
        # Create Chord Voice Selector on the panel
        wx.StaticText(self.partpan, -1, "Chord Voice", pos=(390,5))
        self.chordVoiceBox = wx.ComboBox(self.partpan, -1, choices=mmref.midiname, pos=(390,25), size=(135,-1), style=wx.CB_READONLY)
        self.chordVoiceBox.SetValue(mmref.midiname[self.chordvoice])  # this makes default piano
        self.chordVoiceBox.Bind(wx.EVT_COMBOBOX, self.setChordVoice )   
        self.attlist.append(["chordVoice",self.chordVoiceBox])
        #print self.name, "init"
    
        # Create the Percussion Drum Selectors on the panel
        wx.StaticText(self.partpan, -1, "Percussion", pos=(200,5))
        self.perc1Box = wx.ComboBox(self.partpan, -1, choices=mmref.mididrum, pos=(200,25), size=(135,-1), style=wx.CB_READONLY)
        self.perc1Box.SetValue(mmref.mididrum[self.perc1inst-27])  # this makes default
        self.perc1Box.Bind(wx.EVT_COMBOBOX, self.setPercInstAll )
        self.perc2Box = wx.ComboBox(self.partpan, -1, choices=mmref.mididrum, pos=(200,50), size=(135,-1), style=wx.CB_READONLY)
        self.perc2Box.Bind(wx.EVT_COMBOBOX, self.setPercInstAll )
        self.perc2Box.SetValue(mmref.mididrum[self.perc2inst-27])  # this makes default 
        self.perc3Box = wx.ComboBox(self.partpan, -1, choices=mmref.mididrum, pos=(200,75), size=(135,-1), style=wx.CB_READONLY)
        self.perc3Box.Bind(wx.EVT_COMBOBOX, self.setPercInstAll )
        self.perc3Box.SetValue(mmref.mididrum[self.perc3inst-27])  # this makes default 
    
        # Create the Advance adjustment on the panel
        # This is to make the coming chord constraint take effect a bit before the beat
        # the advancedtime is in milliseconds, setTik turns on a percussive "tik" to hear the transition
        advancedChoices = ["0","10","20","50","75","100","125","150","175","200","250","300","500"]
        wx.StaticText(self.partpan, -1, "Advance", pos=(90,30))
        self.advancedBox = wx.ComboBox(self.partpan, -1, choices=advancedChoices,value="100",pos=(90,50), size=(42,-1), style=wx.CB_READONLY)
        self.advancedBox.Bind(wx.EVT_COMBOBOX, self.setAdvance)
        self.advancedtik = 0
        self.advancedTikBox = wx.ToggleButton(self.partpan, -1, 'tik', pos=(140,50), size=(30,20))
        self.advancedTikBox.Bind(wx.EVT_TOGGLEBUTTON,self.setTik)             
    
    def setTik(self,event):
        self.advancedtik = self.advancedTikBox.GetValue()
    
    def setAdvance(self,event):
        self.advancedtime = int(self.advancedBox.GetValue())
            
    def setChordVoice(self, event):   #
        self.chordvoice = int(re.split(" ",self.chordVoiceBox.GetValue())[0])
        midout.set_instrument(self.chordvoice, self.chordchannel)
        
    def setPercInstAll(self, event):   # 
        self.perc1inst = int(re.split(" ",self.perc1Box.GetValue())[0])
        midout.set_instrument(self.perc1inst, self.perc1channel)
        self.perc2inst = int(re.split(" ",self.perc2Box.GetValue())[0])
        midout.set_instrument(self.perc2inst, self.perc2channel)
        self.perc3inst = int(re.split(" ",self.perc3Box.GetValue())[0])
        midout.set_instrument(self.perc3inst, self.perc3channel)
        
    def run(self):   # This method plays the song and sets the chord constraints as it goes
        global threadsAlive, playing, songpicked
        while threadsAlive:
                 
            while playing:
                
                # if we pressed start without selecting a song, then open browser.
                if not songpicked:
                    songBrowser(1)
                    
                # Read the songfile and set static parameters
                chordarray = self.readSongFile()
                Constraint.setAllScaleNotes(self.keyletter, self.tonality)
                midout.set_instrument(self.chordvoice, self.chordchannel)
                lastchord = []
                iaccomp = 0
                self.advancedtime = int(self.advancedBox.GetValue()) 
                
                lenchordpat = len(self.chordpattern)
                lenconstpat = len(self.constpattern)
                lenperc1pat = len(self.perc1pattern)
                lenperc2pat = len(self.perc2pattern)
                lenperc3pat = len(self.perc3pattern)
                
                oneBeat = int(60.0/self.tempo * 1000)   # milliseconds for one beat
                
                # produce a series of beats leading up to the start of the song
                for beat in range(self.defaultduration):
                    if not playing: break
                    pygame.time.wait(self.advancedtime)
                    midout.note_on(42,accomp.outvol.GetValue(),self.perc1channel)
                    midout.note_off(42,accomp.outvol.GetValue(),self.perc1channel)
                    pygame.time.wait(oneBeat - self.advancedtime)
                
                # Step through the chordarray.  ------- This is the main loop creating the accompaniment ----------          
                for line in chordarray:
                    # line looks like:  [5, [0, 4, 7], 'triad', 0, 4]    see readSongFile
                    keymod, linechord, chordtype, inversion, duration = line
                    
                    if not playing: break
                    
                    # Set the output volumes   ##########  this should be done by binding the control instead   ####
                    chordvol = accomp.outvol.GetValue()
                    perc1vol = chordvol
                    perc2vol = chordvol
                    perc3vol = chordvol
                    
                    # set the advanced chord constraints and then wait the advance time
                    Constraint.setAdvancedChord(keymod,linechord)
                    if self.advancedtik:
                        midout.note_on(42,perc1vol,self.perc1channel)
                        midout.note_off(42,perc1vol,self.perc1channel)
                    pygame.time.wait(self.advancedtime) #### we could start a timer, do some of the stuff below while waiting
                    
                    # set the chord constraint according to line in chordarray
                    Constraint.setChord(keymod,linechord)
                     
                    beats = range(duration) # If duration is 4  then beats is  [0, 1, 2, 3]        
                    
                    # Choose accompaniment notes according to linechord and chordtype
                    chord = []
                    if chordtype != 'free':
                        chord.append(linechord[0] + keymod + 36)  # Root of chord up three octaves from Midi zero
                        chord.append(linechord[2] + keymod + 36)  # Usually this is the fifth of the chord
                        chord.append(linechord[1] + keymod + 48)  # Third of chord placed up an extra octave
                        if chordtype == 'triad': chord.append(linechord[0] + keymod + 60)  # repeat the root up two octaves
                        elif chordtype =='seven': chord.append(linechord[3] + keymod + 48) # add the seventh to the chord
                    elif chordtype == 'free':  # Special 'free' type of chord is specified directly by Midi note numbers
                        for freeNote in linechord:
                            chord.append(freeNote + keymod)
                    
                    # produce the accompaniment chords and rhythm patterns
                    beats2 = range(0,2*len(beats))   # the chord and percussion patterns are on sub-beats half as long
                    for ibeat in beats2:             # ibeat counts out these sub-beats
                        #print iaccomp, "/", beats2
                        if not playing: break
                           
                        # if there is a constraint pattern in the songfile, set mode according to it
                        # this make it possible to have the constraint only enforced on some beats of a measure
                        if self.constpattern:
                            if self.constpattern[iaccomp%lenconstpat] == 'x':
                                Constraint.setAllModes("chord")
                            else:
                                Constraint.setAllModes("scale")
                            
                        # if accomp turned on, play accomp chord and perc rhythms
                        if self.partcb.GetValue():
                            if self.chordpattern[iaccomp%lenchordpat] == 'x':
                                for note in lastchord:    #end last chord
                                    midout.note_off(note, chordvol, self.chordchannel)
                                for note in chord:        #Play the accompaniment chord
                                    midout.note_on(note, chordvol, self.chordchannel)
                                lastchord = chord
                                #print "chord on", chord
                            
                            if self.perc1pattern[iaccomp%lenperc1pat] == 'x':
                                midout.note_on(self.perc1inst,perc1vol,self.perc1channel)
                                midout.note_off(self.perc1inst,perc1vol,self.perc1channel)
                            if self.perc2pattern[iaccomp%lenperc2pat] == 'x':
                                midout.note_on(self.perc2inst,perc2vol,self.perc2channel)
                                midout.note_off(self.perc2inst,perc2vol,self.perc2channel)
                            if self.perc3pattern[iaccomp%lenperc3pat] == 'x':
                                midout.note_on(self.perc3inst,perc3vol,self.perc3channel)
                                midout.note_off(self.perc3inst,perc3vol,self.perc3channel)
                        
                        if ibeat != beats2[-1]:     
                            pygame.time.wait(int(oneBeat/2))  # this is a regular beat, no advance
                        else:
                            pygame.time.wait(int(oneBeat/2)-self.advancedtime)  # last beat so shorten it to account 
                                                                                # for the advanced time
                        iaccomp = iaccomp + 1
                
                # reached the end of the song
                Bn = 0xB0 + self.chordchannel
                midout.write([[[Bn, 123, 0], pygame.midi.time()]]) 
                playing = False
            

    def readSongFile(self):  # Read song file, parse it, and return chordArray
        #chordArray looks like this:
        #[[5, [0, 4, 7], 'triad', 0, 4],       5 is the key+modulation relative to C (5=F)
        # [5, [5, 9, 12], 'triad', 0, 4],      [5, 9, 12] is the chord relative to the I level
        # [5, [0, 4, 7], 'triad', 0, 4],       'triad' or 'seven' is the type of chord
        # [5, [7, 11, 14], 'triad', 0, 4],     0, 1, 2, or 3 is the inversion
        # [5, [0, 4, 7], 'triad', 0, 4], ...]  4 is the duration of this chord in beats
        
        global songfilename
        
        style = 0
        chordvoice = 0
        filearray = []   # an array of raw lines from the file
        chordarray = []   # the final array of chord data
        self.constpattern = ""
        
        #Read the score file and append each line to a filearray
        #Each element in the array will be another array consisting of the elements of one line parsed by ":" 
        file = open(songfilename)
        for line in file:
            aline = line.strip()
            indline = re.split(': ', aline)
            filearray.append(indline)
        #Interpret file array to set variables like, tempo, tonality etc
        #Sets important variables like , keynum (midi number for the key), default_chord_duration, and key
        #Then creates and returns the chordarray(see above)
        for line in filearray:
            if line[0] == 'Key':
                if line[1][0].isupper(): self.tonality = 'major'
                else:
                    if line[1].find('n') != -1: self.tonality = 'natural'
                    elif line[1].find('h') != -1: self.tonality = 'harmonic'
                self.keyletter = line[1].strip('nh')
                if len(self.keyletter) == 1:
                    keynum = mmref.getSig(line[1].upper())        # keynum is the midi number for the key
                elif len(self.keyletter) == 2:
                    keynum = mmref.getSig(line[1][0].upper() + line[1][1])
            if line[0] == 'Tempo':
                self.tempo = int(line[1])
            if line[0] == 'Chord duration':
                self.defaultduration = int(line[1])
                currentduration = float(line[1])
            if line[0] == 'Chords':
                #print "Reading chords"
                modulation = 0
                # chord can be: 'IV', 'iiidim', 'V7/V', 'I64', 'V6'
                # or can be "manually" specified by something like: '(0,3,5,9)'
                # number in parenthesis following chord: 'V7(2)  is special number of beats to override normal chord duration: 
                for info in re.split(' ', line[1]):
                    if info.startswith('/'):  # Not sure how this works
                        modulation = self.modulate(info)
                    elif info.startswith('('):  # this is for manual specifying
                        notes = []  
                        info = info.strip('()')
                        notelist = re.split(',', info)
                        for note in notelist:
                            notes.append(mmref.getNote(note))
                        chordarray.append([0, notes, 'free', 0, delay])
                    elif info != '':  
                        if info.endswith(')') and not info[info.find('(') + 1: info.find(')')].isalpha():  # this is for special chord duration
                            # we have a special chord duration
                            currentduration = float(info[info.find('(') + 1: info.find(')')])
                        else: currentduration = self.defaultduration
                        #print "info:", info
                        notes, chordtype, inversion = mmref.romanToChord(info, self.tonality)
                        #print "roman ok"
                        chordarray.append([keynum + modulation, notes, chordtype, inversion, currentduration]) #This is how the songarray is formatted
                        #print "info appended"
            if line[0] == 'Accompaniment' or line[0] == 'Chord voice':
                self.chordvoice = int(line[1])
                self.chordVoiceBox.SetValue(mmref.midiname[self.chordvoice])
            if line[0] == 'Chord pattern':
                self.chordpattern = line[1].strip(' ')
            if line[0] == 'Const pattern':
                self.constpattern = line[1].strip(' ')
            if line[0] == 'Perc1 instrument':
                self.perc1inst = int(line[1])
                self.perc1Box.SetValue(mmref.mididrum[self.perc1inst-27])
            if line[0] == 'Perc1 pattern':
                self.perc1pattern = line[1].strip(' ')
            if line[0] == 'Perc2 instrument':
                self.perc2inst = int(line[1])
                self.perc2Box.SetValue(mmref.mididrum[self.perc2inst-27])
            if line[0] == 'Perc2 pattern':
                self.perc2pattern = line[1].strip(' ')
            if line[0] == 'Perc3 instrument':
                self.perc3inst = int(line[1])
                self.perc3Box.SetValue(mmref.mididrum[self.perc3inst-27])
            if line[0] == 'Perc3 pattern':
                self.perc3pattern = line[1].strip(' ')
             
            if line[0] == 'Style':      # no longer used
                self.style = int(line[1])
        
        file.close()
        
        #print "chordarray:", chordarray
        return chordarray
    
# Instrument class -- Basis for all instruments    
class Instrument(threading.Thread):
    iArray = []  #   [ [obloe1, <instance>],[obloe2, ...] ]  ### instrument.iArray
        
    def __init__(self,name,comtype):
        threading.Thread.__init__(self)
        self.comtype = comtype
        self.aqueue = queue.Queue()  # these Queues hold the incoming data from the ByteReader
        self.bqueue = queue.Queue()
        self.name = name
        Instrument.iArray.append([name, self])  #each instrument instance gets appended to iArray
        self.scalenotes = []  #This is the set of unconstrained notes available to play in the key 
        self.chordnotes = [] # The constrained notes available
        self.mode = "chord"
        self.chordchanged = False
        self.trace = ""
        self.lock = threading.Lock() # a lock for setting and reading chordnotes and scalenotes
    
    def chooseNote(self,rawnote):  # 
        # Return the note nearest rawnote from among the allowed chordnotes (or scalenotes)
        with self.lock:    # wait until setMyChordNotes (or ScaleNotes)is done writing.
            if self.mode == "chord": allowednotes = self.chordnotes
            else: allowednotes = self.scalenotes
           
        lastinote = 0
        self.trace = "inchoo", rawnote
        for inote in allowednotes:                                    #try each allowed inote
            if inote > rawnote:                                           #if it's above the rawnote
                if inote - rawnote < rawnote - lastinote: note = inote        #if inote is closer use it
                else: note = lastinote                                        #else use lastinote
                lastinote = 999                                               #remember we got one
                break                                                         #get out of this loop goto "if not"
            lastinote = inote                                             #still lookin so update lastinote
            self.trace = "inloop", inote, rawnote
        
        if not (lastinote == 999):
            note = inote
            self.trace = "999:", rawnote
            #print "past top end", rawnote, note
        return note
        
    def setMyScaleNotes(self,midistart,onescalenotes): # creates scalenotes array for instrument
        # midistart is a midi number corresponding to root of the chord
        # onescalenotes is array looking like:[0,2,4,5...,11] specifying relative notes in the scale
        # scalenotes is array [24,28,31,....73] giving all scale notes within instrument range 
        with self.lock:
            self.scalenotes = []
            #print self.name, "setting scalenotes"
            for octave in range(0,10):
                for note in onescalenotes:
                    midinote = midistart + 12*octave + note
                    if midinote >= self.lowend and midinote <= self.lowend + self.noteRange:
                        self.scalenotes.append(midinote)
            #print self.name, "scalenotes", self.scalenotes    
    
    def setMyChordNotes(self,root,chord): # from root and chord, creates chordnotes array
        # root is a midi number corresponding to root of the chord
        # chord is array looking like:[0,4,7] specifying relative notes in the chord
        # chordotes is array [24,28,31,....73] giving all chordal notes within instrument range 
        midistart = 12 + root
        with self.lock:
            self.chordnotes = []
            lowend = self.lowend
            highend = lowend + self.noteRange
            for octave in range(0,10):
                for note in chord:
                    midinote = midistart + 12*octave + note
                    if midinote >= lowend and midinote <= highend:
                        self.chordnotes.append(midinote)
            #print name, "chordnotes", self.chordnotes
        pass
        
    def setMyMode(self, mode):
        # mode can be "chord" or "scale"
        self.mode = mode
    
# Obloe class -- Basis for instruments which have long sustained notes with aftertouch control
class Obloe(Instrument, InPart):
    
    def __init__(self, name, comtype):
        Instrument.__init__(self,name,comtype)
        InPart.__init__(self,name,comtype)
        #self.note = self.lastnote = self.volume = self.lastvolume = 0
        self.lastnote = self.lastrawnote = self.lastvolume = 0
        self.threshold = 12  # blowbytes less than this get volume set to zero
        self.volumefactor = 2.0  # blowbytes get multiplied by this
        self.maxvolume = 127
        self.pitchfactor = 1.0  # turnbytes get multiplied by this
        
    def run(self):  # while active, check the queue, derive note and volume, play the note
        global threadsAlive, active
        note = lastnote = lastvolume = lastrawnote = 0
        
        # define local varaibles and calls to eliminate searching ( may be unnec.)
        self.midichan = self.midich.GetValue()
        self.midivol = 0xB0 + self.midichan
        partcbValue = self.partcb.GetValue    
        turnqueuesize = self.aqueue.qsize
        blowqueuesize = self.bqueue.qsize
        turnqueueget = self.aqueue.get
        blowqueueget = self.bqueue.get
        blowbyte = 0
        turnbyte = 0
        0
        while threadsAlive:
            self.trace = "Idling"           
            while partcbValue() and active:     # loop only when this intrument is on and system is active
                self.trace = "running"
                gotbyte = False
                if turnqueuesize():             # If turnque has a byte
                    #print "turnq"
                    time0 = pygame.time.get_ticks()
                    turnbyte = turnqueueget()   # get it
                    gotbyte = True
                if blowqueuesize():             # If blowqueue has a byte
                    #print "blowq"
                    time0 = pygame.time.get_ticks()
                    blowbyte = blowqueueget()   # get it
                    gotbyte = True
                
                # if we have a byte then determine note and volume and play it
                if gotbyte:
                    #print "gotbyte",  turnbyte, blowbyte
                    self.trace = "raw {0}, {1}".format(turnbyte, blowbyte)
                    
                    rawnote,volume = self.calcRawnoteVolume(turnbyte,blowbyte)
                    self.trace = "choo {0}".format(rawnote)
                    
                    note = self.chooseNote(rawnote) 
                    self.trace = "note chosen"  
                    
                    self.playNote(note,rawnote,volume)
                    
                     
                    
    def calcRawnoteVolume(self, turnbyte, blowbyte):
        # Calculate volume from blowByte
        volume = blowbyte
        if volume < self.threshold: volume = 0
        volume = int(volume * self.volumefactor * self.outvol.GetValue() / 60)  
        if volume > self.maxvolume: volume = self.maxvolume
         
        # Calculate rawnote from turnByte  (rawnote is in midi numbers but floated)
        rawnote = self.lowend + self.noteRange * (turnbyte*self.pitchfactor)/127.0  
        #print "rawnote", self.lowend, self.noteRange, rawnote
        
        return rawnote, volume
    
    def playNote(self,note,rawnote,volume):
        self.trace = "PlayNote"
        if volume != self.lastvolume or note != self.lastnote:
            if self.lastvolume == 0 and volume != 0:              # New note starting from nothing
                midout.note_on(note, 100, self.midichan)
                midout.write([[[self.midivol, 0x07, volume], pygame.midi.time()]])  #Kluge
                #print 'Note on.  Vol: ', volume, 'Note: ', note
                self.lastrawnote = rawnote
                self.lastnote = note
                self.lastvolume = volume
                self.chordchanged = False
            elif self.lastvolume != 0 and volume == 0:       # Note was sounding but is now turned off
                midout.note_off(self.lastnote, self.lastvolume, self.midichan)
                #print 'sounding note is off ', self.lastnote
                self.lastvolume = 0
            elif volume != 0 and note != self.lastnote and (abs(rawnote - self.lastrawnote) > 1.0*self.pitchfactor or self.chordchanged):    # Changing note while sounding
                #print "turned off old note:", self.lastnote
                midout.note_off(self.lastnote, self.lastvolume, self.midichan)
                midout.note_on(note, 100, self.midichan)
                midout.write([[[self.midivol, 0x07, volume], pygame.midi.time()]])  #Kluge
                #print '             New Note:', note, 'Vol:', volume
                self.lastrawnote = rawnote
                self.lastnote = note
                self.lastvolume = volume
                self.chordchanged = False
            elif volume > 0:           # Currently sounding note volume adjusted
                #midout.write([[[0xA3, note, volume], pygame.midi.time()]])   
                midout.write([[[self.midivol, 0x07, volume], pygame.midi.time()]])  #Kluge
                #print 'Note adjust. Vol: ', volume
                self.lastvolume = volume
            else:                                                           
                pass
    
# Sway class -- specifics for Sway n Play, based on Obloe
class Sway(Obloe):
    def __init__(self, name, comtype):
        Obloe.__init__(self,name,comtype)
        self.volumefactor = 1.0
        self.pitchfactor = 2.0
    
# Baron class -- specifics for Baronium, based on Obloe
class Baron(Obloe):
    def __init__(self, name, comtype):
        Obloe.__init__(self,name,comtype)
        self.volumefactor = 2.0
        self.pitchfactor = 1.1
        self.interaction = 0.11  # pressing on one end still creates a small signal on the other
        self.threshold = 3
        
    def calcRawnoteVolume(self, left, right):   # override usual Obloe method 
        # Baronium outputs signal from each end of bar.  These must be turned into volume and pitch.
        sum = right + left
        volume = int(sum * 0.5)
        if sum < self.threshold: sum = -1
        position = int((float(right)- 0.11*left)/sum * 127)
        rawnote = self.lowend + self.noteRange * (position*self.pitchfactor)/127.0  # Divide the slide equally between the number of notes in swaynotes, then set the index to be which of those regions is being pressed on the touch sensor
        if volume < self.threshold: volume = 0
        volume = int(volume * self.volumefactor * self.outvol.GetValue() / 60)  
        if volume > self.maxvolume: volume = self.maxvolume
        #print left, right, rawnote, volume
        return rawnote, volume
    
# Pluck class -- specifics for Pluck n Play 
class Pluck(Instrument, InPart):
    def __init__(self, name, comtype):
        Instrument.__init__(self,name,comtype)
        InPart.__init__(self,name,comtype)
        self.volumefactor = 1.0
        self.pitchfactor = 3.0
        self.threshold = 5  # pluck must exceed this
        self.maxvolume = 127
        
        
    def run(self):
        global threadsAlive, active
        while threadsAlive:
            
            note = lastnote = lastvolume = 0
            partcbValue = self.partcb.GetValue    
            slidequeuesize = self.aqueue.qsize
            pluckqueuesize = self.bqueue.qsize
            slidequeueget = self.aqueue.get
            pluckqueueget = self.bqueue.get
            volumefactor = self.volumefactor
            threshold = self.threshold
            outvolget = self.outvol.GetValue
            maxvolume = self.maxvolume
            pitchfactor = self.pitchfactor
            mode = self.mode
            midoutnote_on = midout.note_on
            midoutwrite = midout.write
            midoutnote_off = midout.note_off
            pygamemiditime = pygame.midi.time
            rawnote = self.lowend
            zerolevel = 70
                            
            channel = self.midich.GetValue()
            midivol = 0xB0 + channel
            
            plucked = False
            while self.partcb.GetValue() and active:
                
                if slidequeuesize():
                    slidebyte = slidequeueget()                                             # Get that byte
                    #print self.name, "got slidebyte:", slidebyte
                    slidepos = zerolevel - slidebyte
                    rawnote = self.lowend + self.noteRange * (slidepos*pitchfactor)/127.0  # Divide the slide equally between the number of notes in swaynotes, then set the index to be which of those regions is being pressed on the touch sensor
                    
                if pluckqueuesize():   
                    volume = pluckqueueget()
                    #print self.name, "got pluckbyte:", volume
                    #volume = int(rawvolume * volumefactor)
                    if volume < threshold: volume = 0
                    else: volume = int(volume * self.volumefactor * self.outvol.GetValue() / 60)  
                    if volume > 127: volume = 127
                    #print "rawvol", rawvolume, "adjusted volume", volume
                    
                    if volume >= lastvolume:     # pluck value is still increasing or sitting at zero, reset lastvolume
                        lastvolume = volume        
                        #print "increasing"
                    elif plucked:                # value is dropping from previous pluck, check if it has reached zero
                        #print "dropping"
                        if volume == 0:   # if zero, then reset for next pluck
                            lastvolume = volume
                            plucked = False
                            #print "now below threshold ready for another"
                            
                    else:                        # value is dropping and not from a previous pluck. Sound the note.
                        note = self.chooseNote(rawnote) 
                        #print "note to sound"
                        midoutnote_off(lastnote, lastvolume, channel)                # Turn off the last note
                        midoutnote_on(note, lastvolume, channel)                     # Turn on the current note
                        lastvolume = volume
                        lastnote = note                                         # Set the note being played to lastnote
                        plucked = True

# Marim class -- specifics for Marimbar
class Marim(Instrument, InPart):
    def __init__(self, name, comtype):
        Instrument.__init__(self,name,comtype)
        InPart.__init__(self,name,comtype)
        self.volumefactor = 2.0
        self.pitchfactor = 1.0
        self.maxvolume = 127
        self.threshold = 3  # hit must exceed this
        self.hitduration = 10  # time (ms) during which we look for peak values
        self.deadtime = 30  # time in ms during which a repeat hit is disabled to avoid retriggering on bar vibrations.
        
    def run(self):
        global threadsAlive, active
        while threadsAlive:
            
            note = lastnote = lastvolume = 0
            partcbValue = self.partcb.GetValue    
            leftqueuesize = self.aqueue.qsize
            rightqueuesize = self.bqueue.qsize
            leftqueueget = self.aqueue.get
            rightqueueget = self.bqueue.get
            volumefactor = self.volumefactor
            threshold = self.threshold
            outvolget = self.outvol.GetValue
            maxvolume = self.maxvolume
            pitchfactor = self.pitchfactor
            mode = self.mode
            midoutnote_on = midout.note_on
            midoutwrite = midout.write
            midoutnote_off = midout.note_off
            pygamemiditime = pygame.midi.time
            rawnote = self.lowend
            zerolevel = 70
            
                            
            channel = self.midich.GetValue()
            midivol = 0xB0 + channel
            midiOnTime = 0
            plucked = False
            #print "init Marim"
            while self.partcb.GetValue() and active:
                hitTime = leftByte = highestLeftByte = rightByte = highestRightByte = note = lastNote = volume = lastVolume = 0
                #print "Marim running"            
                while leftByte < threshold and rightByte < threshold:   # waiting for a byte to come from either sensor that is more than noise
                    if leftqueuesize():
                        leftByte = leftqueueget()
                    if rightqueuesize():
                        rightByte = rightqueueget()
                hitTime = pygame.time.get_ticks()            # time of first value found above threshold
                
                # now find highest value on both left and right sensors until hit duration is past
                while (pygame.time.get_ticks() - hitTime) < self.hitduration:     
                    if leftByte > highestLeftByte: highestLeftByte = leftByte
                    if leftqueuesize(): leftByte = leftqueueget()
                    if rightByte > highestRightByte: highestRightByte = rightByte
                    if rightqueuesize(): rightByte = rightqueueget()
                    
                if (pygame.midi.time() - midiOnTime) > self.deadtime:   # only make notes of hits after deadtime
                
                    rawnote, volume = self.calcRawnoteVolume(highestLeftByte, highestRightByte)
                
                    note = self.chooseNote(rawnote)
                
                    midout.note_off(lastNote, lastVolume, channel)
                    if note != 0: midout.note_on(note, volume, channel)
                    #print " -------------note: ",note, "v:",volume, pygame.midi.time()
                    midiOnTime = pygame.midi.time()
                    lastNote = note
                    lastVolume = volume
                    
                else:
                    #print "passed"
                    pass
               
    def calcRawnoteVolume(self, left, right):
        sum = right + left
        
        volume = int((sum - self.threshold) * 0.5) 
        if volume < 0: volume = 0
        volume = int(volume * self.volumefactor * self.outvol.GetValue() / 60)  
        if volume > self.maxvolume: volume = self.maxvolume
        
        position = int((float(right)- 0.11*left)/sum * 127)
        rawnote = self.lowend + self.noteRange * (position*self.pitchfactor)/127.0  # Divide the slide equally between the number of notes in swaynotes, then set the index to be which of those regions is being pressed on the touch sensor
        #print left, right, rawnote, volume
        return rawnote, volume
    
# Blue class -- has bluetooth com port, otherwise based on Obloe
class Blue(Obloe):
    
    def __init__(self, name, comtype):
        Instrument.__init__(self,name,comtype)
        self.bluechan = 5
        InPart.__init__(self,name,comtype)
        self.lastnote = self.lastrawnote = self.lastvolume = 0
        self.threshold = 1  # blowbytes less than this get volume set to zero
        self.volumefactor = 2.0  # blowbytes get multiplied by this
        self.maxvolume = 127
        self.pitchfactor = 0.25  # turnbytes get multiplied by this
        self.gotblue = False
        self.blueChanCtrl.Bind(wx.EVT_SPINCTRL, self.openBlue)
            
    
    def openBlue(self, event):    # This opens the com port that has a Bluetooth connection to the BlueToot instrument 
    #  Note that all Windows user controls and this GUI ctrl number the COM ports from 1-20 while serial.Serial uses 0-19
        try:
            print ("trying Bluetooth on channel:", self.blueChanCtrl.GetValue())
            self.BlueTootPort = serial.Serial(self.blueChanCtrl.GetValue()-1, 115200, timeout = 0)
            print ("found Bluetooth port on channel ", self.blueChanCtrl.GetValue())
            self.gotblue = True
            self.blueStatus.SetLabel("      OK")
        except Exception as inst:
            print ("Can't find Bluetooth port. >>", inst)
            self.gotblue = False
            self.blueStatus.SetLabel("No port")
           
    def run(self):
        global threadsAlive, active
        self.trace = "pre idle"
        self.midichan = self.midich.GetValue()
        self.midivol = 0xB0 + self.midichan
        partcbValue = self.partcb.GetValue    
        blowbyte = 0
        turnbyte = 0
        self.openBlue(1)
        
        while threadsAlive:
            self.trace = "Idling"       
            # Flush the buffer while waiting
            if (self.gotblue == True) and (self.BlueTootPort != 0):
                throwaway = self.BlueTootPort.read(1)
                        
            while partcbValue() and active:   # main BlueToot loop checking serial port --------------------------
                self.trace = "running"
                
                # check the BlueToot serial port for complete data set and read it into bluestring
                byteswaiting = self.BlueTootPort.inWaiting()  
                if byteswaiting > 8 :     # Sent in groups of 9 characters. 
                    #print "waiting:", byteswaiting,
                    #time0 = pygame.time.get_ticks()
                    bluestring = self.BlueTootPort.read(9)  # #Always read in exactly 9 bytes because that's how data is sent
                    #print bluestring
                    
                    # check to see if the bytes have the proper final character
                    if bluestring[8] != '\n':  # Wrong last byte, so read out all the rest and discard
                        print (bluestring, "is bad")
                        while (self.BlueTootPort.read(1) != '\n'): pass     # read and discard until newline
                        
                    # Good string,so split it into two strings and then reformat those into turnbyte and blowbyte numbers 
                    else:
                        self.trace = "gotstring"
                        blueByteArray = bluestring.split() # parse bluestring into blueByteArray = ['623', '115']
                        #print blueByteArray
                    
                        if len(blueByteArray) != 2:     # Parsed wrong, don't use
                            print ("badly parsed blueByteArray", blueByteArray)
                            
                        else: 
                            turnbyte = int(blueByteArray[0]) - 100   #Subtract 100 which was added to make consistent format
                            blowbyte = int(blueByteArray[1]) - 100
                            #print "bluebytes", turnbyte, blowbyte  #, pygame.time.get_ticks()-time0
                            
                            # Handle the new data in similar fashion to obloe: 
                            self.trace = "gotbyte"
                            #print self.name, "gotbyte", turnbyte, blowbyte
                            rawnote,volume = self.calcRawnoteVolume(turnbyte,blowbyte)
                            self.trace = "rawnoted"
                            note = self.chooseNote(rawnote) 
                            self.trace = "note chosen"  
                            # According to new note and volume, send out midi messages  
                            self.playNote(note,rawnote,volume)
    
# Virtual Class -- Virtual instrument functions. This is a noninstantiated class
class Virtual:
   # This virtual instrument replaces a real physical instrument connected to the eobody.
   # But playing it still uses the Obloe controls created through the Obloe class.
    xylist = []
    pitch = 0
    volch = 0
     
    @staticmethod   # has no self parameter
    def createVirtInst():  # Create a virtual Instrument for use without the Eobody
        win2 = wx.Frame(None, -1, "Virtual obloe", size=(360,300))
        pan2 = wx.Panel(win2)
        wx.StaticText(pan2, -1, "Pitch Eobody  Vol", pos=(40,20))
        
        # Selectors for the Eobody Midi channels it will output pitch and Volume on
        wx.StaticText(pan2, -1, "Move mouse pointer down into gray box to play", pos=(40,80))
        
        pitchsel = wx.SpinCtrl(pan2, -1,  '', (40,40), (40, -1),initial=1)
        Virtual.pitch = pitchsel.GetValue()
        def setpitch(event):
            Virtual.pitch = pitchsel.GetValue()
        pitchsel.Bind(wx.EVT_SPINCTRL, setpitch)
    
        volchsel = wx.SpinCtrl(pan2, -1,  '', (90,40), (40, -1),initial=2)
        Virtual.volch = volchsel.GetValue()
        def setvolch(event):
            Virtual.volch = volchsel.GetValue()
        volchsel.Bind(wx.EVT_SPINCTRL, setvolch)
        
        # Active Touch area that puts data into the xylist acting like a Midi Buffer
        touchpan = wx.Panel(pan2, -1, (40,140), (260,50))
        touchpan.BackgroundColour = (100,100,100)
        def mouseDoer(event):
            x, y = event.GetPosition()
            x= x/2 
            Virtual.xylist.append([[[0,Virtual.pitch,x,0],0]])
            Virtual.xylist.append([[[0,Virtual.volch,y,0],0]])
            #print "mouseDoer",x,y
        touchpan.Bind(wx.EVT_MOUSE_EVENTS, mouseDoer)
        
        win2.Show()
    
    
    class vmidin:   #  Set up a virtual MIDI input from the buffer stack
        
        @staticmethod   # has no self parameter
        def poll():
            nonempty = (len(Virtual.xylist) > 0)
            return nonempty
        
        @staticmethod   # has no self parameter
        def read(number):
            byte = Virtual.xylist.pop(0)  
            #print "vmidinread",byte
            return byte
    

# =================  Runtime execution begins here =========================================

# --------------------------  Create the GUI  ----------------------------------------------
# Color Scheme
COL_BACK = (20,30,90)
COL_PLAY = (100,130,255)
COL_PRACTICE = (180,180,180)
COL_STOP = (100,100,100)
COL_DISABLED = (100,100,100)
COL_ENABLED = (150,180,255)

# Set up the main window
myapp = wx.App(redirect=0)       # 0 = don't redirect errors, use stdout
win = wx.Frame(None, -1, "Musician Maker Main Panel", size=(800,640))
pan = wx.Panel(win)
pan.SetBackgroundColour(COL_BACK)

# Create menubar with File menu for opening and saving the configuration
menubar = wx.MenuBar()
filemenu = wx.Menu()
openmi = filemenu.Append(-1, '&Open\tCtrl+O', 'Open configuration')
savemi = filemenu.Append(-1, '&Save As\tCtrl+S', 'Save configuration')
savedefaultmi = filemenu.Append(-1, 'Save As Default', 'Save as default configuration')
quitmi = filemenu.Append(-1, '&Quit\tCtrl+Q', 'Quit program')
menubar.Append(filemenu, '&File')
win.SetMenuBar(menubar)

win.Bind(wx.EVT_MENU, fileOpen, id = openmi.GetId())
win.Bind(wx.EVT_MENU, fileSave, id = savemi.GetId())
win.Bind(wx.EVT_MENU, fileSaveDefault, id = savedefaultmi.GetId())
win.Bind(wx.EVT_MENU, fileQuit, id = quitmi.GetId())

# Create the top panel for the control buttons and song selector
toppan = wx.Panel(pan, -1, (0,0), (784,80))
toppan.SetBackgroundColour(COL_STOP)

eobodyOK = wx.StaticText(toppan,-1,"No Eobody", (700,10))
rolandOK  = wx.StaticText(toppan,-1,"No Roland", (700,25))

playbutton = wx.ToggleButton(toppan, label='Play', pos=(100,10))
playbutton.Bind(wx.EVT_TOGGLEBUTTON,play)

practicebutton = wx.ToggleButton(toppan, label='Practice', pos=(20,10))
practicebutton.Bind(wx.EVT_TOGGLEBUTTON,practice)

stopbutton = wx.ToggleButton(toppan, label='Stop', pos=(20,40), size=(155,30))
stopbutton.Bind(wx.EVT_TOGGLEBUTTON,stop)

# Create the songpanel showing the current song file and a browse button
songpanel = wx.Panel(toppan, -1, pos=(390,10), size=(220,25))
songpicked = False
songFileCtrl = wx.TextCtrl(songpanel, -1, 'Open a song file', pos=(2,2), size=(150,20))
songFileCtrl.SetEditable(False)
browsebutton = wx.Button(songpanel, -1, 'Browse', pos=(155,0), size=(60,25))
browsebutton.Bind(wx.EVT_BUTTON, songBrowser)

# Create key buttons for manual chord control
chordCbutton = wx.ToggleButton(toppan, label='C', pos=(220,45),size=(25,25))
chordCbutton.Bind(wx.EVT_TOGGLEBUTTON,chordC)

chordDmbutton = wx.ToggleButton(toppan, label='Dm', pos=(260,45),size=(25,25))
chordDmbutton.Bind(wx.EVT_TOGGLEBUTTON,chordDm)

chordGbutton = wx.ToggleButton(toppan, label='G', pos=(300,45),size=(25,25))
chordGbutton.Bind(wx.EVT_TOGGLEBUTTON,chordG)

chordScalebutton = wx.ToggleButton(toppan, label='Scale', pos=(340,45),size=(45,25))
chordScalebutton.Bind(wx.EVT_TOGGLEBUTTON,chordScale)


# Create trace function to show where each thread is
traceButton = wx.ToggleButton(toppan, label='Trace', pos=(700,45),size=(45,25))
def showtrace(event):
    for name,instrument in Instrument.iArray:
        print (name, "is at:", instrument.trace)
    print ("----------")
traceButton.Bind(wx.EVT_TOGGLEBUTTON,showtrace)

# Create a sound test "ding" button
dingButton = wx.Button(toppan, label='Ding', pos=(640,45),size=(35,25))
def ding(event):
    midout.note_on(60, 50, 0)
dingButton.Bind(wx.EVT_BUTTON,ding)

#       more GUI details in Inpart class and in Accomp class

win.Show()  # makes the main window visible

# -----------------------  Start the program  ------------------------------
# Initialize pygame midi module
pygame.midi.init()

# Look for devices and define midin and midout for them
roland = False
eobody = False
deviceCount = pygame.midi.get_count()
for deviceID in range(deviceCount):
    device = pygame.midi.get_device_info(deviceID)
    print(device)
    print(device[1][-5:])
    if device[1][-5:] == b'SD-50' and device[3] == 1:   #-5: gets the last 5 characters. so device can be "3- SD-50" or "SD-50" depending how connected
        midout = pygame.midi.Output(deviceID)         #byte literals start with b'characters'
        roland = True
        rolandOK.SetLabel("Roland OK")
    if device[1] == b'eobody 2' and device[2] == 1:
        midin = pygame.midi.Input(deviceID)
        eobody = True
        eobodyOK.SetLabel("Eobody OK")
       
# If Roland not connected, use sound card instead
if roland == False:
    deviceID = pygame.midi.get_default_output_id()
    midout = pygame.midi.Output(deviceID)
    rolandOK.SetLabel("SoundCard")

# If Eobody not connected, create virtual instrument    
if eobody == False:
    eobodyOK.SetLabel("VirtualEOB")
    Virtual.createVirtInst()
    midin = Virtual.vmidin  
     
# Create the accompaniment, all the instruments, and byteReader
accomp = Accomp("Accompaniment")

sway1 = Sway("Sway n Play","EOB")
obloe1 = Obloe("Obloe1","EOB")
baron1 = Baron("Baronium","EOB")
pluck1 = Pluck("Pluck n Play","EOB")
marim1 = Marim("Marimbar","EOB")
blue1 = Blue("BlueToot","BT")

byteReader = ByteReader()

# Start the threads for each instrument, accomp and byteReader but with active off
active = False
playing = False
threadsAlive = True
readControls(1)
for [name,instrument] in Instrument.iArray:
    instrument.start()   # this starts the thread and then calls the run method
    #print name,   "started"
accomp.start()
byteReader.start()
#print "bytereader started"

# Open the default.mcf file to set things up
readConfig("default.mcf")
stop(1)
chordC(1)
Constraint.setAllScaleNotes("C","major")

# Start looping on the window controls waiting for clicks
myapp.MainLoop()

# attempt to stop everything
playing = False
active = False
threadsAlive = False
print ("dead")
raise SystemExit()


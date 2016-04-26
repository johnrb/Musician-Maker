import wx, re
import wx.lib.scrolledpanel as scrolled
import mmref
 
class Module:
    global ModuleOn
    ModuleOn = False
     
    def __init__(self, instrument, name, theMidout, thePanel):
        volume = 0
        screenWidth = wx.GetDisplaySize().width
        screenHeight = wx.GetDisplaySize().height
        win3 = wx.Frame(None, -1, "Module: " + name, size=(int(screenWidth/4),int(screenHeight/3)),pos=(int(screenWidth-500),400))
        pan3 = scrolled.ScrolledPanel(parent=win3)
         
        box_main = wx.BoxSizer(wx.HORIZONTAL)
        vbox_left = wx.BoxSizer(wx.VERTICAL)
        vbox_right = wx.BoxSizer(wx.VERTICAL)
        
        mod2Toggle = wx.ToggleButton(instrument.partpan, label='Show Mod', pos=(5,25), size=(70,20))         
         
        def practice(event):  # Start instruments without accompaniment song
            # Update the display pane and control buttons
            pan3.SetBackgroundColour((15,200,100))
            pan3.Refresh()
            practicebutton.SetValue(1)
            stopbutton.SetValue(0)
            # initialize instruments and then start them   
#             byteReader.newEobChanArray()
#             readControls(1)
 
        def stop(event):   # Stop instruments and song
            # Update the display pane and control buttons
            pan3.SetBackgroundColour((200,100,15))
            pan3.Refresh()
            practicebutton.SetValue(0)
            stopbutton.SetValue(1)
#             playing = False   # stop the song
#             active = False    # Stop the instruments
#             pygame.time.wait(450)   # Wait to let notes stop gently
#             for ichan in range(0,16):
#                 statusbyte = 0xB0 + ichan
#                 midout.write([[[statusbyte, 123, 0],pygame.midi.time()]]) # Turn all notes off
#             if verbose: print "Stopped"

        def setInstrument(event):
            midi_instrument = int(re.split(" ",instrument.midinst.GetValue())[0])
            theMidout.set_instrument(midi_instrument, instrument.midich.GetValue())
            instrument.midinst.SetValue(mmref.midiname[0])
         
         
#         -----------LEFT BOX----------------
        practicebutton = wx.ToggleButton(pan3, label='Practice')
        practicebutton.Bind(wx.EVT_TOGGLEBUTTON,practice)
        stopbutton = wx.ToggleButton(pan3, label='Stop')
        stopbutton.Bind(wx.EVT_TOGGLEBUTTON,stop)
         
        vbox_left.Add(practicebutton,0,wx.EXPAND | wx.ALL,5)
        vbox_left.Add(stopbutton, 0 ,wx.EXPAND | wx.ALL, 5)
        vbox_left.AddSpacer((20,20))
         
        select_threshold = Selector(pan3, instrument.threshold, "Threshold", vbox_left)
        select_volumefactor = Selector(pan3, instrument.volumefactor, "Vol. Factor", vbox_left)
        select_maxvolume = Selector(pan3, instrument.maxvolume, "Max. Vol.", vbox_left)
        select_pitchfactor = Selector(pan3, instrument.pitchfactor, "Pitch Factor", vbox_left)
         
        vbox_left.AddSpacer((20,20))
              
#         -----------RIGHT BOX----------------
 
        # Create Midi Instrument Selector        
        midinst = wx.ComboBox(pan3, -1, choices=mmref.midiname, pos=(0,0), size=(150,-1), style=wx.CB_READONLY)
        midinst.SetValue(mmref.midiname[0])
        midinst.Bind(wx.EVT_COMBOBOX, setInstrument)   
        vbox_right.Add(midinst,0,wx.EXPAND | wx.ALL, 5)
        vbox_right.AddSpacer((5,10))
         
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.AddSpacer((5,5))
        box1.Add(wx.StaticText(pan3, -1, "Volume: "),0, wx.ALIGN_LEFT,0)
        box1.AddSpacer((5,5))
        vol = wx.StaticText(pan3, -1, str(volume))
        box1.Add(vol,0, wx.ALIGN_LEFT,0)
        box1.AddSpacer((5,5))
        vbox_right.Add(box1,0,wx.ALIGN_CENTER,0)
        vbox_right.AddSpacer((5,10))
         
        box_main.Add(vbox_left, 0 ,wx.EXPAND | wx.ALL, 2)
        box_main.AddSpacer((10,10))
        box_main.Add(vbox_right, 0 ,wx.EXPAND | wx.ALL, 2)
        pan3.SetSizer(box_main)
        pan3.SetupScrolling(False, True, 0, 20, True)
        
        def showMod(self):
            global ModuleOn
            if(ModuleOn == False):
                win3.Show()
                ModuleOn = True
            else:
                win3.Show(False)
                ModuleOn = False
            
        mod2Toggle.Bind(wx.EVT_TOGGLEBUTTON,showMod)
 
         
class Selector:    
    def __init__(self,panel,attribute,label,boxsizer):
        box = wx.BoxSizer(wx.HORIZONTAL)
        select_attr = wx.SpinCtrl(panel, -1,  '', size=(50, -1),max=150,initial=(attribute))
        box.AddSpacer((5,5))
        box.Add(select_attr,0, wx.ALIGN_LEFT,0)
        Selector.attr = select_attr.GetValue()
        def setAttr(event):
            Selector.attr = select_attr.GetValue()
        select_attr.Bind(wx.EVT_SPINCTRL, setAttr)
        box.AddSpacer((5,5))
        box.Add(wx.StaticText(panel, -1, label),0, wx.ALIGN_LEFT,0)
        boxsizer.Add(box,0,wx.ALIGN_LEFT,0)
        boxsizer.AddSpacer((5,10))
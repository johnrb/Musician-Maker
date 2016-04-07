# import wx
# import wx.lib.scrolledpanel as scrolled
# import mmref
# 
# class Module:
#     global ModuleOn
#     ModuleOn = True
#     
#     def __init__(self, instrument, name):
#         volume = 0
#         screenWidth = wx.GetDisplaySize().width
#         screenHeight = wx.GetDisplaySize().height
#         win3 = wx.Frame(None, -1, "Module: " + name, size=(int(screenWidth/4),int(screenHeight/3)),pos=(int(screenWidth-500),400))
# #         pan3 = wx.Panel(win3)
#         pan3 = scrolled.ScrolledPanel(parent=win3)
#         
#         box_main = wx.BoxSizer(wx.HORIZONTAL)
#         vbox_left = wx.BoxSizer(wx.VERTICAL)
#         vbox_right = wx.BoxSizer(wx.VERTICAL)
#         
#         
#         def practice(event):  # Start instruments without accompaniment song
#             # Update the display pane and control buttons
#             pan3.SetBackgroundColour((15,200,100))
#             pan3.Refresh()
#             practicebutton.SetValue(1)
#             stopbutton.SetValue(0)
#             # initialize instruments and then start them   
# #             byteReader.newEobChanArray()
# #             readControls(1)
# 
#         def stop(event):   # Stop instruments and song
#             # Update the display pane and control buttons
#             pan3.SetBackgroundColour((200,100,15))
#             pan3.Refresh()
#             practicebutton.SetValue(0)
#             stopbutton.SetValue(1)
# #             playing = False   # stop the song
# #             active = False    # Stop the instruments
# #             pygame.time.wait(450)   # Wait to let notes stop gently
# #             for ichan in range(0,16):
# #                 statusbyte = 0xB0 + ichan
# #                 midout.write([[[statusbyte, 123, 0],pygame.midi.time()]]) # Turn all notes off
# #             if verbose: print "Stopped"
#         
#         
# #         -----------LEFT BOX----------------
# #         practicebutton = wx.ToggleButton(pan3, label='Practice', pos=(10,10), size=(100,30))
#         practicebutton = wx.ToggleButton(pan3, label='Practice')
#         practicebutton.Bind(wx.EVT_TOGGLEBUTTON,practice)
# #         stopbutton = wx.ToggleButton(pan3, label='Stop', pos=(10,50), size=(100,30))
#         stopbutton = wx.ToggleButton(pan3, label='Stop')
#         stopbutton.Bind(wx.EVT_TOGGLEBUTTON,stop)
#         
#         vbox_left.Add(practicebutton,0,wx.EXPAND | wx.ALL,5)
#         vbox_left.Add(stopbutton, 0 ,wx.EXPAND | wx.ALL, 5)
#         vbox_left.AddSpacer((20,20))
#         
#         select_threshold = Selector(pan3, instrument.threshold, "Threshold", vbox_left)
#         select_volumefactor = Selector(pan3, instrument.volumefactor, "Vol. Factor", vbox_left)
#         select_maxvolume = Selector(pan3, instrument.maxvolume, "Max. Vol.", vbox_left)
#         select_pitchfactor = Selector(pan3, instrument.pitchfactor, "Pitch Factor", vbox_left)
#         
#         vbox_left.AddSpacer((20,20))
#              
# #         -----------RIGHT BOX----------------
# 
#         midinst = wx.ComboBox(pan3, -1, choices=mmref.midiname, pos=(0,0), size=(150,-1), style=wx.CB_READONLY)
#         vbox_right.Add(midinst,0,wx.EXPAND | wx.ALL, 5)
#         vbox_right.AddSpacer((5,10))
#         
#         box1 = wx.BoxSizer(wx.HORIZONTAL)
#         box1.AddSpacer((5,5))
#         box1.Add(wx.StaticText(pan3, -1, "Volume: "),0, wx.ALIGN_LEFT,0)
#         box1.AddSpacer((5,5))
#         vol = wx.StaticText(pan3, -1, str(volume))
#         box1.Add(vol,0, wx.ALIGN_LEFT,0)
#         box1.AddSpacer((5,5))
#         vbox_right.Add(box1,0,wx.ALIGN_CENTER,0)
#         vbox_right.AddSpacer((5,10))
#         
#         testbutton = wx.ToggleButton(pan3, label='Test')
#         vbox_right.Add(testbutton, 0 ,wx.EXPAND | wx.ALL, 5)
# 
# #         text = str(instrument.maxvolume)
# #         wx.StaticText(pan3, -1, text, pos=(120,20))
# #         vbox_left.Add(wx.StaticText(pan3, -1, "Test"))
# #         vbox_left.AddSpacer((100,300))
# #         vbox_left.Add(wx.StaticText(pan3, -1, "Test2"))
# 
# #         pan3.SetSizer(vbox_left)
# #         pan3.SetSizer(vbox_right)
#         box_main.Add(vbox_left, 0 ,wx.EXPAND | wx.ALL, 2)
#         box_main.AddSpacer((10,10))
#         box_main.Add(vbox_right, 0 ,wx.EXPAND | wx.ALL, 2)
#         pan3.SetSizer(box_main)
#         pan3.SetupScrolling(False, True, 0, 20, True)
#         win3.Show()
#         
# #         def buildSelector(attribute,label,pos):
# #             attr = wx.SpinCtrl(pan3, -1,  '', (30,100), (40, -1),initial=(attribute))
# #             Module.attr = attr.GetValue()
# #             def setAttr(event):
# #                 Module.pitch = select_threshold.GetValue()
# #             select_threshold.Bind(wx.EVT_SPINCTRL, setpitch)
#         
# #         select_threshold = wx.SpinCtrl(pan3, -1,  '', (30,100), (40, -1),initial=(instrument.threshold))
# #         Module.pitch = select_threshold.GetValue()
# #         def setpitch(event):
# #             Module.pitch = select_threshold.GetValue()
# #         select_threshold.Bind(wx.EVT_SPINCTRL, setpitch)
# #     
# #         volchsel = wx.SpinCtrl(pan3, -1,  '', (90,40), (40, -1),initial=2)
# #         Module.volch = volchsel.GetValue()
# #         def setvolch(event):
# #             Module.volch = volchsel.GetValue()
# #         volchsel.Bind(wx.EVT_SPINCTRL, setvolch)
# #         
# #         # Active Touch area that puts data into the xylist acting like a Midi Buffer
# #         touchpan = wx.Panel(pan3, -1, (40,140), (260,50))
# #         touchpan.BackgroundColour = (100,100,100)
# #         def mouseDoer(event):
# #             x, y = event.GetPosition()
# #             x= x/2 
# #             Module.xylist.append([[[0,Module.pitch,x,0],0]])
# #             Module.xylist.append([[[0,Module.volch,y,0],0]])
# #             #print "mouseDoer",x,y
# #         touchpan.Bind(wx.EVT_MOUSE_EVENTS, mouseDoer)
#         
# 
#         
# class Selector:    
#     def __init__(self,panel,attribute,label,boxsizer):
#         box = wx.BoxSizer(wx.HORIZONTAL)
#         select_attr = wx.SpinCtrl(panel, -1,  '', size=(50, -1),max=150,initial=(attribute))
#         box.AddSpacer((5,5))
#         box.Add(select_attr,0, wx.ALIGN_LEFT,0)
#         Selector.attr = select_attr.GetValue()
#         def setAttr(event):
#             Selector.attr = select_attr.GetValue()
#         select_attr.Bind(wx.EVT_SPINCTRL, setAttr)
#         box.AddSpacer((5,5))
#         box.Add(wx.StaticText(panel, -1, label),0, wx.ALIGN_LEFT,0)
#         boxsizer.Add(box,0,wx.ALIGN_LEFT,0)
#         boxsizer.AddSpacer((5,10))
#Wezley Mitchell 9/22/2018
#Test code to get analog stick inputs from xbox or other controller using inputs

import inputs

pad = inputs.devices.gamepads

if len(pad) == 0:
    raise Exception("Couldn't find any gamepads!") #if no gamepad is found raise exception

while True:
        events = inputs.get_gamepad() #Get Gamepads
        for event in events:          #cycle through events
            if event.code == 'ABS_Y': #only interested in the Stick1 Y direction
                print(event.state)    #print that state

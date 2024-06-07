#     All commands consist of an identifier, followed by one or more parameters delinieated by commas, then a newline.
#     i.e.:
#     COMMAND,<param1>,<param2><LF>
#     
#     A command will return OK<LF> if successful, and ERROR<LF> if not. Some commands (particuarly transmit commands)
#     may take a significant amount of time to return.
#     
#     Sending a command which takes parameters, without sending the parameters, will return the set parameters.
#     
#     Frequency Settings:
#     
#     FREQ,<freq>     - Set the center freq of the receiver, in Hz.
#     END, 			  - Ends the session.

from machine import Pin
from radio import Radio
import si5351

Pin('WL_GPIO0', Pin.OUT).value(1) # Pico W Power LED
synth = si5351.SI5351( data=Pin(4), clock=Pin(5), addr=0x60 )
frequency = 7000000
band = 1
r = Radio( synth, frequency, band )
r.run()

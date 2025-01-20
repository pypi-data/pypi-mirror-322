# toscinterface
A simple package to receive OSC messages in python sent by TouchOSC. 

Thus far the package contains only one class which instantiates an OscInterface() object.

By calling the start_stream() method, a UDP-socket is initiated 
that listens for incoming OSC messages on the specified port (default: 8000). The stream 
can be blocking or non-blocking (via threading). Received messages are continuously stored 
in the all_responses attribute of the OscInterface object. In theory, OSC messages sent by 
any program or device can be received, but the package is specifically designed around the 
functionalities of TouchOSC and its interfaces. Using this package in a different context
may not work as intended.

Port and IP-Address can be set manually via the attributes of the OscInterface object.

Thus far the package only supports receiving OSC messages. Functionality to send OSC messages
and extend possible interactions with TouchOSC is planned to be implemented in future versions.

Download TouchOSC here: https://hexler.net/touchosc

toscinterface is developed on Windows 11. Compatibility with other operating systems is not 
tested.

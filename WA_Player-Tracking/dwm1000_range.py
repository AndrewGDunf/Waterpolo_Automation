# Decawave DW1000 ranging demo
# Original Code by Jeremy P Bentham
# Copyright (c) Jeremy P Bentham 2019. See iosoft.blog for details

# Andrew Dunford 11/2021
# Code used to help prototype the DWM1000 modules, edited section is the IP and Port Num, added the ability to include a third device

import sys, time
from ctypes import sizeof, LittleEndianStructure as Structure, Union
from ctypes import c_ubyte as U8, c_short as U16, c_ulonglong as U64
from dw1000_regs import Reg, DW1000, msdelay
from dw1000_spi import Spi

VERSION = "0.1"

# Specify SPI interfaces:
#   "UDP", "<IP_ADDR>", <PORT_NUM>
SPIF1       = "UDP", "192.168.100.197", 1401     # entering the pi Zero IP address and the port number the device is listening to 
SPIF2       = "UDP", "192.168.100.241", 1401     # entering the pi 4 IP address and the port number the device is listening to
#SPIF3       = "UDP", "10.1.1.230", 1401

# Blink frame with IEEE EUI-64 tag ID
BLINK_FRAME_CTRL = 0xc5
BLINK_MSG=(('framectrl',   U8),
           ('seqnum',      U8),
           ('tagid',       U64))

MSG_FRAME_CTRL = 0xCC41
MSG_HDR = (('framectrl',   U16),
           ('seqnum',      U8),
           ('panid',       U16),
           ('destaddr',    U64),
           ('srceaddr',    U64))

LIGHT_SPEED = 299702547.0
TSTAMP_SEC  = 1.0 / (128 * 499.2e6)
TSTAMP_DIST = LIGHT_SPEED * TSTAMP_SEC          #timeout code 

# Class to encapsulate a message frame or header with fixed-length fields
class Frame(object):
    def __init__(self, fields, bytes=[]):
        self.fields = fields
        self.seqnum = 1
        class struct(Structure):
            _pack_   = 1
            _fields_ = fields
        class union(Union):
            _fields_ = [("values", struct), ("bytes", U8*sizeof(struct))]
        self.u = union()
        for n, b in enumerate(bytes[0:sizeof(struct)]):
            self.u.bytes[n] = b
        self.bytes, self.values = self.u.bytes, self.u.values

    # Return frame data
    def data(self):                             
        self.values.seqnum = self.seqnum
        self.seqnum += 1
        return list(self.bytes)

    # Return string with field values
    def field_values(self, zeros=True):
        flds = [f[0] for f in self.fields]
        return " ".join([("%s:%x" % (f,getattr(self.values, f))) for f in flds])

if __name__ == "__main__":
    verbose = False
    for arg in sys.argv[1:]:
        if arg.lower() == "-v":
            verbose = True
    spi1 = Spi(SPIF1, '1')
    dw1 = DW1000(spi1)       # module 1 setting spi 1

    spi2 = Spi(SPIF2, '2')
    dw2 = DW1000(spi2)       # module 2 seting spi 2

    #spi3 = Spi(SPIF3, '2')
    #dw3 = DW1000(spi3)      # potential to add in a third module for calibration 

    if verbose:
        spi1.verbose = spi2.verbose = True

    dw1.reset()
    if not dw1.test_irq():
        print("No interrupt from unit 1")
        sys.exit(1)
    dw2.reset()
    if not dw2.test_irq():
        print("No interrupt from unit 2")
        sys.exit(1)
    
    #dw3.reset()
    #if not dw3.test_irq():
    #    print("No interrupt from unit 3")
    #    sys.exit(1)

    dw1.initialise()
    dw2.initialise()
    #dw3.initialise()

    blink1 = Frame(BLINK_MSG)                           #intialising the message packets from dw1 - dw2
    blink1.values.framectrl = BLINK_FRAME_CTRL
    blink1.values.tagid = 0x0101010101010101
    blink2 = Frame(BLINK_MSG)
    blink2.values.framectrl = BLINK_FRAME_CTRL
    blink2.values.tagid = 0x0202020202020202

    errors = count = 0
    while True:
        # Reset devices if 10 concsecutive errors
        errors += 1
        if errors > 10:
            print("Restting")
            dw1.softreset()
            dw1.initialise()
            dw2.softreset()
            dw2.initialise()
            #dw3.softreset()
            #dw3.initialise()
            errors = 0

        # First message                        
        txdata = blink1.data()
        dw2.start_rx()                          # start recieve on 2nd module
        dw1.set_txdata(txdata)                  # send blink1 to set_txdata function (function is in DWm1000_regs.py)
        dw1.start_tx()                          # start to transmit
        rxdata = dw2.get_rxdata()               # reciece 
        if not rxdata:
            print(dw2.sys_status())
            continue
        dw2.clear_irq()

        # Second message
        txdata = blink2.data()                  
        dw1.start_rx()                          # this is the same process as above but this time dw1 is recieving and dw2 is transmitting
        dw2.set_txdata(txdata)
        dw2.start_tx()
        rxdata = dw1.get_rxdata()
        if not rxdata:
            print(dw1.sys_status())
            continue
        dw1.clear_irq()
        dt1 = dw1.rx_time() - dw1.tx_time()             # time taken to transmit a message and then recieve one for the dwm1, this is the total time
        dt2 = dw2.tx_time() - dw2.rx_time()             # time taken to recieve a message and then transmit one for the dwm1, this is the delay time  
        tx1, rx1 = dw1.tx_time(), dw2.rx_time()         # message 1 timestamps used for double sided two way ranging 
        tx2, rx2 = dw2.tx_time(), dw1.rx_time()         # message 2 timestamps used for double sided two way ranging

        # Third message
        txdata = blink1.data()                          # this is the same process as above
        dw2.start_rx()
        dw1.set_txdata(txdata)
        dw1.start_tx()
        rxdata = dw2.get_rxdata()
        if not rxdata:
            print(dw2.sys_status())
            continue
        dw2.clear_irq()

        # Time calculation
        tx3, rx3 = dw1.tx_time(), dw2.rx_time()       # getting the timestamps for the third message
        round1 = rx2 - tx1                            # setting variables for the double sided two way ranging
        round2 = rx3 - tx2
        reply1 = tx2 - rx1
        reply2 = tx3 - rx2
        t1 = ((dt1 - dt2) / 2)                                                                  # single sided two way ranging calculations
        t2 = ((round1 * round2) - (reply1 * reply2)) / (round1 + round2 + reply1 + reply2)      # double sided two way ranging calculations
        print("%7.3f %7.3f" % (t1*TSTAMP_DIST, t2*TSTAMP_DIST))                                 # print the single sided and double sided two way ranging results.
        errors = 0

        # Print message count
        count += 1
        if count%100 == 0:
            sys.stderr.write(str(count) + ' ')
            sys.stderr.flush()
# EOF
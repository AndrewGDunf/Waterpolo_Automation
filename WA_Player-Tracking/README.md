These files are property of Jeremy P Bentham 2019 and were used to prototype the DWM1000 modules. The link to his GitHub is https://github.com/jbentham/uwb and his blog is https://iosoft.blog/2019/11/22/real-time-location-ultra-wideband/

This code was analysised and applied to my hardware. 
The main file is dwm1000_range.py which I have commented how this code works. 
The functions called by this file are presented in dwm1000_regs.py and the SPI set up in dwm1000_spi.py
The code that is uploaded to the pi is spi_server.py which sends the

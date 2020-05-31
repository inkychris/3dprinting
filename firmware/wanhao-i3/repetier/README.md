# Wanhao Duplicator i3 (v2.1) Firmware
This directory contains
custom configured ***AND MODIFIED***
[Repetier](https://github.com/repetier/Repetier-Firmware) firmware.
The configuration used to generate the firmware
can be found at the end of [`Configuration.h`](Configuration.h#L607).
The following modifications were made
to reduce the size of the firmware
in order for it to fit
on the printer's [Atmega1284p](https://www.microchip.com/wwwproducts/en/ATMEGA1284P):
- The logo has been removed from
  the startup splash screen.
  This was done by changing
  the `LOGO_WIDTH` (and `LOGO_HEIGHT`) defines
  in [`logo.h`](logo.h#L7).
- The startup splash screen text
  was modified to display
  "Repetier v1.0.3" in [`ui.cpp`](ui.cpp#L1040).
- The `EEPROM::initalizeUncached()` function in [`Eeprom.cpp`](Eeprom.cpp#L462) 
  was modified to remove calls to set EEPROM values for
  z-probing and axis-compensation features.

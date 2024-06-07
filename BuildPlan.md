## Walla Walla University ENGR357 Board Bring-up Plan Winter 2024

### Build Plan
- Wind inductors for band-pass filters and IF filters in addition to the transformer and measure inductance
- Solder BNC, 3.5mm audio jack, Raspberry Pi Pico W, crystal, inductors, and transformer
- Flash firmware to Pico W
- *Test ADC (Stretch Goal)*

### Testing Proceedure
- Check that PWR and GND planes are not connected X
- Continuity checks X
- Check LDO X
- Test functionality of Si5351 programmable oscillator by programming with Pico and measuring clocks directly from test points
- Test the selectable filter switches X
- Test Tayloe detector functionality by driving mux with the Si5351 and supplying a tone from a signal generator as the RF input through bypass capacitor
- Test the IF filtering and gain of the Tayloe detector and subsequent stages by sweeping the frequency of the signal generator
- Test the frequency response of the two BPFs and the BPF before the AM mixer
- Test quisk control
- Check for ground loops
- Test the frequency response of the crystal filter
- Test the AM switching mixer in a similar manner to the Tayloe detector
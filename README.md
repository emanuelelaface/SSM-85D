# SSM-85D

**Yaesu SSM-85D Raspberry Pi Remote Interface**

This is an interface that allows a Raspberry Pi to emulate an SSM-85D microphone in order to remotely control radios like the Yaesu FTM-150, which do not have a built-in CAT remote controller.

The microphone’s electronics are quite simple: each button activates a resistor with specific values (0, 27, 39, 82, or 220 kΩ) on two wires.
For example, when button "1" is pressed, wire SW1 sees 0 Ω and wire SW2 sees 27 kΩ.
If button "0" is pressed, SW1 sees 27 + 39 + 82 kΩ, and SW2 sees 27 + 39 kΩ.

The idea is to use a digital potentiometer that can reproduce these resistor values programmatically. A good option is the **AD5204**, which provides a simple SPI interface to control four resistors between 0 and 100 kΩ. By combining the four channels, it's possible to create any value up to 400 kΩ, which is sufficient, as the highest needed value is 27 + 39 + 82 + 220 = 368 kΩ.

Two AD5204 chips are needed to control the two lines independently. As shown in the diagram, both AD5204s are connected to the Raspberry Pi’s SPI hardware interface (a Raspberry Pi Zero is shown, but any model should work). The CS (Chip Select) pins are connected to two separate SPI channels, allowing the Pi to switch between the potentiometers.

The software sets the appropriate resistance values for each button press. The user interface is a basic keypad implemented using **NiceGUI**.
Ensure that the SPI interface is enabled via `raspi-config`, so it's active at boot time.

from time import sleep
import spidev
from nicegui import ui

# SPI initializer
def init_spi(device):
    spi = spidev.SpiDev()
    spi.open(0, device)
    spi.max_speed_hz = 1_000_000
    spi.mode = 0b00
    return spi

# Resistor value set
def set_R(device, val):
    setpoint = int(val/100*64)
    for i in range(4):
        device.xfer2([i, setpoint])

# Resistos values for each button
def push_button(sw1, sw2, button):
    match button:
        case '1':   set_R(sw1,0);             set_R(sw2,27)
        case '2':   set_R(sw1,0);             set_R(sw2,27+39)
        case '3':   set_R(sw1,0);             set_R(sw2,27+39+82)
        case '4':   set_R(sw1,27);            set_R(sw2,27)
        case '5':   set_R(sw1,27);            set_R(sw2,27+39)
        case '6':   set_R(sw1,27);            set_R(sw2,27+39+82)
        case '7':   set_R(sw1,27+39);         set_R(sw2,27)
        case '8':   set_R(sw1,27+39);         set_R(sw2,27+39)
        case '9':   set_R(sw1,27+39);         set_R(sw2,27+39+82)
        case '0':   set_R(sw1,27+39+82);      set_R(sw2,27+39)
        case 'A':   set_R(sw1,0);             set_R(sw2,27+39+82+220)
        case 'B':   set_R(sw1,27);            set_R(sw2,27+39+82+220)
        case 'C':   set_R(sw1,27+39);         set_R(sw2,27+39+82+220)
        case 'D':   set_R(sw1,27+39+82);      set_R(sw2,27+39+82+220)
        case '*':   set_R(sw1,27+39+82);      set_R(sw2,27)
        case '#':   set_R(sw1,27+39+82);      set_R(sw2,27+39+82)
        case 'P1':  set_R(sw1,27+39+82+220);  set_R(sw2,27)
        case 'P2':  set_R(sw1,27+39+82+220);  set_R(sw2,27+39)
        case 'P3':  set_R(sw1,27+39+82+220);  set_R(sw2,27+39+82)
        case 'P4':  set_R(sw1,27+39+82+220);  set_R(sw2,27+39+82+220)
        case 'UP':  set_R(sw1,27);            set_R(sw2,0)
        case 'DOWN':set_R(sw1,27+39);         set_R(sw2,0)
        case 'MUTE':set_R(sw1,27+39+82+220);  set_R(sw2,0)
        case _:
            set_R(sw1,400); set_R(sw2,400)
    sleep(0.1)
    # ripristino
    set_R(sw1,400); set_R(sw2,400)
    sleep(0.1)

# Initialize the two SPI
sw1 = init_spi(0)
sw2 = init_spi(1)

# GUI layout
layout = [
    ['UP','DOWN','','MUTE'],
    ['1','2','3','A'],
    ['4','5','6','B'],
    ['7','8','9','C'],
    ['*','0','#','D'],
    ['P1','P2','P3','P4']
]

# Create the page
@ui.page('/')
def keyboard_page():
    ui.markdown('## Yaesu SSM-85D Emulator')
    with ui.grid(columns=4).style('gap: 10px;'):
        for row in layout:
            for label in row:
                if label:
                    ui.button(label, on_click=lambda l=label: push_button(sw1, sw2, l)) \
                      .style('width: 60px; height: 60px; font-size: 1.2em;')
                else:
                    ui.element('div').style('width: 60px; height: 60px;')

ui.run(title='Yaesu SSM-85D Emulator', port=5002)

# Grove - 16x2 LCD(White on Blue) connected to I2C port

from grove.display.jhd1802 import JHD1802


def get_displayed_text():
    return "dupa"

def set_displayed_text(text):
    lcd = JHD1802()
    lcd.setCursor(0, 0)
    lcd.write(text)
    return
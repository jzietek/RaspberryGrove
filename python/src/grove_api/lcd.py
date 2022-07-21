# Grove - 16x2 LCD(White on Blue) connected to I2C port

from grove.display.jhd1802 import JHD1802

current_lcd_text = ""
current_cursor_row = 0
current_cursor_column = 0

def get_displayed_text():        
    global current_lcd_text
    return current_lcd_text

def set_displayed_text(row, column, text):        
    global current_lcd_text
    global current_cursor_column
    global current_cursor_row
    current_lcd_text = text
    current_cursor_column = column
    current_cursor_row = row
    
    lcd = JHD1802()    
    lcd.setCursor(row, column)
    lcd.write(text)    
    print("Set LCD display text to {} on row {} and column {}".format(text, row, column))
    return

def clear_displayed_text():
    global current_lcd_text
    global current_cursor_column
    global current_cursor_row
    current_lcd_text = ""
    current_cursor_column = 0
    current_cursor_row = 0
    lcd = JHD1802()
    lcd.clear()        
    print("Cleared LCD display text and cursor position")
    return

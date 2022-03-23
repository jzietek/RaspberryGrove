# app.py
from cgitb import text
import re
from flask import Flask, request, jsonify
from grove_api import lcd

app = Flask(__name__)

@app.get("/lcd")
def get_lcd_text():
    return jsonify(lcd.get_displayed_text())


@app.post("/lcd")
def update_lcd_text():
    if request.is_json:
        request_json = request.get_json()
        cursor_row = request_json["cursorRow"]
        cursor_column = request_json["cursorColumn"]
        text = request_json["text"]
        lcd.set_displayed_text(cursor_row, cursor_column, text)
        return request_json, 201
    return {"error": "Request must be JSON"}, 415


@app.delete("/lcd")
def delete_lcd_text():
    lcd.clear_displayed_text()
    return "LCD content cleared"
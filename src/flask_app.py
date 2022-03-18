# app.py
from flask import Flask, request, jsonify
from grove_api import lcd

app = Flask(__name__)

@app.get("/lcd")
def get_lcd_displayed_text():
    return jsonify(lcd.get_displayed_text())

@app.post("/lcd")
def update_lcd_content():
    if request.is_json:
        request_json = request.get_json()
        lcd.set_displayed_text(request_json["content"])
        return 201
    return {"error": "Request must be JSON"}, 415

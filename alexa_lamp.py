import os, sys, time
import RPi.GPIO as gpio
from flask import Flask, render_template, request, redirect, url_for
from flask_ask import Ask, statement, question, session

# init flask and ask objects
app = Flask(__name__)
ask = Ask(app, '/')

# gpio settings
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.cleanup()

on = False
off = True

# gpio BCM-17
pin = 11
gpio.setup(pin, gpio.OUT)
gpio.output(pin, off)

@app.route('/')
def index():
    return render_template("lamp.html")


@app.route('/on/', methods = ['GET', 'POST'])
def onButton():
    if request.method == 'POST':
        gpio.output(pin, on)

    return redirect('/')

@app.route('/off/', methods = ['GET', 'POST'])
def offButton():
    if request.method == 'POST':
        gpio.output(pin, off)

    return redirect('/')

@ask.launch
def start():
    return question("on or off?")

@ask.intent("OnIntent")
def turnOn():
    gpio.output(pin, on)
    return statement("Lamp is on")

@ask.intent("OffIntent")
def turnOff():
    gpio.output(pin, off)
    return statement("Lamp is off")

if __name__ == "__main__":
    app.run(debug=False)




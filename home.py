from flask import Flask, render_template, request
import datetime
import requests
import json
import serial

bluetoothSerial = serial.Serial( "/dev/rfcomm0", baudrate=9600 )

app = Flask(__name__)
@app.route("/", methods=['GET'])
def hello():
    temperature = "N/A"
    humidity = "N/A"
    rain = "N/A"

    bluetoothSerial.write(bytes('get', 'ascii'))
    info = bluetoothSerial.readline().decode('ascii') # H:62.80;T:25.00;R:N
    infoDetails = info.split(';')
    humidity = infoDetails[0].split(':')[1]
    temperature = infoDetails[1].split(':')[1]
    rainDrops = infoDetails[2].split(':')[1]
    drying = infoDetails[3].split(':')[1]

    templateData = {
        'temperature' : temperature,
        'humidity' : humidity,
        'rainDrops' : rainDrops,
        'drying': drying
    }

    return render_template('info.json', **templateData)

@app.route("/on", methods=['GET'])
def on():
    bluetoothSerial.write(bytes('on', 'ascii'))
    return '', 204

@app.route("/off", methods=['GET'])
def of():
    bluetoothSerial.write(bytes('off', 'ascii'))
    return '', 204

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)

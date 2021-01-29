  #!/usr/bin/python
import MySQLdb, adafruit_dht, datetime, time, board

dhtDevice = adafruit_dht.DHT22(board.D18)
db = MySQLdb.connect(host='ryzen.ddns.net',user='timelapse', passwd='9_7b:r%HR-G%y@*U;>*3KDrU!-v,65U]Wq6H.xT5G}uiPAE}8k', db='timelapse')

# humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

try:
    # Print the values to the serial port
    temperature = dhtDevice.temperature
    humidity = dhtDevice.humidity
    print(
        "Température: {:.1f}°C    Humidité: {}% ".format(
            temperature, humidity
        )
    )

except RuntimeError as error:
    # Errors happen fairly often, DHT's are hard to read, just keep going
    print(error.args[0])
    time.sleep(2.0)
except Exception as error:
    dhtDevice.exit()
    raise error

dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

if humidity is not None and humidity >= 0.0 and humidity <= 100.0 and temperature is not None and temperature > -100.0 and temperature < 150.0:
    cur = db.cursor()
    cur.execute("INSERT INTO mesures(id_capteur, temperature, humidity, date) VALUES ('2'," + str(temperature) + "," + str(humidity) + ",'" + dt + "')")
    db.commit()
    cur.close()
    del cur
    db.close()
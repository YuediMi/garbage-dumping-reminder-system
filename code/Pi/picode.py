#!/usr/bin/env python

import pymongo
import bme680
import RPi.GPIO as GPIO
# import paho.mqtt.client as mqtt
import time
import pymysql
import joblib
import numpy as np
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(17, GPIO.OUT)

detecttime=0
timerange=60
print("""read-all.py - Displays temperature, pressure, humidity, and gas.

Press Ctrl+C to exit!

""")

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These calibration data can safely be commented
# out, if desired.

print('Calibration data:')
for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

        if isinstance(value, int):
            print('{}: {}'.format(name, value))

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

print('\n\nInitial reading:')
for name in dir(sensor.data):
    value = getattr(sensor.data, name)

    if not name.startswith('_'):
        print('{}: {}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)


# host = '192.168.1.18'
# port = 1883
# keepalive = 60
# topic = 'pi'

# client = mqtt.Client()
# client.connect(host,port,keepalive)
# client.publish(topic,'This is a message form pi.')
# client.disconnect()


def distance():
    GPIO.output(GPIO_TRIGGER, False) 
    time.sleep(0.000002)
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    ii = 0
    while GPIO.input(GPIO_ECHO) == 0:
        ii = ii + 1
        if ii > 10000: 
            print('Ultrasound error: the sensor missed the echo')
            return 0
        pass

    start_time = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        pass

    stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2

    return distance


# def getiaq():
#     # if sensor.get_sensor_data():
#     #     output = '{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH'.format(
#     #     sensor.data.temperature,
#     #     sensor.data.pressure,
#     #     sensor.data.humidity)

#     # if sensor.data.heat_stable:
#     #     print('{0},{1} Ohms'.format(
#     #         output,
#     #         sensor.data.gas_resistance))

#     # else:
#     #     print(output)
#     x = np.array([sensor.data.pressure*100,sensor.data.gas_resistance*10,sensor.data.temperature,sensor.data.humidity])
#     load_model = joblib.load("rfrmodel.dat")
#     y = load_model.predict(x.reshape(1,-1))
#     return y



try:
    while True:
        y=0
        if sensor.get_sensor_data():
            output = '{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH'.format(
                sensor.data.temperature,
                sensor.data.pressure,
                sensor.data.humidity)

            if sensor.data.heat_stable:
                print('{0},{1} Ohms'.format(
                    output,
                    sensor.data.gas_resistance))

            else:
                print(output)
            x = np.array([sensor.data.pressure*100,sensor.data.gas_resistance*10,sensor.data.temperature,sensor.data.humidity])
            # start1 = time.time()
            # load_model = joblib.load("knn.dat")
            # load_model = joblib.load("lrmodel.dat")
            # load_model = joblib.load("nnr.dat")
            # load_model = joblib.load("dtr.dat")
            # load_model = joblib.load("extratree.dat")
            # load_model = joblib.load("gradientboosting.dat")
            load_model = joblib.load("adaboost.dat")
            # load_model = joblib.load("bagging.dat")
            y = load_model.predict(x.reshape(1,-1))
            # end1 = time.time()
            # print("model time:",end1-start1)
            # print(y)
        # iaq = getiaq()
        dist = distance()
        height = (30-dist)/30*100
        print(y,height)
        if (y>200 or height>70):
            GPIO.output(17, True)
        if (y<=200 and height<=70):
            GPIO.output(17, False)
        start2 = time.time()
        db = pymysql.connect(host='3.145.215.29', user='xhy', password='root', port=3306, database='trashbin')
        cursor = db.cursor()
        insertsql = "insert into trashinfo(trashid, iaq, height) values(%s,%s,%s)"
        cursor.execute(insertsql, (1,'%.2f' %y, height))
        db.commit()
        results = cursor.fetchall()
        print(results)
        cursor.close()
        db.close()
        end2 = time.time()
        print(end2-start2)
        


        # start2 = time.time()
        # client = pymongo.MongoClient("mongodb+srv://Luka:root@creativeproject.uee95.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # db = client.Realtime
        # infodb = db.info
        # infodb.update_one({'infoname': "iaq"}, {'$set': {'val': '%.2f' %y}})
        # infodb.update_one({'infoname': "height"}, {'$set': {'val': height}})
        # end2 = time.time()
        # print("database time:",end2-start2)


        time.sleep(1)
        # print("Measured Distance = {:.2f} cm".format(dist))
        # if dist<50.0:
        #     detecttime+=1
        #     if detecttime==12:
        #         client = mqtt.Client()
        #         client.connect(host,port,keepalive)
        #         client.publish(topic,'Trash can is full')
        #         client.disconnect()
        #         GPIO.output(17, True)
        #         time.sleep(5)
        #         GPIO.output(17, False)
        #         detecttime=0
        # else:
        #     detecttime = 0
            # else:
            #     time.sleep(5)
            #     print('{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH, {0},{1} Ohms'.format(
            #     sensor.data.temperature,
            #     sensor.data.pressure,
            #     sensor.data.humidity,
            #     sensor.data.gas_resistance),distance())

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()

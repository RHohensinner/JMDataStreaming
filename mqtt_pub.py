#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import serial

topic_dict = \
{"T1":"JM/container/alpha/sensor/temp", "P1":"JM/container/alpha/sensor/pH", "D1":"JM/container/alpha/sensor/depth", 
 "T2":"JM/container/beta/sensor/temp", "P2":"JM/container/beta/sensor/pH", "D2":"JM/container/beta/sensor/depth", 
 "T3":"JM/container/charlie/sensor/temp", "P3":"JM/container/charlie/sensor/pH", "D3":"JM/container/charlie/sensor/depth", 
 "T4":"JM/container/delta/sensor/temp", "P4":"JM/container/delta/sensor/pH", "D4":"JM/container/delta/sensor/depth", 
 "T5":"JM/container/echo/sensor/temp", "P5":"JM/container/echo/sensor/pH", "D5":"JM/container/echo/sensor/depth", 
 "T6":"JM/container/foxtrot/sensor/temp", "P6":"JM/container/foxtrot/sensor/pH", "D6":"JM/container/foxtrot/sensor/depth"}
 
client = mqtt.Client()
client.connect("0.0.0.0",1883,60)
client.publish("topic/test", "Hello World!")
client.publish("api", "BCtpMsuS_fYOXdb8Cgv0f6AbGhRfo5HjG_1cOIXKKwAAl8Nfdw1AEH_pqW2afmgOjp3iBtz1rlzVW-OEbw3SNw==")


import serial
if __name__ == '__main__':
    print("Publishing values to: \nmqtt://localhost:1883 \nTopic: \"JM/123456\"\n...")
    ser1 = serial.Serial('/dev/ttyACM0', 115000, timeout=5)
    ser1.reset_input_buffer()
    ser2 = serial.Serial('/dev/ttyACM1', 115000, timeout=5)
    ser2.reset_input_buffer()
    line1 = ""
    line2 = ""
    while True:
        if ser1.in_waiting > 0:
            line1 = ser1.readline().decode('utf-8').rstrip()
            #print(line1)
            if len(line1) >= 2:
                if line1[:2] in topic_dict.keys():
                    client.publish(topic_dict[line1[:2]], line1[3:(len(line1)-1)])
            if line1 == "-" or line1[:2] == "ID":
                continue
            client.publish("JM/123456", line1)
        if ser2.in_waiting > 0:
            line2 = ser2.readline().decode('utf-8').rstrip()
            tmp = list(line2)
            try:
                    if len(line2) >= 2:
                        if line2[1] == "1":
                                tmp[1] = "4"
                                
                        if line2[1] == "2":
                                tmp[1] = "5"
                        
                        if line2[1] == "3":
                                tmp[1] = "6"
            except:
                        print("err")
            line2 = "".join(tmp)
            # print(line2)
            if len(line2) >= 2:
                if line2[:2] in topic_dict.keys():
                    client.publish(topic_dict[line2[:2]], line2[3:(len(line2)-1)])
            if line2 == "-" or line2[:2] == "ID":
                continue
            client.publish("JM/123456", line2)


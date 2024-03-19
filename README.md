# Juice Mixer Data Streaming

![Alt text](/jm.jpg)

## MQTT - Sensor Data Broadcasting
Currently each of the 6 (juice) containers is equiped with 3 sensors each. 
A **temperature sensor**, a **depth sensor** and a **pH-value sensor**. A broker, which is
running on the juice mixer's raspberry pi broadcasts the sensor values in fixed intervals 
to dedicated sensor topics. The MQTT broker is available at "192.168.1.107:1883" within the juice mixer's
"VR Lab" wifi-network.

### Topics

- **JM/123456** (all-in-one)

Broadcasts all available data of every sensor in one topic with a given syntax: 

**<sensor-type><container-id>[\<value\>]**

sensor-type => (T... Temperature, P... pH-value, D... Depth)

container-id => (1, 2, 3, 4, 5, 6)

As an example: **T3[10.3]** provides the temperature value ("T") of container three ("3") with a
float value of 10.3 (degrees).

- **wild-cards** (individual sensors & containers)

These topics provide available data for a particular sensor of a chosen container with the given topic syntax:

**JM/container/<container-name>/sensor/<sensor-type>**

container-name => (alpha, beta, charlie, delta, echo, foxtrot)

sensor-type => (temp... Temperature, pH... pH-value, depth... Depth)

As an example: subscribing to the topic **JM/container/beta/sensor/temp** will receive all temperature values
of container number 3 (=charlie) in float format.

## InfluxDB (v2.0) 

![Alt text](/jm_database.png)

The juice mixer is also equipped with a InfluxDB (2.0) to store (and retrieve) historical sensor data.
InfluxDB was installed and set up via this [guide](https://pimylifeup.com/raspberry-pi-influxdb/) on the raspberry pi.
The database is available at "192.168.1.107:8086" within the juice mixer's "VR Lab" wifi-network.

## Data Storing

Via an additional python script and the MQTT-broker (see above) the database automatically gets filled
with all available sensor data (as long as the MQTT-Topics get published to). For this a 
dedicated 'Bucket' was created within the data base called "Sensors". Inside of this Bucket
_measurements for the sensors are stored as "sensor_measurements" and can be filtered further by
"_field" (sensor types) as well as "container" (container names).

## Data Retrieval

For Data Retrieval and Evaluation the InfluxDB (v2) provides a web application as well as an
api which can be found [here](https://docs.influxdata.com/influxdb/v2/api/).


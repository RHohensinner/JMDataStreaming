from paho.mqtt import client as mqtt_client
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

### MQTT
#broker = '192.168.1.107'
broker = 'localhost'
port = 1883
topic = "JM/123456"

client_id = f'subscribe-69'

# username = 'emqx'
# password = 'public'

### InfluxDB
bucket = "Sensors"
org = "Know Center"
#url="http://192.168.1.107:8086"
url="http://localhost:8086"
token = "BCtpMsuS_fYOXdb8Cgv0f6AbGhRfo5HjG_1cOIXKKwAAl8Nfdw1AEH_pqW2afmgOjp3iBtz1rlzVW-OEbw3SNw=="

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

c_dict = {"1":"alpha", "2":"beta", "3":"charlie", "4":"delta", "5":"echo", "6":"foxtrot"}
s_dict = {"T":"temp", "P":"pH", "D":"depth"}

# Write script
write_api = client.write_api(write_options=SYNCHRONOUS)


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):

        message = msg.payload.decode()
        if len(message) >= 2:
            if message[0] in s_dict.keys() and message[1] in c_dict.keys():
                write_api.write(bucket=bucket,
                                org=org,
                                record=influxdb_client.Point("sensor_measurements").tag("container", c_dict[message[1]]).field(
                                    s_dict[message[0]], float(message[3:(len(message)-1)])))
                #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()

import argparse

from pythonosc import osc_message_builder
from pythonosc import udp_client

port_num = 8000

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="localhost", help="The ip of th OSC Server")
parser.add_argument("--port", type=int, default=port_num, help="The port the OSC server is listening on")
args = parser.parse_args()
client = udp_client.UDPClient(args.ip, args.port)

print("ip:localhost, port:" + str(port_num) + ", address:/data")

def sendString(add, m):
    msg = osc_message_builder.OscMessageBuilder(address = add)
    msg.add_arg(m)
    print(m)
    msg = msg.build()
    client.send(msg)

def sendList(add, li):
    msg = osc_message_builder.OscMessageBuilder(address = add)
    for i in li:
        msg.add_arg(i)
        print(i)
    msg = msg.build()
    client.send(msg)

if __name__ == "__main__":
    while True:
        input_str = input()
        sendString("/data", input_str)

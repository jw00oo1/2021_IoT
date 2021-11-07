import bluetooth


#after paring
target_name = "Galaxy Note8"
target_address = None

nearby_devices = bluetooth.discover_devices()

for bd_addr in nearby_devices:
    #print(bluetooth.lookup_name(bd_addr))
    if target_name == bluetooth.lookup_name(bd_addr):
        target_address = bd_addr
        break

if target_address is not None:
    print("found target bluetooth device with address ", target_address)
else:
    print("could not find target bluetooth device nearby")

port = 4

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

server_sock.bind(("",port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print("Accepted connection from ",address)

data = client_sock.recv(1024)
print("received [%s]" % data)

client_sock.close()
server_sock.close()
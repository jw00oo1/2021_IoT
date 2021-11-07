# pybluez library
import bluetooth
import sys
import numpy as np
from matplotlib import pyplot as plt
import time
import pyautogui as gui
#import real_time_plot1.rt_plot
gui.FAILSAFE = False

server_socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
client_sockets = []

server_socket.bind(("",bluetooth.PORT_ANY))
port = server_socket.getsockname()[1]
uuid = "00001117-0000-1000-8000-00805F9B34FB"

print("Listening for devices...")

# advertise service
server_socket.listen(1)
bluetooth.advertise_service( server_socket, "Validation Host",
    service_id = uuid,
    service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
    profiles = [ bluetooth.SERIAL_PORT_PROFILE ],
)

one = []
two = []
# accept incoming connections
client_sock, client_info = server_socket.accept()
print("Server Connection!")
ACK = "ack".encode('utf-8')
# data = client_sock.recv(34)
# print(data)
# print(sys.getsizeof(data))

# interval = 50
# plt.axis([0, interval, -10,10])
# plt.ion()
# plt.show()
t = np.array([0])
distx, disty = 0, 0
accx_pre, accy_pre = 0, 0
c_time, b_time = 0, time.time()
vx_pre, vy_pre, vx_now, vy_now = 0, 0, 0, 0
x_history = np.array([0])
y_history = np.array([0])
start = 1
threshold = 0.03
dpi = 1000

# fig, ax = plt.subplots(2,1)

def init_var(var1, var2=None):
    if abs(var1) < threshold:
        var1 = 0
    if var2 and abs(var2) < threshold:
        var2 = 0
    return (var1, var2) if var2 is not None else var1

if __name__ == '__main__':
    screenWidth, screenHeight = gui.size()

    while True:
        try:
            data = client_sock.recv(1024) #CRASHES HERE
            # print(type(data))

            if data.decode('utf-8') == "0":
                print("Socket End")
                break
            elif data.decode('utf-8') == '1':
                one.append(1)
                client_sock.send(ACK)
            else:
                two.append(2)
                client_sock.send(ACK)
            
            #헤더로 데이터 분리 (가속도 or 중력가속도)
            string_list = data.split()
            data_type = string_list[0].decode()[0]

            #if get accelation data...
            if data_type == 'a':
                x_acc = (float)(string_list[0].decode()[1:])
                y_acc = (float)(string_list[1].decode()[1:])
                c_time = time.time()                
                
                t_interval = (c_time - b_time) / 1000

                vx_now = vx_pre + t_interval*(x_acc + accx_pre) / 2
                vy_now = vy_pre + t_interval*(y_acc + accy_pre) / 2
                #acc 값도 작고 velocity 값도 threshold보다 작으면 0으로 초기화
                #acc 값이 어느정도 존재하면 초기화하면 안 됌
                if x_acc == 0:
                    vx_now = init_var(vx_now)
                if y_acc == 0:
                    vy_now = init_var(vy_now)

                #dist = cm
                distx += (t_interval*(vx_pre + vx_now) / 2) * 100
                disty += (t_interval*(vy_pre + vy_now) / 2) * 100
                if vx_now == 0:
                    distx = init_var(distx)
                if vy_now == 0:
                    disty = init_var(disty)

                print("accx : {:f}, accy : {:f}, vx : {:f}, vy : {:f}".format(x_acc, y_acc, vx_now, vy_now))

                #cm to pixel 
                pixelx = distx * dpi / 2.54 * 10
                pixely = disty * dpi / 2.54 * 10

                print("time : {:f}, x : {:f} {:f}, y : {:f} {:f}\n".format(t_interval, distx, pixelx, disty, pixely))
                gui.move(int(pixelx),int(pixely))
                
                #print(x_acc, y_acc)


                b_time, vx_pre, vy_pre, accx_pre, accy_pre = c_time, vx_now, vy_now, x_acc, y_acc

            # x_acc = (float)(string_list[0].decode())
            # y_acc = (float)(string_list[1].decode())
            # print(x_acc, y_acc, sep=" ")

            # if abs(x_acc) < threshold:
            #     x_acc = 0
            # if abs(y_acc) < threshold:
            #     y_acc = 0

            # t = np.append(t, t[-1]+1)
            # x_history = np.append(x_history, x_acc)
            # y_history = np.append(y_history, y_acc)
            
            # ax[0].plot(t, x_history, color='b')
            # # ax[0].subtitle('x value')

            # ax[1].plot(t, y_history, color='r')
            # # ax[1].title('y value')
            # plt.draw()
            # plt.pause(0.001)
            # if len(t) > interval:
            #     x_history = x_history[1:]
            #     y_history = y_history[1:]
            #     t = t[1:]
            #     ax[0].axis([t[0], t[-1]+1,-10,10])
            #     ax[1].axis([t[0], t[-1]+1, -10, 10])
        
        except KeyboardInterrupt:
        # Ctrl+C 입력시 예외 발생
            sys.exit() #종료

    client_sock.close()
    server_socket.close()
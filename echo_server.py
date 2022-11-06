import json
from socket import *

HOST = '172.16.11.31'  # внутренний служебный адрес текущей машины
PORT = 65485        # любой свободный порт
addr = (HOST,PORT)
udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(addr)
users = []
def xod(n,m):
    while users[m]['broken'] != 20:
        udp_socket.sendto('Стреляй'.encode(), users[n]['addr'])
        data, addr = udp_socket.recvfrom(1024)
        coord = json.loads(data)
        coordx, coordy = coord
        if users[m]['map'][coordx][coordy] == 0 or users[m]['map'][coordx][coordy] == '●' or users[m]['map'][coordx][coordy] == '▪':
            udp_socket.sendto('0'.encode(), users[n]['addr'])
            users[m]['map'][coordx][coordy] = '▪'
            j = json.dumps(users[m]['map'])
            udp_socket.sendto('2'.encode(), users[m]['addr'])
            udp_socket.sendto(j.encode(), users[m]['addr'])
            return 1
        else:
            users[m]['broken'] += 1
            users[m]['map'][coordx][coordy] = '●'
            udp_socket.sendto('1'.encode(), users[n]['addr'])
            j = json.dumps(users[m]['map'])
            udp_socket.sendto('2'.encode(), users[m]['addr'])
            udp_socket.sendto(j.encode(), users[m]['addr'])
    else:
        udp_socket.sendto('Проиграл'.encode(),users[m]['addr'])
        udp_socket.sendto('Победа'.encode(), users[n]['addr'])
        exit()


while True:
    if (question := input('Do you want to quit? y or n')) == 'y':
        break
    while len(users) < 2:
        data, addr = udp_socket.recvfrom(1024)
        a = json.loads(data)
        user = {
            'addr':addr,
            'map': a,
            'broken': 0
        }
        if users:
            if users[0]['addr'] != addr:
                users.append(user)
        else:
            users.append(user)
    while xod(0,1) and xod(1,0):
        pass




    '''print('wait data...')
    print('message received by the server', data)
    print('client addr: ', addr)
    print(a)'''

    #udp_socket.sendto(data, addr)

udp_socket.close()


import socket

addr=('',51423)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(addr)

while True:
    data,addr=s.recvfrom(2048)
    print(data)
    if data=='bye':
        print('client has exit')
        break
    print('received:',data," from",addr)
s.close()
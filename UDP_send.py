import socket

s = socket.socket()
host = '192.168.50.231' #ip of raspberry pi
port = 12345
s.bind((host, port))

s.listen(5)
while True:
  c, addr = s.accept()
  print ('Got connection from',addr)
  c.send('Hello There!')
  c.close()

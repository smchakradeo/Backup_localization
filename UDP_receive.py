import socket

s = socket.socket()
host = '127.0.0.1' #ip of raspberry pi
port = 12345
s.bind((host, port))

s.listen(5)
while True:
  c, addr = s.accept()
  #print ('Got connection from',addr)
  c.send('Thank you for connecting')
  c.close()

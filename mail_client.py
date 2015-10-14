# required libraries
from socket import *
import sys

# message to be sent
msg = '\r\nThe arc of the moral universe is long, but it bends towards justice'
endmsg = '\r\n.\r\n'

# define BU mail server
mailserver = ("smtp.bu.edu", 587)

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

# get initial data buffer
data = clientSocket.recv(1024)
print data

# check for 220 server response
if data[:3] != '220':
	print '220 reply not received from server.'
 	sys.exit(1)

# send HELO command
heloCommand = 'HELO Mark\r\n'
clientSocket.send(heloCommand)
# receive and print the server's response
data1 = clientSocket.recv(1024)
print data1

# check for 250 server response
if data1[:3] != '250':
	print '250 reply not received from server.'
	sys.exit(1)

# send FROM command
fromCommand = 'MAIL From: barrasso@bu.edu\r\n'
clientSocket.send(fromCommand)
# receive and print the server's response
data2 = clientSocket.recv(1024)
print data2

# send RCPT command
rcptCommand = 'RCPT To: iprobabyldontexist@bu.edu\r\n'
clientSocket.send(rcptCommand)
# receive and print the server's response
data3 = clientSocket.recv(1024)
print data3

# check for 550 server response
if data3[:3] != '550':
	print '550 reply not received from server.'
	sys.exit(1)

# send DATA command
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand)
# receive and print the server's response
data4 = clientSocket.recv(1024)
print data4

# send message data
clientSocket.send(msg)

# message ends with a single period
clientSocket.send(endmsg)

# send QUIT command
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand)
# receive and print the server's response
data5 = clientSocket.recv(1024)
print data5

# close socket
clientSocket.close()
# import required libraries
from socket import *
import time

# define server variables
host = '' # default localhost
port = 8080 # port number
size = 1024 # buffer size
backlog = 5 # maximum number of queued requests

# setup socket server
serverSocket = socket(AF_INET, SOCK_STREAM)

# assign name to socket
serverSocket.bind((host,port))

# start listening
serverSocket.listen(backlog)
print 'Server is now listening on port %s' % port

# loop until connection is made
while True:

	print 'Ready to serve...'
	# accept incoming connection
	connectionSocket, addr = serverSocket.accept()
	 
	try:
		# get message request
		message = connectionSocket.recv(size)

		# check for valid message length
		if len(message) > 1:

			# open requested file
			filename = message.split()[1]
			f = open(filename[1:])

			# read file
			outputdata = f.read()

			# close file reader
			f.close()

			# send HTTP status to client
			connectionSocket.send('HTTP/1.1 200 OK\r\n')
			
			# send Last-Modified HTTP header line to client with current time
			currentTime = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
			connectionSocket.send('Last-Modified: {0}\r\n'.format(currentTime))

			# send content type to client
			connectionSocket.send("Content-Type: text/html\r\n\r\n")

			# send the content of the requested file to the client
			for i in range(0, len(outputdata)):
				connectionSocket.send(outputdata[i])
			connectionSocket.send("\r\n")

			# close client socket
			connectionSocket.close()

	except IOError:

		# send response message for file not found
		connectionSocket.send('HTTP/1.1 404 Not Found\r\n')
		connectionSocket.send("Content-Type: text/html\r\n\r\n")
		connectionSocket.send('<html><body><h1>Error</h1><h2>404 Not Found</h2></body></html>')

		# close client socket
		connectionSocket.close()
serverSocket.close()
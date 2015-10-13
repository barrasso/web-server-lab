# import required libraries
from socket import *
import time
import os.path

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
		# get request and filename
		request = connectionSocket.recv(size)

		# check for valid request length
		if len(request) > 1:

			# check the last time the requested file was modified
			filename = request.split()[1]
			lastModifiedTime = time.ctime(os.path.getmtime(filename[1:]))

			# check for 'If-Modified-Since' header
			if not "If-Modified-Since" in request:
				print('Did not find If-Modified-Since header in client request.')
			else:
				# get request time from request header
				requestTime = request.split("If-Modified-Since: ",1)[1]

				# trim excess whitespace/null characters
				requestTime = "".join(requestTime.split()) 
				lastModifiedTime = "".join(lastModifiedTime.split()) 

				# compare last modified time to request time 
				print 'Comparing request time: {0} to last modified time: {1}'.format(requestTime, lastModifiedTime)

				if requestTime > lastModifiedTime:
					print('requestTime is greater than the lastModifiedTime time.')
				else: 
					print('requestTime is less than the lastModifiedTime time.')

			# open requested file
			f = open(filename[1:])

			# read file
			outputdata = f.read()

			# close file reader
			f.close()

			# send HTTP status to client
			connectionSocket.send('HTTP/1.1 200 OK\r\n')
			
			# send Last-Modified HTTP header line to client
			lastModifiedTime = time.strftime('%a %b %d %H:%M:%S %Y')
			connectionSocket.send('Last-Modified: {0}\r\n'.format(lastModifiedTime))

			# send content type to client
			connectionSocket.send("Content-Type: text/html\r\n\r\n")

			# send the content of the requested file to the client
			for i in range(0, len(outputdata)):
				connectionSocket.send(outputdata[i])
			connectionSocket.send("\r\n")

			# close client socket
			connectionSocket.close()

	except IOError:

		# send response request for file not found
		connectionSocket.send('HTTP/1.1 404 Not Found\r\n')
		connectionSocket.send("Content-Type: text/html\r\n\r\n")
		connectionSocket.send('<html><body><h1>Error</h1><h2>404 Not Found</h2></body></html>')

		# close client socket
		connectionSocket.close()
serverSocket.close()
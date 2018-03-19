import sys
import socket
import select

class ChatServer:
	
	def __init__(self, port):
		self.port = port

		self.ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ssocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.ssocket.bind(("", port))
		self.ssocket.listen(5)

		self.slist = [self.ssocket]
		print('ChatServer started at port %s' % port)

	def run(self):
		while True:
			(sread, swrite, sexc) = select.select( self.slist, [], [])

			for sock in sread:
				if sock == self.ssocket:
					self.accept_new_connection()
				else:
					recstr = sock.recv(100)

					if recstr == '':
						host,port = sock.getpeername()
						bstr = 'Client left [%s:%s] \r\n' % (host,port)
						self.broadcast_msg( bstr, sock )
						sock.close()
						self.slist.remove(sock)
					else:
						host,port = sock.getpeername()
						nbstr = '[%s:%s] %s' % (host, port, recstr)
						self.broadcast_msg( nbstr, sock )

	def broadcast_msg(self, bstr, skip_socket):
		for sock in self.slist:
			if sock != self.ssocket and sock != skip_socket:
				sock.send(bstr.encode('ascii'))
		print(bstr);
		
	def accept_new_connection(self):
		
		newsock, (newsockhost, newsockport) = self.ssocket.accept()
		self.slist.append( newsock )

		msg = "You are now connected \r\n"
		newsock.send(msg.encode('ascii'))
		nbstr = 'New client joined %s:%s \r\n' % (newsockhost, newsockport)
		self.broadcast_msg( nbstr, newsock )
		
myServer = ChatServer( 9999 ).run()

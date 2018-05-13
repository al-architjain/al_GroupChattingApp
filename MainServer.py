#A group chatting application via terminal :)

import sys
import socket
import select

class ChatServer:
	
	def __init__(self, port):
		self.port = port
		self.host = socket.gethostname()
		self.ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ssocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.ssocket.bind(("", port))
		self.ssocket.listen(5)

		self.socketlist = [self.ssocket]
		print('ChatServer [ %s ] started at port [ %s ]' % (self.host, self.port))


	def run(self):
		while True:
			(sread, swrite, serr) = select.select( self.socketlist, [], [], 0)

			for sock in sread:
				# new connection request if socket is Server socket
				if sock == self.ssocket:
					self.accept_new_connection()

				# message from a connection if socket is not a Server socket but a client socket
				else:
					try:
						recstr = sock.recv(4096)

						if recstr:
							recvmsg = recstr.decode('ascii')
							host,port = sock.getpeername()
							bmsg = '[%s:%s] %s' % (host, port, recvmsg)
							self.broadcast_msg( bmsg, sock )

						else:
							host,port = sock.getpeername()
							bmsg = 'Client [%s:%s] left \r\n' % (host,port)
							self.broadcast_msg( bmsg, sock )
							sock.close()
							self.socketlist.remove(sock)
					except:
						host,port = sock.getpeername()
						bmsg = 'Client [%s:%s] left \r\n' % (host,port)
						self.broadcast_msg( bmsg, sock )
						sock.close()
						self.socketlist.remove(sock)
						continue;


	def broadcast_msg(self, bmsg, skip_socket):
		for sock in self.socketlist:
			if sock != self.ssocket and sock != skip_socket:
				try:
					sock.send(bmsg.encode('ascii'))
				except:
					sock.close()
					self.socketlist.remove(sock)
		
		print(bmsg);


	def accept_new_connection(self):
		newcsock, newcsockaddr = self.ssocket.accept()
		( newcsockhost, newcsockport ) = newcsockaddr
		self.socketlist.append( newcsock )

		msg = "You are now connected \r\n"
		newcsock.send(msg.encode('ascii'))

		bmsg = 'New client joined %s:%s \r\n' % (newcsockhost, newcsockport)
		self.broadcast_msg( bmsg, newcsock )
		
		
		
sobj = ChatServer( int(sys.argv[1]) )
sobj.run()


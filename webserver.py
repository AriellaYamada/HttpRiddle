import socket
import datetime
import commands 
import os

class HTTPResponse:
	__reasonPhrase = {
			200:"OK",
			400:"Bad Request",
			401:"Unauthorized",
			403:"Forbidden",
			404:"Not Found"
			#...
	}
	def __init__(self, code, connection, ctype, content):
		
		self.statusLine = "HTTP/1.1 " + str(code) + " " + self.__reasonPhrase[code];
		
		self.generalHeaders = []
		self.generalHeaders.append("Date: " + datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"))
		self.generalHeaders.append("Connection: " + connection)
		
		self.entityHeaders = []
		self.entityHeaders.append("Content-Type: " + ctype)
		self.entityHeaders.append("Content-Length: " + str(len(content)))

		self.content = content

	def getMessage(self):
		msg = ""
		msg = msg + self.statusLine + "\r\n"
		for line in self.generalHeaders:
			msg = msg + line + "\r\n"
		for line in self.entityHeaders:
			msg = msg + line + "\r\n"
		msg = msg + "\r\n"
		msg = msg + self.content
		return msg



serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(os.environ.get("PORT", 17995))
print ("Binding to port %d..." %port)

serverSocket.bind(("0.0.0.0", port))
serverSocket.listen(1)

print("Bind successful.")

while 1:
	connectionSocket, addr = serverSocket.accept()
	request = connectionSocket.recv(1024)
	#print("Got request:")
	#print(request);
	parts = request.split()

	if (len(parts) > 0 and parts[0] == "GET"):
		filename = parts[1][1:]
	else:
		connectionSocket.close()
		continue

	try:
		f = open(filename, "r")
	except (IOError):
		response = HTTPResponse(404, "close", "text/html", "")
		connectionSocket.send(response.getMessage())
	else:
		mimetype = commands.getstatusoutput("file -b --mime-type " + filename)[1]
		if (".css" in filename):
			mimetype = "text/css"
		content = f.read()
		response = HTTPResponse(200, "close", mimetype, content)
		connectionSocket.send(response.getMessage())
		f.close()
	connectionSocket.close()

serverSocket.close()

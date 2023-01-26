#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Omar Niazie
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

sc200 = "HTTP/1.1 200 OK\r\n"
sc301 = "HTTP/1.1 301 Moved Permanently\r\n"
sc400 = "HTTP/1.1 400 Bad Request\r\n"
sc404 = "HTTP/1.1 404 Not Found\r\n"
sc405 = "HTTP/1.1 405 Method Not Allowed\r\n"

htmlMime = 'Content-Type: text/html\r\n'
cssMime = 'Content-Type: text/css\r\n'
class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip().decode('utf-8')
        print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))

        data = self.data.split(' ')
        header = data[0]
        #print(header)
        filename = data[1]
        #print(filename)
        if header != 'GET':
            self.request.sendall(bytearray(sc405, 'utf-8'))

        if filename == '/' or filename.endswith("/"):
            filename += 'index.html'
        # if not (filename.endswith(".html") or filename.endswith('.css')):
        #     filename += '/index.html'
        #     print(filename)
        if not (filename.endswith("/") or filename.endswith(".css") or filename.endswith(".html")):
            # filename += "/index.html"
            print(f'FILENAME: {filename}')
            response = sc301 + "\nLocation: " + filename + "\r\n"

        try:
            if filename[0:3] == "/..":
                raise Exception
            
            fin = open("./www" + filename)
            content = fin.read()
            #print("CONTENT: " + content)
            fin.close()

            # if .html exists, html mime
            if filename.endswith('.html'):
                response = sc200 + htmlMime + "\r\n" + content 
                #print(f'HTML RESPONSE: {response}')
            # if .css exists, css mime
            elif filename.endswith('.css'):
                response = sc200 + cssMime + "\r\n" + content
                #print(f'CSS RESPONSE: {response}')
        except:
            response = sc404
        finally:
            self.request.sendall(bytearray(response, 'utf-8'))



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

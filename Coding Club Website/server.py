import BaseHTTPServer,mimetools,os,select
from tkSimpleDialog import *

class HTML:
    def __init__(self,template = "%s",header = "",pretitle = "",posttitle = "",footer = "",name = ""):
        self.template = template
        self.header = header
        self.footer = footer
        self.t1 = pretitle
        self.t2 = posttitle
        self.pages = {}
        self.stylesheets = {}
        self.pictures = {}
        self.scripts = {}

    def page(self,title,contents,shortcuticon = None):
        return """
<html><head><title>%s%s%s</title></head>
<body>%s</body></html>""" %(self.t1,title,self.t2,contents)

    def add_header(self,contents):
        return self.header + contents

    def add_footer(self,contents):
        return contents + self.footer

    def add_template(self,contents):
        return self.header + (self.template % contents) + self.footer

    def create_page(self,title,contents):
        return self.page(title,self.add_template(contents))

    def add_page(self,page,address):
        self.pages[address] = self.template + page

    def add_stylesheet(self,sheet,name):
        self.stylesheets[name] = sheet

    def add_image(self,image,name):
        self.pictures[name] = image

    def add_script(self,script,name):
        self.pictures[name] = script
with open("template.html") as template:
    website = HTML(template=template.read())
    
for page in ("index","links","blog","about","contact"):
    with open(page+".html") as htmlpage:
        website.add_page(page+".html",htmlpage.read())

with open("code.css") as css:
    website.add_stylesheet("stylesheet.css",css.read())

with open("template.js") as js:
    website.add_script("template.js",js.read())

class Message(mimetools.Message):
    def __init__(self, fp, seekable=1):
        Message = self.__class__
        Message.__bases__[0].__bases__[0].__init__(self, fp, seekable)
        self.encodingheader = self.getheader('content-transfer-encoding')
        self.typeheader = self.getheader('content-type')
        self.parsetype()
        self.parseplist()

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self,sitename,*args):
        self.site = sitename
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self,*args)

    def send_document(self,doctype,title,contents = None):
        if doctype == "html":
            code = 200
            contenttype = "text/html"
        elif doctype == "css":
            code = 200
            contenttype = "text/css"
        elif doctype == "bmp":
            code = 200
            contenttype = "image/bmp"
        else:
            code = 404
            contenttype = "text/html"
            contents = self.site.errormessage
            title = "Error"
        try:
            self.send_response(code)
            self.send_header("Content-Type",contenttype)
            self.end_headers()
            if title and contents:
                self.wfile.write(self.site.create_page(title,contents))
            else:
                self.wfile.write(title)
        except IOError:
            pass

    def do_GET(self):
        path = self.path
        if path[0] == "/": path = path[1:]
        if path == '' or path[-1] == "/": path += "index.html"

        if path in self.site.pages:
            self.send_document("html",self.site.pages[path])

        elif path in self.site.stylesheets:
            self.send_document("css",self.site.stylesheets[path])

        elif path in self.site.pictures:
            self.send_document(path[path.find(".")+1:],self.site.pictures[path])

        else:
            self.send_document("html",self.site.create_page("Error",self.site.errormessage))

    def log_message(self, *args): pass

class Server(BaseHTTPServer.HTTPServer):
    def __init__(self,port,callback,sitename):
        host = "192.168.0.4"
        self.address = (host,port)
        self.callback = callback
        self.base.__init__(self,self.address,self.handler) 

    def serve_until_quit(self):
        self.quit = False
        while not self.quit:
            rd, wr, ex = select.select([self.socket.fileno()], [], [], 1)
            if rd: self.handle_request()

    def server_activate(self):
        self.base.server_activate(self)
        if self.callback: self.callback(self)

    def finish_request(self,*args):
        self.RequestHandlerClass(self.sitename,*args+(self,))

Server.base = BaseHTTPServer.HTTPServer
Server.handler = Handler
Handler.MessageHandler = Message

def serve(port,site):
    try:
        try:
            Server(port, None, site).serve_until_quit()
        except (KeyboardInterrupt, select.error):
            pass
    finally: pass
    
if __name__ == "__main__":
    serve(8080,website)

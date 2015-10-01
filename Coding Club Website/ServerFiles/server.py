import BaseHTTPServer,mimetools,os,select

from tkSimpleDialog import *


import xmlloader


class BlogPage(xmlloader.XMLObject):

    def write_xml(self):

        string = "<BlogPage>\n  "

        for b in self.children:

            string += b.write_xml()

            string += "\n  "

        string += "</BlogPage>"

        return string


class Blog(xmlloader.XMLObject):

    def __init__(self,text,tail,title="",**options):

        self.text = text

        self.title = title

        self.children = []


    def write_xml(self):

        string = "<Blog title='"+self.title+"'>\n"+self.text

        for c in self.children:

            string += c.write_xml()

        string += "</Blog>"

        return string


    def convert_html(self):

        return """

        <h2 class="Title">%s</h2>

        <div class="entry">

        %s

        </div>

        """ % (self.title,self.text)


class Comment(xmlloader.XMLObject):

    def __init__(self,text,tail,name,**options):

        self.text = text

        self.name = name

        self.children = []

    def write_xml(self):

        return "<Comment name='"+self.name"'>"+self.text+"</Comment>"


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

        self.error = ""


    def add_page(self,address,title,page):

        self.pages[address] = self.template%(title,page)

    def add_error(self,text):

        self.error = self.template%("Error",text)

    def add_stylesheet(self,name,stylesheet):

        self.stylesheets[name] = stylesheet


    def get_blog


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
            title = self.site.error
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

        elif path == "reload":
            self.site = load_website()
            self.send_response(301)
            self.send_header("Location","index.html")
            self.end_headers()
            
        else:
            self.send_document("html",self.site.error)

    def log_message(self, *args): pass

class Server(BaseHTTPServer.HTTPServer):
    def __init__(self,port,callback,site):
        host = "192.168.0.4"
        self.address = (host,port)
        self.callback = callback
        self.site = site
        print "Server started"
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
        self.RequestHandlerClass(self.site,*args+(self,))

Server.base = BaseHTTPServer.HTTPServer
Server.handler = Handler
Handler.MessageHandler = Message

def load_website():
    with open("template.txt") as template:
        website = HTML(template=template.read())
        
    for page,title in (("index","Home"),("links","Coding Links"),("about","About"),("contact","Contact")):
        with open(page+".txt") as htmlpage:
            website.add_page(page+".html",title,htmlpage.read())

    with open("error.txt") as error:
        website.add_error(error.read())

    for stylesheet in ("stylesheet","nhs","vampire","green","rainbow","unicorn"):
        with open(stylesheet+".css") as css:
            website.add_stylesheet(stylesheet+".css",css.read())
    return website

def serve(port,site):
    try:
        try:
            Server(port, None, site).serve_until_quit()
        except (KeyboardInterrupt, select.error):
            pass
    finally: pass
    
if __name__ == "__main__":
    serve(8080,load_website())

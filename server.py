import BaseHTTPServer
import mimetools
import os
import select
import urllib

import xmlloader

class BlogPage(xmlloader.XMLObject):
    def write_xml(self):
        string = "<BlogPage>"
        for b in self.children:
            string += "\n  "
            string += b.write_xml()
        string += "\n</BlogPage>"
        return string

class Blog(xmlloader.XMLObject):
    def __init__(self,text,tail,title="",**options):
        self.text = text
        self.title = title
        self.children = []

    def write_xml(self):
        string = "<Blog title='"+self.title+"'>\n"+self.text.strip().replace("<","&lt;")
        for c in self.children:
            string += "\n    "
            string += c.write_xml()
        string += "\n  </Blog>"
        return string

    def convert_html(self):
        return """
        <article class="blog">
        <h2 class="blog_title">{title}</h2>
        <div class="blog_entry">
        {content}
        </div>
        <h5>Comments: {num}</h5>
        <table>
        {comments}
        <tr>
            <td>
                <label id="text-{title}">Name:</label>
                <input type="text" id="name-{title}">
                <p><input type="button" value="Leave a comment" onClick="comment('{title}')" id="comment-{title}"></p>
            </td>
            <td>
                <label id="block-{title}">Comment</label>
                <input type="text" id="content-{title}">
            </td>
        </tr>
        </table>
        </article>
        """.format(content=self.text,num=len(self.children),comments="\n".join(c.convert_html() for c in self.children),title=self.title)

class Comment(xmlloader.XMLObject):
    def __init__(self,text,tail,name,**options):
        self.text = text
        self.name = name
        self.children = []
    def write_xml(self):
        return "<Comment name='"+self.name+"'>"+self.text.strip().replace("<","&lt;")+"</Comment>"
    def convert_html(self):
        return "<tr><td class='name'>%s:</td><td class='comment' colspan='500'>%s</td></tr>"%(self.name,self.text)

class HTML:
    def __init__(self,template = "%s"):
        self.template = template
        self.blog_template = ""
        self.pages = {}
        self.stylesheets = {}
        self.pictures = {}
        self.scripts = {}
        self.error = ""
        self.blog = None

    def add_page(self,address,title,page):
        self.pages[address] = self.template%(title,page)
    def add_error(self,text):
        self.error = self.template%("Error",text)
    def add_stylesheet(self,name,stylesheet):
        self.stylesheets[name] = stylesheet
    def add_image(self,name,image):
        self.pictures[name] = image

    def blog_page(self,name=None):
        if not self.blog:
            return self.template%("Blog","<h1>Sorry, no blog entries yet!</h1>")
        page = ""
        if name != None:
            for blog in self.blog.children:
                if "-".join(blog.title.split()) == name:
                    page = blog.convert_html()
        else:
            for blog in self.blog.children[:3]:
                page += blog.convert_html()
        return self.template%(name if name else "Blog",self.blog_template%(self.blog_list(),page))
    def blog_list(self):
        blist = ""
        for child in self.blog.children:
            blist += "<li><a href='/blog/{}'>{}</a></li>\n".format("-".join(child.title.split()),child.title)
        return blist

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

    def send_document(self,doctype,contents):
        if doctype == "html":
            code = 200
            contenttype = "text/html"
        elif doctype == "css":
            code = 200
            contenttype = "text/css"
        elif doctype in ("bmp","jpg","gif","png"):
            code = 200
            contenttype = "image/"+doctype
        else:
            code = 404
            contenttype = "text/html"
            contents = self.site.error
        try:
            self.send_response(code)
            self.send_header("Content-Type",contenttype)
            self.end_headers()
            self.wfile.write(contents)
        except IOError:
            pass

    def do_GET(self):
        path = self.path
        if path[0] == "/": path = path[1:]
        if path == '' or path[-1] == "/": path += "index.html"

        if path == "reload":
            self.site = load_website()
            self.send_response(301)
            self.send_header("Location","/")
            self.end_headers()
            
        elif path == "save_blog":
            write_blog(self.site.blog)
            self.send_response(301)
            self.send_header("Location","/")
            self.end_headers()
            
        elif path.startswith("blog") and path != "blog.css":
            if path == "blog.html":
                page = self.site.blog_page()
                if page:
                    self.send_document("html",page)
                else:
                    self.send_response(301)
                    self.send_header("Location","/")
            else:
                name = path[5:]
                if name.endswith(".html"):
                    name = name[:-5]
                page = self.site.blog_page(name)
                if not page:
                    self.send_response(301)
                    self.send_header("Location","blog.html")
                    self.end_headers()
                else:
                    self.send_document("html",page)
            return

        if path in self.site.pages:
            self.send_document("html",self.site.pages[path])

        elif path in self.site.stylesheets:
            self.send_document("css",self.site.stylesheets[path])

        elif path in self.site.pictures:
            self.send_document(path[path.find(".")+1:],self.site.pictures[path])

        else:
            print path
            self.send_document("error",self.site.error)

    def do_POST(self):
        attrs = self.rfile.read().split("&")
        attrvalues = {}
        for attr in attrs:
            name,value = attr.split("=")
            value = urllib.unquote(value.replace("+"," "))
            attrvalues[name] = value
        print attrvalues.keys()
        if attrvalues.keys() == ["blog","content","name"]:
            for blog in self.site.blog.children:
                if blog.title == attrvalues["blog"]:
                    blog.children.append(Comment(attrvalues["content"].replace("\n","<br/>"),"",attrvalues["name"]))
                    break
        elif attrvalues.keys() == ["content","title"]:
            self.site.blog.children.append(Blog(attrvalues["content"],"",attrvalues["title"]))

    def log_message(self, *args): pass

class Server(BaseHTTPServer.HTTPServer):
    def __init__(self,port,callback,site):
        import socket
        host = os.getenv("IP","0.0.0.0")
        port = int(os.getenv("PORT",8080))
        self.address = (host,port)
        self.callback = callback
        self.site = site
        print "Server started on {}".format(self.address)
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

def load_website(blog=None):
    with open("template.txt") as template:
        website = HTML(template=template.read())

    with open("blog_template.txt") as blog_template:
        website.blog_template = blog_template.read()
        
    for page,title in (("index","Home"),
                       ("links","Coding Links"),
                       ("about","About"),
                       ("contact","Contact"),
                       ("boogaboogabooga-newblog","New Blog")):
        with open(page+".txt") as htmlpage:
            website.add_page(page+".html",title,htmlpage.read())

    with open("error.txt") as error:
        website.add_error(error.read())

    for stylesheet in ("stylesheet","nhs","vampire","green","rainbow","unicorn","blog"):
        with open(stylesheet+".css") as css:
            website.add_stylesheet(stylesheet+".css",css.read())

    with open("unicorn.jpg","rb") as unicorn:
        website.add_image("unicorn.jpg",unicorn.read())
    
    website.blog = blog
    return website

def load_blog():
    with open("blog.xml") as blogfile:
        blog = xmlloader.load_xml(blogfile,{"BlogPage":BlogPage,"Blog":Blog,"Comment":Comment})
    return blog

def write_blog(blog):
    print "Saving blog"
    with open("blog.xml","w") as blogfile:
        blogfile.write(blog.write_xml())

def serve(port,site):
    try:
        try:
            Server(port, None, site).serve_until_quit()
        except (KeyboardInterrupt, select.error):
            pass
    finally:
        if site.blog:write_blog(site.blog)
    
if __name__ == "__main__":
    serve(8080,load_website(load_blog()))

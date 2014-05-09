import requests
import re

class Egloos(object):
    def __init__(self, user, password, nick):
        self.id = id
        self.user = user
        self.password = password
        self.nick = nick

        self.login()

    def login(self):
        self.s = requests.Session()

        values = {'userid':self.user, 'userpwd':self.password}
        r = self.s.post('https://sec.egloos.com/login/sauthid.php', data=values)

    def get_content(self, id):
        r = self.s.get('http://' + self.nick + '.egloos.com/' + str(id))
        html = r.text
        
        content = re.sub("<div id=\"__KO_DIC_LAYER__\".*?/div>", '', html)
        m = re.search("<div id=\"content\">.*?<div class=\"content\">(.*?)<!--", content, re.S)
        content = m.group(1).strip()
        
        temp = "!@#!@#!"
        while temp != content:
            temp = content
            content = re.sub(re.compile("<div>(?P<content>.*?)</div>", re.S), "\n\g<content>\n", content)
        content = re.sub(re.compile("<p[^>]*>(?P<content>.*?)</p>", re.S), "\n\g<content>\n", content)
        content = re.sub(re.compile("<span[^>]*>(?P<content>.*?)</span>", re.S), "\g<content>", content)
        content = re.sub("&nbsp;", " ", content)
        content = re.sub("<br[^>]*>", "\n", content)
        content = re.sub("\n+", "\n", content).strip()

        return content

    def view_article(self, id):
        r = self.s.get('http://dslk.egloos.com/'+str(id))
        html = r.text

        m= re.search("<h3 class=\"posttitle\">.*?<a .*?>(.*?)</a>", html)
        title = m.group(1).strip()

        content = re.sub("<div id=\"__KO_DIC_LAYER__\".*?/div>", '', html)
        m = re.search("<div id=\"content\">.*?<div class=\"content\">(.*?)<!--", content, re.S)
        content = m.group(1).strip()

        temp = "!@#!@#!"
        while temp != content:
            temp = content
            content = re.sub(re.compile("<div>(?P<content>.*?)</div>", re.S), "\n\g<content>\n", content)
        content = re.sub(re.compile("<p[^>]*>(?P<content>.*?)</p>", re.S), "\n\g<content>\n", content)
        content = re.sub(re.compile("<span[^>]*>(?P<content>.*?)</span>", re.S), "\g<content>", content)
        content = re.sub("&nbsp;", " ", content)
        content = re.sub("<br[^>]*>", "\n", content)
        content = re.sub("\n+", "\n", content).strip()

        m= re.search("2\d\d\d/\d\d/\d\d", html)
        date = m.group(0).strip()

        return Article(int(id), title, content, date)

class Article(object):
    def __init__(self, id, title, content, date):
        self.id = id
        self.title = title
        self.content = content
        self.date = date

    def __str__(self):
        return "(%d) %s\n%s\n" % (self.id, self.title, self.content)

    def __byte__(self):
        return self.__str__().encode("UTF-8")

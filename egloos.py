import requests
import re

TITLE=0
CONTENT=1

category_dict = {
    'Music':'7', 'Muse':'2', 'RATM':'9', 'SOAD':'4', 'Queen':'6',
    'Radiohead':'5', 'Dog Sound':'3', 'Diary':'11', 'Movie':'10',
    'Show':'13', 'Book':'12', 'Game':'14', '▒▒▒▒':'8', 'Piano':'15'
}


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
        r = self.s.get('http://' + self.nick + '.egloos.com/'+str(id))
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

    def get_article_list_sub(self, category, page):
        r = self.s.get("http://" + self.nick +
                       ".egloos.com/category/"+category+"/list/"+str(page))
        html = r.text

        m = re.search("</p>\s*<div class=\"content\">(.*?)<div", html, re.S)
        articles = [x.strip() for x in m.group(1).split("<br/>")[:-1]]
        articles = [Article(int(re.search("<a href=\"/(\d+)\">", x, re.S).group(1)),
                            re.search("<a href=\"/\d+\">(.*?)</a>", x, re.S).group(1),
                            None,
                            re.search("archivedate\">(.*?)<", x, re.S).group(1)) for x in articles]
        for a in articles:
            a.content = self.get_content(a.id)
        return articles

    def get_article_list(self, category, regex,
                         option, flags, fast_print=False):
        page = 1
        articles = []

        articles_sub = self.get_article_list_sub(category, page)
        if fast_print:
            for a in self.filter_article(articles_sub, regex, option, flags):
                print(a)
        articles = articles + articles_sub
        page += 1
        while len(articles_sub) == 50:
            articles_sub = self.get_article_list_sub(category, page)
        if fast_print:
            for a in self.filter_article(articles_sub, regex, option, flags):
                print(a)
            articles = articles + articles_sub
            page += 1
        return articles

    def filter_article(self, articles, regex, option=CONTENT, flags=0):
        if option == TITLE:
            return [a for a in articles if re.search(regex, a.title, flags)]
        elif option == CONTENT:
            return [a for a in articles if re.search(regex, a.content, flags)]

    def write_article(self, category, title, content):
        values = {'eid':'e0080700',
                  'uid':'yourface',
                  'cgiid':category_dict[category],
                  'cgname':category,
                  'subject':title,
                  'content':content,
                  'contentlength':len(content),
                  'moresubject':'',
                  'morecontent':'',
                  'openflag':'3',
                  'cmltflag':'1',
                  'trbflag':'1',
                  'e4cflag':-1,
                  'postdate':'',
                  'editor_opt':'0',
                  'pstdate':'0',
                  'posttag':'',
                  'posttheme':'',
                  'old_posttag':'',
                  'allowHotTag':0,
                  'ismenu':'0'}
        r = self.s.post('http://www.egloos.com/egloo/post_insert_exec.php',
                        data=values)

        return r.text


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

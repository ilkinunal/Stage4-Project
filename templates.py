import webapp2
import jinja2
import os
import time
from google.appengine.ext import ndb


template_dir = os.path.join(os.path.dirname(__file__), 'notes')
JINJA_ENVIRONMENT = jinja2.Environment( loader=jinja2.FileSystemLoader(template_dir), 
    extensions=['jinja2.ext.autoescape'], autoescape=True)


class Handler(webapp2.RequestHandler): 
    """
    Basic Handler; will be inherited by more specific path Handlers
    """
    def write(self, *a, **kw):
        "Write small strings to the website"
        self.response.out.write(*a, **kw)  

    def render_str(self, template, **params):  
        "Render jinja2 templates"
        t = JINJA_ENVIRONMENT.get_template(template)
        return t.render(params)   
    
    def render(self, template, **kw):
        "Write the jinja template to the website"
        self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
        self.render("Notes-4.html")

class UserComment(ndb.Model):
    user = ndb.StringProperty()
    comment = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class MainPageComments(webapp2.RequestHandler):
    def get(self):
        error = self.request.get('error','')
        query = UserComment.query().order(UserComment.date)
        usercomment_list = query.fetch(10)

        for usercomment in query:
            user = usercomment.user
            comment = usercomment.comment
            self.response.out.write(user, comment)

    def post(self):
        user = self.request.get('user')
        comment = self.request.get('comment')

        if user and comment:
            usercomment = UserComment(user=user, comment=comment)
            usercomment.put()
            time.sleep(.1)
            self.redirect('/')
        else:
            self.redirect('/?error=Please fill out the name and comment sections!')

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/', MainPageComments)
], debug=True)


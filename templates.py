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

class UserComment(ndb.Model):
    user = ndb.StringProperty()
    comment = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    def user_key(user): 
        return ndb.Key('User', user)

    def comment_key(comment): 
        return ndb.Key('Comment', comment)

class MainPageComments(Handler):
    def get(self):
        error = self.request.get('error','')
        query = UserComment.query().order(UserComment.date)
        usercomment_list = query.fetch(10)

        self.render("Notes-4.html", 
            usercomments = usercomment_list)

    def post(self):
        user = self.request.get('user')
        comment = self.request.get('comment')

        if comment:
            usercomments = UserComment(user=user, comment=comment)
            usercomments.put()
            time.sleep(.1)
            self.redirect('/')
        else:
            self.redirect('/?error=Please fill out the name and comment sections!')

app = webapp2.WSGIApplication([
    ('/', MainPageComments)
], debug=True)

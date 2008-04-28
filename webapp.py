#!/usr/bin/env python
# encoding: utf-8
"""
webapp.py

Created by Pradeep Gowda on 2008-04-23.
Copyright (c) 2008 Yashotech. All rights reserved.
"""
import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
import functools
import os
from lib import utils, markdown2, BeautifulSoup
from requesthandler import TehRequestHandler
import shooin
import blog

class LoginHandler(TehRequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            self.redirect('/')

class LogoutHandler(TehRequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect(users.create_logout_url('/'))
        else:
            self.redirect('/')

class HomePageHandler(TehRequestHandler):
    def get(self):
        entries = blog.Entry.all()
        entries.filter("static =", False)
        entries.order('-published').fetch(limit=5)
        self.render("templates/home.html", entries=entries)


def main():
    application = webapp.WSGIApplication([
        (r"/", HomePageHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        
        (r"/entries", blog.EntryIndexHandler),
        (r"/feed", blog.FeedHandler),
        (r"/entry/([^/]+)", blog.EntryHandler),
        (r"/entry/([^/]+)/edit", blog.NewEntryHandler),
        (r"/entry/([^/]+)/del", blog.EntryDeleteHandler),
        (r"/new", blog.NewEntryHandler),
        (r"/topic/([^/]+)", blog.TagHandler),
        (r"/shooin/([^/]+)", shooin.ShooinHandler),
        
        (r"/([^/]+)", blog.PageHandler),
        ], debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
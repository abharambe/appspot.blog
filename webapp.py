#!/usr/bin/env python
# encoding: utf-8
"""
webapp.py

Created by Pradeep Gowda on 2008-04-23.
Copyright (c) 2008 Yashotech. All rights reserved.
"""
import logging
import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users

import os
from lib import utils, markdown2, BeautifulSoup
from utils import TehRequestHandler, administrator, Config
import blog
import admin


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
        each = TehRequestHandler.entries_per_page

        num = db.Query(blog.Entry).filter("static =", False).count()
        num_pages = num / each 
        if num % each > 0:
            num_pages += 1

        page = self.request.get('page')
        if not page:
            page = 1
        else:
            page = int(page)

        offset = (page - 1) * each
        entries = db.Query(blog.Entry).filter("static =", False).order("-published").fetch(each, offset)
        nav = {}

        if page < num_pages:
            nav['prev'] = page + 1
        if page > 1:
            nav['forward'] = page - 1

        self.render("templates/home.html", entries=entries, admin=users.is_current_user_admin(), nav=nav)
        
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
        (r"/([^/]+)/edit", blog.NewEntryHandler),
        (r"/([^/]+)/del", blog.EntryDeleteHandler),
        (r"/topic/([^/]+)", blog.TagHandler),
        
        (r"/admin", admin.AdminHandler),
        (r"/admin/new", blog.NewEntryHandler),
        (r"/admin/config", admin.ConfigHandler),
        (r"/admin/entrylist", admin.EntryListHandler),

       # (r"/shooin/([^/]+)", shooin.ShooinHandler),
        (r"/([^/]+)", blog.PageHandler),
        ], debug=True)
    
    config = Config.all()
    if config.count() > 0:
        config = config.fetch(1)[0]
    else: 
        config = Config(title="t-ashbha", url="http://ashwin-bharambe.appspot.com")
        config.put()
       
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()

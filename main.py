#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
import utils
import json
from utils import index, db
import logging
import exercises
import exercisehandlers
import ideoneclient
import auth
import user
from user import User
import mail

"""
TODO:

-Refactor all these handlers
-Settings page
	-Change Password
	-Change CSS style
	-Change CodeMirror style
	-Change CodeMirror Add-ons
-Disable editing and submitting while AJAX is working
-Randomly generated Quizes
-Implement CodeMirror across the site
-Check out what my fetch requests look like

Design:
-Sassy-fy the CSS
-Make everything RESPONSIVO
-Make it look like http://philipwalton.com/

Content:
-Add section about typecasting
-Finish section about errors
-Clean up "What's next" section
-NCURSES section
-Cover nested for loops

Exercises:
-Remove newlines when testing outputs
-Highlight errors (special semicolon error)
-Make sure number of inputs and outputs is the same
-Implement the following testing modes:
	-Insert submission into larger piece of code to test function
	-Find some way to test File I/O
"""

class LessonHandler(user.UserHandler):
	def user_get(self, *args):
		if args[0] is None:
			self.redirect('/')
		else:
			page = None
			for group in index:
				for topic in group['topics']:
					if topic['url']==args[0]:
						page = topic

			if page:
				self.render_with_user("lessons/" + args[0] + ".html", {'page':page})
			else:
				page = {'url':'404', 'topic_name':"Error 404"}
				self.render_with_user("404.html", {'page': page})

class MainHandler(user.UserHandler):
	def user_get(self, *args):
		page = {'url':'/', 'topic_name':""}
		self.render_with_user("index.html", {'page':page})

app = utils.webapp2.WSGIApplication(
	[	
		# User Authentication
		('/signup', auth.SignupHandler),
		('/login', auth.LoginHandler),
		('/logout', auth.LogoutHandler),
		('/recover_password', auth.PasswordRecoveryHandler),

		# User pages
		('/user/([a-zA-Z0-9_]+)?', user.UserPageHandler),
		('/admin', user.AdminPageHandler),

		# Adding new exercises and Ideone Accounts
		('/upload', exercisehandlers.FlowchartUploadHandler),
		('/serve/([^/]+)?', exercisehandlers.FlowchartServeHandler),
		('/addexercise', exercisehandlers.AddExerciseHandler),
		('/ideone', exercisehandlers.IdeoneAccountHandler),

		# Exercise Pages
		('/exercises/?([a-zA-Z0-9_]+)?', exercisehandlers.ExerciseHandler),

		# Suggestions
		('/suggestion', user.SuggestionHandler),

		# Lessons
		('/lessons/([a-zA-Z0-9_]+)?', LessonHandler),

		# Index
		('/', MainHandler)
	
	], debug=True)

exercises.Exercise.warmup()
user.User.warmup()
ideoneclient.IdeoneAccount.warmup()

def main():
 	run_wsgi_app(application) 




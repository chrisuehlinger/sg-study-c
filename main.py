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
import logging
import lesson.views
import example.models
import example.views
import exercise.models
import exercise.views
import ideoneclient
from user.views import UserHandler, AdminHandler
import user.views
from user.models import User

class WarmupHandler(utils.Handler):
	def get(self):
		exercise.models.Exercise.warmup()
		User.warmup()
		example.models.Example.warmup()
		self.redirect('/')

class MainHandler(UserHandler):
	def user_get(self, *args):
		page = {'url':'/', 'topic_name':"Welcome!"}
		self.render_with_user("index.html", {'page':page})

app = utils.webapp2.WSGIApplication(
	[	
		# User Authentication
		('/signup', user.views.SignupHandler),
		('/login', user.views.LoginHandler),
		('/logout', user.views.LogoutHandler),
		('/recover_password', user.views.PasswordRecoveryHandler),

		# User pages
		('/user/([a-zA-Z0-9_]+)?', user.views.UserPageHandler),
		('/admin', user.views.AdminPageHandler),
		('/settings', user.views.SettingsHandler),

		# Adding new exercises and Ideone Accounts
		('/upload', exercise.views.FlowchartUploadHandler),
		('/serve/([^/]+)?', exercise.views.FlowchartServeHandler),
		('/addexercise', exercise.views.AddExerciseHandler),

		# Exercise Pages
		('/exercises/?([a-zA-Z0-9_]+)?', exercise.views.ExerciseHandler),

		# Adding new Examples
		('/addexample', example.views.AddExampleHandler),

		# Examples
		('/example/([a-zA-Z0-9_]+)?', example.views.ExampleHandler),

		# Suggestions
		('/suggestion', user.views.SuggestionHandler),

		# Lessons
		('/lessons/([a-zA-Z0-9_]+)?', lesson.views.LessonHandler),

		# Warmup database
		('/warmup', WarmupHandler),

		# Index
		('/', MainHandler)
	
	], debug=True)

def main():
 	run_wsgi_app(application) 




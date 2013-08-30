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
import example
import exercises
import exercisehandlers
import ideoneclient
import auth
import user
from user import User
import datetime, time

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
				inline_examples = []
				for e in page['examples']:
					ex = example.Example.query().filter('url = ', e).get()
					inline_examples.append(ex)
					logging.info(ex)

				now = datetime.datetime.now()
				now_stamp = int(time.mktime(now.timetuple()))
				self.render_with_user("lessons/" + args[0] + ".html", { 'page': page, 
																		'curr_time-formatted': now, 
																		'curr_timestamp': now_stamp,
																		'examples': inline_examples})
			else:
				page = {'url':'404', 'topic_name':"Error 404"}
				self.render_with_user("404.html", {'page': page})

	def user_post(self, *args):
		submission = self.request.get('code')
		message = ''
		client = ideoneclient.IdeoneClient()
		response = client.submit(submission, self.request.get('input'))
		if response['error'] != "OK" or int(response['result']) != 15 or response['output'] is None:
			message = response['error_message']

		response['message'] = message

		self.write_json(response);

class MainHandler(user.UserHandler):
	def user_get(self, *args):
		page = {'url':'/', 'topic_name':"Welcome!"}
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
		('/settings', user.SettingsHandler),

		# Adding new exercises and Ideone Accounts
		('/upload', exercisehandlers.FlowchartUploadHandler),
		('/serve/([^/]+)?', exercisehandlers.FlowchartServeHandler),
		('/addexercise', exercisehandlers.AddExerciseHandler),

		# Exercise Pages
		('/exercises/?([a-zA-Z0-9_]+)?', exercisehandlers.ExerciseHandler),

		# Adding new Examples
		('/addexample', example.AddExampleHandler),

		# Examples
		('/example/([a-zA-Z0-9_]+)?', example.ExampleHandler),

		# Suggestions
		('/suggestion', user.SuggestionHandler),

		# Lessons
		('/lessons/([a-zA-Z0-9_]+)?', LessonHandler),

		# Index
		('/', MainHandler)
	
	], debug=True)

exercises.Exercise.warmup()
user.User.warmup()
example.Example.warmup()

def main():
 	run_wsgi_app(application) 




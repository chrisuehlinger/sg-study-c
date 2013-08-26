#!/usr/bin/env python
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

import re
import utils
import time
from user import User
import user
import logging
from google.appengine.ext import db
from google.appengine.api import mail

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return PASS_RE.match(password)

def verify_password(password, verify):
	if password and verify and password == verify:
		return True
	else:
		return False

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
	if email:
		return EMAIL_RE.match(email)
	else:
		return True

def valid_number(number):
	try:
		int(number)
		return number
	except Exception, e:
		return False


class SignupHandler(utils.Handler):
	def get(self):
		page = {'url':'exercises', 'topic_name':'Signup'}
		self.render("signup.html", {"page":page})

	def post(self):
		page = {'url':'exercises', 'topic_name':'Signup'}
		input_username = self.request.get("username")
		input_password = self.request.get("password")
		input_verify = self.request.get("verify")
		input_email = self.request.get("email")
		input_room = self.request.get("room")
		input_number = self.request.get("number")

		username = valid_username(input_username)
		password = valid_password(input_password)
		verify = verify_password(input_password, input_verify)
		email = valid_email(input_email)
		room = valid_number(input_room)
		number = valid_number(input_number)

		name_free = None
		if username:
			name_free = User.username_free(input_username)
		
		room_number_free = None
		if room and number:
			room_number_free = User.unique_student(input_room, input_number)
			

		if not (username and name_free and password and verify and email and room and number and room_number_free):
			username_error = ""
			if not username:
				username_error = "Invalid Username."

			if username and not name_free:
				username_error = "User name taken."

			password_error = ""
			if not password:
				password_error = "Invalid Password."

			verify_error = ""
			if not verify:
				verify_error = "Passwords do not match."

			email_error = ""
			if not email:
				email_error = "Invalid Email."

			room_error = ""
			if not room:
				room_error = "Not a number."

			number_error = ""
			if not number:
				number_error = "Not a number."

			if room and number and not room_number_free:
				number_error = "M 5/{0} #{1} has already signed up.".format(input_room, input_number)

			self.render("signup.html",{	"username": input_username,
										"password": input_password,
										"verify": input_verify,
										"email": input_email,
										"room": input_room,
										"number": input_number,
										"usernameerror": username_error,
										"passworderror": password_error,
										"verifyerror": verify_error,
										"emailerror": email_error,
										'roomerror':room_error,
										'numbererror':number_error,										
										'groups':utils.index, "page":page})
		else:
			new_user = User.register(input_username, input_password, input_email)
			new_user.room = int(input_room)
			new_user.number = int(input_number)
			new_user.put()
			self.set_secure_cookie("username", input_username)
			self.set_secure_cookie("css", new_user.pref_css)
			self.redirect('/')

class LoginHandler(utils.Handler):
	def get(self):
		page = {'url':'exercises', 'topic_name':'Login'}
		self.render("login.html", {"page":page})

	def post(self):
		page = {'url':'exercises', 'topic_name':'Login'}
		valid=False
		input_username = self.request.get("username")
		input_password = self.request.get("password")

		if valid_username(input_username) and valid_password(input_password):
			the_user = User.query().filter('username = ',input_username).get()
			if the_user and the_user.valid_pw(input_username, input_password):
					valid=True
					self.set_secure_cookie("username", input_username)
					self.set_secure_cookie("css", the_user.pref_css)
					if the_user.admin_priv:
						self.redirect('/admin')
						self.set_secure_cookie("admin", "yes")
					else:
						self.redirect('/user/%s' % input_username)
					
		if not valid:
			error = "Invalid username or password"
			self.render("login.html", {'username':input_username, 'password':input_password, 'error': error, "page":page})

class LogoutHandler(utils.Handler):
	def get(self):
		self.delete_cookie("username")
		self.delete_cookie("admin")
		self.delete_cookie("css")
		self.redirect('/')

class WelcomeHandler(utils.Handler):
	def get(self):
		username = self.get_cookie("username")
		if username:
			self.redirect("/")
		else:
			self.redirect("/signup")

class PasswordRecoveryHandler(utils.Handler):
	def get(self):
		page = {'url':'/recover_password', 'topic_name':'Recover Password'}
		self.render("recover_password.html", {'page':page})

	def post(self):
		email = self.request.get('email')
		user = None
		user_list = User.query()
		for u in user_list:
			if u.email == email:
				user = u

		if user:
			message = mail.EmailMessage(sender="no-reply@sg-study-c.appspotmail.com",
                            		subject="Password Reset")

			message.to = user.email
			message.body = "Your password for {0} has been reset to: {1}\n\nTry to log in again.".format(user.username, user.reset_pw())
			message.send()
			self.write_json({'message':'Password reset, check your email.'})
		else:
			self.write_json({'message':'Failed to reset password, try again.'})
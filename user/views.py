import utils
import logging
from google.appengine.ext import db
from google.appengine.api import mail
import hashlib
import random
import string
from models import User, Suggestion
from exercise.models import Exercise
import re
import time

class SuggestionHandler(utils.Handler):
	def post(self):
		user = None
		username = self.get_cookie("username")
		if username:
			user = User.query().filter('username = ', username).get()

		suggestionText = self.request.get('suggestion')
		if suggestionText:
			suggestion = Suggestion(content=suggestionText,
									submitter=user,
									page=self.request.get('page_url'))
			logging.info(self.request.get('page_url'))
			suggestion.put()
			self.write_json({'message':'Thanks!'})
		else:
			self.write_json({'message':'Whoops, there was nothing there!'})

class UserHandler(utils.Handler):
	username = None
	isAdmin = None

	def get(self, *args):
		self.username = self.get_cookie("username")

		if self.get_cookie("admin") == "yes":
			self.isAdmin = True

		if self.get_cookie("css"):
			self.stylesheet = self.get_cookie("css")

		if self.get_cookie('cm_theme'):
			self.codemirror_theme = self.get_cookie('cm_theme')

		self.user_get(*args)

	def post(self, *args):
		self.username = self.get_cookie("username")

		if self.get_cookie("admin") == "yes":
			self.isAdmin = True

		if self.get_cookie("css"):
			self.stylesheet = self.get_cookie("css")

		if self.get_cookie('cm_theme'):
			self.codemirror_theme = self.get_cookie('cm_theme')

		self.user_post(*args)

	def render_with_user(self,template_name, template_values={}):
		logging.info('User: "%s"' % self.username)
		template_values['logged_in_username'] = self.username
		template_values['isAdmin'] = self.isAdmin
		self.render(template_name, template_values)

class AdminHandler(UserHandler):
	user = None

	def user_get(self, *args):
		if self.isAdmin:
			self.admin_get(*args)
		else:
			self.redirect('/')

	def user_post(self, *args):
		if self.isAdmin:
			self.admin_post(*args)
		else:
			self.redirect('/')

class SettingsHandler(UserHandler):
	def user_get(self):
		if self.username:
			page = {'url':'settings', 'topic_name':'Settings'}
			self.render_with_user("settings.html", {'page':page,
													'styles':utils.styles,
													'themes':utils.codemirror_themes})
		else:
			self.redirect('/')

	def user_post(self):
		user = User.query().filter('username = ', self.username).get()
		if user:
			if self.request.get("form_id") == "change_password":
				self.change_password(user)
			elif self.request.get("form_id") == "css":
				self.change_css(user)
			
		else:
			self.redirect('/')

	def change_css(self, user):
		page = {'url':'settings', 'topic_name':'Settings'}

		new_css = self.request.get('style')
		self.set_secure_cookie("css", new_css)
		user.pref_css = new_css
		self.stylesheet = new_css

		new_theme = self.request.get('cm_theme')
		self.set_secure_cookie('cm_theme', new_theme)
		user.pref_codemirror_css = new_theme
		self.codemirror_theme = new_theme

		user.put()
		
		logging.info(new_css)
		self.render_with_user("settings.html", {'page':page,
												'styles':utils.styles,
												'themes':utils.codemirror_themes})

	def change_password(self, user):
		page = {'url':'settings', 'topic_name':'Settings'}
		old_password = user.valid_pw(user.username, self.request.get('old_password'))
		new_password = valid_password(self.request.get('new_password'))
		confirm_password = verify_password(self.request.get('new_password'), self.request.get('confirm_password'))

		if not (old_password and new_password and confirm_password):
			old_error=''
			if not old_password:
				old_error='Password incorrect.'

			new_error=''
			if not new_password:
				new_error='Invalid password.'

			confirm_error=''
			if not confirm_password:
				confirm_error='Passwords do not match'

			self.render_with_user("settings.html", {'page':page,
													'styles':utils.styles,
													'themes':utils.codemirror_themes,
													'old_password':self.request.get('old_password'),
													'new_password':self.request.get('new_password'),
													'confirm_password':self.request.get('confirm_password'),
													'old_error':old_error,
													'new_error':new_error,
													'confirm_error':confirm_error})
		else:
			user.password = make_pw_hash(user.username, self.request.get('new_password'))
			user.put()
			self.render_with_user("settings.html", {'page':page, 
													'styles':utils.styles,
													'themes':utils.codemirror_themes,
													'message':'Success!'})

class UserPageHandler(UserHandler):
	def user_get(self, *args):
		user = User.query().filter('username = ', self.username).get()
		if user and args[0] and ( user.username == args[0] or user.admin_priv):
			page = {'url':'/user/%s' % user.username, 
					'topic_name':'{0} - M5/{1} #{2}'.format(user.username, user.room, user.number) }

			exercise_list = Exercise.query()
			exercises_completed = list()
			for e in exercise_list:
				if e.key() in user.exercises_completed:
					exercises_completed.append(e)
					logging.info(e.name)


			self.render_with_user("userpage.html", {'page':page,
													'user':user,
													'exercises_completed':exercises_completed})
		else:
			self.redirect('/')

class AdminPageHandler(AdminHandler):
	def admin_get(self, *args):
		page = {'url':'/admin', 'topic_name':'Admin Page'}
		user_list = User.query()
		exercise_list = Exercise.query()
		suggestion_list = Suggestion.query().order("-posted_date")
		current_user = User.query().filter("username = ", self.username).get()
		self.render_with_user("adminpage.html", {   'page':page, 
													'user':current_user,
													'user_list':user_list, 
													'exercise_list':exercise_list, 
													'suggestion_list':suggestion_list})


"""User Authentication"""

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


class SignupHandler(UserHandler):
	def get(self):
		page = {'url':'exercises', 'topic_name':'Signup'}
		self.render("signup.html", {"page":page})

	def post(self):
		page = {'url':'exercises', 'topic_name':'Signup'}
		input_username = self.request.get("username")
		input_password = self.request.get("password")
		input_verify   = self.request.get("verify")
		input_email    = self.request.get("email")
		input_room     = self.request.get("room")
		input_number   = self.request.get("number")

		username = valid_username(input_username)
		password = valid_password(input_password)
		verify   = verify_password(input_password, input_verify)
		email    = valid_email(input_email)
		room     = valid_number(input_room)
		number   = valid_number(input_number)

		name_free = None
		if username:
			name_free = User.username_free(input_username)
		
		room_number_free = None
		if room and number:
			room_number_free = User.unique_student(input_room, input_number)
			

		if not (username and name_free and password and verify and
			email and room and number and room_number_free):

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
										'groups':utils.index, 
										"page":page})
		else:
			new_user = User.register(input_username, input_password, input_email)
			new_user.room = int(input_room)
			new_user.number = int(input_number)
			new_user.put()
			self.set_secure_cookie("username", input_username)
			self.set_secure_cookie("css", new_user.pref_css)
			self.set_secure_cookie('cm_theme', new_user.pref_codemirror_css)
			self.redirect('/')

class LoginHandler(UserHandler):
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
					self.set_secure_cookie('cm_theme', the_user.pref_codemirror_css)
					if the_user.admin_priv:
						self.redirect('/admin')
						self.set_secure_cookie("admin", "yes")
					else:
						self.redirect('/user/%s' % input_username)
					
		if not valid:
			error = "Invalid username or password"
			self.render("login.html", {'username':input_username, 
										'password':input_password, 
										'error': error, 
										"page":page})

class LogoutHandler(UserHandler):
	def get(self):
		self.delete_cookie("username")
		self.delete_cookie("admin")
		self.delete_cookie("css")
		self.delete_cookie('cm_theme')
		self.redirect('/')

class WelcomeHandler(UserHandler):
	def get(self):
		username = self.get_cookie("username")
		if username:
			self.redirect("/")
		else:
			self.redirect("/signup")

class PasswordRecoveryHandler(UserHandler):
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


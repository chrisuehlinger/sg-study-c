import utils
import logging
from google.appengine.ext import db
import hashlib
import random
import string
from exercise.models import Exercise
import re

warmups = [{ 'username':'chris',
			 'password':'1234',
			 'email':'',
			 'admin':True,
			 'room':0,
			 'number':0},
			{'username':'testStudent',
			 'password':'1234',
			 'email':'',
			 'admin':False,
			 'room':3,
			 'number':42}]

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return PASS_RE.match(password)

def verify_password(password, verify):
	if password and verify and password == verify:
		return True
	else:
		return False

def make_salt():
	return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt=make_salt()):
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s,%s' % (h, salt)

class User(utils.Model):
	username=db.StringProperty(required=True)
	password=db.StringProperty(required=True)
	email=db.StringProperty()
	created=db.DateTimeProperty(auto_now_add=True)
	admin_priv=db.BooleanProperty(default=False)

	room=db.IntegerProperty()
	number=db.IntegerProperty()

	exercises_completed=db.ListProperty(db.Key)

	#Preferences
	pref_css=db.StringProperty(default="the_new_style")
	pref_codemirror_css=db.StringProperty(default="night")
	pref_codemirror_addons=db.ListProperty(str)


	def reset_pw(self):
		new_pw = ''.join(random.choice(string.letters) for x in xrange(5))
		self.password = make_pw_hash(self.username, new_pw)
		self.put()
		return new_pw

	def valid_pw(self, name, pw):
		if make_pw_hash(name,pw,self.password.split(',')[1]) == self.password:
			return True

	@classmethod
	def username_free(cls, username):
		if not User.query().filter('username = ', username).count():
			return True

	@classmethod
	def unique_student(cls, room, number):
		unique = True
		user_list = User.query()
		for u in user_list:
			if u.room == int(room) and u.number == int(number):
				return False
		return True

	@classmethod
	def register(cls, username, password, email=None):
		if username and password:
			hash = make_pw_hash(username, password)
			return User(username=username, password=hash, email=email)

	@classmethod
	def warmup(cls):
		if User.query().count() == 0:
			logging.info("Warming up Users")
			for u in warmups:
				user = User.register(u['username'], u['password'], u['email'])
				user.admin_priv = u['admin']
				user.room = u['room']
				user.number = u['number']
				user.put()


class Suggestion(utils.Model):
	content = db.StringProperty(required=True)
	submitter = db.ReferenceProperty(User)
	page = db.StringProperty()
	posted_date = db.DateTimeProperty(auto_now_add=True)

	def submitter_string(self):
		if self.submitter:
			return "{0}, M 5/{1} #{2}".format(self.submitter.username, 
											  self.submitter.room,
											  self.submitter.number)
		else:
			return "Anonymous"
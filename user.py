import utils
import logging
from google.appengine.ext import db
import hashlib
import random
import string
from exercises import Exercise

warmups = [{ 'username':'chris',
			 'password':'1234',
				'email':'',
				'admin':True,
				'room':0,
				'number':0},
		   { 'username':'testStudent',
			 'password':'1234',
				'email':'',
				'admin':False,
				'room':3,
				'number':42}]

def make_salt():
	return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt=make_salt()):
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s,%s' % (h, salt)

class User(db.Model):
	username=db.StringProperty(required=True)
	password=db.StringProperty(required=True)
	email=db.StringProperty()
	created=db.DateTimeProperty(auto_now_add=True)
	admin_priv=db.BooleanProperty(default=False)
	room=db.IntegerProperty()
	number=db.IntegerProperty()
	exercises_completed=db.ListProperty(db.Key)

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
		q = db.GqlQuery("SELECT * FROM User WHERE username= '%s'" % username)
		if q.count()==0:
			return True

	@classmethod
	def unique_student(cls, room, number):
		unique = True
		user_list = db.Query(User)
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
		if db.Query(User).count() == 0:
			logging.info("Warming up Users")
			for u in warmups:
				user = User.register(u['username'], u['password'], u['email'])
				user.admin_priv = u['admin']
				user.room = u['room']
				user.number = u['number']
				user.put()

class Suggestion(db.Model):
	content = db.StringProperty(required=True)
	submitter = db.ReferenceProperty(User)
	page = db.StringProperty()
	posted_date = db.DateTimeProperty(auto_now_add=True)

	def submitter_string(self):
		if self.submitter:
			return "{0}, M 5/{1} #{2}".format(self.submitter.username, self.submitter.room, self.submitter.number)
		else:
			return "Anonymous"

class SuggestionHandler(utils.Handler):
	def post(self):
		user = None
		username = self.get_cookie("username")
		if username:
			user = db.Query(User).filter('username = ', username).get()

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
		self.user_get(*args)

	def post(self, *args):
		self.username = self.get_cookie("username")
		if self.get_cookie("admin") == "yes":
			self.isAdmin = True
		self.user_post(*args)

	def render_with_user(self,template_name, template_values={}):
		template_values['username'] = self.username
		template_values['isAdmin'] = self.isAdmin
		self.render(template_name, template_values)

class AdminHandler(UserHandler):
	user = None

	def user_get(self, *args):
		user = db.Query(User).filter('username = ', self.username).get()
		if self.isAdmin:
			self.admin_get(*args)
		else:
			self.redirect('/')

	def user_post(self, *args):
		user = db.Query(User).filter('username = ', username).get()
		if self.isAdmin:
			self.admin_post(*args)
		else:
			self.redirect('/')

class UserPageHandler(UserHandler):
	def user_get(self, *args):
		user = db.Query(User).filter('username = ', self.username).get()
		if user and args[0] and ( user.username == args[0] or user.admin_priv):
			page = {'url':'/user/%s' % user.username, 'topic_name':'{0} - M5/{1} #{2}'.format(user.username, user.room, user.number) }

			exercise_list = db.Query(Exercise)
			exercises_completed = list()
			for e in exercise_list:
				if e.key() in user.exercises_completed:
					exercises_completed.append(e)
					logging.info(e.name)


			self.render_with_user("userpage.html", {'page':page, 'user':user, 'exercises_completed':exercises_completed})
		else:
			self.redirect('/')

class AdminPageHandler(AdminHandler):
	def admin_get(self, *args):
		page = {'url':'/admin', 'topic_name':'Admin Page'}
		user_list = db.Query(User)
		exercise_list = db.Query(Exercise)
		suggestion_list = db.Query(Suggestion).order("-posted_date")
		self.render_with_user("adminpage.html", {'page':page, 'user':self.user, 'user_list':user_list, 'exercise_list':exercise_list, 'suggestion_list':suggestion_list})

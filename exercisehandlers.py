import json
import time
import utils
import string
from utils import db
import logging
import difflib
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from exercises import Exercise, ExerciseChecker
from user import User
import user
from ideoneclient import IdeoneClient

class FlowchartUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		upload_files = self.get_uploads()
		used_methods = list()
		for method in test_methods:
			if self.request.get(method):
				used_methods.append(method)

		inputs = list()
		for i in string.replace(self.request.get('test_input'), '\r', '').split(';'):
			inputs.append(db.Text(i))

		outputs = list()
		for o in string.replace(self.request.get('output'), '\r', '').split(';'):
			outputs.append(db.Text(o))

		checker = ExerciseChecker(	test_methods=used_methods,
									inputs=inputs,
									outputs=outputs,
									keywords=string.replace(self.request.get('keywords'), '\r', '').split(';'))
		checker.put()
		exercise = Exercise(name=self.request.get('name'), 
							url=self.request.get('url'), 
							description=string.replace(string.replace(self.request.get('description'), '\r', ''), '\n', '<br>'),
							start_code=string.replace(self.request.get('start_code'), '\r', ''),
							checker=checker)
		if len(upload_files):
			exercise.flowchart = upload_files[0].key()
		exercise.put()
		time.sleep(5)
		self.redirect('/exercises/'+exercise.url)

class FlowchartServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, blob_key):
		blob_key = str(urllib.unquote(blob_key))
		if not blobstore.get(blob_key):
			self.error(404)
		else:
			self.send_blob(blobstore.BlobInfo.get(blob_key), save_as=True)

class AddExerciseHandler(user.AdminHandler):
	def admin_get(self):
		upload_url = blobstore.create_upload_url('/upload')
		page = {'topic_name': 'Create an Exercise'}
		self.render_with_user("addexercise.html", {'page':page, 'test_methods':test_methods, 'upload_url': upload_url})

class ExerciseHandler(user.UserHandler):
	def user_get(self, *args):
		pagename = args[0]
		if pagename is None:
			exercise_list = db.Query(Exercise).order('name')
			page = {'url':'exercises', 'topic_name':'Practice Exercises'}
			self.render_with_user("exerciseindex.html", {'page':page, 'exercises':exercise_list})
		else:
			exercise = db.Query(Exercise).filter("url = ",pagename).get()
			if exercise is None:
				self.write("No Exercise named '%s'" % pagename)
			else:
				logging.info("Serving exercise: " + repr(exercise.name))
				logging.info("Serving exercise: " + repr(string.replace(exercise.start_code, '\r', '')))
				logging.info("Serving exercise: " + repr(exercise.description))
				self.render_with_user("exercise.html", {'page':exercise})

	def user_post(self, *args):
		pagename = args[0]
		if args[0] is None:
			pagename=""

		submission = self.request.get('code')
		action = self.request.get('action')

		response = dict()
		if action == 'check':
			exercise = db.Query(Exercise).filter("url = ",pagename).get()
			response = exercise.checker.checkWork(submission)
			if response['passed']:
				user = db.Query(User).filter('username = ', self.username).get()
				if not exercise.key() in user.exercises_completed:
					user.exercises_completed.append(exercise.key())
					user.put()

		elif action == 'test':
			message = ''
			client = IdeoneClient()
			response = client.submit(submission, self.request.get('input'))
			if response['error'] != "OK" or int(response['result']) != 15 or response['output'] is None:
				message = response['error_message']

			response['message'] = message

		self.write_json(response);
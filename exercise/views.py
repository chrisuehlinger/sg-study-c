import json
import time
import utils
import string
from utils import db
import logging
import difflib
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from models import Exercise, ExerciseChecker
from user.models import User
from user.views import UserHandler, AdminHandler
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

		if len(inputs) != len(outputs):
			self.write("Error: Number of inputs did not match number of outputs.")
		else:
			keywords = string.replace(self.request.get('keywords'), '\r', '').split(';')
			checker = ExerciseChecker(	test_methods=used_methods,
										inputs=inputs,
										outputs=outputs,
										keywords=keywords)
			checker.put()

			start_code=string.replace(self.request.get('start_code'), '\r', '')

			description = self.request.get('description')
			description = string.replace(description, '\r', '')
			description = string.replace(description, '\n', '<br>')

			exercise = Exercise(name=self.request.get('name'), 
								url=self.request.get('url'), 
								description=description,
								start_code=start_code,
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

class AddExerciseHandler(AdminHandler):
	def admin_get(self):
		upload_url = blobstore.create_upload_url('/upload')
		page = {'topic_name': 'Create an Exercise'}
		self.render_with_user("addexercise.html", { 'page':page, 
													'test_methods':test_methods,
													'upload_url': upload_url})

class ExerciseHandler(UserHandler):
	def user_get(self, *args):
		pagename = args[0]
		if pagename is None:
			exercise_list = Exercise.query().order('name')
			page = {'url':'exercises', 'topic_name':'Practice Exercises'}
			self.render_with_user("exerciseindex.html", {'page':page,
														 'exercises':exercise_list})
		else:
			exercise = Exercise.query().filter("url = ",pagename).get()
			if exercise is None:
				self.write("No Exercise named '%s'" % pagename)
			else:
				logging.info("Serving exercise: " + repr(exercise.name))
				logging.info("Serving exercise: " + repr(exercise.start_code))
				logging.info("Serving exercise: " + repr(exercise.description))
				self.render_with_user("exercise.html", {'page':exercise})

	def user_post(self, *args):
		pagename = args[0]
		if args[0] is None:
			pagename=""

		exercise = Exercise.query().filter("url = ",pagename).get()
		submission = self.request.get('code')
		program = exercise.outside_code.format(submission)
		action = self.request.get('action')

		response = dict()
		if action == 'check':
			response = exercise.checker.checkWork(program)
			if response['passed']:
				user = User.query().filter('username = ', self.username).get()
				if user and (not exercise.key() in user.exercises_completed):
					user.exercises_completed.append(exercise.key())
					user.put()

		elif action == 'test':
			message = ''
			client = IdeoneClient()
			response = client.submit(program, self.request.get('input'))
			
			if (response['error'] != "OK" or 
				int(response['result']) != 15 or 
				response['output'] is None):
					message = response['error_message']

			response['message'] = message

		self.write_json(response);
import json
import time
import utils
import urllib
import re
import os
import string
from utils import db
import logging
from ideoneclient import IdeoneClient
from coliruclient import ColiruClient
import difflib
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

test_methods = ['Input/Output', 'Check Keywords', 'Randomness Test']

class ExerciseChecker(utils.Model):
	test_methods = db.ListProperty(str)
	inputs       = db.ListProperty(db.Text)
	outputs      = db.ListProperty(db.Text)
	keywords     = db.ListProperty(unicode)

	def submit(self, submission, username="", the_input=""):
		col_client = ColiruClient()
		response = col_client.submit(submission, the_input)

		if response['error'] != "OK":
			client = ideoneclient.IdeoneClient()
			user = User.query().filter('username = ', username).get()
			if user and user.ideone_acct:
				client.change_account(user.ideone_acct)

			response = client.submit(submission, the_input)

		return response

	def checkWork(self, submission, username=""):
		message = ''
		passed = True
		response = dict()

		if "Input/Output" in self.test_methods:
			test_result = self.ioTest(submission, username)
			if not test_result['passed']:
				passed = False
			message = message + test_result['message']
			response = test_result['response']

		if "Check Keywords" in self.test_methods and passed:
			test_result = self.checkKeywords(submission)
			if not test_result['passed']:
				passed = False
			message = message + test_result['message']

		if "Randomness Test" in self.test_methods and passed:
			test_result = self.checkRandom(submission, username)
			if not test_result['passed']:
				passed = False
			message = message + test_result['message']
		
		response['passed'] = passed
		response['message'] = message

		if passed:
			response['message'] = "Great job!"
		
		return response

	def ioTest(self, submission, username=""):
		passed   = True
		message  = ""
		response = dict()
		for i in self.inputs:
			response = self.submit(submission, username, the_input=i)
			expected_output = string.replace(self.outputs[self.inputs.index(i)], '\n', '')

			if (response['error'] != "OK" or 
				int(response['result']) != 15 or 
				response['output'] is None):
					passed = False
					message = "Sorry, try again.\n\n" + response['error_message']
					break
			else:
				student_output = string.replace(response['output'], '\n', '')
				if student_output != expected_output:
					passed = False
					message = "Sorry, try again.\n\n'" + response['output'] + "'\n\nis not \n'" + expected_output +"'"
					#differ = difflib.HtmlDiff()
					#message = message + differ.make_table(response.output, exercise.valid_output)
					break
				else:
					message = response['output']

		return {'passed':passed, 'message':message, 'response':response}

	def checkKeywords(self, submission):
		message = ''
		passed = True
		code = utils.remove_comments(submission)
		for word in self.keywords:
			if not re.compile(r'\b({0})\b'.format(word)).search(code):
				passed=False
				message = "You did not use '%s'" % word
		return {'passed':passed, 'message':message}

	def checkRandom(self, submission, username=""):
		message = ''
		passed = True

		response = list(self.submit(submission, username=username))
		for x in xrange(1,3):
			response.append(self.submit(submission, username=username))
			for y in xrange(0,x-1):
				if (not response[x]['output'] or 
					not response[y]['output'] or 
					response[x]['output'] == response[y]['output']):
						passed=False
						message= "This program has the same output every time, it is not random."
		return {'passed':passed, 'message':message, 'response':response}

class Exercise(utils.Model):
	name         = db.StringProperty(required=True)
	url          = db.StringProperty(required=True)
	description  = db.TextProperty(required=True)
	start_code   = db.TextProperty(required=True)
	checker      = db.ReferenceProperty(ExerciseChecker)
	flowchart    = blobstore.BlobReferenceProperty()
	outside_code = db.TextProperty(default="{0}")
	due_date     = db.DateTimeProperty()

	@classmethod
	def warmup(cls):
		if Exercise.query().count()==0:
			logging.info("Warming up Exercises")
			path = os.path.join(os.path.dirname(__file__), 'exercises.json')
			warmups = json.loads(open(path, 'r').read())
			for e in warmups:
				c = e['checker']
				used_methods = [method for method in c['test_methods']]

				inputs = [db.Text(i) for i in c['test_input'].split(';')]
				outputs = [db.Text(o) for o in c['output'].split(';')]
				keywords = [unicode(k) for k in c['keywords'].split(';')]


				checker = ExerciseChecker(	test_methods=used_methods,
												inputs=inputs,
												outputs=outputs,
												keywords=keywords)
				checker.put()
				exercise = Exercise(name=e['name'], 
									url=e['url'], 
									description=string.replace(e['description'], '\n', '<br>'),
									start_code=e['start_code'],
									checker=checker)
				exercise.put()

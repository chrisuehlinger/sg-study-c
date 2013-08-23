import json
import time
import utils
import urllib
import re
import string
from utils import db
import logging
from ideoneclient import IdeoneClient
import difflib
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

test_methods = ['Input/Output', 'Check Keywords', 'Randomness Test']

warmups = [
{	'name':'Hello World',
	'url':'hello',
	'description':'Write a program that outputs "Hello World!".',
	'start_code':'''#include<stdio.h>

int main()
{
	//Code here

	return 0;
}''',
	'checker':{	'test_methods':['Input/Output'],
				'test_input':'none',
				'output':'Hello World!',
				'keywords':''}
},
{	'name':'If Statements',
	'url':'if',
	'description':'''Write a program that asks the user:

How old are you?

If the user is 18 or older, the program should say:

You can drive a car.

If the user is under 18 years old, the program should say:

You will have to walk.''',
	'start_code':'''#include<stdio.h>

int main()
{
	printf("How old are you?\\n");

	return 0;
}''',
	'checker':{	'test_methods':['Input/Output', 'Check Keywords'],
				'test_input':'23;5;18',
				'output':'''How old are you?
You can drive a car.;How old are you?
You will have to walk.;How old are you?
You can drive a car.''',
				'keywords':'if;else'}
}
]

class ExerciseChecker(db.Model):
	test_methods = db.ListProperty(str)
	outside_code = db.ListProperty(db.Text)
	inputs = db.ListProperty(db.Text)
	outputs = db.ListProperty(db.Text)
	keywords = db.ListProperty(unicode)

	def checkWork(self, submission):
		message = ''
		passed = True
		response = dict()

		if "Input/Output" in self.test_methods:
			test_result = self.ioTest(submission)
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
			test_result = self.checkRandom(submission)
			if not test_result['passed']:
				passed = False
			message = message + test_result['message']
		
		response['passed'] = passed
		response['message'] = message

		if passed:
			response['message'] = "Great job!"
		
		return response

	def ioTest(self, submission):
		client = IdeoneClient()
		passed = True
		message = ""
		response = dict()
		for i in self.inputs:
			response = client.submit(submission, i)
			expected_output = self.outputs[self.inputs.index(i)]

			if response['error'] != "OK" or int(response['result']) != 15 or response['output'] is None:
				passed = False
				message = "Sorry, try again.\n\n" + response['error_message']
				break
			elif response['output'] != expected_output:
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

	def checkRandom(self, submission):
		message = ''
		passed = True
		response = list(response.append(client.submit(submission)))
		for x in xrange(1,3):
			response.append(client.submit(submission))
			for y in xrange(0,x-1):
				if response[x] == response[y]:
					passed=False
					message= "This program has the same output every time, it is not random."
		return {'passed':passed, 'message':message, 'response':response}

class Exercise(db.Model):
	name = db.StringProperty(required=True)
	url = db.StringProperty(required=True)
	description = db.TextProperty(required=True)
	start_code = db.TextProperty(required=True)
	checker = db.ReferenceProperty(ExerciseChecker)
	flowchart = blobstore.BlobReferenceProperty()
	due_date = db.DateTimeProperty()

	@classmethod
	def warmup(cls):
		if db.Query(Exercise).count()==0:
			logging.info("Warming up Exercises")
			for e in warmups:
				used_methods = list()
				c = e['checker']
				for method in c['test_methods']:
					used_methods.append(method)

				inputs = list()
				for i in c['test_input'].split(';'):
					inputs.append(db.Text(i))

				outputs = list()
				for o in c['output'].split(';'):
					outputs.append(db.Text(o))

				keywords = list()
				for k in c['keywords'].split(';'):
					keywords.append(unicode(k))

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

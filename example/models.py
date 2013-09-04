from utils import db
import utils
import logging
import string
import os
import json
from ideoneclient import IdeoneClient
from coliruclient import ColiruClient

class Example(utils.Model):
	name        = db.StringProperty(required=True)
	url         = db.StringProperty(required=True)
	description = db.TextProperty(required=True)
	start_code  = db.TextProperty(required=True)
	takes_input = db.BooleanProperty(default=False)
	test_input  = db.TextProperty(default="")

	@classmethod
	def warmup(cls):
		if Example.query().count()==0:
			logging.info("Warming up Examples")
			path = os.path.join(os.path.dirname(__file__), 'examples.json')
			logging.info(open(path, 'r').read())
			warmups = json.loads(open(path, 'r').read())

			for e in warmups:
				example = Example(name=e['name'], 
									url=e['url'], 
									description=string.replace(e['description'], '\n', '<br>'),
									start_code=db.Text(e['start_code']),
									takes_input=e['takes_input'])
				
				if example.takes_input:
					example.test_input = e['test_input']

				example.put()

	@classmethod
	def submit(cls, submission, username="", the_input=""):
		col_client = ColiruClient()
		response = col_client.submit(submission, the_input)

		if response['error'] != "OK":
			client = ideoneclient.IdeoneClient()
			user = User.query().filter('username = ', self.username).get()
			if user and user.ideone_acct:
				client.change_account(user.ideone_acct)

			response = client.submit(submission, the_input)

		return response
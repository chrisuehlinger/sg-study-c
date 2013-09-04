from utils import db
import utils
import logging
import string
import os
import json

class Example(utils.Model):
	name        = db.StringProperty(required=True)
	url         = db.StringProperty(required=True)
	description = db.TextProperty(required=True)
	start_code  = db.TextProperty(required=True)
	takes_input = db.BooleanProperty(default=False)

	@classmethod
	def warmup(cls):
		if Example.query().count()==0:
			logging.info("Warming up Examples")
			path = os.path.join(os.path.dirname(__file__), 'examples.json')
			warmups = json.loads(open(path, 'r').read())

			for e in warmups:
				example = Example(name=e['name'], 
									url=e['url'], 
									description=string.replace(e['description'], '\n', '<br>'),
									start_code=db.Text(e['start_code']),
									takes_input=e['takes_input'])
				example.put()
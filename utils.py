from google.appengine.ext import db
import logging
import jinja2
import string
import os
import webapp2
import hmac
import time
import re
import json

styles = {'old_reliable':'Old Reliable',
		  'the_new_style':'The NEW Style'}

codemirror_themes = [
'3024-day',
'3024-night',
'ambiance-mobile',
'ambiance',
'base16-dark',
'base16-light',
'blackboard',
'cobalt',
'eclipse',
'elegant',
'erlang-dark',
'lesser-dark',
'midnight',
'monokai',
'neat',
'night',
'rubyblue',
'solarized',
'tomorrow-night-eighties',
'twilight',
'vibrant-ink',
'xq-dark',
'xq-light'
]

index = [	{'group':'The Basics', 'topics': [	#{'url':"whatis", 'topic_name':"What is C?", 'examples':[]},
												{'url':"basic_syntax", 'topic_name':"Basic Syntax", 'examples':[]},
												{'url':"math", 'topic_name':"Basic Math in C", 'examples':[]},
												{'url':"compiler", 'topic_name':"The Compiler", 'examples':[]},
												{'url':"errors", 'topic_name':"Fixing Errors", 'examples':[]}]
			},
			{'group':'Values', 'topics': [		{'url':"variables", 'topic_name':"Variables and Types", 'examples':[]},
												{'url':"constants", 'topic_name':"Constants", 'examples':['constant']},
												#{'url':"strings", 'topic_name':"Strings", 'examples':[]},
												{'url':"input_output", 'topic_name':"Input and Output", 'examples':[]}]
			}, 
			{'group':'Control Flow', 'topics':[ {'url':"conditions", 'topic_name':"If, Else and Conditions", 'examples':['logical_operators', 'strcmp']},
												{'url':"switch_case", 'topic_name':"Switch-Case Statements", 'examples':[]},
												{'url':"while", 'topic_name':"While and Do-While Loops", 'examples':[]},
												{'url':"for", 'topic_name':"For Loops", 'examples':[]}]
			},
			{'group':'Other Topics', 'topics':[ {'url':"random", 'topic_name':"Random Numbers", 'examples':[]},
												{'url':"functions", 'topic_name':"Functions", 'examples':[]},
												{'url':"arrays", 'topic_name':"Arrays", 'examples':[]},
												{'url':"files", 'topic_name':"File Input/Output", 'examples':[]}]
			},
			{'group':'Advanced Topics','topics':[{'url':'time', 'topic_name':'Time in C', 'examples':[]},
			# 									{'url':"preprocessor", 'topic_name':"Pre-Processor Commands"},
			 									{'url':"structs", 'topic_name':"Structs", 'examples':[]},
			 									{'url':"fork", 'topic_name':"fork() and Multithreading", 'examples':[]},
												{'url':"unicode", 'topic_name':"UNICODE", 'examples':[]}]
			},
			{'group':'The Final', 'topics':[	{'url':"final_project", 'topic_name':"THE FINAL PROJECT", 'examples':[]},
												{'url':"whatsnext", 'topic_name':"What's Next?", 'examples':[]}]
			}
		]

jinja_environment = jinja2.Environment(	autoescape=True,
    									loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

lastQuery=time.time()

def time_since_query():
	return round(time.time()-lastQuery, 2)

SECRET = "Everything That Happens Will Happen Today"

def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
	if h:
		val = h.split('|')[0]
		if h == make_secure_val(val):
			return val

def render_str(template_name, template_values={}):
	template = jinja_environment.get_template(template_name)
	return template.render(template_values)

def remove_comments(code):
	return re.sub(r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)', '', code, flags=re.MULTILINE)

class Handler(webapp2.RequestHandler):
	stylesheet = 'the_new_style'
	codemirror_theme = 'night'

	def write(self,output=""):
		self.response.out.write(output)

	def write_json(self,object={}):
		self.response.headers['Content-Type'] = 'application/json'
		self.write(json.dumps(object))

	def render(self,template_name, template_values={}):
		template_values['groups'] = index
		template_values['stylesheet'] = self.stylesheet
		template_values['codemirror_theme'] = self.codemirror_theme
		self.write(render_str(template_name, template_values))

	def set_secure_cookie(self, name, value):
		cookie = make_secure_val(value)
		self.response.headers.add_header("Set-Cookie", str("%s=%s; Path=/" % (name,cookie)))

	def get_cookie(self, name):
		cookie = self.request.cookies.get(name, 0)
		return check_secure_val(cookie)

	def delete_cookie(self, name):
		self.response.headers.add_header("Set-Cookie", str("%s=; Path=/" % name))

class Model(db.Model):
	@classmethod
	def query(cls):
		logging.info("DB Query - %s" % cls)
		return db.Query(cls)

import datetime
import json
import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)


class Candidate(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(100))
  last_name = db.Column(db.String(100))
  email = db.Column(db.String(250))
  # Idealy use an ENUM here - starting with string for ease of implementation
  race_ethnicity = db.Column(db.String(100))
  age = db.Column(db.Integer)
  # Idealy use an enum here
  gender = db.Column(db.String(100))
  # Idealy use an enum here
  education = db.Column(db.String(100))
  # Idealy use an enum here
  first_language = db.Column(db.String(100))
  accepted_tac = db.Column(db.Boolean)
  created = db.Column(db.DateTime)

  def __init__(self):
    self.created = datetime.datetime.utcnow()

class Evaluation(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  created = db.Column(db.DateTime)
  completed = db.Column(db.DateTime)
  candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))

  def __init__(self):
    self.created = datetime.datetime.utcnow()


class Question(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  question_index = db.Column(db.Integer)
  text = db.Column(db.String(2500))
  answer = db.Column(db.String(2500))
  evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluation.id'))
  evaluation = db.relationship("Evaluation")


REQUIRED_CANDIDATE_FIELDS = ['first_name',
                             'last_name',
                             'email',
                             'race',
                             'age',
                             'gender',
                             'edu',
                             'lang',
                             'tac']


# TODO(dgriff): Move this to a database table of "Questions" + table "Survey"
QUESTION_LIST = [
  'In your career thus far, what has been your favorite job and least favorite job and why?',
  'What do you hope to be doing professionally five years from now?',
  'Please write a sample email to a client asking to follow up on a recent sales call',
  'Imagine that you are hired to work at a home repair company. Please describe how you would go about generating customers for your new company.',
  'What is a CRM? What are the greatest benefits of using a CRM?'
]



# Length of answers is confirmed to be equal to QUESTION_LIST before calling.
def add_questions(eval_id, answers):
  for i, answer in enumerate(answers):
    q = Question()
    q.question_index = i
    q.text = QUESTION_LIST[i]
    q.answer = answer
    evaluation_id = eval_id
    db.session.add(candidate)
    db.session.commit()


# Ballpark approximation for a 'real' email
def validate_email(email):
  split = email.split('@')
  if len(split) != 2:
    return False
  if split[1].count('.') < 1:
    return False
  return True


# Returns a Candidate object if the form data is valid, otherwise returns None.
# TODO(daniel): Return which fields caused the error.
def candidate_from_form(form):
  print form
  for field in REQUIRED_CANDIDATE_FIELDS:
    if field not in form or not form[field]:
      print "error on {}".format(field)
      return None
  if not validate_email(form['email']):
    return None
  candidate = Candidate()
  candidate.first_name = form['first_name']
  candidate.last_name = form['last_name']
  candidate.email = form['email']
  candidate.race_ethnicity = form['race']
  candidate.education = form['edu']
  candidate.first_language = form['lang']
  if type(form['tac']) == bool:
    candidate.accepted_tac = form['tac']
  else:
    candidate.accepted_tac = form['tac'].lower() == 'true'
  try:
    int(form['age'])
  except:
    return None
  if int(form['age']) <= 0:
    return None
  candidate.age = int(form['age'])
  return candidate


@app.route('/', methods=['GET'])
def index():
  return render_template('index.html', users=Candidate.query.all())


@app.route('/user', methods=['POST'])
def user():
  candidate = candidate_from_form(request.form)
  if candidate is None:
    # TODO(Daniel): Show error page
    return redirect(url_for('index'))
  db.session.add(candidate)
  db.session.commit()
  # Refirect to the format page -- pass the candidate ID!!!
  # db.session.flush()
  # db.session.refresh(candidate)
  return redirect(url_for('index'))


# TODO(Daniel): Should probably obfuscate the user id at some point...
@app.route('/exam/<candidate_id>', methods=['GET'])
def exam(candidate_id):
  return render_template('question.html',
    candidate_id=candidate_id,
    question_list=QUESTION_LIST,
    num_questions=len(QUESTION_LIST))


# Data format:
# {
#  eval_id: <num>
#  answers : [string...] // In order of questions
# }
@app.route('/evaluation', methods=['POST'])
def evaluation():
  if 'eval_id' not in request.form:
    print "Missing eval_id"
    return redirect(url_for('index'))
  if 'answers' not in request.form or len(request.form['answers']) != len(QUESTION_LIST):
    print "Missing answers"
    return redirect(url_for('index'))
  eval_id = int(request.form['eval_id'])
  evaluation = Evaluation.query.get(eval_id)
  if not evaluation:
    print "Missing eval_id"
    return redirect(url_for('index'))
  evaluation.completed = datetime.datetime.utcnow()
  db.session.commit()
  add_questions(eval_id, request.form['answers'])
  return redirect(url_for('index'))



if __name__ == '__main__':
  db.create_all()
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)


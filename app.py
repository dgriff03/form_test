import datetime
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


REQUIRED_CANDIDATE_FIELDS = ['first_name',
                             'last_name',
                             'email',
                             'race',
                             'age',
                             'gender',
                             'edu',
                             'lang',
                             'tac']

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

if __name__ == '__main__':
  db.create_all()
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)

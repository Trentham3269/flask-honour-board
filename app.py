from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine('postgresql:///honourboard', echo=True)

Base = declarative_base()

class Winner(Base):
	__tablename__ = 'winners'

	id = Column(Integer, primary_key=True)
	first_name = Column(String(25))
	last_name = Column(String(25))

	def ___init__(self, id=None, first_name=None, last_name=None):
		self.id = id
		self.first_name = first_name
		self.last_name = last_name

	def __repr__(self):
		return "<Winner(first_name='%s', last_name='%s')>" % (self.first_name, self.last_name)

	def serialize(self):
		return {
			'id': self.id,
			'First Name': self.first_name,
			'Last Name': self.last_name,
			'Full Name':"{0} {1}".format(self.first_name, self.last_name)
		}
			
class Competition(Base):
	__tablename__ = 'competitions'

	id = Column(Integer, primary_key=True)
	year = Column(Integer)
	championship = Column(String(10))
	winner = Column(Integer, ForeignKey('winners.id'))

	def __init__(self, id=None, year=None, championship=None, winner=None):
		self.id = id
		self.year = year
		self.championship = championship
		self.winner = winner

	def __repr__(self):
		return "<Competition(year='%s', championship='%s', winner='%i')>" % (self.year, self.championship, self.winner)

	def serialize(self):
		return {
			'id': self.id,
			'Year': self.year,
                        'Championship': self.championship,
			'Winner id': self.winner
		}
             
Session = sessionmaker(bind=engine)
session = Session()

from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route('/api/winner/<int:id>')
def winner(id):
	winner = session.query(Winner).filter_by(id=id).first()
	return jsonify(winner.serialize())

@app.route('/api/competition/<int:id>')
def competition(id):
	competition = session.query(Competition).filter_by(id=id).first()
	return jsonify(competition.serialize())

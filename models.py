#!/usr/local/bin/python3

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship

engine = create_engine('postgresql:///honourboard', echo=True)

Base = declarative_base()

class Winner(Base):
	__tablename__ = 'winners'

	id = Column(Integer, primary_key=True)
	first_name = Column(String(25))
	last_name = Column(String(25))
	competitions = relationship('Competition')

	def __init__(self, id, first_name, last_name, competitions):
		self.id = id
		self.first_name = first_name
		self.last_name = last_name
		self.competitions = competitions

	def __repr__(self):
		return '{0} {1}, {2} {3}'.format('Winner :', self.first_name, self.last_name, 'Wins :', len(self.competitions))

	def serializeWinner(self):
		return {
    		'id': self.id,
    		'name': '{0} {1}'.format(self.first_name, self.last_name),
    		'wins': [w.serialize() for w in self.competitions]
    	}

	def serializeWinners(self):
		return {
			'id': self.id,
			'name': '{0} {1}'.format(self.first_name, self.last_name),
			'win_count': len(self.competitions)
		}

class Competition(Base):
	__tablename__ = 'competitions'

	id = Column(Integer, primary_key=True)
	year = Column(Integer)
	championship = Column(String(10))
	winner = Column(Integer, ForeignKey('winners.id'))

	def __init__(self, id, year, championship, winner):
		self.id = id
		self.year = year
		self.championship = championship
		self.winner = winner

	def __repr__(self):
		return '{0} {1}, {2} {3}, {4} {5}'.format('Year :', self.year, 'Championship :', self.championship, 'Winner :', self.winner)

	def serializeCompetition(self):
		return {
			'year': self.year,
			'championship': self.championship,
            'winner': self.winner
		}
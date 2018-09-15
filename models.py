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
	competitions = relationship("Competition")

	def __init__(self, id=None, first_name=None, last_name=None):
		self.id = id
		self.first_name = first_name
		self.last_name = last_name

	def __repr__(self):
		return "[ Winner: {0} {1}, Wins: {2} ]".format(self.first_name, self.last_name, len(self.competitions) )

	def serializeWinners(self):
		return {
			'id': self.id,		
			'first_name': self.first_name,
			'last_name': self.last_name,
			'win_count': len(self.competitions)
		}
	
	def serialize(self):
		return {
			'id': self.id,
			'full_name':"{0} {1}".format(self.first_name, self.last_name),
			'wins': [w.serialize() for w in self.competitions]
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
		return "[ Year:{0}, Championship={1}, Winner={2} ]".format(self.year, self.championship, self.winner)

	def serialize(self):
		return {
			'id': self.id,
			'year': self.year,
            'championship': self.championship,
		}
          
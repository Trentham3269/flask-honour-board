from flask import Flask
from flask import jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc, func
from models import engine, Winner, Competition


app = Flask(__name__)

Session = sessionmaker(bind=engine)
session = Session()

# Endpoint for top n winners
@app.route('/api/winners/<int:k>')
def winners(k):
	winners = session.query(Winner).\
		join(Competition).\
		group_by(Winner.id).\
		order_by(desc(func.count(Competition.id))).\
		limit(10).\
		all()
	# return str(winners)
	# print(winners[0])
	# return "woohooo"
	return jsonify([w.serializeWinners() for w in winners])

# Endpoint to list individual's wins
@app.route('/api/winner/<int:id>')
def winner(id):
	winner = session.query(Winner).\
		 filter_by(id=id).\
		 first()
	return jsonify(winner.serialize())

@app.route('/api/competition/<int:id>')
def competition(id):
	competition = session.query(Competition).\
		      filter_by(id=id).\
		      first()
	return jsonify(competition.serialize())

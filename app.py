from flask import Flask, jsonify, send_from_directory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc, func
from models import engine, Winner, Competition

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

# Serve index.html
@app.route('/')
def index():
	# return send_from_directory(directory="static", filename="index.html")
	return '{0}, {1}'.format('Test', 'ing!')

# Endpoint for top n winners
@app.route('/api/winners/<int:n>')
def winners(n):
	winners = session.query(Winner).\
				join(Competition).\
				group_by(Winner.id).\
				order_by(desc(func.count(Competition.id))).\
				limit(n).\
				all()	
	return jsonify([w.serializeWinners() for w in winners])

# Endpoint to list individual's wins
@app.route('/api/winner/<int:id>')
def winner(id):
	winner = session.query(Winner).\
				filter_by(id=id).\
				first()
	return jsonify(winner.serializeWinner())

# Endpoint to list a championship's winners
@app.route('/api/competition/<string:championship>')
def competition(championship):
	competition = session.query(Competition).\
					filter_by(championship=championship).\
					order_by(desc(Competition.year)).\
					all()	
	return jsonify([c.serializeCompetition() for c in competition])



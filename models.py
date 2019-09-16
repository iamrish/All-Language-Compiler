from temp_back import db

class Model(db.Model):

	__tablename__ = "data"

	username = db.Column(db.String, primary_key = True, unique=True, nullable=False)
	error = db.Column(db.Integer, nullable = True)
	corrected = db.Column(db.Integer, nullable = True )
	typing_speed = db.Column(db.Float, nullable=True)

	def __init__(self, username, typing_speed=0, error=0, corrected=0) :
		self.error = error
		self.corrected = corrected
		self.username = username
		self.typing_speed = typing_speed

	def __repr__(self):
		return '<User: {}, Errors: {}, Corrected: {}, Typin Speed: {}'.format(self.username, self.error, \
			self.corrected, self.typing_speed)
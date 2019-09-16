from flask import Flask, render_template, \
 url_for, redirect, request, flash, session, jsonify
from datetime import timedelta
import os, time
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = "ABC"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///sess.db'
db = SQLAlchemy(app)

from models import *



def calCompileTime(language):
	cmd  = "./compile haha."+ language + " &> compile_time.txt"
	os.system(cmd)
	f = open("compile_time.txt", "r")
	compile_time = f.read()
	f.close()
	return compile_time

def checkEmpty(filename):
	with open(filename) as my_file:
		my_file.seek(0, os.SEEK_END)
		if my_file.tell():
			return 0 
				
		else:
			return 1



@app.route('/', methods= ['GET', 'POST'])
def home():

	
	if request.method == 'POST':

		username = "Rishabh"

		# Takes input from form	
		code = request.form['code']
		language = request.form['language']
		typing_time = request.form['typing_time']
		typing_speed = len(code)*1000/int(typing_time)
		print(code)
		print(language)
		print(typing_time)
		print("typing_speed:", typing_speed)
		
		# Writes in a file named 'haha' along with an extension of that language
		f = open("haha."+language, "w")
		f.write(code)
		f.close()

		# Calculate the compile time
		cmd  = "./compile haha."+ language + " 2> compile_time.txt"
		os.system(cmd)
		f = open("compile_time.txt", "r")
		compile_time = f.read()
		f.close()
		print("compile_time:", compile_time)
		# time.sleep(1)

		# Directs stdout to a file therefore, no error will be directed
		cmd  = "./compile haha."+ language + " > output.txt"
		os.system(cmd)
		f = open("output.txt", "r")
		output = f.read()
		print("1: "+ str(output) + "\n")
		f.close()

		# Checks if file is empty
		error_flag = 0
		error_flag = checkEmpty("output.txt")

		# username will be generated using random string for every visit
		user = Model.query.filter_by(username=username).first()


		# File is empty i.e. there exists some error
		if error_flag:  

			# Write the error to a file
			print("Empty File!")
			cmd  = "./compile haha."+ language + " > output.txt 2>&1"
			os.system(cmd)

			# if a new user
			if user == None	:
				new_user = Model(username=username, error=1)
				db.session.add(new_user)
				db.session.commit()

			# existing user? add to errors
			else:
				user_errors = user.error
				user_errors += 1
				user.error = user_errors
				db.session.commit()


		# If file 'output.txt' is not empty, i.e. no error present in the code
		else:

			# if a new user
			if user == None	:
				new_user = Model(username=username)
				db.session.add(new_user)
				db.session.commit()	

			# the user exists in the error table
			else:
				user_corrected = user.corrected
				user_error = user.error
				user_corrected = user_corrected + 1
				if user_corrected > user_error:
					user_corrected -= 1
				user.corrected = user_corrected



		user.typing_speed = typing_speed
		db.session.commit()

		# Retrieves output from output.txt
		f = open("output.txt", "r")
		output = f.read()
		print("2: "+ str(output) + "\n")
		f.close()

		# Empties 'output.txt'
		open("output.txt", 'w').close()
		os.remove("haha."+language)
		print("compile_time:", compile_time)
		try:
			os.remove("c")
			os.remove("cpp")
			os.remove("haha")
			os.remove("output.txt")
		except:
			pass

		print("Next is the return statement")
		return jsonify({"code": code, "output": output})

	return render_template("webpage.html")


if __name__ == '__main__':

	app.run(debug=True)

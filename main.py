
import pymysql
from app import app
from tables import Results
from db_config import mysql
from flask import flash, render_template, request, redirect

conn = mysql.connect()
cursor = conn.cursor()
@app.route('/new_user')
def add_user_view():
	return render_template('add.html')
		
@app.route('/add', methods=['POST'])
def add_user():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()		
		_fname = request.form['firstName']
		_lname = request.form['lastName']
		_email = request.form['inputEmail']
		_phone = request.form['phone']
		# validate the received values
		if _fname and _lname and _email and _phone and request.method == 'POST':
			# save edits
			sql = "INSERT INTO myproject6(firstName, lastName,email, phone) VALUES(%s, %s, %s,%s)"
			data = (_fname,_lname, _email, _phone,)
			cursor.execute(sql, data)
			conn.commit()
		
			return redirect('/')
		else:
			return 'Error while adding user'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/')
def users():
	try:

		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM myproject6")
		row = cursor.fetchall()
		
		return render_template('users.html', row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/edit/<int:id>')
def edit_view(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM myproject6 WHERE user_id=%s", id)
		row = cursor.fetchone()
		if row:
			return render_template('edit.html', row=row)
		else:
			return 'Error loading #{id}'.format(id=id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/update', methods=['POST'])
def update_user():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()		
		_fname = request.form['firstName']
		_lname = request.form['lastName']
		_email = request.form['inputEmail']
		_phone = request.form['phone']
		_id = request.form['id']
		# validate the received values
		if _fname and _lname and _email and _phone and _id and request.method == 'POST':
			# save edits
			sql = "UPDATE myproject6 SET firstName=%s,lastName=%s, email=%s, phone=%s WHERE user_id=%s"
			data = (_fname,_lname, _email, _phone, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('User updated successfully!')
			return redirect('/')
		else:
			return 'Error while updating user'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/delete/<int:id>')
def delete_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM myproject6 WHERE user_id=%s", (id,))
		conn.commit()
		return redirect('/')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
if __name__ == "__main__":
    app.run(debug=True)
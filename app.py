from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Paru@244455' # Update with your MySQL password
app.config['MYSQL_DB'] = 'task_management'

db = MySQL(app)

@app.route('/')
def index():
    if 'loggedin' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM manager WHERE username = %s AND password = %s", (username, password))
        manager_account = cursor.fetchone()
        cursor.close()
        
        if manager_account:
            session['loggedin'] = True
            session['username'] = manager_account['username']
            return redirect(url_for('dashboard'))
        else:
            msg = 'Incorrect username or password!'
            
    return render_template('login.html', msg=msg)

@app.route('/dashboard')
def dashboard():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add_task_page')
def add_task_page():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    return render_template('add_task.html')

@app.route('/api/task_titles', methods=['GET'])
def get_task_titles():
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT title_id, title FROM task_title")
    titles = cursor.fetchall()
    cursor.close()
    return jsonify(titles)

@app.route('/api/employees', methods=['GET'])
def get_employees():
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT employee_id, employee_name FROM employee")
    employees = cursor.fetchall()
    cursor.close()
    return jsonify(employees)

@app.route('/api/title/<int:title_id>/instances', methods=['GET'])
def get_title_instances(title_id):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT t.task_id, t.completed, e.employee_id, e.employee_name
        FROM task t
        JOIN employee e ON t.employee_id = e.employee_id
        WHERE t.title_id = %s
    """, (title_id,))
    instances = cursor.fetchall()
    cursor.close()
    return jsonify(instances)

@app.route('/api/tasks/update_status', methods=['POST'])
def update_task_status():
    data = request.json
    task_id = data.get('task_id')
    completed = data.get('completed')
    
    cursor = db.connection.cursor()
    cursor.execute("UPDATE task SET completed = %s WHERE task_id = %s", (completed, task_id))
    db.connection.commit()
    cursor.close()
    
    return jsonify({"success": True})

@app.route('/api/tasks/add', methods=['POST'])
def add_task():
    data = request.json
    title_id = data.get('title_id')
    employee_id = data.get('employee_id')
    completed = data.get('completed')
    
    db_completed = 1 if completed == 'Yes' else 0
    
    cursor = db.connection.cursor()
    cursor.execute("INSERT INTO task (employee_id, title_id, completed) VALUES (%s, %s, %s)", 
                   (employee_id, title_id, db_completed))
    db.connection.commit()
    cursor.close()
    
    return jsonify({"success": True, "message": "Task assigned successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
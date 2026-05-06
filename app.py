import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')

# Initialize MySQL
mysql = MySQL(app)

def init_db():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT
        );
        ''')
        mysql.connection.commit()  
        cur.close()

@app.route('/')
def hello():
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': new_message})

# New Webhook Route
@app.route('/github-webhook/', methods=['POST'])
def handle_webhook():
    # GitHub sends data as JSON
    data = request.json
    
    if data:
        pusher = data.get('pusher', {}).get('name', 'Unknown')
        repo = data.get('repository', {}).get('full_name', 'Unknown')
        commit_msg = data.get('head_commit', {}).get('message', 'No commit message')
        
        log_entry = f"GitHub Webhook: {pusher} pushed to {repo} - '{commit_msg}'"
        print(f"✅ {log_entry}")
        
        # Automatically insert the webhook event into your database
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO messages (message) VALUES (%s)', [log_entry])
            mysql.connection.commit()
            cur.close()
            return jsonify({'status': 'success', 'received': log_entry}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    else:
        return jsonify({'status': 'invalid payload'}), 400

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

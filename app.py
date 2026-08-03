import sqlite3
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
DB_NAME = 'tracker.db'

# Initialize database and create table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity TEXT NOT NULL,
            calories INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fitness & Calorie Tracker</title>
    <style>
        * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; }
        body { background-color: #0f172a; color: #f8fafc; display: flex; justify-content: center; padding: 40px 20px; }
        .container { width: 100%; max-width: 500px; background: #1e293b; padding: 30px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
        h1 { text-align: center; font-size: 1.8rem; margin-bottom: 20px; color: #38bdf8; }
        .stat-card { background: #334155; padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 25px; }
        .stat-card h2 { font-size: 2rem; color: #4ade80; }
        form { display: flex; flex-direction: column; gap: 12px; margin-bottom: 25px; }
        input { padding: 12px; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: #fff; font-size: 1rem; }
        input:focus { outline: none; border-color: #38bdf8; }
        button { padding: 12px; border-radius: 8px; border: none; background: #38bdf8; color: #0f172a; font-weight: bold; font-size: 1rem; cursor: pointer; transition: 0.2s; }
        button:hover { background: #7dd3fc; }
        ul { list-style: none; display: flex; flex-direction: column; gap: 10px; }
        li { background: #334155; padding: 12px 16px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }
        .calories-eaten { color: #f87171; font-weight: bold; }
        .calories-burned { color: #4ade80; font-weight: bold; }
        .delete-btn { color: #94a3b8; text-decoration: none; font-size: 0.8rem; margin-left: 10px; }
        .delete-btn:hover { color: #f87171; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ Calorie Tracker</h1>
        
        <div class="stat-card">
            <p style="font-size: 0.9rem; color: #94a3b8;">Net Calories</p>
            <h2>{{ total_calories }} kcal</h2>
        </div>

        <form action="/add" method="POST">
            <input type="text" name="activity" placeholder="Activity or Food (e.g. Apple, Running)" required>
            <input type="number" name="calories" placeholder="Calories (+ for food, - for exercise)" required>
            <button type="submit">Add Log</button>
        </form>

        <h3>Activity Log</h3>
        <br>
        <ul>
            {% for item in logs %}
                <li>
                    <span>{{ item[1] }}</span>
                    <div>
                        <span class="{{ 'calories-eaten' if item[2] > 0 else 'calories-burned' }}">
                            {{ '+' if item[2] > 0 else '' }}{{ item[2] }} kcal
                        </span>
                        <a href="/delete/{{ item[0] }}" class="delete-btn">✕</a>
                    </div>
                </li>
            {% else %}
                <p style="color: #64748b; text-align: center;">No logs saved yet.</p>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, activity, calories FROM logs')
    logs = cursor.fetchall()
    conn.close()

    total_calories = sum(item[2] for item in logs)
    return render_template_string(HTML_TEMPLATE, logs=logs, total_calories=total_calories)

@app.route('/add', methods=['POST'])
def add():
    activity = request.form.get('activity')
    try:
        calories = int(request.form.get('calories'))
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO logs (activity, calories) VALUES (?, ?)', (activity, calories))
        conn.commit()
        conn.close()
    except ValueError:
        pass
    return redirect(url_for('home'))

@app.route('/delete/<int:log_id>')
def delete(log_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM logs WHERE id = ?', (log_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

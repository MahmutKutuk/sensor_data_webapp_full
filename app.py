from flask import Flask, render_template, request, jsonify, send_file, Response
import sqlite3, csv, os, io, datetime, random, json

app = Flask(__name__, static_folder='static')

DB = 'sensor_data.db'
CSV_LOG = os.path.join('data', 'sensor_log.csv')

def init_db():
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('''CREATE TABLE sensor_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_type TEXT,
            value REAL,
            date TEXT
        )''')
        # insert some sample data
        now = datetime.datetime.now()
        for i in range(1,121):
            d = (now - datetime.timedelta(minutes=120-i)).strftime('%Y-%m-%d %H:%M:%S')
            sensor = random.choice(['sicaklik','voltaj','akim'])
            val = round(random.uniform(24.0, 31.0) if sensor=='sicaklik' else (random.uniform(3.4,4.2) if sensor=='voltaj' else random.uniform(0.4,1.6)), 2)
            c.execute("INSERT INTO sensor_logs (sensor_type, value, date) VALUES (?,?,?)", (sensor, val, d))
        conn.commit()
        conn.close()

def query_db(query, params=()):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/sensors')
def sensors():
    return render_template('sensors.html')

@app.route('/api/sensors')
def api_sensors():
    # return last value per sensor type
    rows = query_db("SELECT sensor_type, value, date FROM sensor_logs WHERE id IN (SELECT MAX(id) FROM sensor_logs GROUP BY sensor_type)")
    data = [{'sensor_type': r[0], 'value': r[1], 'date': r[2]} for r in rows]
    return jsonify(data)

@app.route('/api/data')
def api_data():
    sensor = request.args.get('sensor', None)
    start = request.args.get('start', None)
    end = request.args.get('end', None)
    query = "SELECT id, sensor_type, value, date FROM sensor_logs WHERE 1=1"
    params = []
    if sensor:
        query += " AND sensor_type = ?"
        params.append(sensor)
    if start:
        query += " AND date >= ?"
        params.append(start)
    if end:
        query += " AND date <= ?"
        params.append(end)
    query += " ORDER BY date ASC"
    rows = query_db(query, params)
    data = [{'id': r[0], 'sensor_type': r[1], 'value': r[2], 'date': r[3]} for r in rows]
    return jsonify(data)

@app.route('/api/chart/<sensor_type>')
def api_chart(sensor_type):
    rows = query_db("SELECT date, value FROM sensor_logs WHERE sensor_type = ? ORDER BY date ASC", (sensor_type,))
    labels = [r[0] for r in rows]
    values = [r[1] for r in rows]
    return jsonify({'labels': labels, 'values': values})

@app.route('/download')
def download():
    # stream CSV of all data
    rows = query_db("SELECT id, sensor_type, value, date FROM sensor_logs ORDER BY date ASC")
    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(['ID','SensorType','Value','Date'])
    writer.writerows(rows)
    mem = io.BytesIO()
    mem.write(si.getvalue().encode('utf-8'))
    mem.seek(0)
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    return send_file(mem, as_attachment=True, download_name=f'sensor_export_{ts}.csv', mimetype='text/csv')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

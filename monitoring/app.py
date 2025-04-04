from flask import *
from db import DB
from ha_graph import *

app = Flask(__name__, template_folder='templates')
db = DB()

minute_range = 15

@app.route('/')
def redirection():
    return redirect('/sessions')

@app.route('/sessions')
def sessions():
    sessions = db.get_sessions()
    return render_template("sessions.html",
                           title="Sessions Table", sessions=sessions)

@app.route('/sessions/<session_id>')
def session_by_id(session_id):
    auths = db.get_auth_by_session(session_id)
    inputs = db.get_input_by_session(session_id)
    ha = db.get_sessionId_in_ha(session_id)
    print(ha)
    return render_template("session_by_id.html",
                           title=f"Session:{session_id}, IP:{ha[1]}", 
                            auths=auths, inputs=inputs, ha=ha[0])

@app.route('/home-assistant', methods=['GET', 'POST'])
def ha_tracker():
    options = ['15m', '1h', '12h', '1j', "1w"]
    if not request.form.get('option'):
        mrange = '15m'
    else:
        mrange = request.form.get('option')
    
    return render_template("ha_tracker.html",
                           title="Home-assistant live tracker",
                            minute_range=mrange,
                            options=options)

@app.route('/get_csv_data')
def get_csv_data_route():
    minute_range = request.args.get('minute_range')
    if minute_range == None:
        minute_range = '15m'
    data = ha_last_min(db, minute_range)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug = False, host='0.0.0.0', port=5000)

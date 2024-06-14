from flask import Flask, request, render_template
import time, datetime

notice_time = datetime.datetime.now() + datetime.timedelta(minutes=-5)
notice_status = 'offline'
status_html = 'status.html'


app = Flask(__name__)

@app.route('/')

def hello_world():
    return 'Hello World!'


@app.route('/status', methods=['POST', 'GET'])

def status():
    global notice_time, notice_status
    if request.method == 'POST':
        try:
            notice_time = datetime.datetime.strptime(request.form['time'], '%Y-%m-%d %H:%M:%S.%f')
            notice_status = request.form['status']
        except:
            notice_status = 'offline'
    else:
        if datetime.datetime.now() > notice_time + datetime.timedelta(minutes=5):
            notice_status = 'offline'
        return render_template(status_html, notice_time = notice_time, notice_status = notice_status)

if __name__ == '__main__':
    app.run()
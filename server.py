import main
from flask import Flask, render_template, request, redirect

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    return render_template('input.html')

@app.route('/findings')
def findings():
    print('here')
    return render_template('findings.html')


@app.route('/input/', methods=['POST'])
def input():
    question1 = request.form['question1']
    question2 = request.form['question2']
    question3 = request.form['question3']
    question4 = request.form['question4']
    question5 = request.form['question5']
    user_input = [int(question1),int(question2),int(question3),int(question4),int(question5)]

    result = main.return_response(user_input)
    age = list(result)[0]
    confidence = list(result.values())[0]
    print(result)
    return render_template('result.html', age=age,confidence=confidence)

@app.route("/download/templates/Final Writeup.pdf")
def DownloadLogFile (path = None):
    if path is None:
        self.Error(400)
    try:
        return send_file('templates/Final Writeup.pdf', as_attachment=True)
    except Exception as e:
        self.log.exception(e)
        self.Error(400)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
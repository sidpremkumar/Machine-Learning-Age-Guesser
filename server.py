import main
from flask import Flask, render_template, request, session, make_response


app = Flask(__name__, static_url_path='/static')
app.secret_key = "1201"

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
    session['user_input'] = user_input
    result = main.return_response(user_input)
    age = list(result)[0]
    confidence = list(result.values())[0]
    session['confidence'] = confidence
    session['age'] = age
    print(result)
    return render_template('result.html', age=age,confidence=confidence)

@app.route('/ageinput/', methods=['POST'])
def ageinput():
    age = request.form['age']
    user_input = session.get('user_input', 1201)
    confidence = session.get('confidence', 1201)
    theage = session.get('age', 1201)
    user_input.append(int(age))
    main.addtocsv(user_input)
    return render_template('result2.html', age=theage, confidence=confidence)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
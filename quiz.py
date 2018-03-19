from flask import Flask, render_template, request, jsonify
import time
import gc
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a very secret string'
times = []
seconds = 60

Question = [
    {'Q': 'Who invented C programming language?', 'A': 'James Gosling', 'B': 'Dennis Ritchie', 'C': 'Dennis Grunt',
     'D': 'Rich Green', 'Ans': 'B'},
    {'Q': '"Dont Be Evil" was the tagline of?', 'A': 'Microsoft', 'B': 'Skype', 'C': 'Google', 'D': 'Kaspersky', 'Ans': 'C'},
     {'Q': 'How many steps are there in SDLC?', 'A': '4', 'B': '5', 'C': '6', 'D': '10', 'Ans': 'C'},
    {'Q': 'How many bits are there in an Ethernet address?', 'A': '32', 'B': '48', 'C': '16', 'D': '64', 'Ans': 'B'},
    {'Q': 'Each IP packet must contain _______ address.', 'A': 'Only Source', 'B': 'Source or Destination',
     'C': 'Only Destination', 'D': 'Source and Destination', 'Ans': 'D'},
    {'Q': 'Tensorflow was developed by,', 'A': 'Google', 'B': 'Facebook', 'C': 'Uber', 'D': 'Microsoft', 'Ans': 'A'},
    {'Q': '______ is a basic element repeated to create a pattern.', 'A': 'Shape', 'B': 'Form', 'C': 'Motif',
     'D': 'Hue', 'Ans': 'C'},
    {'Q': 'DNS translates a domain into', 'A': 'Binary', 'B': 'Hexadecimal', 'C': 'URL', 'D': 'IP', 'Ans': 'D'},
    {'Q': '"CUDA" is a technology of', 'A': 'Nvidia', 'B': 'Intel', 'C': 'AMD', 'D': 'MediaTek', 'Ans': 'A'},
    {'Q': '________ is any plan for organizing colours.', 'A': 'Colour Wheel', 'B': 'Colour Scheme', 'C': 'Composition',
     'D': 'Closure', 'Ans': 'B'},
    {'Q': 'Two dimentional arrays are also called', 'A': 'Table Arrays', 'B': 'Matrix Arrays', 'C': 'both A and B',
     'D': 'None of above', 'Ans': 'C'},
    {'Q': 'What is the default port number for most web servers?', 'A': '80', 'B': '83', 'C': '20', 'D': '27',
     'Ans': 'A'},
]
state = ['Waiting', 0, time.time(), False]
score = {}
answered = []


def convertMillis():
    millis = int((seconds * 100) - (time.time() - state[2]) * 100)
    if millis <= 0:
        return "Time's Up!"
    if state[3]:
        return ''
    miliseconds_ = millis % 100
    seconds_ = int((millis / 100) % 60)
    minutes = int(millis / 60 / 100)
    return '{0:01d} : {1:01d} : {2:01d}'.format(minutes, seconds_, miliseconds_)


def getMax():
    min_ = 999
    school = ''
    global times
    for i in times:
        if i[1] < min_:
            school = i[0]
            min_ = i[1]
    return school


@app.route('/')
def index():
    gc.collect()
    school = request.args.get('school')
    if school not in score.keys():
        score[school] = [0, '']
    return render_template('index.html', time_out=seconds * 100, school=school)


@app.route('/backend/')
def backend():
    gc.collect()
    return json.dumps(Question[state[1]])


@app.route('/state/')
def current_state():
    gc.collect()
    if request.args.get('state'):
        state[2] = time.time()
        state[0] = request.args.get('state')
        if state[0] == 'show_answer':
            state[3] = True
            global times
            if getMax() != '':
                if score[getMax()][1] == Question[state[1]]['Ans']:
                    # print(score[getMax()][1], Question[state[1]]['Ans'], score, times, 'lol')
                    score[getMax()][0] += 5
            times = []
        else:
            state[3] = False
    if request.args.get('q_num'):
        state[1] = int(request.args.get('q_num'))
    return json.dumps({'state_': state[0], 'answer_': Question[state[1]]['Ans'], 'q_num': state[1]})


@app.route('/answer/')
def answer():
    gc.collect()
    answer_ = request.args.get('answer')
    school = request.args.get('school')
    time_ = seconds * 100 - int(request.args.get('time')) + 1
    qnum = state[1]
    if answer_ == Question[state[1]]['Ans']:
        score[school][0] += 5
    global times
    times.append([school, time_])
    score[school][1] = answer_
    print(qnum, school, answer_, time_, score[school],
          file=open('D:/results.txt', 'a'), sep=',')
    return jsonify(True)


@app.route('/vmix/')
def vmix():
    gc.collect()
    return_json = [{'Q': Question[state[1]]['Q'],
                    'A': Question[state[1]]['A'],
                    'B': Question[state[1]]['B'],
                    'C': Question[state[1]]['C'],
                    'D': Question[state[1]]['D'],
                    'School_1': '',
                    'School_2': '',
                    'School_3': '',
                    'Sch1_Answer': '',
                    'Sch2_Answer': '',
                    'Sch3_Answer': '',
                    'Sch1_Score': '',
                    'Sch2_Score': '',
                    'Sch3_Score': '',
                    'time': convertMillis(),
                    'Answer': 'waiting for answers'
                    }]

    if state[3]:
        return_json[0]['Answer'] = '{}. {}'.format(Question[state[1]]['Ans'],
                                                   Question[state[1]][Question[state[1]]['Ans']])
        i = 1
        for school in score:
            return_json[0]['School_' + str(i)] = school
            return_json[0]['Sch' + str(i) + '_Score'] = score[school][0]
            return_json[0]['Sch' + str(i) + '_Answer'] = score[school][1]
            i += 1
    else:
        return_json[0]['Answer'] = 'waiting for answers'
    return json.dumps(return_json)


if __name__ == '__main__':
    app.run(debug=True)

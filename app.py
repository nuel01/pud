from flask import Flask, render_template, redirect, jsonify, request, send_file, Response
from rcmdr import *



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/feedback')
def feedback():
    return render_template('fdbk.html')

@app.route('/submit', methods=['POST', 'GET'])
def submit():    
    print(request.args)
    weight = request.args.get('wght')
    #print(weight)
    name = request.args.get('name')
    #print(name)
    sex = request.args.get('sex')
    #print(sex)
    icd = request.args.get('icd')
    #print(icd)
    age = request.args.get('age')
    #print(age)
    cond = [request.args.get('cond')]
    #print(cond)
    med = [request.args.get('med')]
    #print(med)
    #if weight == '': 
    #    return jsonify({"error_input":".   No Weight"})
    res,err = run(weight, age, sex, icd, cond, med)
    if res == '' :
        #print(sex)
        return jsonify({"error_input":err})
    else:
        return jsonify({'result':res})

 
if __name__ == "__main__":
    #app.run(debug=True, port=5000)
    app.run()

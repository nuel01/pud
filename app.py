from flask import Flask, render_template, redirect, jsonify, request, send_file, Response
#from google_apps_scraper import runApp, fileD
from rcmdr import *
import joblib


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
 
@app.route('/viewresult')
def viewresult():
   q = list(joblib.load(open('save.p', 'rb')))
   new_q = joblib.load(open('save.p', 'rb'))
   return render_template('viewresult.html', query=new_q, query2=q)

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
"""  



   else:
      res = runApp(appID, sch_opt, sort_opt, int(btnum))
      print('I got here')
      if type(res) == str:
         return jsonify({'result':res})
      else:
      #return send_file(res, as_attachment=True)
         return jsonify({'result':""})


@app.route('/getfile')
def getfile():
   file = joblib.load(open('save.p', 'rb'))
   res = fileD(file)
   
   response = Response(response=res, status=200, mimetype='application/txt')
   return response

"""

@app.route('/onlineprocessing2')
def onlineprocessing2():
    input_text = request.args.get('query', '0', type=str)
   # models = request.args.get('models', '0', type=str)
    if len(input_text) == 0 or input_text=='':
       return jsonify({"error_input":"No data supplied"})
   # elif models == '' or len(models) == 0:
   #    return jsonify({"model_err":"No model selected"})
    
   #sentenc = createCSV(textToSentence(input_text))

  # principleResult =  keypercase()
   #print(tagResults)
   #for item in principleResult:
    #  print(item)  

 #  result2 = jsonify({'results2':principleResult})
   

  # return result2
 
if __name__ == "__main__":
    app.run(debug=True, port=5000)
    #app.run()

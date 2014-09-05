'''
Created on 2014. 9. 4.

@author: jerryj
'''
from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/")
def hello():
    body = "<form action='/'>name: <input name='name'><br>dept: <input name='dept'><br><p><input type='submit'></form>"
    name = request.args.get('name', '')
    dept = request.args.get('dept', '')
    if name == "":
        return Response(response=body, mimetype='text/html')
    else:
        data1 = "The data has been stored successfully<p>"
        data2 = "Data: " + name + ", dept: " + dept
        return Response(response=data1+data2, mimetype='text/html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)


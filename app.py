from flask import Flask,render_template,request
import requests
from pymongo import MongoClient

app=Flask(__name__)


@app.route("/",methods=["get","post"])
def api():
    list=[145488,146679,147951,147197,147532]
    l=[]
    for i in list:
        url="https://api.mfapi.in/mf/"+str(i)
        resp=requests.get(url)
        fund=resp.json().get('meta').get('fund_house')
        nav=resp.json().get('data')[0].get('nav')
        temp={"fund_house":fund,"nav":nav}
        l.append(temp)
    client=MongoClient("mongodb://localhost:27017")
    database=client.user
    collection=database.fund
    collection.insert_many(l)
    client.close()
    return render_template("index.html",data=l)

@app.route("/update")
def update():
    client=MongoClient("mongodb://localhost:27017")
    database=client.user
    collection=database.fund
    collection.update_one({"nav":"1000.36950"},{ "$set" :  {'nav':'108'}})
    return 'updated'


@app.route("/delete")
def delete():
    client=MongoClient("mongodb://localhost:27017")
    database=client.user
    collection=database.fund
    collection.delete_one( {'nav':'108'})
    return "success"




if __name__=='__main__':
    app.run(debug=True)
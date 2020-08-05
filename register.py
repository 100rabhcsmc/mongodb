from flask import Flask,jsonify,request,json
from flask_pymongo import PyMongo 
from bson.objectid import ObjectId 
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)
from flask import render_template

app=Flask(__name__)

app.config['MONGO_DBNAME']="sau"
app.config['MONGO_URI']="mongodb://cluster0-shard-00-01-bblz8.mongodb.net:27017/sau"
app.config['JWT_SECRET_KEY']="secret"

mongo=PyMongo("mongodb://cluster0-shard-00-01-bblz8.mongodb.net:27017/sau")
bcrypt=Bcrypt(app)
jwt=JWTManager(app)

CORS(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/users/register',methods=['POST'])
def register():
    users=mongo.db.users
    print(request.form['name'])
    name=request.form['name']
    email=request.form['email']
    phone=request.form['phone']
    password=bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    created=datetime.utcnow()

    user_id=users.insert({
        'name':name,
        'email':email,
        'phone':phone,
        'password':password,
        'created':created
    })
    new_user=users.find_one({'_id':user_id})

    result={'email':new_user['email']+'registered'}

    return jsonify({'result':result})


@app.route('/users/login',methods=['POST'])
def login():
        users=mongo.db.users
        email=request.get_json()['email']
        password=request.get_json()['password']
        result=""

        response=users.find_one({'email':email})

        if response:
            if bcrypt.check_password_hash(response['password'],password):
                access_token=create_access_token(identity={
                    'first_name':response['first_name'],
                    'last_name':response['last_name'],
                    'email':response['email']
                })
                
                result=jsonify({"token":access_token})
            else:
                    result=jsonify({"error":"Invalid username and password"})
        else:
                      result=jsonify({"result":"No result found"}) 
        return result


if __name__=='__main__':
    app.run(debug=True,use_reloader=False)   
    #  app.run()   
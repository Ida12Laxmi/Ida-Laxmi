from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345@",
        database="dress"
    )

#RegisterAPI

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name=data.get('fullname')
    email=data.get('email')
    address=data.get('address')
    phone=data.get('phone')
    age=data.get('age')
    password=data.get('password')
    

    if not all([name,email,address,phone,age,password]):
        return jsonify({"error" : "All fields are required"}),400
    
    hashed_password=generate_password_hash(password)

    try: 
        conn=get_db_connection()
        cursor=conn.cursor()

        cursor.execute("SELECT * FROM customer WHERE cus_email= %s", (email, ))
        if cursor.fetchone():
            return jsonify ({"error" : "Email already registered"}),400
        
        sql="""INSERT INTO customer (cus_name, cus_email, cus_address, cus_age, cus_phone, cus_password)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql,(name,email,address,age,phone,hashed_password))

        conn.commit()

        return jsonify({"message":"Registration successful"}), 201
    
    except Exception as e:
        print("Error : ",e)
        return jsonify({"error":str(e)}),500
    
    finally:
        cursor.close()
        conn.close()



#LoginAPI

 #--Login API--


@app.route('/login',methods=['POST'])
def login():
        data=request.get_json()

        email=data.get('email')
        password=data.get('password')

        if not all([email,password]):
            return jsonify({"error":"Email and Passwords are required"}),400
        
        try:
            conn=get_db_connection()
            cursor=conn.cursor(dictionary=True)

            cursor.execute("SELECT * from customer where cus_email=%s",(email,))
            user=cursor.fetchone()

            if not user:
                 return jsonify({"error": "User not found"}), 404
            if not check_password_hash(user['cus_password'],password):
                return jsonify({"error": "Incorrect password"}), 401
            
            return jsonify({"message": "Login successful"}), 200
        
        except Exception as e:
             return jsonify({"error": str(e)}), 500
        
        finally:
         cursor.close()
         conn.close()
            

#--APP
if __name__ == '__main__':
    app.run(port=5000, debug=True)


#app.py
from flask import Flask, jsonify, request
 
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import os
 
app = Flask(__name__)
 
#Fetch Postgresql connection parameters from environment variables
DB_HOST = os.getenv("DATABASE_HOST")
DB_NAME = os.getenv("DATABASE_NAME")
DB_USER = os.getenv("DATABASE_USER")
DB_PASS = os.getenv("DATABASE_PASSWORD")
     
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

 
#API to get single book info, pass work_id in query string parameters
@app.route('/get_book')
def get_book():
    try:
        id = request.args.get('id')
        if id:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT * FROM works WHERE work_id=%s", id)
            row = cursor.fetchone()
            resp = jsonify(row)
            resp.status_code = 200
            return resp
        else:
            resp = jsonify('Work "id" not found in query string')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

#API to get specific books info, pass work_ids in request data
@app.route('/get_books', methods = ['POST'])
def get_books():
    try:
        request_data = request.get_json()
        ids = request_data['work_ids']
        
        if len(ids) > 0:
            t_ids = tuple(ids)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            query = "SELECT * FROM works WHERE work_id in {}".format(t_ids)
            cursor.execute(query)
            response_list = [item[0] for item in cursor.fetchall()]
            resp = jsonify(response_list)
            resp.status_code = 200
            return resp
        else:
            resp = jsonify('work_ids not found in request data')
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

#API to get all the books info
@app.route('/get_all_books')
def get_books():
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM works")
        response_list = [item[0] for item in cursor.fetchall()]
        resp = jsonify(response_list)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
 
if __name__ == "__main__":
    app.run()
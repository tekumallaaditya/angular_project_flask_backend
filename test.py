from flask import Flask, request , jsonify, flash, Session
from flask_restful import Resource, Api
import pymysql as MySQLdb
from flask_cors import CORS, cross_origin
import helper, re


#cursor for the database
db = MySQLdb.connect("localhost", "root", "root", "angularproject")
cur = db.cursor()

app = Flask(__name__)
CORS(app)
#sess = Session()

@app.route('/', methods=["GET", "POST", "OPTIONS"])
def RegisterUser():
    try:
        if request.method == 'POST':
            print request.data
            Fname = request.json.get('Fname')
            print Fname
            Lname = request.json.get('Lname')
            print Lname
            Email = request.json.get('Email')
            print Email
            Uname = request.json.get('Uname')
            print Uname
            Password = request.json.get('Password')
            print Password
            #checking of the username used is already registered?
            cur.execute("select * from admin")
            for each in cur.fetchall():
                if (each[4] == Uname):
                    return '', 293
            cur.execute("""insert into admin(`Fname`, `Lname`,`email`, `Uname`, `Password`) values (%s,%s,%s,%s,%s);""",
                        (Fname, Lname, Email, Uname, Password))
            db.commit()
            print "just before return"
            return '', 201
        else:
            #user_data = []
            user_data = helper.get_users()
            print user_data
            print jsonify(user_data)
            return jsonify(user_data)
    except Exception as e:
        flash(e)

@app.route('/user', methods=["GET","POST", "OPTIONS"])
def UserLogin():
    try:
        print "inside user try"
        if request.method == "POST":
            print "insdie post"
            Uname = request.json.get('Uname')
            print Uname
            Password = request.json.get('Password')
            print Password
            #checking if the login id is valid
            cur.execute("select * from admin")
            for each in cur.fetchall():
                if (each[4] == Uname and each[5] == Password):
                    return 'Login Successfull', 201
            return '', 293
        else:
            return '', 202
    except Exception as e:
        flash(e)

@app.route('/add', methods=["POST"])
def AddContact():
    try:
        if request.method == "POST":
            ContactName = request.json.get('ContactName')
            print ContactName, 'contact name'
            ContactNumber = request.json.get('ContactNumber')
            print ContactNumber
            Uname = request.json.get('Uname')
            print Uname
            cur.execute("select ContactList from admin where Uname = '%s';" %(Uname))
            contacts = cur.fetchall()
            print 'contacts are->',list(contacts), type(list(contacts)), contacts, type(contacts)
            contacts_str = ''
            for inside in list(contacts):
                for inside_each in inside:
                    if inside_each == None:
                        res = 'empty'
                    else:
                        res = 'ok'
            if (res == 'ok'):
                print "still entering here", len(list(contacts))
                for each in list(contacts):
                    for each_one in each:
                        print each_one, type(each_one)
                        contacts_str = contacts_str +each_one

            print 'contacts_str',contacts_str
            if (contacts_str == ''):
                contacts_str = contacts_str + ContactName + ':' + ContactNumber
            else:
                contacts_str = contacts_str + ',' + ContactName + ':' + ContactNumber

            print 'after adding->', contacts_str, type(contacts_str)
            query = """update admin  set ContactList = %s where Uname = %s;"""
            cur.execute(query, (contacts_str, Uname))
            db.commit()
            return '', 201
        else:
            return '', 293
    except Exception as e:
        flash(e)

@app.route('/del', methods=["POST"])
def DelContact():
    if request.method == "POST":
        contactname = request.json.get('ContactName')
        Uname = request.json.get('Uname')
        print contactname, Uname
        cur.execute("select ContactList from admin where Uname = '%s';" % (Uname))
        contacts = cur.fetchall()
        contacts_str = ''
        for each in contacts:
            print each
            for each_one in each:
                print each_one, type(each_one)
                contacts_str = contacts_str + each_one
        print contacts_str
        contacts_array = contacts_str.split(',')
        print contacts_array
        n = 0
        for each in contacts_array:
            if contactname in each:
                print 'here'
                del contacts_array[n]
            n = n + 1
        print contacts_array
        final_contacts = ''
        com = 0
        for each in contacts_array:
            if (com < len(contacts_array)-1):
                final_contacts = final_contacts + each + ','
            else:
                final_contacts = final_contacts + each
            com = com + 1
        print final_contacts, type(final_contacts)
        query = """update admin  set ContactList = %s where Uname = %s;"""
        cur.execute(query, (final_contacts, Uname))
        db.commit()


        return '', 201
    else:
        return '', 293

@app.route('/admin', methods=["GET","POST", "OPTIONS"])
def AdminLogin():
    try:
        print "inside Admin try"
        if request.method == "POST":
            print "insdie post"
            print request.json
            Uname = request.json.get('Uname')
            print Uname
            Password = request.json.get('Password')
            print Password
            #checking if the login id is valid
            cur.execute("select * from adminlogin")
            for each in cur.fetchall():
                if (each[4] == Uname and each[5] == Password):
                    return 'Login Successfull', 201
            return '', 293
        else:
            return '', 202
    except Exception as e:
        flash(e)

@app.route('/admindel', methods=["POST"])
def DelUser():
    if request.method == "POST":
        print 'into the deluser function'
        contactname = request.json.get('Unamedel')
        print contactname
        #checking if the Uname is valid
        cur.execute("select Uname from admin;")
        checklist = cur.fetchall()
        check_token = 'false'
        for each in checklist:
            for each_one in each:
                print each_one
                if (each_one == contactname ):
                    cur.execute("delete from admin where Uname = '%s';" % (contactname))
                    db.commit()
                    return '', 201
        return '', 293

    else:
        return '', 293



if __name__ == '__main__':
    app.secret_key = 'super secret key'
    #app.config['SESSION_TYPE'] = 'filesystem'

    #sess.init_app(app)
    app.run(host='localhost', port=5000, debug=True)
import pymysql as MySQLdb


#cursor for the database



def get_users():
    db = MySQLdb.connect("localhost", "root", "root", "angularproject")
    cur = db.cursor()
    cur.execute("select * from admin")
    users = cur.fetchall()
    db.close()
    finalusers_info = []
    for each in users:
        print 'in the helper function'
        each_user = {}
        final_each_user = {}
        each_user['id'] = each[0]
        each_user['FirstName'] = each[1]
        each_user['LastName'] = each[2]
        each_user['Email'] = each[3]
        each_user['ContactList'] = each[6]
        final_each_user[each[4]] = each_user
        finalusers_info.append(final_each_user)
    print type(finalusers_info)
    return finalusers_info

    #print finalusers_info


get_users()


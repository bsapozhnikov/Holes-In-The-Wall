import sqlite3
import cgi

conn = sqlite3.connect("data.db")

c = conn.cursor()

def dropTable(tablename):
    c.execute("DROP TABLE %s" % (tablename))
    conn.commit()
    print ("DROP TABLE %s" % (tablename))

def createTable(tablename, attr):
    """Creates a table in the database \'blog.db\'
    1st parameter - name of table (string)
    2nd parameter - Dictionary with keys and types as values'
    """
    print tablename
    L = [k[0]+' '+k[1] for k in attr]
##    L = [k+' '+attr[k] for k in attr.keys()]
    s = ','.join(L)
    c.execute("CREATE TABLE %s(%s)" % (tablename, s))
    conn.commit()
    print ("CREATE TABLE %s(%s)") % (tablename, s)

def createTables():
    '(re)creates tables for users, places, and reviews'
    #dropTable('users')
    #dropTable('places')
    #dropTable('reviews')
    createTable('users', [('username','text'),('pw','text')]) ##not sure what else needs to go here
    createTable('places', [('placename','text'),('lat','text'),('lng','text'),('adderID','integer'),('imgsrc','text')])
    createTable('reviews', [('title','text'),('content','text'),('rating','integer'),('authorID','integer'),('placeID','integer')])

def validateUser(user, pw):
    users = getUsers()
    for userID in users.keys():
        some = users[userID]
        if some['username'] == user:
            return some['pw'] == pw
    return False
    
def addUser(username, pw):
    if not existingName(username):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?,?)",(cgi.escape(username,quote=True),cgi.escape(pw,quote=True)))
        conn.commit()
        print "added %s to users" % (username)
    else:
        print "Username already taken. Please enter a different username"

'''add place into db
still needs an existingPlace method to check if a the place is already in the db'''
def addPlace(place):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO places VALUES (?)",(place,))
    conn.commit()
    print "added %s to places" %(places)

def existingName(username):
    username = cgi.escape(username,quote=True)
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    users = {}
    for row in c.execute("SELECT oid,* FROM users"):
        content = {'username':row[1],'pw':row[2]}
        users[row[0]]=content
    for x in users:
        if (username == x):
            return True
    return False 

def updatePass(username, oldpw, newpw):
    username = cgi.escape(username,quote=True)
    oldpw = cgi.escape(oldpw,quote=True)
    newpw = cgi.escape(newpw,quote=True)
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    if getUser(username)['pw']==oldpw:
        c.execute("UPDATE users SET pw = ? WHERE username = ? and pw = ?", (newpw,username,oldpw)) 
        conn.commit()
        print "updated password"
        return True
    else:
        return False

def addPlace(placename, lat, lng, adderID, imgsrc):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO places VALUES (?,?,?,?,?)" ,(cgi.escape(placename), lat, lng, adderID, cgi.escape(imgsrc)))
    conn.commit()
    print "added %s to places" % (placename)

def addReview(title, content, rating, authorID, placeID):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO reviews VALUES (?,?,?,?,?)" ,(title, content, rating, authorID, placeID))
    conn.commit()
    print "added %s to reviews" % (title)


def getUser(user):
    '''returns user as a dictionary
    This dictionary will also contain the user's oid'''
    users = getUsers()
    for userID in users.keys():
        some = users[userID]
        if some['username'] == user:
            some['oid']=userID
            return some
    
def getUsers():
    '''returns dictionary of users: 
    the key is the unique id
    the value is a dictionary containing the rest of the data'''
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    users = {}
    for row in c.execute("SELECT oid,* FROM users"):
        content = {'username':row[1],'pw':row[2]}
        users[row[0]]=content
    return users

def getPlaces():
    '''returns dictionary of places: 
    the key is the unique id
    the value is a dictionary containing the rest of the data'''
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    places = {}
    for row in c.execute("SELECT oid,* FROM places"):
        content = {'placename':row[1],'lat':row[2],'lng':row[3],'adderID':row[4],'imgsrc':row[5]}
        places[row[0]]=content
    return places

def getReviews(placeID=None):
    '''returns dictionary of reviews: 
    the key is the unique id
    the value is a dictionary containing the rest of the data'''
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    reviews = {}
    if placeID==None:
        s = c.execute('SELECT oid,* FROM reviews')
    else:
        print "Place given, returning only some: "+`int(placeID)`
        t = (`int(placeID)`,)
        s = c.execute('SELECT oid,* FROM reviews WHERE placeID=?',t)
    for row in s:
        print "row "+`row`
        content = {'title':row[1],'content':row[2],'rating':row[3],'authorID':row[4],'placeID':row[5]}
        reviews[row[0]]=content
    return reviews

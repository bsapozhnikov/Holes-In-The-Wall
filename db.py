import sqlite3

conn = sqlite3.connect("data.db")

c = conn.cursor()

def dropTable(name):
    c.execute("DROP TABLE %s" % (name))
    conn.commit()
    print ("DROP TABLE %s" % (name))
    
def createTable(name, attr):
    """Creates a table in the database \'blog.db\'
    1st parameter - name of table (string)
    2nd parameter - Dictionary with keys and types as values'
    """
    print name
    L = [k+' '+attr[k] for k in attr.keys()]
    s = ','.join(L)
    c.execute("CREATE TABLE %s(%s)" % (name, s))
    conn.commit()
    print ("CREATE TABLE %s(%s)") % (name, s)
    
def createTables():
    '(re)creates tables for users, places, and reviews'
    #drop_table('users')
    #drop_table('places')
    #drop_table('reviews')
    createTable('users', {'name':'text', 'pw':'text'}) ##not sure what else needs to go here
    createTable('places', {'name':'text', 'lat':'text', 'lng':'text', 'adderID':'integer', 'imgsrc':'text'})
    createTable('reviews', {'title':'text', 'content':'text', 'authorID':'integer','placeID':'integer'})
    
def validateUser(name, pw):
    for row in c.execute("SELECT oid,* FROM users"):
        content = {'name':row[1],'pw':row[2]}
        users[row[0]]=content
    for x in users:
        if (len(name) <= 5):
            return False
        if (len(pw) <= 5):
            return False
    else:
        return True

def addUser(name, pw):
    if not existingName(name) and validateUser(name,pw): 
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES ('%s','%s')" %(name,pw))
        conn.commit()
        print "added %s to users" % (name)
    else:
        print "Username already taken. Please enter a different username"

def existingName(name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    users = {}
    for row in c.execute("SELECT oid,* FROM users"):
        content = {'name':row[1],'pw':row[2]}
        users[row[0]]=content
    for x in users:
        if (name == x):
            return True
        else:
            return False

def updatePass(name, oldpw, newpw):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    UPDATE users
    SET pw = newpw
    WHERE name = name and pw = oldpw 
    conn.commit()
    print "updated password"
def addPlace(name, lat, lng, adderID, imgsrc):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO places VALUES ('%s','%s','%s','%s','%s')" %(name, lat, lng, adderID, imgsrc))
    conn.commit()
    print "added %s to places" % (name)

def addReview(title, content, authorID, placeID):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO reviews VALUES ('%s','%s','%s','%s')" %(title, content, authorID, placeID))
    conn.commit()
    print "added %s to reviews" % (title)

    
def getUsers():
    '''returns dictionary of users: 
    the key is the unique id
    the value is a dictionary containing the rest of the data'''
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    users = {}
    for row in c.execute("SELECT oid,* FROM users"):
        content = {'name':row[1],'pw':row[2]}
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
        content = {'name':row[1],'lat':row[2],'lng':row[3],'adderID':row[4],'imgsrc':row[5]}
        places[row[0]]=content
    return places

def getReviews():
    '''returns dictionary of reviews: 
    the key is the unique id
    the value is a dictionary containing the rest of the data'''
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    reviews = {}
    for row in c.execute("SELECT oid,* FROM reviews"):
        content = {'title':row[1],'content':row[2],'authorID':row[3],'placeID':row[4]}
        reviews[row[0]]=content
    return reviews

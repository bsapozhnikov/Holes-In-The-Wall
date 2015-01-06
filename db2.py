from pymongo import Connection

conn = Connection()

db2 = conn['iBM-Brian-Michael']

print db2.collection_names()

def getName(user):
    return db2.users.find_one({'user':user})['name']
def existingName(user):
    
    x = db2.users.find_one({'user':user})
    if x == None:
        return True
    else:
        return False
def validateUser(user,pw):
    print [doc['user'] for doc in db2.users.find()]
    print [doc['name'] for doc in db2.users.find()]
    print [doc['color'] for doc in db2.users.find()]
    print [doc['password'] for doc in db2.users.find()]
    x = db2.users.find_one({'user':user})
    if x != None:
        return x['password'] == pw

def registerUser(user,name,color,pw):
    x = db2.users.find_one({"user":user})
    if x == None and pw != None:
        db2.users.insert({"user":user,
                         "name":name,
                         "color":color,
                         "password":pw})
        return True
    else:
        return False

def updateUserInfo(user,pw,newpw,name,color):
    x = db2.users.find_one({"user":user})
    if x["password"] == pw:
        if name == None or name == '':
            name =x["name"]
        if newpw == None or newpw == '':
            newpw = x["password"]
        if color == None or color == '':
            color = x["color"]
        db2.users.update({"user":user},{'$set': {"password":newpw,
                                                "name":name,
                                                "color":color}})
        return True
    else:
        return False


            
                                    
        
    

        
    

#user
#name
#color
#pw

#register
#check if user/pw valid
#update user info

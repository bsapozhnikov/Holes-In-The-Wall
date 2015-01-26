from flask import Flask,request,redirect,render_template,session,flash
import db
import json
import urllib2
import ast
import cgi
import requests
import math

app=Flask(__name__)
app.secret_key ='insert_clever_secret_here'

def unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    # this has to be last:
    s = s.replace("&amp;", "&")
    return s

@app.route('/')
def root():
    return redirect('about')

@app.route('/login',methods=['GET','POST'])
def login():
    if "user" in session:
        
        flash("Please logout first to log into another account!")
        return render_template('about.html',name=db.getName(session['user']))
    if request.method=='GET':
        return render_template('login.html')
    else:
        user=cgi.escape(request.form['user'],quote=True)
        pw=cgi.escape(request.form['pass'],quote=True)
        if db.validateUser(user,pw):
            session['user']=user
            if 'return_to' in session:
                s = session['return_to']
                session.pop('return_to',None)
                return redirect(s)
            else: return redirect('/about')
        else:
            flash('Please enter a valid username and password')
            return render_template('login.html')
            
@app.route('/register',methods=['GET','POST'])
def register():
    if "user" in session:
        
        flash("Please logout first to register another account!")
        return render_template('home.html',name=db.getName(session['user']))
    if request.method=='GET':
        return render_template('register.html')
    else:
        
        name=request.form['name']
        user=request.form['user']
        pw=request.form['pass']
        color=request.form['color']
        if name == "" or user == "" or pw =="" or color == "":
            flash('Please fill in all the fields')
            return redirect('/register')
        elif db.existingName(user):
            flash('Your username is already taken!')
            return redirect('/register')
        else:
            
            if db.addUser(user,pw):
                return redirect('/login')
            else:
                return redirect('/about') ##should be replaced with flash

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/login')

def findPlaces(places,query):
    '''return list of places from dictionary, ordered based on query'''
    if query=='':
        return [x for x in places]
    else:
        ## split the query into a set of keywords
        qWords = set(query.split(' '))
        matches = {}
        ## for each place, split the name into a set of words
        ## count the number of words in common with the keywords
        ## make a dictionary with key = place key and value = number of matches
        ## sort dictionary in decreasing order of matches
        ## return places as list in that order
        for oid in places.keys():
            pWords = set(places[oid]['placename'].split(' '))
            matches[oid] = len(qWords & pWords)
        ans = [x[0] for x in sorted(matches.items(), key=lambda y: y[1], reverse=True)]
        return ans[:10]
        ##return ['I don\'t ','know what ','should go here - ','what\'s our search algorithm?']## ???

def findPlacesByGeo(places,lat,lng):
    matches = {}
    print("User's location: (%d,%d)"%(lat,lng))
    for oid in places.keys():
        plat = float(places[oid]['lat'])
        plng = float(places[oid]['lng'])
        print("%s's location: (%d,%d)"%(places[oid]['placename'],lat,lng))
        dist = math.sqrt(math.pow(lng-plng,2)+math.pow(lat-plat,2))
        matches[oid] = dist
    ans = [x[0] for x in sorted(matches.items(), key=lambda y: y[1])]
    return ans[:10]    
        
@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='GET':
        return render_template('search.html', name=db.getUser(session['user']))
    else:
        
        if request.form['submit']=='Search': ##search by keywords
            ## get the query from the HTML form
            query = request.form['holeInTheWall']
            print "The query is '%s'"%query
            ## get the places from the database
            places = db.getPlaces()
            ## sort the dictionary into a list
            results = findPlaces(places,query)
            ##results = ['I don\'t ','know what ','should go here - ','what\'s our search algorithm?']## ???
            ## pass sorted list to template
            return render_template('search.html',places=places, results=results, name=db.getUser(session['user']))
        else: ##search by location
            ##get ip address
            ip = urllib2.urlopen('http://ip.42.pl/raw').read()
            #get geo data
            URL = "http://www.freegeoip.net/json/" + ip
            req = requests.get(URL)###req= urllib2.urlopen(URL)###
            result = req.text###result = req.read()###
            data = json.loads(result)
            resultList = data.values()
            dump = ast.literal_eval(json.dumps(data))
            lat = dump.get("latitude")
            lng = dump.get("longitude")
            places = db.getPlaces()
            results = findPlacesByGeo(places,lat,lng)
            return render_template('search.html',places=places, results=results, name=db.getUser(session['user']))
            
@app.route('/reviews',methods=['GET','POST'])
@app.route('/reviews/<oid>',methods=['GET','POST']) ## I'm just putting this here for now        
def review(oid=1):
    if request.method=='GET':
        return render_template('reviews.html', oid=oid, place=db.getPlaces()[int(oid)], name=db.getUser(session['user']), reviews=db.getReviews(oid), users=db.getUsers(), plat = float(places[oid]['lat']), plng = float(places[oid]['lng']))
    else:
        ## get the review from the HTML form
        rating = request.form['stars']
        content = request.form['myTextBox']
        authorID = db.getUser(session['user'])['oid'] ##assumes user is in session (this is a protected page) and the value is set the user's ID
        title = "no title" ## no comment title in HTML form
        placeID = oid ## no placeID in HTML form
        ## add comment to database
        db.addReview(title,content,int(rating),authorID,placeID)
        ## flash success
        flash('Thank you for your review!')
        ## return template
        return render_template('reviews.html', oid=oid, place=db.getPlaces()[int(oid)], name=db.getUser(session['user']), reviews=db.getReviews(oid), users=db.getUsers(), plat = float(places[oid]['lat']), plng = float(places[oid]['lng']))

@app.route('/about')
def about():
    if 'user' not in session:
        return render_template('about.html')
    else:
        print session['user']
        return render_template('about.html',user=session['user'],name=db.getUser(session['user']))

@app.route('/home')
def home():
    if 'user' not in session:
        session['return_to']='/home'
        return redirect('/login')
    else:
        return render_template('home.html',name=db.getUser(session['user']))


#I want to use the location to center the add map- Maria
#get ip address
ip = urllib2.urlopen('http://ip.42.pl/raw').read()

#get geo data
URL = "http://www.freegeoip.net/json/" + ip
req = requests.get(URL)###req= urllib2.urlopen(URL)###
result = req.text###result = req.read()###
data = json.loads(result)
resultList = data.values()
dump = ast.literal_eval(json.dumps(data))

city = dump.get("city")
z = dump.get("zipcode")
lat = dump.get("latitude")
lon = dump.get("longitude")


@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'user' not in session:
        session['return_to']='/settings'
        return redirect('/login')
    else:   
        #Why is the places stuff here?
        places=request.form['places']
        db.addPlace(places)
        #Trying to make it also take your location for centering the map
        return render_template('add.html', lat = lat, lon = lon)
        
@app.route('/settings',methods=['GET','POST'])
def settings():
    if 'user' not in session:
        session['return_to']='/settings'
        return redirect('/login')
    else:
        if request.method=='GET':
            return render_template('settings.html',name=db.getUser(session['user']))
        else:
            
            ##get new info and update
            user = session['user']
            name=request.form['name']
            pw = request.form['oldpw']
            newpw = request.form['newpw']
            if pw == "" or not db.updateUserInfo(user,pw,newpw,name,color):
                flash("Please enter your correct current password to make any changes!")
                return redirect("/settings")
            else:
                return redirect('/home')

if __name__ == '__main__':
    
    app.debug=True
    app.run()

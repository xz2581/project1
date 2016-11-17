#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, flash,url_for, session

#tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder="/Users/xuchenzhou/project1/webserver/templates")
app.config['DEBUG'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'super secret key'


DATABASEURI = "postgresql://xz2581:67qfr@104.196.175.120/postgres"
engine = create_engine(DATABASEURI)



@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


apt = []
pr = []
interests = []
results = []
people = []
userss=[]
username = 'default'
u = ''
p = ''
users = []

@app.route('/')
def index():
  context = dict(data = apt)
  if apt == []:
    return render_template("index.html", **context)
  else:
    return render_template("index2.html", **context)

@app.route('/searcherror')
def searcherror():
  return render_template("searcherror.html")


def get_apt(cur):
  
  result = []
  for i in range(23):
    result.append([])
    
  for record in cur:
    for i in range(23):
      if (i>=18):
        if record[i] == True:
          result[i].append("Yes")
        else:
          result[i].append("No")
      else:
        result[i].append(record[i])    
  cur.close()  
  
  num = len(result[0])
  availability = []
  address = []
  for i in range(num):
    availability.append(str(result[5][i]) + " to " + str(result[6][i]))
  
  for i in range(num):
    address.append(str(result[8][i]) + " " + str(result[9][i]) + " # " 
                   + str(result[3][i]) + ", " + str(result[10][i]) + ", "
                   + result[11][i])
  
    userid = []
    aptid = []
    area = []
    price = []
    capacity = []
    aval = []
    nl = []
    nk = []
    nba = []
    nbe = []
    add = []
    gym = []
    laundry = []
    parking = []
    heater = []
    ac = []  

  userid = result[0]
  aptid = result[1]
  area = result[2]
  price = result[7]
  capacity = result[4]
  aval = availability
  nl = result[12]
  nk = result[13]
  nba = result[14] 
  nbe = result[15]
  add = address
  gym = result[18]
  laundry = result[19]
  parking = result[20] 
  heater = result[21]
  ac = result[22]
  
  return userid, aptid, area, price, capacity, aval, nl, nk, nba, nbe, add, gym, laundry, parking, heater, ac, address
  

def get_user(cur):
  result = []
  for i in range(7):
    result.append([])
    
  for record in cur:
    for i in range(7):
      if record[i] not in result[i]:
        result[i].append(record[i])    
  cur.close() 
  uid = result[0]
  birthyear = result[1]
  occupation = result[2]
  gender = result[3]
  emailaddress = result[4]
  rating = result[5]
  lifestyle = result[6]
  
  return uid,birthyear,occupation,gender,emailaddress,rating,lifestyle
    
@app.route('/profile', methods = ['POST','GET'])
def profile():
  global username
  username = u.encode('ascii')
  cmd1 = ("Select * from Apartment_owned_is_at_and_has_type as A INNER JOIN" 
          +" has as B on (A.uid = B.uid and A.uid = :u)")
  cur1 = g.conn.execute(text(cmd1), u= username)
  
  userid, aptid, area, price, capacity, aval, nl, nk, nba, nbe, add, gym, laundry, parking, heater, ac, address = get_apt(cur1)
  #print userid

  cmd2 = ("Select A.uid,A.aid, area, apt_num, capacity, start_date, end_date," 
          +"price, streetnum, streetname, counties, zipcode, numlivingroom, " 
          +"numkitchen, numbathroom, numbedroom, C.uid, C.aid, C.gym," 
          +"C.laundry, C.parking, C.heater, C.ac from Apartment_owned_is_at_and_has_type" 
          +" as A INNER JOIN has as C on (A.uid = C.uid and A.aid = C.aid) " 
          +"INNER JOIN has_interest_in as B on (A.uid = B.lid and " 
          + "A.aid = B.aid and B.tid = :u)")
  cur2 = g.conn.execute(text(cmd2), u = username)
  userid1, aptid1, area1, price1, capacity1, aval1, nl1, nk1, nba1, nbe1, add1, gym1, laundry1, parking1, heater1, ac1, address1 = get_apt(cur2)

  
  cmd3 = ("Select b.tid, birthyear, occupation, gender, emailaddress,"
          +" t.trating, t.life_style from Apartment_owned_is_at_and_has_type"
          +" as A INNER JOIN has_interest_in as B on (A.uid = B.lid and A.aid = B.aid" 
          +" and A.uid = :u) INNER JOIN potential_tenant as t on (b.tid = t." 
          +"uid) INNER join users as u on (b.tid = u.uid)")
  cur3 = g.conn.execute(text(cmd3),u=username)
  
  uid,birthyear,occupation,gender,emailaddress,rating,lifestyle = get_user(cur3)
  #global people
  #for record in cur3:
    #if record not in people:
      #people.append(record)
  
  
  context = dict(userid = userid, aptid = aptid, area = area, price = price,
                 capacity = capacity, aval = aval, nl = nl, nk = nk, nba = nba, 
                 nbe = nbe, add = address, gym = gym, laundry = laundry, 
                 parking = parking, pll = interests, heater = heater, ac = ac, 
                 userid1 = userid1, aptid1 = aptid1, area1 = area1, 
                 price1 = price1,capacity1 = capacity1, aval1 = aval1,
                 nl1 = nl1, nk1 = nk1, nba1 = nba1,nbe1 = nbe1, add1 = address1, 
                 gym1 = gym1, laundry1 = laundry1, parking1 = parking1,
                 heater1 = heater1, ac1 = ac1, uid = uid, gender = gender,
                 birthyear = birthyear, occupation = occupation, 
                 emailaddress = emailaddress, rating = rating, 
                 lifestyle = lifestyle)  
  
  return render_template("profile.html",**context)


@app.route('/wronguser')
def wronguser():
  return render_template("wronguser.html")

@app.route('/search',methods=['POST'])
def search():
  
  #input setup
  apt = []
  sdate = request.form['sdate']
  edate = request.form['edate']
  p1 = request.form['p1']
  p2 = request.form['p2']
  c1 = request.form['c1']
  c2 = request.form['c2']
  basic_info = [sdate, edate, p1, p2, c1, c2]
  
  for i in basic_info:
    if i == '':
      return redirect('/searcherror')
  
  
  aptno = request.form.get('aptno')
  stno = request.form.get('stno')
  stna = request.form.get('stna')
  counties = request.form.get('Counties')
  zipcode = request.form.get('zip')
  
  l = request.form.get('l')
  k = request.form.get('k')
  be = request.form.get('be')
  ba = request.form.get('ba')

  parking = request.form.get('parking').encode('ascii')
  laundry = request.form.get('laundry').encode('ascii')
  gym = request.form.get('gym').encode('ascii')
  heater = request.form.get('heater').encode('ascii')
  ac = request.form.get('AC').encode('ascii')
  
  addl = [aptno, stno, stna, counties, zipcode]
  tyl = [l,k,be,ba]
  afl = [gym,laundry,parking,heater,ac]
  
  
  for i in afl:
    if i == "Yes":
      i = True
    elif i == "No":
      i = False
  
  
  #paramdict setup
  address = {"apt_num":[aptno, 'a'], "streetnum":[stno, 'b'],
             "streetname":[stna,'c'], "counties": [counties, 'd'],
             "zipcode": [zipcode,'e']} 
  tyd = {"numlivingroom":[l,'f'], "numkitchen": [k,'g'], 
         "numbathroom":[ba,'h'], "numbedroom":[be,'i']}
  afd = {"gym":[gym,'j'],"laundry":[laundry,'k'],"parking":[parking,'l'],
         "heater":[heater,'m'],"ac":[ac,'n']}
  paramdict = {'x':p1, 'y':p2, 'sd':sdate, 'ed':edate,'sc':c1, 'ec':c2}
  
  #Initialize query
  cmd = ("SELECT * from Apartment_owned_is_at_and_has_type as A, has as B" +
          " where A.aid = B.aid and A.uid = B.uid and"
          +" price between :x AND :y" 
          + " AND start_date >= :sd and end_date <= :ed" 
          + " and capacity between :sc AND :ec")
  
  #If address is filled out
  if not all(x == '' for x in addl):
    #print "Hi first checkpoint"
    for i in address.keys():
      if address[i][0] != '' and address[i][0] != "None":
        if type(i.encode('ascii') == str):
          cmd += " and " + 'upper(' + i + ") = upper(:" + address[i][1] + ')'
        else:
          cmd += " and " + i + "= :" + address[i][1] 
        paramdict[address[i][1]]=address[i][0]
  
  #If type is filled out
  if not all(x == '' for x in tyl):
    for i in tyd.keys():
      if tyd[i][0] != '':
          cmd += " and " + i + "= :" + tyd[i][1] 
          print "Hi again!"
          paramdict[tyd[i][1]]=tyd[i][0]

  #If amenities and firnishings is filled out
  if not all(x== "None" for x in afl):
    for i in afd.keys():
      if afd[i][0] != "None":
        cmd += " and B." + i + "= :" + afd[i][1]
        paramdict[afd[i][1]]=afd[i][0]
        
  cur = g.conn.execute(text(cmd), paramdict)
  userid, aptid, area, price, capacity, aval, nl, nk, nba, nbe, add, gym, laundry, parking, heater, ac, address = get_apt(cur)
  
  context = dict(userid = userid, aptid = aptid, area = area, price = price,
                 capacity = capacity, aval = aval, nl = nl, nk = nk, nba = nba, 
                 nbe = nbe, add = address, gym = gym, laundry = laundry, 
                 parking = parking, heater = heater, ac = ac)  

  return render_template("searchresult.html", **context)

# Return boolean value of an input from the form
def get_bool(a):
  if a == 'true':
    a = True
  else:
    a = False
  return a


@app.route('/postnew',methods = ['POST'])
def postnew():
  uid = username
  aid = request.form.get('aid')
  area = request.form.get('area')
  cap = request.form.get('cap')
  
  sd = request.form.get('sdate1')
  ed = request.form.get('edate1')
  price = request.form.get('price')
  basic_info = [username, aid, area, cap, sd, ed, price]
  
  aptno = request.form.get('aptno')
  stno = request.form.get('stno')
  stna = request.form.get('stna')
  counties = request.form.get('Counties')
  zipcode = request.form.get('zip')
  addl = [aptno, stno, stna, counties, zipcode]
  
  l = request.form.get('l')
  k = request.form.get('k')
  be = request.form.get('be')
  ba = request.form.get('ba')
  tyl = [l,k,be,ba]

  
  parking = request.form.get('parking').encode('ascii')
  laundry = request.form.get('laundry').encode('ascii')
  gym = request.form.get('gym').encode('ascii')
  heater = request.form.get('heater').encode('ascii')
  ac = request.form.get('AC').encode('ascii')
  
  parking = get_bool(parking)
  laundry = get_bool(laundry)
  gym = get_bool(gym)
  heater = get_bool(heater)
  ac = get_bool(ac)
  
  lsr = request.form.get('lsr')
  afl = [gym,laundry,parking,heater,ac]
  
  
  
  #Exception checking
  lp = basic_info + addl + tyl +afl
  for i in lp:
    if i == '':
      return redirect('/searcherror')
    
  
  l = int(l)
  k = int(k)
  be = int(be)
  ba = int(ba)
  
  address = {"apt_num":[aptno, 'a'], "streetnum":[stno, 'b'],
             "streetname":[stna,'c'], "counties": [counties, 'd'],
             "zipcode": [zipcode,'e']} 
  tyd = {"numlivingroom":[l,'f'], "numkitchen": [k,'g'], 
         "numbathroom":[ba,'h'], "numbedroom":[be,'i']}
  afd = {"gym":[gym,'j'],"laundry":[laundry,'k'],"parking":[parking,'l'],
         "heater":[heater,'m'],"ac":[ac,'n']}
  
  #INSERT INTO LANDLORD
  if lsr != None:
    cmd0 = "Insert into landlord values (:U, :l)"
  else:
    cmd0 = "Insert into landlord values (:U)"
  
  try:
    g.conn.execute(text(cmd0),{'U':username, 'l':lsr.encode('ascii')})
  except:
    pass
  
  #INSERT INTO LOCATION
  cmd1 = "Insert into location values (:b,:c,:d,:e)"
  try:
    g.conn.execute(text(cmd1),{'b': stno, 'c': stna, 'd':counties, 'e': zipcode})
  except:
    pass
  
  #INSERT INTO APARTMENT_TYPE
  cmd2 = "INSERT into apartment_type values (:l,:k,:ba,:be)"
  #print "I'm here!"
  try:
    g.conn.execute(text(cmd2),{'l':l,'k':k,'ba':ba,'be':be})
    #print "I'm here!"
  except:
    pass
  
  #insert into amenities and furnishings
  cmd3 = "INSERT into amenities_and_furnishings values (:j, :k, :l, :m, :n)"
  try:
    g.conn.execute(text(cmd3),{'j':gym,'k':laundry,'l':parking,'m': heater, 'n':ac})
  except:
    "print I'm at cmd3!"
    pass
  
  #Insert into apartment
  cmd4 = ("INSERT into apartment_owned_is_at_and_has_type values(:uidf, :aidf, "
          + ":areaf, :a, :capf, :sdf, :edf, :pf, :b, :c, :d, :e, :f, :g, :h, :i)")
  
  #try:
  g.conn.execute(text(cmd4),{"uidf":username, "aidf":aid, "areaf": area,'a':aptno, "capf": cap,
                             "sdf":sd, "edf":ed, "pf":price, 'b': stno, 'c': stna, 
                             'd':counties, 'e': zipcode, 'f':l,'g':k,'h':ba,'i':be})
  #except:
    #return render_template('searcherror2.html')  
  
  #Isert into has table
  cmd35 = "INSERT into has values (:u, :ai, :g, :l, :p, :h, :a)"
  try:
    g.conn.execute(text(cmd35),{'u':username, 'ai' :aid, 'g':gym,'l':laundry,'p':parking,'h': heater, 'a':ac})  
  except:
    pass 
  
  return redirect('/profile')

@app.route('/interest', methods = ['POST'])
def interest():
  lid = request.form.get('lid').encode('ascii')
  aid = request.form.get('aid').encode('ascii')
  tid = username
  ls = str(request.form.get('lifestyle'))
  if (lid == '' or aid == '' or tid == ''):
    return redirect('/searcherror')
  
  cmd1 = "INSERT into potential_tenant values(:ut,:ls)"
  try:
    g.conn.execute(text(cmd1),{"ut": tid, "ls" : ls}) 
  except:
    cmd0 = "Select life_style from potential_tenant where uid = :u"
    cur0 = g.conn.execute(text(cmd0),{'u':tid})
    res = []
    for result in cur0:
      res = result[0]
    if res == None:
      g.conn.execute(text("update potential_tenant set life_style = "
                     + ":l where uid = :ui"), {'l':ls, 'ui' :tid});
    else:
      pass
  
  cmd2 = "INSERT into has_interest_in values(:ut,:ul, :a)"
  
  try:
    cur = g.conn.execute(text(cmd2),{"ut": tid, "a": aid, "ul": lid})
  except:
    return render_template("/nosuchcombo.html")
  
  return redirect('/profile')

@app.route('/getlandlord',methods=['POST'])
def getlandlord():
  lid = request.form.get('lid').encode("ascii")
  
  cmd = ("Select u.uid, birthyear, occupation, gender, emailaddress,"
          +" l.lrating, l.life_style_required from users as u, landlord as "
          +"l where l.uid = u.uid and u.uid = :l")
  
  cur = g.conn.execute(text(cmd),{'l':lid})
  uid,birthyear,occupation,gender,emailaddress,rating,lifestyle = get_user(cur)
  context = dict(uid = uid, birthyear = birthyear, occupation = occupation,
                 gender = gender, emailaddress = emailaddress, rating = rating,
                 lifestylerequired = lifestyle)
  
  return render_template("vp.html",**context)
  
@app.route('/delete',methods=['POST'])
def delete():
  aid = request.form['aid'].encode('ascii')
  if aid == '':
    return redirect ('/searcherror')
  
  cmd0 = ("Select Count(uid) from has as B where B.aid = :aidf and B.uid = :u")
  cur1 = g.conn.execute(text(cmd0),{'aidf':aid, 'u':username})
  result = []
  for res in cur1:
    count = res[0]
    if count == 0:
      return render_template("nosuchcombo.html")

  cmd1 = ("DELETE from has as B where B.aid = :aidf and B.uid = :u")
  g.conn.execute(text(cmd1),{'aidf':aid, 'u':username})
  cmd2 = ("DELETE from apartment_owned_is_at_and_has_type as A where"
          +" A.uid = :u and A.aid = :aidf")
  
  g.conn.execute(text(cmd2),{'u': username, 'aidf' :aid})
  
  return redirect ('/profile')  

  
@app.route('/login', methods=['GET', 'POST'])
def login():
  session['logged_in'] = False
  error = None
  if request.method == 'POST':
      global u,p
      u = request.form.get('username')
      p = request.form.get('password')
      cmd = "Select Count(uid) from users where uid = :u1"
      cur = g.conn.execute(text(cmd),{'u1':u})
      for result in cur:
        count = result[0]
      if count == 0:
            error = 'Invalid username!'
      elif count > 0:
        cmd+=" and pwd = md5(:p1)"
        cur = g.conn.execute(text(cmd),{'u1':u,'p1':p})
        for result in cur:
          count = result[0]
          
        if count == 0:
          error = 'Invalid password'
        else:
          #print "Im here"
          session['logged_in'] = True
          #print "Im here"
          apt.append( "You are logged in!")
          return redirect('/')
      return render_template('login.html', error=error)

@app.route('/logout', methods=['POST'])
def logout():
  global u,p
  u = ' '
  p = ' '
  session['logged_in'] = False
  global apt
  apt = []
  return render_template("index.html")

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()

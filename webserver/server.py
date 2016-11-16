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


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
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
#dummy1 = []
#dummy2 = []
#dummy3 = []

@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """
  print request.args
  context = dict(data = apt)
  if apt == []:
    return render_template("index.html", **context)
  else:
    return render_template("index2.html", **context)

@app.route('/searcherror')
def searcherror():
  return render_template("searcherror.html")



@app.route('/profile', methods = ['POST','GET'])
def profile():
  global username
  username = u.encode('ascii')
  cmd1 = ("Select * from Apartment_owned_is_at_and_has_type as A, has as B where A.uid = B.uid and A.uid = :u1")
  cur1 = g.conn.execute(text(cmd1),u1 = username)
  
  global pr
  for record in cur1:
    if record not in pr:
      pr.append(record)
  cur1.close()
  
  cmd2 = ("Select A.aid, A.uid, A.price from Apartment_owned_is_at_and_has_type as A INNER"
          + " JOIN has_interest_in as B on (A.uid = B.lid and A.aid = B.aid and B.tid = :u)")
  cur2 = g.conn.execute(text(cmd2),u = username)
  
  global interests
  for record in cur2:
    if record not in interests:
      interests.append(record)
  cur2.close()
  
  cmd3 = ("Select b.tid from Apartment_owned_is_at_and_has_type as A INNER"
          + " JOIN has_interest_in as B on (A.uid = B.lid and A.aid = B.aid and A.uid = :u)")
  cur3 = g.conn.execute(text(cmd3),u=username)
  
  global people
  for record in cur3:
    if record not in people:
      people.append(record)
  
  context = dict(pl1 = pr, pll = interests, plll = people)
  print context
  return render_template("profile.html",**context)

@app.route('/searchresult')
def searchresult():
  context = dict(data = results)
  return render_template("searchresult.html",**context)

#@app.route('/post')
#def afterpost():
  #context = dict(data = pr)
  #return reunder_template("profile.html", **context)

# Searching for apartments

@app.route('/search',methods=['POST'])
def search():
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
    if i == "true":
      i = True
    elif i == "false":
      i = False
  
  
  
  address = {"apt_num":[aptno, 'a'], "streetnum":[stno, 'b'],
             "streetname":[stna,'c'], "counties": [counties, 'd'],
             "zipcode": [zipcode,'e']} 
  tyd = {"numlivingroom":[l,'f'], "numkitchen": [k,'g'], 
         "numbathroom":[ba,'h'], "numbedroom":[be,'i']}
  afd = {"gym":[gym,'j'],"laundry":[laundry,'k'],"parking":[parking,'l'],
         "heater":[heater,'m'],"ac":[ac,'n']}
  
  
  

  paramdict = {'x':p1, 'y':p2, 'sd':sdate, 'ed':edate,'sc':c1, 'ec':c2}
  cmd = ("SELECT * from Apartment_owned_is_at_and_has_type" +
          " where Apartment_owned_is_at_and_has_type.price between :x AND :y" 
          + " AND start_date >= :sd and end_date <= :ed" 
          + " and capacity between :sc AND :ec")
  
  if all(x == '' for x in addl) == False:
    #print "Hi first checkpoint"
    for i in address.keys():
      if address[i][0] != '':
        if type(i.encode('ascii') == str):
          cmd += " and " + 'upper(' + i + ") = upper(:" + address[i][1] + ')'
        else:
          cmd += " and " + i + "= :" + address[i][1] 
        paramdict[address[i][1]]=address[i][0]
  
  if all(x == '' for x in tyl) == False:
    print "Hi second checkpoint"
    print cmd
    for i in tyd.keys():
      if tyd[i][0] != '':
          cmd += " and " + i + "= :" + tyd[i][1] 
          print "Hi again!"
          paramdict[tyd[i][1]]=tyd[i][0]  
  
  if all(x== "None" for x in afl) == False:
    #print "Ugh i'm here"
    cmd = "Select * from (" + cmd + ") as A, has as B where A.aid = B.aid and A.uid = B.uid "
    for i in afd.keys():
      if afd[i][0] != "None":
        cmd += " and B." + i + "= :" + afd[i][1]
        paramdict[afd[i][1]]=afd[i][0]
        
  

  cursor = g.conn.execute(text(cmd), paramdict)
  entries = cursor.fetchall()
  cursor.close()
  

  global results
  results = []
    
  for record in entries:
    if record not in results:
      results.append(record)
  
  return redirect('/searchresult')
    
#def check_int(num):
  #return float(num) != int(num)

#Post new Apartments
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
  afl = [gym,laundry,parking,heater,ac]
  
  #Exception checking
  lp = basic_info + addl + tyl +afl
  for i in lp:
    if i == '':
      return redirect('/searcherror')
    
  #for i in [cap,l,k,be,ba]:
    #if i != '' and check_int(i) == False:
      #return redirect('searcherror')
    
  parking = request.form.get('parking').encode('ascii')
  laundry = request.form.get('laundry').encode('ascii')
  gym = request.form.get('gym').encode('ascii')
  heater = request.form.get('heater').encode('ascii')
  ac = request.form.get('AC').encode('ascii')
  afl = [gym,laundry,parking,heater,ac]
  
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
  

  cmd1 = "Insert into location values (:b,:c,:d,:e)"
  try:
    g.conn.execute(text(cmd1),{'b': stno, 'c': stna, 'd':counties, 'e': zipcode})
  except:
    pass
  
  cmd2 = "INSERT into apartment_type values (:l,:k,:ba,:be)"
  #print "I'm here!"
  try:
    g.conn.execute(text(cmd2),{'l':l,'k':k,'ba':ba,'be':be})
    print "I'm here!"
  except:
    pass
  
  cmd3 = "INSERT into amenities_and_furnishings values (:j, :k, :l, :m, :n)"
  try:
    g.conn.execute(text(cmd3),{'j':gym,'k':laundry,'l':parking,'m': heater, 'n':ac})
  except:
    "print I'm at cmd3!"
    pass
  
  ##print "I'm at cmd4!"
  cmd4 = ("INSERT into apartment_owned_is_at_and_has_type values(:uidf, :aidf, "
          + ":areaf, :a, :capf, :sdf, :edf, :pf, :b, :c, :d, :e, :f, :g, :h, :i)")
  
  g.conn.execute(text(cmd4),{"uidf":username, "aidf":aid, "areaf": area,'a':aptno, "capf": cap,
                            "sdf":sd, "edf":ed, "pf":price, 'b': stno, 'c': stna, 
                            'd':counties, 'e': zipcode, 'f':l,'g':k,'h':ba,'i':be})
  
  #print "I'm at cmd5!"
  #cmd5("INSERT into has values (:uidf, :aidf, :j, :k, :l, :m, :n)")
  #g.conn.execute(text(cmd5), {"uidf":username, "aidf":aid, 'j':gym,'k':laundry,
                              #'l':parking,'m': heater, 'n':ac})
  

  return redirect('/profile')

@app.route('/interest', methods = ['POST'])
def interest():
  lid = request.form.get('lid')
  print lid
  aid = str(request.form.get('aid'))
  tid = str(request.form.get('tid'))
  ls = str(request.form.get('lifestyle'))
  if (lid == '' or aid == '' or tid == ''):
    return redirect('/searcherror')
  
  cmd1 = "INSERT into potential_tenant values(:ut,:ls)"
  try:
    g.conn.execute(text(cmd1),{"ut": tid, "ls" : ls})
  except:
    pass
  cmd2 = "INSERT into has_interest_in values(:ut,:ul, :a)"
  
  cur = g.conn.execute(text(cmd2),{"ut": tid, "a": aid, "ul": lid})
  return redirect('/profile')

@app.route('/vd',methods=['POST'])
def vd():
  lid = request.form.get('lid')
  try:
    cmd = "Select uid,birthyear,occupation,gender,emailaddress from users where uid = :l"
  except:
    return redirect('/searchresult')
  
  cur = g.conn.execute(text(cmd),{'l':lid})
  global users
  for record in cur:
    if record not in users:
      users.append(record)
  cur.close()  
  context = dict(bla = users)
  return render_template("vp.html",**context)
  
@app.route('/vp',methods=['POST'])
def vp():
  tid = request.form.get('tid')
  try:
    cmd = "Select uid,birthyear,occupation,gender,emailaddress from users where uid = :t"
  except:
    return redirect('/searchresult')
  
  cur = g.conn.execute(text(cmd),{'t':tid})
  
  global userss
  for record in cur:
    if record not in userss:
      userss.append(record)
  cur.close()  
  context = dict(bla = userss)
  return render_template("vp.html",**context)  


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
      global u,p
      u = request.form.get('username')
      p = request.form.get('password')
      cmd = "Select Count(uid) from users where uid = :u1"
      cur = g.conn.execute(text(cmd),{'u1':u})
      for result in cur:
        count = result[0]
      #cur.close()
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

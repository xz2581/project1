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
from flask import Flask, request, render_template, g, redirect, Response

#tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder="/Users/xuchenzhou/project1/webserver/templates")
app.config['DEBUG'] = True

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
results = []
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args

  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = apt)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an addressa different path.  You can see it at
# 
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#
@app.route('/searcherror')
def another():
  return render_template("searcherror.html")

@app.route('/searchresult')
def searchresult():
  context = dict(data = results)
  #print data
  return render_template("searchresult.html",**context)

# addressadding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  #print name
  cmd = 'INSERT INTO test(name) VALUES (:name1)';
  g.conn.execute(text(cmd), name1 = name);
  return redirect('/')

@app.route('/search',methods=['POST'])
def search():
  
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
         "numbathroom":[ba,'g'], "numbedroom":[be,'h']}
  afd = {"gym":[gym,'i'],"laundry":[laundry,'j'],"parking":[parking,'k'],
         "heater":[heater,'l'],"ac":[ac,'m']}
  
  
  

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
  #print entries
  cursor.close()
  
  for record in entries:
    if record not in results:
      results.append(record)
  cursor.close()
  return redirect('/searchresult')
    
  
  
@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


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

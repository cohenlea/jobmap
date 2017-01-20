# Resume map project. Lea Cohen. 19 January 2017.
# import the Flask module from the flask package
from flask import Flask

# import render_template to use templates
from flask import render_template

# import psycopg2 to add database to app
import psycopg2
import json

# create the app
app = Flask(__name__)

# make the simple http server refresh on saving/chaning a file
# will also send errors
app.debug = True

@app.route("/")
def jobdata():
	try:
		# this database connection will not work, obviously. for example purposes only.
	    conn = psycopg2.connect("dbname='leacohen' user='leacohen' host='localhost' password=''")
	    print "Connection successful"
	except:
	    print "I am unable to connect to the database"

	# create cursor object
	cur = conn.cursor()

	# run query
	cur.execute("""SELECT title, company, descript, city, state, country, longitude, latitude, purpose from lea.jobs order by job_id asc""")
	# create variable to store query output
	rows = cur.fetchall()

	thefeatures = []	
	for row in rows:
		thefeatures.append({'type':'Feature','geometry':{'type':'Point','coordinates':[row[6],row[7]],}, 'properties':{'title':row[0], 'company':row[1], 'descript':row[2], 'city':row[3], 'state':row[4], 'country':row[5],'purpose':row[8]}})
	jobs = [{'type': 'Featurecollection','features':thefeatures}]
	json_jobs = json.dumps(jobs, indent=2)


	return render_template('index.html',jobs=thefeatures)

if __name__ == "__main__":
    app.run()


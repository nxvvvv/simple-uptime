import requests, replitdb, asyncio, flask, threading
db = replitdb.AsyncClient()
async def ping():
	lst = []
	pings = str(await db.view('pings')).split('\n')
	for i in pings:
		if i not in lst:
			try:
				if i != '':requests.get(i)
			except:
				continue
			lst.append(i)

async def loop():
	await ping()
	await asyncio.sleep(5)

asyncio.ensure_future(loop())


app = flask.Flask(__name__)
@app.route('/')
def contact():
	return flask.render_template('add.html')
  
@app.route('/add', methods=['POST'])
def send():
	newPing = flask.request.form['add']
	pings = str(asyncio.run(db.view('pings'))).split('\n')
	if newPing in pings:
		return flask.render_template('duplicate.html')
	try:
		requests.get(newPing)
		asyncio.run(db.set(pings=str(asyncio.run(db.view('pings'))) + '\n' + newPing))
		return flask.render_template('success.html')
	except:
		return flask.render_template('incorrect.html')


app.run(host='0.0.0.0', port=8080)
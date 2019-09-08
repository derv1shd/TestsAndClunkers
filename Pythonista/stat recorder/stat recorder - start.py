#!python3

'''
This script implements an "elapsed time" recorder, where you start a timer and you stop it, continously updating a median.
This part marks the start.
The current data set is persisted to a file, so it can be restored when the widget is restarted.
'''

import appex, ui, os, sys, webbrowser, clipboard
import datetime, statistics, json, urllib

dataset = []

# Try to load previous dataset value from file:
try:
	with open('stats.json') as f:
		dataset = json.load(f)
except IOError:
	pass
except:
	pass

def mark_start():
	global dataset
	# There can only be one
	for v in dataset:
		start, end = v
		if end == None:
			dataset.remove(v)
	dataset.append((str(datetime.datetime.now()),None))

def calc_median():
	global dataset
	elapsed = []
	for v in dataset:
		start, end = v
		if end != None:
			start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
			end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')
			elapsed.append(end - start)
	if len(elapsed) == 0:
		return datetime.timedelta(0)
	return statistics.median(elapsed)

def current_start():
	global dataset
	if len(dataset) == 0:
		return datetime.datetime.now()
	for v in dataset:
		start, end = v
		if end == None:
			return datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
	else:
		return datetime.datetime.now()
	
def main():
	global dataset
	mark_start()
	with open('stats.json', 'w') as f:
		json.dump(dataset, f)
	eta = current_start() + calc_median()
	clipboard.set('ETA is ' + eta.strftime('%H:%M:%S'))
	# this will open your shortcut with as input the device clipboard
	query = [("name", "Tell Lu I’m on my way"),("input","clipboard")]
	url = "shortcuts://x-callback-url/run--shortcut?" + urllib.parse.urlencode(query,quote_via=urllib.parse.quote)
	webbrowser.open(url)

if __name__ == '__main__':
	main()
	

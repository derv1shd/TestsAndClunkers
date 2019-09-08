#!python3

'''
This widget script implements an "elapsed time" recorder, where you start a timer and you stop it, continously updating a median.
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
	
def mark_end():
	global dataset, lastelapsed
	# Search for started time
	for v in dataset:
		start, end = v
		if end == None:
			# Remove and readd
			dataset.remove(v)
			end = datetime.datetime.now()
			dataset.append((start, str(end)))
			start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
			lastelapsed = end - start
			break
	else:
		return	

def main():
	global dataset, lastelapsed
	mark_end()
	with open('stats.json', 'w') as f:
		json.dump(dataset, f)
	# this will open your shortcut with as input the device clipboard
	clipboard.set('Ended, elapsed: ' + str(lastelapsed))
	query = [("name", "Got Home"),("input","clipboard")]
	url = "shortcuts://x-callback-url/run--shortcut?" + urllib.parse.urlencode(query,quote_via=urllib.parse.quote)
	webbrowser.open(url)

if __name__ == '__main__':
	main()
	

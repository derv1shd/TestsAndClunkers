#!python3

'''
This widget script implements an "elapsed time" recorder, where you start a timer and you stop it, continously updating a median.
The current data set is persisted to a file, so it can be restored when the widget is restarted.
'''

import appex, ui, os, json, clipboard
import datetime, statistics

dataset = []
lastelapsed = datetime.timedelta()

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
	# Try to load previous dataset value from file:
	try:
		with open('stats.json') as f:
			dataset = json.load(f)
	except IOError:
		pass
	except:
		pass
	# There can only be one
	for v in dataset:
		start, end = v
		if end == None:
			dataset.remove(v)
	dataset.append((str(datetime.datetime.now()),None))
	# Save the new dataset value to a file:
	with open('stats.json', 'w') as f:
		json.dump(dataset, f)
	
def mark_end():
	global dataset, lastelapsed
	# Try to load previous dataset value from file:
	try:
		with open('stats.json') as f:
			dataset = json.load(f)
	except IOError:
		pass
	except:
		pass
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
			# Save the new dataset value to a file:
			with open('stats.json', 'w') as f:
				json.dump(dataset, f)
			break
	else:
		print("Timer not started")

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
						
def button_tapped(sender):
	# Update the dataset, depending on which button was tapped:
	global dataset, lastelapsed
	if sender.name == 'end':
		mark_end()
		sender.superview['text_label'].text = 'Ended: ' + str(lastelapsed)
	elif sender.name == 'start':
		mark_start()
		eta = current_start() + calc_median()
		sender.superview['text_label'].text =  'Started, ETA is ' + eta.strftime('%H:%M:%S')
		clipboard.set('ETA is ' + eta.strftime('%H:%M:%S'))

def main():
	# Optimization: Don't create a new view if the widget already shows the tally dataset.
	widget_name = __file__ + str(os.stat(__file__).st_mtime)
	v = appex.get_widget_view()
	if v is not None and v.name == widget_name:
		return
	v = ui.View(frame=(0, 0, 320, 64), name=widget_name)
	label = ui.Label(frame=(0, 32, 320, 32), flex='wh', font=('HelveticaNeue-Light', 24), alignment=ui.ALIGN_CENTER, text='Median: ' + str(calc_median()), line_break_mode=ui.LB_WORD_WRAP)
	label.name = 'text_label'
	v.add_subview(label)
	logout_btn = ui.Button(name='start', image=ui.Image('iow:log_out_32'), flex='hl', tint_color='#666', action=button_tapped)
	logout_btn.frame = (-32, -16, 32, 32)
	v.add_subview(logout_btn)
	home_btn = ui.Button(name='end', image=ui.Image('iow:log_in_32'), flex='hl', tint_color='#666', action=button_tapped)
	home_btn.frame = (320-64, -16, 32, 32)
	v.add_subview(home_btn)
	appex.set_widget_view(v)

if __name__ == '__main__':
	main()
	

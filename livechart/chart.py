"""
Contains functions for reading data from stdin, parsing it, and plotting it on
a `matplotlib` figure.
"""

from __future__ import print_function
from matplotlib import pyplot
import sys
import json
import time
import math
import warnings

def parse_json(string):
	"""
	Attempt to parse an int, float, or dictionary from a JSON string. Return
	None if parsing failed, and print an error.
	"""

	try:
		json_blob = json.loads(string)

	except ValueError as excep:
		msg = "Failed to parse line `{0}` with `{1}` exception."
		print(msg.format(string, excep), file=sys.stderr)
		return

	if isinstance(json_blob, (int, float)):
		return {"value": json_blob}

	elif isinstance(json_blob, dict):
		return json_blob

	else:
		print(
			"Decoded JSON is not a chartable data-type: {}".format(json_blob),
			file=sys.stderr
		)

def handle_close(evt):
	sys.exit(0)

def configure_pyplot():
	pyplot.ion()
	pyplot.xlabel("time (seconds)")
	canvas = pyplot.gcf().canvas
	canvas.set_window_title("livechart")
	canvas.mpl_connect("close_event", handle_close)

def render_stdin(config):
	"""
	Continuously read in data from stdin, parse it using `parse_json()`, and
	update the matplotlib plot with `render_data_points()`. Accepts a `config`
	dictionary argument that contains all configuration options.
	"""

	start_time = time.time()
	times = [0]

	data_points = {}
	line = sys.stdin.readline().rstrip("\n")
	initial_data = parse_json(line)
	if initial_data is None:
		print("No valid data detected in first line of STDIN.", file=sys.stderr)
		return 1

	initial_data = initial_data.items()
	sub_conf = config["subplots"]
	if not ("vertical" in sub_conf and "horizontal" in sub_conf):
		num_data_points = len(initial_data)
		sub_conf["vertical"] = math.ceil(math.sqrt(num_data_points))
		sub_conf["horizontal"] = math.ceil(num_data_points / sub_conf["vertical"])

	elif sub_conf["vertical"] * sub_conf["horizontal"] < len(initial_data):
		print(
			"Number of subplots is less than the number of data points.",
			file=sys.stderr
		)
		return 1

	for id_, (key, val) in enumerate(initial_data, start=1):
		if config["subplots"]["show"]:
			pyplot.subplot(
				config["subplots"]["vertical"],
				config["subplots"]["horizontal"],
				id_
			)
			pyplot.title(key)

		data_points[key] = {
			"graph": pyplot.plot([val], [val], label=key)[0],
			"values": [val]
		}

	if not config["subplots"]["show"] and len(data_points) > 1:
		pyplot.legend(loc="lower right")

	prevRenderTime = time.time()
	line = sys.stdin.readline()

	# Track the time spent rendering, to subtract it from the new times plotted
	# on the x-axis and thus avoid artefacts (flat parts of the graph) caused
	# by it.
	time_spent_rendering = 0

	while line:
		new_data = parse_json(line.rstrip("\n"))
		if new_data is not None:
			curr_time = time.time()
			times.append(curr_time - start_time - time_spent_rendering)
			for key, val in new_data.items():
				try:
					data_points[key]["values"].append(val)
				except KeyError as e:
					msg = (
						"Key `{}` not found. The data you pipe into livechart"
						" must be consistent (ie, only numbers or JSON"
						" dictionaries)"
					)
					print(msg, file=sys.stderr)
					return 1

			if not config["no_refresh"] and \
				curr_time - prevRenderTime >= config["render_interval"]:
				render_data_points(times, data_points, config)
				time_spent_rendering += time.time() - curr_time
				prevRenderTime = curr_time

		line = sys.stdin.readline()

	render_data_points(times, data_points, config)
	pyplot.show(block=True)

def normalize(values):
	"""
	Normalize a list of numeric values against the maximum absolute value.
	"""

	max_value = float(max(map(abs, values)) or 1)
	return [val / max_value for val in values]

def render_data_points(times, data_points, config):
	"""
	Update the matplotlib figure with new data.
	"""

	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		pyplot.pause(0.01)

	for id_, graph in enumerate(data_points.values(), start=1):
		if config["subplots"]["show"]:
			pyplot.subplot(
				config["subplots"]["vertical"],
				config["subplots"]["horizontal"],
				id_
			)

		y_values = normalize(graph["values"]) if config["normalize"] \
			else graph["values"]
		graph["graph"].set_data(times, y_values)

	axes = pyplot.gca()
	axes.relim()
	axes.autoscale_view()
	pyplot.draw()

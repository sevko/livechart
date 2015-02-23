from matplotlib import pyplot
import sys
import json
import time

# for i in range(9):
	# pyplot.subplot(3, 1, i)

# pyplot.show()

def parse_json(string):
	try:
		json_blob = json.loads(string)

	except ValueError as excep:
		print >> sys.stderr, \
			"{0}Failed to parse JSON for line: {1}".format(excep, string)

	if isinstance(json_blob, (int, float)):
		return {"value": json_blob}

	elif isinstance(json_blob, dict):
		return json_blob

	else:
		print >> sys.stderr, \
			"Decoded JSON is not a chartable data-type: {}".format(json_blob)

def configure_pyplot():
	pyplot.ion()
	pyplot.xlabel("time (seconds)")

def render_stdin():
	startTime = time.time()
	times = [0]

	data_points = {}
	line = sys.stdin.readline()

	num_horizontal = 2
	num_vertical = 2
	subplots = False

	for id_, (key, val) in enumerate(parse_json(line).items(), start=1):
		if subplots:
			pyplot.subplot(num_vertical, num_horizontal, id_)
			pyplot.title(key)

		data_points[key] = {
			"graph": pyplot.plot([val], [val], label=key)[0],
			"values": [val]
		}

	if not subplots and len(data_points) > 1:
		pyplot.legend(loc="lower right")

	while line:
		line = sys.stdin.readline()
		times.append(time.time() - startTime)

		for key, val in parse_json(line).items():
			data_points[key]["values"].append(val)

		render_data_points(subplots, times, data_points)

def render_data_points(subplots, times, data_points):
	num_horizontal = 2
	num_vertical = 2

	normalize = False
	pyplot.pause(0.01)
	for id_, graph in enumerate(data_points.values(), start=1):
		if subplots:
			pyplot.subplot(num_vertical, num_horizontal, id_)

		if normalize:
			max_value = float(max(map(abs, graph["values"])) or 1)
			values = [val / max_value for val in graph["values"]]
		else:
			values = graph["values"]
		graph["graph"].set_data(times, values)

		axes = pyplot.gca()
		axes.relim()
		axes.autoscale_view()

		pyplot.draw()

if __name__ == "__main__":
	configure_pyplot()
	return_code = render_stdin()
	if return_code is not None:
		sys.exit(return_code)

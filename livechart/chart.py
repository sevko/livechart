from matplotlib import pyplot
import sys
import json
import time
import math
import warnings

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

def render_stdin(config):
	startTime = time.time()
	times = [0]

	data_points = {}
	line = sys.stdin.readline()

	initial_data = parse_json(line).items()
	sub_conf = config["subplots"]
	if not ("vertical" in sub_conf and "horizontal" in sub_conf):
		num_data_points = len(initial_data)
		sub_conf["vertical"] = math.ceil(math.sqrt(num_data_points))
		sub_conf["horizontal"] = math.ceil(num_data_points / sub_conf["vertical"])

	elif sub_conf["vertical"] * sub_conf["horizontal"] < len(initial_data):
		print >> sys.stderr, \
			"Provided number of subplots is less than the number of data points."
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

	while line:
		line = sys.stdin.readline()
		times.append(time.time() - startTime)

		for key, val in parse_json(line).items():
			data_points[key]["values"].append(val)

		render_data_points(times, data_points, config)

def normalize(values):
	max_value = float(max(map(abs, values)) or 1)
	return [val / max_value for val in values]

def render_data_points(times, data_points, config):
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

if __name__ == "__main__":
	configure_pyplot()
	return_code = render_stdin({
		"normalize": True,
		"subplots": {
			"show": True
		}
	})
	if return_code is not None:
		sys.exit(return_code)

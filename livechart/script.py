"""
Contains functions for parsing command-line arguments and initializing the
tool. Intended to serve as the command-line entry point.
"""

from __future__ import print_function
import argparse
import sys

from livechart import chart

def parse_args():
	"""
	Parse command-line arguments with `argparse`, and return the resulting
	dictionary.
	"""

	description = (
		"Plot a graph of STDIN data, live. Pipe in either rows of "
		"JSON-serialized dictionaries/objects or numbers. If objects are "
		"received, each top-level key is expected to be mapped to a number."
	)
	parser = argparse.ArgumentParser(
		description=description,
		formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)
	parser.add_argument(
		"-s", "--subplots", default=False, const=True, nargs="?", type=str,
		help=(
			"Whether to plot each data point on a separate graph. "
			"`livechart` will intelligently format the subplots, but you can "
			"specify custom dimensions in the form of a 'XxY' string (eg '5x6')."
		)
	)
	parser.add_argument(
		"-n", "--normalize", action="store_true",
		help=(
			"Whether data points should be normalized. May be desirable when "
			"points with vastly different ranges are getting plotted on the "
			"same graph."
		)
	)

	parser.add_argument(
		"-i", "--interval", type=float, default=1.0, dest="render_interval",
		help="The second interval at which to re-render the graph."
	)

	parser.add_argument(
		"-N", "--no-refresh", action="store_true",
		help=(
			"Whether to refresh the graph while ingesting data, which might "
			"not make sense for bulk loads."
		)
	)

	args = vars(parser.parse_args())
	if not args["subplots"]:
		args["subplots"] = {
			"show": False
		}
	elif isinstance(args["subplots"], str):
		hor, ver = args["subplots"].split("x")
		args["subplots"] = {
			"show": True,
			"horizontal": int(hor),
			"vertical": int(ver)
		}
	else:
		args["subplots"] = {
			"show": True
		}

	return args

def run():
	"""
	Runs the tool.
	"""

	if sys.stdin.isatty():
		print(
			"No STDIN input detected. `livechart --help` for help information.",
			file=sys.stderr
		)
		sys.exit(1)

	chart.configure_pyplot()
	try:
		chart.render_stdin(parse_args())
	except KeyboardInterrupt:
		pass

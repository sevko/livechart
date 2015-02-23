import argparse
# import charter as livechart
import livechart

def parse_args():
	parser = argparse.ArgumentParser(description="Plot a graph of STDIN data, live.")
	parser.add_argument("-s", "--subplots", default=False, const=True, nargs="?", type=str, help="TODO")
	parser.add_argument("-n", "--normalize", action="store_true", help="TODO")

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

livechart.configure_pyplot()
livechart.render_stdin(parse_args())

from routeElevationMapper import RouteElevationMapper
from routeElevationDrawer import RouteElevationDrawer

import argparse
import pathlib
import pickle

def main():
	parser = argparse.ArgumentParser(prog='ConsumptionOverTime',
									 description='Maps the route and draws the electricity consumption or speed over time. Either `--generate` or `--draw` option have to be used.')
	parser.add_argument('-b', '--sumo-binary',
						help='Path to sumo or sumo-gui',
						type=str,
						default='../../sumo/bin/sumo')
	parser.add_argument('-s', '--sumo-scenario',
						help='Path to sumo scenario (\'.sumocfg\' file)',
						type=str,
						default='../StuttgartSouthModel/osm.sumocfg')

	parser.add_argument('-o', '--origin',
						help='EdgeID from netedit that represents the route origin',
						type=str,
						default='4821895#1')
	parser.add_argument('-d', '--destination',
						help='EdgeID from netedit that represents the route destination',
						type=str,
						default='-96266013#0')

	parser.add_argument('-g', '--generate',
						help='Generates the data in the given path',
						type=str,
						default=None)
	parser.add_argument('-c', '--draw-consumption',
						help='Draws the data at the given paths',
						type=str,
						default=None)
	parser.add_argument('-e', '--draw-elevation-time',
						help='Draws the route and elevation over time with the given property name. Property name should be "electricityConsumption" or "speed"',
						type=str,
						default=None)

	args = parser.parse_args()
	rem = RouteElevationMapper(args.sumo_binary, args.sumo_scenario, args.origin, args.destination)

	if args.generate is not None or args.draw_elevation_time is not None:
		rem.simulate()

		if args.generate is not None:
			container = {
				'prefix': pathlib.Path(args.generate).stem,
				'time': rem.time[1:],
				'consumption': rem.route_consumption[1:],
				'speed': rem.route_speed[1:]
			}

			with open(args.generate, 'wb') as fh:
				pickle.dump(container, fh)

		if args.draw_elevation_time is not None:
			red = RouteElevationDrawer(rem, args.draw_elevation_time)
			red.draw_elevation_figure()

	elif args.draw_consumption is not None:

		containers = []

		for path in args.draw_consumption[1:-1].split(', '):
			path = path[1:-1]
			with open(path, 'rb') as fh:
				tmp = pickle.load(fh)
				containers.append(tmp)

		red = RouteElevationDrawer(rem)
		red.draw_consumption_over_time(containers)

	else:
		raise ValueError('One of the options `--generate`, `--draw-consumption`, `--draw-elevation-time` has to be used.')

if __name__ == '__main__':
	main()
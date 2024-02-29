import traci

class RouteElevationMapper:

	def __init__(self, sumo_binary, sumo_scenario, origin, destination,
				 trip_name='test_ebike', veh_id='test_ebike', type_id='e_bicycle',
				 emission_class='Energy/unknown', setup_in_route_file=True):

		self.sumo_cmd = [sumo_binary, '-c', sumo_scenario]
		self.origin = origin
		self.destination = destination

		self.time = []
		self.route_positions = []
		self.route_elevation = []
		self.route_speed = []
		self.route_consumption = []

		self.trip_name = trip_name
		self.veh_id = veh_id
		self.type_id = type_id
		self.emission_class = emission_class

		self.setup_in_route_file = setup_in_route_file



	def setup(self):
		route = traci.simulation.findRoute(self.origin, self.destination)
		traci.route.add(self.trip_name, route.edges)

		traci.vehicle.add(self.veh_id, 'test_trip')
		traci.vehicle.setType(self.veh_id, self.type_id)

		traci.vehicle.setEmissionClass(self.veh_id, self.emission_class)

		traci.vehicle.setVehicleClass(self.veh_id, 'bicycle')
		# Other attributes that correspond to the default parameters of the
		# bicycle vClass
		traci.vehicle.setShapeClass(self.veh_id, 'bicycle')

		traci.vehicle.setLength(self.veh_id, 1.6)
		traci.vehicle.setWidth(self.veh_id, 0.65)
		traci.vehicle.setHeight(self.veh_id, 1.7)

		traci.vehicle.setMinGap(self.veh_id, 0.5)
		traci.vehicle.setAccel(self.veh_id, 1.2)
		traci.vehicle.setDecel(self.veh_id, 3)
		traci.vehicle.setEmergencyDecel(self.veh_id, 7)
		traci.vehicle.setMaxSpeed(self.veh_id, 5.56)

		return route


	def simulate(self):
		traci.start(self.sumo_cmd)

		# Skip setup when defined in route file
		if not self.setup_in_route_file:
			route = self.setup()

		while True:
			try:
				current_position = traci.vehicle.getPosition(self.veh_id)
				lon_lat = traci.simulation.convertGeo(*current_position)
				self.route_positions.append(lon_lat)

				position = traci.vehicle.getPosition3D(self.veh_id)
				current_elevation = position[2]
				self.route_elevation.append(current_elevation)

				current_speed = traci.vehicle.getSpeed(self.veh_id)
				self.route_speed.append(current_speed)

				current_consumption = traci.vehicle.getElectricityConsumption(self.veh_id)
				self.route_consumption.append(current_consumption)

				cur_time_sec = traci.simulation.getCurrentTime() / 1_000
				self.time.append(cur_time_sec)

				print('Time:', cur_time_sec, ' s')
				print('Elevation:', current_elevation)
				print('Speed:', current_speed)
				print('Electricity Consumption:', current_consumption)
				print(50 * '-')

				traci.simulationStep()
			except traci.exceptions.TraCIException:
				break

		traci.close()
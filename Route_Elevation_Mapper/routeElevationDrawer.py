import numpy as np
import matplotlib.pyplot as plt
import pyproj as pp

import pandas as pd
import geopandas as gpd

import contextily as cx
from shapely.geometry import Point


class RouteElevationDrawer:

	def __init__(self, elevation_mapper, property_type='electricityConsumption'):
		self.ele_mapper = elevation_mapper
		self.property = property_type

		self.route_start_wm = None
		self.route_end_wm = None
		self.route_ele_wm = None

		if self.property == 'electricityConsumption':
			self.property_name = 'Electricity Consumption [Wh]'
			self.route_property = self.ele_mapper.route_consumption
		elif self.property == 'speed':
			self.property_name = 'Speed [m/s]'
			self.route_property = self.ele_mapper.route_speed
		else:
			raise ValueError('No such property. Choose between `electricityConsumption` and `speed`.')


	def draw_elevation_figure(self, start_end_colors=['white', 'black'], shrink_fig_wcolorbar=0.81):
		fig1, ax1 = plt.subplots(figsize=(5, 4))
		fig2, ax2 = plt.subplots(figsize=(7, 7))

		scattered = self.draw_elevation_with_property_over_time(ax1)
		self.draw_route(ax2)
		self.draw_bike_stations(ax2)
		self.draw_start_end_points(ax2, start_end_colors)
		self.draw_max_min_elevation(ax2)
		ax2.legend()

		fig1.colorbar(scattered, ax=ax1, label=self.property_name)
		fig2.colorbar(scattered, ax=ax2, label=self.property_name, shrink=shrink_fig_wcolorbar)

		fig1.savefig(f'1_{self.property}_elevationOverTime.png', bbox_inches='tight')
		fig2.savefig(f'2_{self.property}_elevationOverTime.png', bbox_inches='tight')


	def draw_elevation_with_property_over_time(self, ax):
		ax.set_ylabel('Elevation [m]')
		ax.set_xlabel('Time [s]')

		scattered = ax.scatter(self.ele_mapper.time[1:], self.ele_mapper.route_elevation[1:], c=self.route_property[1:], cmap='coolwarm')

		return scattered


	def draw_route(self, ax):
		points = gpd.points_from_xy([lon for lon, lat in self.ele_mapper.route_positions[1:]], [lat for lon, lat in self.ele_mapper.route_positions[1:]])

		gdf_route = gpd.GeoDataFrame(data={'points': points}, crs='epsg:4326', geometry='points')
		gdf_route['speed'] = self.route_property[1:]
		gdf_route['elevation'] = self.ele_mapper.route_elevation[1:]


		gdf_route_wm = gdf_route.to_crs(epsg=3857)
		gdf_route_wm['lon'] = gdf_route_wm['points'].x
		gdf_route_wm['lat'] = gdf_route_wm['points'].y

		self.route_ele_wm = gdf_route_wm

		ax.scatter(gdf_route_wm['lon'], gdf_route_wm['lat'], c=gdf_route_wm['speed'], cmap='coolwarm', alpha=0.7)
		ax.margins(0.3, 0)

		self.route_start_wm = gdf_route_wm.loc[0, ['lon', 'lat']]
		self.route_end_wm = gdf_route_wm.loc[len(gdf_route_wm)-1, ['lon', 'lat']]

		cx.add_basemap(ax, source=cx.providers.CartoDB.Voyager)

		x_labels = ax.get_xticklabels()
		x_labels = [float(label.get_text()) for label in x_labels]
		x_labels_ext = [(x * 10**6, 0) for x in x_labels]

		y_labels = ax.get_yticklabels()
		y_labels = [float(label.get_text()) for label in y_labels]
		y_labels_ext = [(0, y * 10**6) for y in y_labels]

		transformer = pp.Transformer.from_crs('epsg:3857', 'epsg:4326', always_xy=True)
		new_x_labels = list(transformer.itransform(x_labels_ext))
		new_y_labels = list(transformer.itransform(y_labels_ext))

		new_x_labels = [round(x, 2) for x, _ in new_x_labels]
		new_y_labels = [round(y, 2) for _, y in new_y_labels]

		ax.set_xticks(ax.get_xticks())
		ax.set_xticklabels(new_x_labels)

		ax.set_yticks(ax.get_yticks())
		ax.set_yticklabels(new_y_labels)

		ax.set_xlabel('Longitude')
		ax.set_ylabel('Latitude')

		ax.set_aspect('equal')


	def draw_bike_stations(self, ax, stations_path='../GBFS_Import/station_information.json', size=150):
		df = pd.read_json(stations_path)
		df = df['data']
		df = pd.json_normalize(df['stations'])

		df['points'] = gpd.points_from_xy(df['lon'], df['lat'])
		gdf = gpd.GeoDataFrame(data=df[['name', 'capacity', 'points']], crs='epsg:4326', geometry='points')

		gdf_wm = gdf.to_crs(epsg=3857)
		ax.scatter(gdf_wm['points'].x, gdf_wm['points'].y, label='bike station', color='red', s=size, zorder=0, alpha=0.7)


	def draw_start_end_points(self, ax, colors, size=75):
		ax.scatter(self.route_start_wm['lon'], self.route_start_wm['lat'], c=colors[0], label='start', edgecolors='black', linewidth=1.5, marker='h', s=size)
		ax.scatter(self.route_end_wm['lon'], self.route_end_wm['lat'], c=colors[1], label='end', edgecolors='black', linewidth=1.5, marker='H', s=size)


	def draw_max_min_elevation(self, ax, size=50):
		max_ele_idx = self.route_ele_wm['elevation'].idxmax()
		max_ele = self.route_ele_wm.iloc[max_ele_idx]

		min_ele_idx = self.route_ele_wm['elevation'].idxmin()
		min_ele = self.route_ele_wm.iloc[min_ele_idx]

		ax.scatter(min_ele['lon'], min_ele['lat'], c='lightcoral', edgecolors='black', linewidth=0.5, marker='^', s=size, label='elevation')
		ax.annotate(f'{round(min_ele["elevation"])}m', (min_ele['lon'], min_ele['lat']), size=10, xytext=(-35,-2), textcoords='offset points')

		below_min_ele = self.route_ele_wm.iloc[min_ele_idx-100]
		ax.scatter(below_min_ele['lon'], below_min_ele['lat'], c='lightcoral', edgecolors='black', linewidth=0.5, marker='^', s=size)
		ax.annotate(f'{round(below_min_ele["elevation"])}m', (below_min_ele['lon'], below_min_ele['lat']), size=10, xytext=(-35,-2), textcoords='offset points')

		above_ele_idx = min_ele_idx + 200
		while above_ele_idx < len(self.route_ele_wm):
			above_ele = self.route_ele_wm.iloc[above_ele_idx]
			ax.scatter(above_ele['lon'], above_ele['lat'], c='lightcoral', edgecolors='black', linewidth=0.5, marker='^', s=size)
			ax.annotate(f'{round(above_ele["elevation"])}m', (above_ele['lon'], above_ele['lat']), size=10, xytext=(-35,-2), textcoords='offset points')
			above_ele_idx += 200


	def draw_consumption_over_time(self, containers, figsize=(5, 4), linewidth=5):
		fig, ax = plt.subplots(figsize=figsize)

		for i, container in enumerate(containers):
			ax.plot(container['time'], np.cumsum(container['consumption']), c=f'C{i}', label=container['prefix'], alpha=0.7, lw=linewidth)

		ax.set_ylabel('Total Electricity Consumed [Wh]')
		ax.set_xlabel('Time [s]')
		ax.legend()

		fig.savefig('consumptionOverTime.png', bbox_inches='tight')
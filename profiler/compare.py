import numpy as np
from scipy.spatial.distance import pdist, squareform
import os
import sys

def find_closest_group(series, top_x):
	"""
	Find the top X series that group closest together in values.

	Parameters:
	series (list of np.array): List of series where each series is an array of X/Y coordinates.
	top_x (int): Number of top closest series to find.

	Returns:
	list of int: List of indices of the top X closest series.
	"""
	# Calculate the pairwise distances between series
	distances = pdist(series, metric='euclidean')
	distance_matrix = squareform(distances)

	# Sum the distances for each series to all other series
	distance_sums = np.sum(distance_matrix, axis=1)

	# Find the indices of the top X series with the smallest distance sums
	closest_indices = np.argsort(distance_sums)[:top_x]

	return closest_indices

# Example usage
if __name__ == "__main__":

	if len(sys.argv) < 3:
		print("Usage: python compare.py <profiles_folder> <top_x>")
		sys.exit(1)

	profiles_folder = sys.argv[1]
	series = []
	filenames = []

	for filename in os.listdir(profiles_folder):
		filepath = os.path.join(profiles_folder, filename)
		if os.path.isfile(filepath):
			with open(filepath, 'r') as file:
				content = file.read()
				rows = content.split(';')
				d = [int(row.split(',')[1]) for row in rows if row]

				data = np.array(d)
				filenames.append(filename)
			
			series.append(data)

	top_x = int(sys.argv[2])
	closest_indices = find_closest_group(series, top_x)

	# Print the filenames related to the closest indices
	closest_filenames = [filenames[i] for i in closest_indices]
	print("Top {} closest series filenames: {}".format(top_x, closest_filenames))
import numpy as np

class WeightedMeanCalculator:
    def __init__(self):
        pass

    def weighted_mean(self, points, weights):

        assert len(points) == len(weights), "Number of points and weights must be equal"

        # Convert list of arrays to a single array
        points_array = np.array(points)

        # Compute weighted mean for each coordinate
        weighted_mean_x = np.average(points_array[:, 0], axis=0, weights=weights)
        weighted_mean_y = np.average(points_array[:, 1], axis=0, weights=weights)
        weighted_mean_z = np.average(points_array[:, 2], axis=0, weights=weights)
        
        return np.array([weighted_mean_x, weighted_mean_y, weighted_mean_z])
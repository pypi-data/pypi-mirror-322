import numpy as np
from typing import List, Tuple
import matplotlib.pyplot as plt
import math

from utils import get_rotation_matrix

from scipy.spatial import KDTree


# - Lattice vectors must have a +ve y component (both of them need to be in the first or second quadrant)
# - lv1 must be along the x-axis (i.e. have y = 0)
# - accordingly lv2 must be writen
# - If lv2 should not have a negative y component... however if it is desired to have a negative y component, that case is similar to having an lv2 which is
#     180 degrees rotated (diagonally opposite, -lv2) which has a +ve y component and should be used instead


class Layer:  # parent class
    def __init__(self, pbc=False, study_proximity = 1) -> None:
        self.toll_scale = max(
            np.linalg.norm(self.lv1),
            np.linalg.norm(self.lv2)
        )

        if self.lv1[1] != 0 or self.lv2[1] < 0:
            raise ValueError(
                """lv1 was expected to be along the x-axis, and lv2 should have a +ve y component
                Please refer to the documentation for more information: https://example.com
                """  # @jabed add link to documentation
            )

        self.rot_m = np.eye(2)
        self.pbc = pbc
        self.points = None
        self.kdtree = None
        self.study_proximity = study_proximity

    def perform_rotation(self, rot=None) -> None:
        rot_m = get_rotation_matrix(rot)
        self.rot_m = rot_m

        # Rotate lv1 and lv2 vectors
        self.lv1 = rot_m @ self.lv1
        self.lv2 = rot_m @ self.lv2

        # Rotate lattice_points
        self.lattice_points = [
            [*(rot_m @ np.array([x, y])), atom_type]
            for x, y, atom_type in self.lattice_points
        ]

        # Rotate neighbours
        self.neighbours = {
            atom_type: [rot_m @ np.array(neighbour) for neighbour in neighbour_list]
            for atom_type, neighbour_list in self.neighbours.items()
        }

    def generate_points(
            self,
            mlv1: np.array,
            mlv2: np.array,
            mln1: int=1,
            mln2: int=1,
            # bring_to_center=False
        ) -> None:
        self.mlv1 = mlv1  # Moire lattice vector 1
        self.mlv2 = mlv2  # Moire lattice vector 2
        self.mln1 = mln1  # Number of moire unit cells along mlv1
        self.mln2 = mln2  # Number of moire unit cells along mlv2

        # Step 1: Find the maximum distance to determine the grid resolution
        points = [np.array([0, 0]), mlv1, mlv2, mlv1 + mlv2]
        max_distance = max(
            np.linalg.norm(points[0] - points[1]),
            np.linalg.norm(points[0] - points[2]),
            np.linalg.norm(points[0] - points[3]),
        )

        # Calculate number of grid points based on maximum distance and lattice vectors
        n = math.ceil(max_distance / min(np.linalg.norm(self.lv1), np.linalg.norm(self.lv2))) * 2

        # print(f"Calculated grid size: {n}")

        # Step 2: Generate points inside one moire unit cell (based on `lv1` and `lv2`)
        step1_points = []  # List to hold points inside the unit cell
        step1_names = []  # List to hold the names of the points
        for i in range(-n, n+1):  # Iterate along mlv1
            for j in range(-n, n+1):  # Iterate along mlv2
                # Calculate the lattice point inside the unit cell
                point_o = i * self.lv1 + j * self.lv2
                for xpos, ypos, name in self.lattice_points:
                    point = point_o + np.array([xpos, ypos])
                    step1_points.append(point)
                    step1_names.append(name)

        step1_points = np.array(step1_points)
        step1_names = np.array(step1_names)

        # Apply the boundary check method (_inside_boundaries) to filter the points
        mask = self._inside_boundaries(step1_points, 1, 1)
        step1_points = step1_points[mask]
        step1_names = step1_names[mask]

        # Step 3: Copy and translate the unit cell to create the full moire pattern
        points = []  # List to hold all the moire points
        names = []
        for i in range(self.mln1):  # Translate along mlv1 direction
            for j in range(self.mln2):  # Translate along mlv2 direction
                translation_vector = i * mlv1 + j * mlv2
                translated_points = step1_points + translation_vector  # Translate points
                points.append(translated_points)
                names.append(step1_names)

        self.points = np.vstack(points)
        self.point_types = np.hstack(names)
        # print(f"{self.point_types.shape=}, {self.points.shape=}")
        self.generate_kdtree()

    def _point_positions(self, points: np.ndarray, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        # for each point this returns it's position corresponding to the parallelogram of interest
        # - if the point is inside, returns (0, 0)
        # - for outside, left side and right side will give -1 and 1 respectively
        # - for outside, top side and bottom side will give -1 and 1 respectively

        # Compute determinants for positions relative to OA and BC
        det_OA = (points[:, 0] * A[1] - points[:, 1] * A[0]) <= self.toll_scale * 1e-2
        det_BC = ((points[:, 0] - B[0]) * A[1] - (points[:, 1] - B[1]) * A[0]) <= self.toll_scale * 1e-2
        position_y = det_OA.astype(float) + det_BC.astype(float)

        # Compute determinants for positions relative to OB and AC
        det_OB = (points[:, 0] * B[1] - points[:, 1] * B[0]) > -self.toll_scale * 1e-2
        det_AC = ((points[:, 0] - A[0]) * B[1] - (points[:, 1] - A[1]) * B[0]) > -self.toll_scale * 1e-2
        position_x = det_OB.astype(float) + det_AC.astype(float)

        return np.column_stack((position_x, position_y)) - 1

    def _inside_polygon(self, points: np.ndarray, polygon: np.ndarray) -> np.ndarray:
        # find the points inside the polygon using the ray casting method
        x, y = points[:, 0], points[:, 1]
        px, py = polygon[:, 0], polygon[:, 1]
        px_next, py_next = np.roll(px, -1), np.roll(py, -1)
        edge_cond = (y[:, None] > np.minimum(py, py_next)) & (y[:, None] <= np.maximum(py, py_next))
        with np.errstate(divide='ignore', invalid='ignore'):
            xinters = np.where(py != py_next, (y[:, None] - py) * (px_next - px) / (py_next - py) + px, np.inf)
        ray_crosses = edge_cond & (x[:, None] <= xinters)
        inside = np.sum(ray_crosses, axis=1) % 2 == 1
        return inside  # mask

    def _inside_boundaries(self, points: np.ndarray, mln1=None, mln2=None) -> np.ndarray:

        v1 = (mln1 if mln1 else self.mln1) * self.mlv1
        v2 = (mln2 if mln2 else self.mln2) * self.mlv2

        p1 = np.array([0, 0])
        p2 = np.array([v1[0], v1[1]])
        p3 = np.array([v2[0], v2[1]])
        p4 = np.array([v1[0] + v2[0], v1[1] + v2[1]])

        return self._inside_polygon(
            points,
            np.array([p1, p2, p4, p3]) - self.toll_scale * 1e-4
        )

    def generate_kdtree(self) -> None:
        if not self.pbc:  # OBC is easy
            self.kdtree = KDTree(self.points)
            return

        # in case of periodic boundary conditions, we need to generate a bigger set of points
        all_points = []
        all_point_names = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                all_points.append(self.points + i * self.mln1 * self.mlv1 + j * self.mln2 * self.mlv2)
                all_point_names.append(self.point_types)

        all_points = np.vstack(all_points)
        all_point_names = np.hstack(all_point_names)

        v1 = self.mln1 * self.mlv1
        v2 = self.mln2 * self.mlv2

        neigh_pad_1 = (1 + self.study_proximity) * np.linalg.norm(self.lv1) / np.linalg.norm(v1)
        neigh_pad_2 = (1 + self.study_proximity) * np.linalg.norm(self.lv2) / np.linalg.norm(v2)

        mask = self._inside_polygon(all_points, np.array([
                ( -neigh_pad_1) * v1 + ( -neigh_pad_2) * v2,
                (1+neigh_pad_1) * v1 + ( -neigh_pad_2) * v2,
                (1+neigh_pad_1) * v1 + (1+neigh_pad_2) * v2,
                ( -neigh_pad_1) * v1 + (1+neigh_pad_2) * v2,
            ])
        )
        print(mask.shape, mask.dtype)
        points = all_points[mask]
        point_names = all_point_names[mask]

        self.bigger_points = points
        self.bigger_point_types = point_names


        self.kdtree = KDTree(points)




        # # plot the points but with colours based on the point_positions
        # # - point_positions = [0, 0] -> black
        # # - point_positions = [1, 0] -> red
        # # - do not plot the rest of the points at all

        # plt.plot(points[point_positions[:, 0] == 0][:, 0], points[point_positions[:, 0] == 0][:, 1], 'k.')
        # plt.plot(points[point_positions[:, 0] == 1][:, 0], points[point_positions[:, 0] == 1][:, 1], 'r.')

        # plt.plot(*all_points.T, "ro")
        # plt.plot(*points.T, "b.")

        # # parallellogram around the whole lattice
        # plt.plot([0, self.mln1*self.mlv1[0]], [0, self.mln1*self.mlv1[1]], 'k', linewidth=1)
        # plt.plot([0, self.mln2*self.mlv2[0]], [0, self.mln2*self.mlv2[1]], 'k', linewidth=1)
        # plt.plot([self.mln1*self.mlv1[0], self.mln1*self.mlv1[0] + self.mln2*self.mlv2[0]], [self.mln1*self.mlv1[1], self.mln1*self.mlv1[1] + self.mln2*self.mlv2[1]], 'k', linewidth=1)
        # plt.plot([self.mln2*self.mlv2[0], self.mln1*self.mlv1[0] + self.mln2*self.mlv2[0]], [self.mln2*self.mlv2[1], self.mln1*self.mlv1[1] + self.mln2*self.mlv2[1]], 'k', linewidth=1)

        # # just plot mlv1 and mlv2 parallellogram
        # plt.plot([0, self.mlv1[0]], [0, self.mlv1[1]], 'k', linewidth=1)
        # plt.plot([0, self.mlv2[0]], [0, self.mlv2[1]], 'k', linewidth=1)
        # plt.plot([self.mlv1[0], self.mlv1[0] + self.mlv2[0]], [self.mlv1[1], self.mlv1[1] + self.mlv2[1]], 'k', linewidth=1)
        # plt.plot([self.mlv2[0], self.mlv1[0] + self.mlv2[0]], [self.mlv2[1], self.mlv1[1] + self.mlv2[1]], 'k', linewidth=1)

        # plt.grid()
        # plt.show()

        self._generate_mapping()

    def _generate_mapping(self) -> None:
        self.mappings = {}
        tree = KDTree(self.points)
        translations = self._point_positions(
            self.bigger_points,
            self.mln1 * self.mlv1,
            self.mln2 * self.mlv2
        )


        for i, (dx, dy) in enumerate(translations):
            point = self.bigger_points[i] - (dx * self.mlv1 * self.mln1 + dy * self.mlv2 * self.mln2)
            distance, index = tree.query(point)
            if distance >= self.toll_scale * 1e-3:
                print(f"Distance {distance} exceeds tolerance for point {i} at location {point} with translation ({dx}, {dy}).")


                plt.plot(*self.bigger_points.T, "ko", alpha=0.3)
                plt.plot(*self.points.T, "k.")



                # plt.plot(*self.bigger_points[i], "b.")
                # plt.plot(*point, "r.")
                # plt.plot(*self.points[index], "g.")


                # parallellogram around the whole lattice
                plt.plot([0, self.mln1*self.mlv1[0]], [0, self.mln1*self.mlv1[1]], 'k', linewidth=1)
                plt.plot([0, self.mln2*self.mlv2[0]], [0, self.mln2*self.mlv2[1]], 'k', linewidth=1)
                plt.plot([self.mln1*self.mlv1[0], self.mln1*self.mlv1[0] + self.mln2*self.mlv2[0]], [self.mln1*self.mlv1[1], self.mln1*self.mlv1[1] + self.mln2*self.mlv2[1]], 'k', linewidth=1)
                plt.plot([self.mln2*self.mlv2[0], self.mln1*self.mlv1[0] + self.mln2*self.mlv2[0]], [self.mln2*self.mlv2[1], self.mln1*self.mlv1[1] + self.mln2*self.mlv2[1]], 'k', linewidth=1)

                # just plot mlv1 and mlv2 parallellogram
                plt.plot([0, self.mlv1[0]], [0, self.mlv1[1]], 'k', linewidth=1)
                plt.plot([0, self.mlv2[0]], [0, self.mlv2[1]], 'k', linewidth=1)
                plt.plot([self.mlv1[0], self.mlv1[0] + self.mlv2[0]], [self.mlv1[1], self.mlv1[1] + self.mlv2[1]], 'k', linewidth=1)
                plt.plot([self.mlv2[0], self.mlv1[0] + self.mlv2[0]], [self.            mlv2[1], self.mlv1[1] + self.mlv2[1]], 'k', linewidth=1)
                # for index, point in enumerate(self.bigger_points):
                #     plt.text(*point, f"{index}", fontsize=6)
                plt.gca().add_patch(plt.Circle(point, distance/2, color='r', fill=False))

                plt.grid()
                plt.show()

                raise ValueError(f"FATAL ERROR: Distance {distance} exceeds tolerance for point {i} at location {point}.")
            self.mappings[i] = index

        # point positions... for each point in self.point, point position is a array of length 2 (x, y)
        # where the elemnts are -1, 0 and 1... this is what their value mean about their position
        # 
        # (-1, 1) | (0, 1) | (1, 1)
        # -----------------------------
        # (-1, 0) | (0, 0) | (1, 0)
        # -----------------------------
        # (-1,-1) | (0,-1) | (1,-1)
        # 
        # (0, 0) is our actual lattice part... 
        # do this for all points in self.bigger_points:
        # all point with point_positions = (x, y) need to be translated by
        # (-x*self.mlv1*self.mln1 - y*self.mlv2*self.mln2) to get the corresponding point inside the lattice
        # then you would need to run a query on a newly kdtree of the smaller points...
        # to the get the index of the corresponding point inside the lattice (distance should be zero, just saying)
        # now we already know the index of the point in the self.bigger_points... so we can map that to the index of the point in the self.points
        # then we will store that in `self.mappings``
        # self.mapppings will be a dictionary with keys as the indices in the
        # self.bigger_points (unique) and values as the indices in the self.points (not unique)


    # def kth_nearest_neighbours(self, points, types, k = 1) -> None:
    #     distance_matrix = self.kdtree.sparse_distance_matrix(self.kdtree, k)


    def first_nearest_neighbours(self, points: np.ndarray, types: np.ndarray):
        assert self.kdtree is not None, "Generate the KDTree first by calling `Layer.generate_kdtree()`."
        assert points.shape[0] == types.shape[0], "Mismatch between number of points and types."

        distances_list, indices_list = [], []

        for point, t in zip(points, types):
            if t not in self.neighbours:
                raise ValueError(f"Point type '{t}' is not defined in self.neighbours.")

            relative_neighbours = np.array(self.neighbours[t])
            absolute_neighbours = point + relative_neighbours
            distances, indices = self.kdtree.query(absolute_neighbours, k=1)

            filtered_distances, filtered_indices = [], []
            for dist, idx in zip(distances, indices):
                if self.pbc:
                    if dist > 1e-2 * self.toll_scale:
                        raise ValueError(f"Distance {dist} exceeds tolerance.")
                    filtered_distances.append(dist)
                    filtered_indices.append(self.mappings[idx])
                else:
                    # if dist > 1e-2 * self.toll_scale:
                    #     raise ValueError(f"Distance {dist} exceeds tolerance.")
                    filtered_distances.append(dist)
                    filtered_indices.append(idx)

            distances_list.append(filtered_distances)
            indices_list.append(filtered_indices)

        return distances_list, indices_list


    def query(self, points: np.ndarray, k: int = 1) -> Tuple[np.ndarray, np.ndarray]:
        # Step 1:
        # - get a normal query from KDTree
        # - distance, index = self.kdtree.query(points, k=k)
        # - remove all the points farther than (1+0.1*toll_scale) * min distance
        # - return here just that if OBC

        # Step 2: it will come here if PBC is True
        # - for all the points map them using self.mappings
        # - replace the indices with the mapped indices
        # - return the mapped indices and distances (distance will be the same)

        assert self.kdtree is not None, "Generate the KDTree first by calling `Layer.generate_kdtree()`."
        distances, indices = self.kdtree.query(points, k=k)

        # for k=1, it returns squeezed arrays... so we need to unsqueeze them
        if k == 1:
            distances = distances[:, None]
            indices = indices[:, None]

        distances_list, indices_list = distances.tolist(), indices.tolist()
        if k > 1:
            # Set minimum distance threshold
            min_distance = distances[:, 1].min()
            threshold = (1 + 1e-2 * self.toll_scale) * min_distance
            # print(f"{min_distance = }, {threshold = }")

            # Filter distances and indices based on thresholds
            for i in range(len(distances_list)):
                while distances_list[i] and distances_list[i][-1] > threshold:
                    distances_list[i].pop()
                    indices_list[i].pop()

        if not self.pbc:
            return distances_list, indices_list


        # Convert lists back to numpy arrays for PBC
        try:
            distances = np.array(distances_list)
            indices = np.array(indices_list)
        except ValueError as e:
            raise RuntimeError("FATAL ERROR: Uneven row lengths in PBC.") from e

        # Apply mappings
        try:
            vectorized_fn = np.vectorize(self.mappings.get)
            remapped_indices = vectorized_fn(indices)
        except TypeError as e:
            raise RuntimeError("FATAL ERROR: Mapping failed during vectorization. Check if all indices are valid.") from e
        return distances, remapped_indices

    def query_non_self(self, points: np.ndarray, k: int = 1) -> Tuple[np.ndarray, np.ndarray]:
        distances, indices = self.query(points, k=k+1)

        if self.pbc is False:
            for i in range(len(indices)):
                indices[i] = indices[i][1:]
                distances[i] = distances[i][1:]
        else:
            indices = indices[:, 1:]
            distances = distances[:, 1:]

        # return distances[:, 1:], indices[:, 1:]
        return distances, indices


    def plot_lattice(self, plot_connections: bool = True, plot_unit_cell: bool = False) -> None:
        # plt.figure(figsize=(8, 8))

        for atom_type, atom_points in self.lattice_points.items():
            x_coords = [point[0] for point in atom_points]
            y_coords = [point[1] for point in atom_points]
            plt.scatter(x_coords, y_coords, s=50)

            if plot_connections:
                for point in atom_points:
                    for neighbor in self.neighbours[atom_type]:
                        connection = point + np.array(neighbor)
                        plt.plot(
                            [point[0], connection[0]],
                            [point[1], connection[1]],
                            "r--",
                            alpha=0.5,
                        )

        if plot_unit_cell:
            for i in range(self.ny + 1):
                # line from (lv1*0 + lv2*i) to (lv1*nx + lv2*i)
                plt.plot(
                    [self.lv1[0] * 0 + self.lv2[0] * i, self.lv1[0] * self.nx + self.lv2[0] * i],
                    [self.lv1[1] * 0 + self.lv2[1] * i, self.lv1[1] * self.nx + self.lv2[1] * i],
                    "k:",
                    alpha=0.3,
                )

            for i in range(self.nx + 1):
                # line from (lv1*i + lv2*0) to (lv1*i + lv2*ny)
                plt.plot(
                    [self.lv1[0] * i + self.lv2[0] * 0, self.lv1[0] * i + self.lv2[0] * self.ny],
                    [self.lv1[1] * i + self.lv2[1] * 0, self.lv1[1] * i + self.lv2[1] * self.ny],
                    "k:",
                    alpha=0.3,
                )

        plt.title("Lattice Points")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.axis("equal")



# ===============================================
# ========      some example layers      ======== 
# ===============================================



class SquareLayer(Layer):
    def __init__(self, pbc=False) -> None:
        self.lv1 = np.array([1, 0])  # Lattice vector in the x-direction
        self.lv2 = np.array([0, 1])  # Lattice vector in the y-direction
        self.lattice_points = (
            [0, 0, "A"],
        )
        self.neighbours = {
            "A": [
                [1, 0],  # Right
                [0, 1],  # Up
                [-1, 0], # Left
                [0, -1], # Down
            ],
        }
        self.study_proximity = 1
        # study_proximity = 1 means only studying nearest neighbours will be eabled, 2 means study of next nearest neighbours will be enabled too and so on
        super().__init__(pbc=pbc)  # this has to go at the end

class TriangularLayer(Layer):
    def __init__(self, pbc=False) -> None:
        self.lv1 = np.array([1, 0])  # Lattice vector in the x-direction
        self.lv2 = np.array([0.5, np.sqrt(3)/2])  # Lattice vector at 60 degrees
        self.lattice_points = (
            [0, 0, "A"],
        )
        self.neighbours = {
            "A": [
                [1, 0],  # Right
                [0.5, np.sqrt(3)/2],  # Right-up
                [-0.5, np.sqrt(3)/2],  # Left-up
                [-1, 0],  # Left
                [-0.5, -np.sqrt(3)/2],  # Left-down
                [0.5, -np.sqrt(3)/2],  # Right-down
            ],
        }
        self.study_proximity = 1
        # study_proximity = 1 means only studying nearest neighbours will be eabled, 2 means study of next nearest neighbours will be enabled too and so on
        super().__init__(pbc=pbc)  # this has to go at the end

class Rhombus60Layer(Layer):
    def __init__(self, pbc=False) -> None:
        angle = 60  # hardcoded angle... make a copy of the whole class for different angles
        self.lv1 = np.array([1, 0])  # Lattice vector in the x-direction
        cos_angle = np.cos(np.radians(angle))
        sin_angle = np.sin(np.radians(angle))
        self.lv2 = np.array([cos_angle, sin_angle])  # Lattice vector at specified angle
        self.lattice_points = np.array(
            [0, 0, "A"],
        )
        self.neighbours = {
            "A": [
                [1, 0],  # Right
                [cos_angle, sin_angle],  # Up
                [-1, 0],  # Left
                [-cos_angle, -sin_angle],  # Down
            ],
        }
        self.study_proximity = 1
        # study_proximity = 1 means only studying nearest neighbours will be eabled, 2 means study of next nearest neighbours will be enabled too and so on
        super().__init__(pbc=pbc)  # this has to go at the end


# class KagomeLayer(Layer):
#     def __init__(self, pbc=False) -> None:
#         self.lv1 = np.array([1, 0])  # Lattice vector in the x-direction
#         self.lv2 = np.array([0.5, np.sqrt(3)/2])  # Lattice vector at 60 degrees

#         self.lattice_points = (
#             [0, 0, "A"],
#             [0.5, 0, "B"],
#             [0.25, np.sqrt(3)/4, "C"],
#         )

#         self.neighbours = {
#             "A": [
#                 [ 0.5,              0],  # Right
#                 [ 0.25,  np.sqrt(3)/4],  # Right-up
#                 [-0.5,              0],  # Left
#                 [-0.25, -np.sqrt(3)/4],  # Left-down
#             ],
#             "B": [
#                 [ 0.5,              0],  # Right
#                 [-0.25,  np.sqrt(3)/4],  # Left-up
#                 [-0.5,              0],  # Left
#                 [ 0.25, -np.sqrt(3)/4],  # Right-down
#             ],
#             "C": [
#                 [ 0.25,  np.sqrt(3)/4],  # Right-up
#                 [-0.25,  np.sqrt(3)/4],  # Left-up
#                 [-0.25, -np.sqrt(3)/4],  # Left-down
#                 [ 0.25, -np.sqrt(3)/4],  # Right-down
#             ],
#         }
#         super().__init__(pbc=pbc)


# class HexagonalLayer(Layer):
#     def __init__(self, pbc=False) -> None:
#         self.lv1 = np.array([1, 0]) # Lattice vector in the x-direction
#         self.lv2 = np.array([0.5, np.sqrt(3) / 2])

#         self.lattice_points = (
#             # coo_x, coo_y, atom_type (unique)
#             [0, 0, "A"],
#             [1, 1/np.sqrt(3), "B"],
#         )
#         self.neighbours = {
#             "A": [
#                 [0, 1/np.sqrt(3)],
#                 [-0.5, -1/(2 * np.sqrt(3))],
#                 [ 0.5, -1/(2 * np.sqrt(3))],
#             ],
#             "B": [
#                 [0.5, 1/(2 * np.sqrt(3))],
#                 [-0.5, 1/(2 * np.sqrt(3))],
#                 [0, -1/np.sqrt(3)],
#             ],
#         }
#         super().__init__(pbc=pbc)
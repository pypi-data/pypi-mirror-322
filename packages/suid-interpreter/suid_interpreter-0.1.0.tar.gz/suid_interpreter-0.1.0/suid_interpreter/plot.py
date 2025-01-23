import numpy as np
import matplotlib.pyplot as plt
from math import *
class Plane:
    def __init__(self, _min_coordinate, _max_coordinate, point_a, point_b):
        self._max = np.array(_max_coordinate)
        self._min = np.array(_min_coordinate)
        self.point_a = np.array(point_a)
        self.point_b = np.array(point_b)

class Correlation:
    def __init__(self, plane_a, plane_b):
        self.plane_a = plane_a
        self.plane_b = plane_b

    @property
    def scale_matrix(self):
        # Escala baseada na razão entre as distâncias
        dist_a = np.linalg.norm(self.plane_a.point_b - self.plane_a.point_a)
        dist_b = np.linalg.norm(self.plane_b.point_b - self.plane_b.point_a)
        scale = dist_b / dist_a
        return np.array([[scale, 0, 0],
                         [0, scale, 0],
                         [0, 0, 1]])

    @property
    def rotation_matrix(self):
        # Ângulo de rotação entre os vetores dos pontos
        delta_a = self.plane_a.point_b - self.plane_a.point_a
        delta_b = self.plane_b.point_b - self.plane_b.point_a
        angle = np.arctan2(delta_b[1], delta_b[0]) - np.arctan2(delta_a[1], delta_a[0])
        
        # angle = np.rad2deg(np.arctan2(plane_b.point_b[1], plane_b.point_b[0]))
        # angle2 = np.rad2deg(np.arctan2(plane_a.point_b[1], plane_a.point_b[0]))
        print("angles:", np.rad2deg(angle))
        return Correlation.calc_rotation(angle) 
        
    
    def calc_rotation(angle):
        # angle = np.rad2deg(angle)
        return np.array([[cos(angle), -sin(angle), 0],
                        [sin(angle), cos(angle), 0],
                        [0, 0, 1]])

    @property
    def reflection_matrix(self):
        # Verificação de reflexão com base no determinante
        delta_a = self.plane_a.point_b - self.plane_a.point_a
        delta_b = self.plane_b.point_b - self.plane_b.point_a

        print("A:", self.plane_a.point_a, self.plane_a.point_b)
        print("B:", self.plane_b.point_a, self.plane_b.point_b)
        print("deltas:",delta_a, delta_b)

        # Obter os sinais de cada componente
        signal_a = np.sign(delta_a)
        signal_b = np.sign(delta_b)

        print("signals:", signal_a, signal_b)

        signals = signal_a*signal_b
        # Verificar igualdade dos sinais para determinar reflexão
        # reflect_x = 1 if signal_a[0] == signal_b[0] else -1
        # reflect_y = 1 if signal_a[1] == signal_b[1] else -1

        # Construir a matriz de reflexão
        return np.array([
            [signals[0] or 1, 0, 0],
            [0, signals[1] or 1, 0],
            [0, 0, 1]
        ])

    @property
    def translation_matrix(self):

        reflect = lambda c: (np.r_[c,[1]] @ self.reflection_matrix)[:2]

        signal_a = reflect(reflect(self.plane_a.point_a)-self.plane_b.point_a)*-1
        delta_a = self.plane_a.point_b - self.plane_a.point_a
        delta_b = self.plane_b.point_b - self.plane_b.point_a

        print(delta_a, delta_b)

        # signal_a = delta_b-delta_a
        return np.array([[1, 0, signal_a[0]],
                         [0, 1, signal_a[1]],
                         [0, 0, 1]]) 

    @property
    def matrix(self):
        # Ordem: escala -> rotação -> reflexão -> translação
        # return self.rotation_matrix @ self.translation_matrix #@ self.reflection_matrix
        return self.translation_matrix @ self.rotation_matrix
        # return np.array([[1, 0, 0],
        #                  [0, 1, 0],
        #                  [0, 0, 1]])

    def apply_transformation(self, coords, transformation):
        # Adiciona a dimensão homogênea para multiplicação
        coords_homogeneous = np.hstack((coords, np.ones((coords.shape[0], 1))))
        transformed_coords = (transformation @ coords_homogeneous.T).T
        return transformed_coords[:, :2]  # Retorna às dimensões 2D

    def plot_planes(self, coordinates, correct_coordinates):
        # Plota os planos A e B, com os pontos e a transformação aplicada
        coords_a = np.array(coordinates)
        coords_b = self.apply_transformation(coords_a, self.matrix)
        # print("RESP:", coords_b)
        # Plotando o plano A e os pontos
        plt.scatter(coords_a[:, 0], coords_a[:, 1], color='blue', label="Plano A")
        plt.scatter(coords_b[:, 0], coords_b[:, 1], color='red', label="Plano B")
        
        plt.plot([coords_a[0, 0], coords_a[1, 0]], [coords_a[0, 1], coords_a[1, 1]], 'bo-', label="Plano A Linha")
        plt.plot([coords_b[0, 0], coords_b[1, 0]], [coords_b[0, 1], coords_b[1, 1]], 'ro-', label="Plano B Linha")
        plt.plot([correct_coordinates[0, 0], correct_coordinates[1, 0]], [correct_coordinates[0, 1], correct_coordinates[1, 1]], 'go-', label="Plano B Linha Certa")
        
        plt.xlabel('Eixo X')
        plt.ylabel('Eixo Y')
        plt.xticks(range(-30, 31))
        plt.yticks(range(-30, 31))
        plt.legend()
        plt.grid(True)
        plt.show()


# Exemplo de uso

c_a = [(98, 14), (14, 98)]
c_b = [(46, 46), (-38, -38)]
# plane_a = Plane((0, 0), (112, 112), *c_a)
# plane_b = Plane((0, 0), (112, 112), *c_b)

# c_a = [(0, 0), (20, 0)]
plane_a = Plane((0, 0), (112, 112), *c_a)

offset = np.array([-10,2])
mirror = np.array([1,1])
angle = np.deg2rad(90)

pba = ((Correlation.calc_rotation(angle) @ np.array([*plane_a.point_a,1]))[:2]+offset)*mirror
pbb = ((Correlation.calc_rotation(angle) @ np.array([*plane_a.point_b,1]))[:2]+offset)*mirror

# c_b = [ pba, pbb]
plane_b = Plane((0, 0), (112, 112), *c_b)


correlation = Correlation(plane_a, plane_b)
# coordinates = [(5, 0), (-5, 0)]
coordinates = c_a
# print(correlation.scale_matrix)
print(correlation.reflection_matrix)
print(correlation.translation_matrix)
# print(correlation.rotation_matrix)
# result = correlation.apply_transformation(np.array([10,10,1]), correlation.reflection_matrix @ correlation.translation_matrix )
# print("Result: ",result, pba)
# result = correlation.apply_transformation(result, correlation.translation_matrix)
# print(result)

# # print(result == c_b)
correlation.plot_planes(np.array(c_a), np.array(c_b))
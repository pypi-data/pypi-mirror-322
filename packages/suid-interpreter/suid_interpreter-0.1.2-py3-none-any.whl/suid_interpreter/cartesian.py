#from worldmapping import PointCorrelation as CameraMatrices
import numpy as np

class Transformation2D:
    """Classe para lidar com transformações homogêneas em 2D."""
    def __init__(self, source_points, target_points):
        """
        Inicializa a transformação calculando a matriz homogênea baseada
        em pares de pontos fornecidos.
        
        :param source_points: Pontos de origem (Nx2)
        :param target_points: Pontos de destino (Nx2)
        """
        if len(source_points) < 3 or len(target_points) < 3:
            raise ValueError("São necessários pelo menos 3 pontos para calcular a transformação.")
        
        self.source_points = np.array(source_points)
        self.target_points = np.array(target_points)
        self.transformation_matrix = self._calculate_transformation_matrix()
    
    def _calculate_transformation_matrix(self):
        """Calcula a matriz de transformação homogênea usando mínimos quadrados."""
        A = []
        B = []
        for (x, y), (xp, yp) in zip(self.source_points, self.target_points):
            A.extend([
                [x, y, 1, 0, 0, 0],
                [0, 0, 0, x, y, 1]
            ])
            B.extend([xp, yp])
        
        A = np.array(A)
        B = np.array(B)

        # Resolve o sistema para obter os coeficientes da matriz
        coeffs = np.linalg.lstsq(A, B, rcond=None)[0]
        return np.array([
            [coeffs[0], coeffs[1], coeffs[2]],
            [coeffs[3], coeffs[4], coeffs[5]],
            [0, 0, 1]
        ])
    
    def transform(self, points):
        """
        Aplica a transformação em um conjunto de pontos.
        
        :param points: Pontos para transformar (Nx2)
        :return: Pontos transformados (Nx2)
        """
        points_homogeneous = np.hstack((points, np.ones((len(points), 1))))
        transformed_points = (self.transformation_matrix @ points_homogeneous.T).T
        return transformed_points[:, :2]
    
    def inverse_transform(self, points):
        """
        Aplica a transformação inversa em um conjunto de pontos.
        
        :param points: Pontos para transformar (Nx2)
        :return: Pontos transformados inversamente (Nx2)
        """
        inv_matrix = np.linalg.inv(self.transformation_matrix)
        points_homogeneous = np.hstack((points, np.ones((len(points), 1))))
        transformed_points = (inv_matrix @ points_homogeneous.T).T
        return transformed_points[:, :2]

class plane:
    def __init__(self, known_coordinates=None):
        self.known_coordinates = known_coordinates
        self.coordinate = None

    def setCoordinate(self, coordinate):
        self.coordinate = coordinate

    def getCoordinate(self):
        return {k:v for k,v in zip(['x','y','z'],self.coordinate.flatten())}

class correlation:
    def __init__(self, virtual_plane, real_plane):
        self.virtual_plane = virtual_plane
        self.real_plane = real_plane

    def virtual2real(self, coordinate):
        pass

    def real2virtual(self, coordinate):
        pass

    def update(self):
        self.real_plane.coordinate = self.virtual2real(self.virtual_plane.coordinate)

class CameraCorrelation(correlation):
    def __init__(self, virtual_plane, real_plane):
        super().__init__(virtual_plane, real_plane)
        self.matrices = None #CameraMatrices()

    def virtual2real(self, coordinate):
        return self.matrices._3DP(coordinate)
    
    def real2virtual(self, coordinate):
        return self.matrices._2DP(coordinate)

class BoardCorrelation(correlation):
    def __init__(self, virtual_plane:plane, real_plane:plane):
        super().__init__(virtual_plane, real_plane)
        self.transformer = Transformation2D(virtual_plane.known_coordinates, real_plane.known_coordinates)
    
    @property
    def matrix(self):
        # inter scale signal to mirro axis
        return self.transformer.transformation_matrix
    
    def virtual2real(self, coordinates):
        return self.transformer.transform(coordinates.reshape(1,3)[:,:2])
    
    def real2virtual(self, coordinates):
        return self.transformer.inverse_transform(coordinates)

class Object:
    def __init__(self, *correlations):
        self.crrs = correlations
    
    def setCoordinate(self, plane, coordinate):
        plane.setCoordinate(coordinate)

        for c in self.crrs:
            c.update()

    def getCoordinate(self, plane):
        return  plane.getCoordinate()


if __name__ == '__main__':
    camera  = plane((0,0), (1280, 960))
    board   = plane((50,50), (100, 100))
    machine = plane((0,0), (100, 100))

    C2B = CameraCorrelation(camera, board)
    B2M = BoardCorrelation(board, machine)

    item = Object(B2M)

    coordinate = np.array((50, 50, 0))

    item.setCoordinate(board, coordinate)

    print(item.getCoordinate(machine))



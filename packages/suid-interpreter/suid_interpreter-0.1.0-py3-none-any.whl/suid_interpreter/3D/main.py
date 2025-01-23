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

# Testando a classe
if __name__ == "__main__":
    # Pontos de origem e destino
    source = [(98, 14), (98/2, 14/2), (98/4, 14/4), (14, 98)]
    target = [(52, 53), (52/2, 53/2), (52/4, 53/4), (-38, -34)]
    
    # Instanciação da classe
    transform = Transformation2D(source, target)
    
    # Transformação direta
    transformed_points = transform.transform([source[0]])
    print("Pontos transformados:")
    print(transformed_points)
    
    # Verificação de consistência com os pontos de destino
    print("\nPontos esperados:")
    print(target)
    
    # Transformação inversa
    original_points = transform.inverse_transform(target)
    print("\nPontos originais recuperados:")
    print(transform.transformation_matrix)

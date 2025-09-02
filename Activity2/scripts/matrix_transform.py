import numpy as np

def build_transformation_matrix(delta_x, delta_y, theta_deg=0):
    """
    Build a 3x3 homogeneous transformation matrix for 2D.
    
    Parameters:
        delta_x, delta_y : translation from O3 to O4
        theta_deg        : rotation of O4 relative to O3 (in degrees)
    
    Returns:
        3x3 numpy array
    """
    theta = np.radians(theta_deg)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    
    # 3x3 homogeneous transformation
    T = np.array([
        [ cos_t, sin_t, -(cos_t*delta_x + sin_t*delta_y)],
        [-sin_t, cos_t, -(-sin_t*delta_x + cos_t*delta_y)],
        [  0,      0, 1]
    ])
    return T

delta_x = 10
delta_y = 2
theta = 30

T = build_transformation_matrix(delta_x, delta_y, theta)
print("Transformation matrix O3 -> O4:\n", T)

points_O3 = np.array([
    [0, 0, 1],    # origin of O3
    [15, -3, 1],   # object at (15, -3)
    [10, 2, 1]     # O4's origin
]).T

points_O4 = T @ points_O3
print("\nPoints in O4 frame (columns):\n", points_O4)
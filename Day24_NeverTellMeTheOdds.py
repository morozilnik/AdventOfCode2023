import numpy as np
from scipy.sparse.linalg import cg
from scipy.optimize import minimize, optimize, basinhopping
from sympy import solve_poly_system, symbols, Symbol
import sympy


def parse_input(text):
    text = [line.strip() for line in text]
    coords = []
    speeds = []
    for line in text:
        coord_str, speed_str = line.split(' @ ')
        coords.append([int(x) for x in coord_str.split(', ')])
        speeds.append([int(x) for x in speed_str.split(', ')])
    return coords, speeds

def find_intersection_point(ray1_origin, ray1_direction, ray2_origin, ray2_direction):
    """
    Find the intersection point of two rays on a 2D plane.

    Parameters:
    - ray1_origin: The origin of the first ray as a tuple (x1, y1).
    - ray1_direction: The direction of the first ray as a tuple (dx1, dy1).
    - ray2_origin: The origin of the second ray as a tuple (x2, y2).
    - ray2_direction: The direction of the second ray as a tuple (dx2, dy2).

    Returns:
    - intersection_point: The intersection point as a tuple (x, y). If there is no intersection, returns None.
    """

    x1, y1 = ray1_origin
    dx1, dy1 = ray1_direction

    x2, y2 = ray2_origin
    dx2, dy2 = ray2_direction

    # Check if the rays are parallel (cross product of their directions is zero)
    cross_product = dx1 * dy2 - dx2 * dy1
    if abs(cross_product) < 1e-6:
        # Rays are parallel, no intersection
        return None

    # Calculate the parameter t for the intersection point
    t = ((x2 - x1) * dy2 - (y2 - y1) * dx2) / cross_product

    if t < 0:
        # Intersection point is behind the first ray
        print(f"Intersection point is behind the first ray (t = {t})")
        return None
    
    # Calculate the intersection point
    intersection_point = (x1 + t * dx1, y1 + t * dy1)
    # check second ray
    diff = intersection_point - ray2_origin
    if (diff[0] < 0 and dx2 >= 0) or (diff[0] > 0 and dx2 <= 0) or (diff[1] < 0 and dy2 >= 0) or (diff[1] > 0 and dy2 <= 0):
        print(f"Intersection point is behind the second ray")
        return None

    return intersection_point


def solve1(coords, speeds):
    # search_area = np.array([7, 27]) # for test case
    search_area = [200000000000000, 400000000000000] # for real case

    XY = np.array(coords)[:, 0:2]
    dXY = np.array(speeds)[:, 0:2]
    total_intersections = 0
    for i in range(len(XY)):
        for j in range(i+1, len(XY)):
            ray1_origin = XY[i]
            ray1_direction = dXY[i]
            ray2_origin = XY[j]
            ray2_direction = dXY[j]
            intersection = find_intersection_point(ray1_origin, ray1_direction, ray2_origin, ray2_direction)
            if intersection is not None:
                if search_area[0] <= intersection[0] <= search_area[1] and search_area[0] <= intersection[1] <= search_area[1]:
                    total_intersections += 1
                    print(intersection)
                else:
                    print(intersection, " outside the area ")
    
    return total_intersections

# Define the objective function
def objective_function(variables, coords, speeds):
    x_prime, y_prime, z_prime, dx_prime, dy_prime, dz_prime = variables[:6]
    N_values = variables[6:]
    error = 0.0

    for k in range(len(coords)):
        # Calculate the left-hand side of the equation
        lhs_x = x_prime + N_values[k] * dx_prime
        lhs_y = y_prime + N_values[k] * dy_prime
        lhs_z = z_prime + N_values[k] * dz_prime

        x, y, z = coords[k]
        dx, dy, dz = speeds[k]

        # Calculate the right-hand side of the equation
        rhs_x = x + N_values[k] * dx
        rhs_y = y + N_values[k] * dy
        rhs_z = z + N_values[k] * dz

        # Add the squared difference to the error
        error += (lhs_x - rhs_x)**2 + (lhs_y - rhs_y)**2 + (lhs_z - rhs_z)**2

    return error

def build_sympy_equations(coords, speeds):
    x_prime, y_prime, z_prime = sympy.symbols('x_prime y_prime z_prime')
    dx_prime, dy_prime, dz_prime = sympy.symbols('dx_prime dy_prime dz_prime')
    Ns = [Symbol(f'N{k}') for k in range(len(coords))]
    # Define the symbolic equations
    equations = []
    for k in range(len(coords)):
        N_value = Ns[k]
        lhs_x = x_prime + N_value * dx_prime
        lhs_y = y_prime + N_value * dy_prime
        lhs_z = z_prime + N_value * dz_prime

        x, y, z = coords[k]
        dx, dy, dz = speeds[k]

        rhs_x = x + N_value * dx
        rhs_y = y + N_value * dy
        rhs_z = z + N_value * dz

        equation_x = lhs_x - rhs_x
        equation_y = lhs_y - rhs_y
        equation_z = lhs_z - rhs_z
        equations.extend([equation_x, equation_y, equation_z])
    symbols = [x_prime, y_prime, z_prime, dx_prime, dy_prime, dz_prime] + Ns
    result = solve_poly_system(equations, symbols)
    return result

def solve2(coords, speeds):
    # Build a system of equations x' + Nk * dx' = xk + Nk * dxk for xyz
    coords = coords[:3]
    speeds = speeds[:3]
    N = len(coords)
    # initial_guess = np.random.randint(0, 1000000, size=N+6)
    initial_guess = coords[0] + speeds[0] + [1 for _ in range(N)]
   
    # Optimizer works for test but not for actual data
    # result = minimize(
    #     objective_function,
    #     initial_guess,
    #     args=(coords, speeds),
    #     method='SLSQP',  # You can choose a different method based on your problem
    # ) 

    result = build_sympy_equations(coords, speeds)
    print(result[0])
    
    return sum(result[0][:3])

if __name__ == "__main__":
    path = "Day24.txt"
    with open(path) as f:
        text = f.readlines()
    
    data = parse_input(text)
    print(solve2(*data))
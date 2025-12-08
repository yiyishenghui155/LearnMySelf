"""
Calculate the area of a triangle using different methods.
"""
import math


def calculate_area_by_base_height(base: float, height: float) -> float:
    """
    Calculate triangle area using base and height.
    
    Args:
        base: The base length of the triangle
        height: The height of the triangle
        
    Returns:
        The area of the triangle
        
    Raises:
        ValueError: If base or height is not positive
    """
    if base <= 0 or height <= 0:
        raise ValueError("Base and height must be positive numbers")
    
    return 0.5 * base * height


def calculate_area_by_three_sides(a: float, b: float, c: float) -> float:
    """
    Calculate triangle area using three sides (Heron's formula).
    
    Args:
        a: Length of first side
        b: Length of second side
        c: Length of third side
        
    Returns:
        The area of the triangle
        
    Raises:
        ValueError: If sides don't form a valid triangle
    """
    if a <= 0 or b <= 0 or c <= 0:
        raise ValueError("All sides must be positive numbers")
    
    if a + b <= c or a + c <= b or b + c <= a:
        raise ValueError("Sides do not form a valid triangle")
    
    semi_perimeter = (a + b + c) / 2
    area = math.sqrt(
        semi_perimeter * (semi_perimeter - a) * (semi_perimeter - b) * (semi_perimeter - c)
    )
    return area


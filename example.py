"""
Example usage of triangle area calculation functions.
"""
from triangle_area import calculate_area_by_base_height, calculate_area_by_three_sides


def main():
    # Example 1: Calculate area using base and height
    base = 10
    height = 5
    area1 = calculate_area_by_base_height(base, height)
    print(f"Triangle with base {base} and height {height}: area = {area1}")
    
    # Example 2: Calculate area using three sides
    a, b, c = 3, 4, 5
    area2 = calculate_area_by_three_sides(a, b, c)
    print(f"Triangle with sides {a}, {b}, {c}: area = {area2}")
    
    # Example 3: Error handling
    try:
        calculate_area_by_three_sides(1, 2, 10)
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()


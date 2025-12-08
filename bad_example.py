from triangle_area import calculate_area_by_base_height, calculate_area_by_three_sides

# Bad code with code smells
def calc(x, y, z):
    # Magic numbers
    result = calculate_area_by_base_height(10, 5)
    print(result)
    
    # No error handling - potential crash
    data = None
    result2 = calculate_area_by_three_sides(data, 4, 5)
    
    # Magic numbers and hardcoded values
    if result > 20:
        a = calculate_area_by_three_sides(3, 4, 5)
        b = calculate_area_by_three_sides(6, 8, 10)
        c = calculate_area_by_three_sides(5, 12, 13)
        print(a + b + c + 100 + 200)
    
    # Poor variable naming and duplicate code
    for i in range(5):
        t = calculate_area_by_base_height(i, i)
        t2 = calculate_area_by_base_height(i, i)
        t3 = calculate_area_by_base_height(i, i)
    
    # Unnecessary complexity
    return result if result != None else 0

calc(1, 2, 3)


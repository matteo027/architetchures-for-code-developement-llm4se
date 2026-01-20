def is_beautiful_poles(heights: List[int]) -> str:
    if len(heights) < 3:
        return "Invalid input"
    if len(set(heights)) != len(heights):
        return "Invalid input"
    if any(h < 0 for h in heights):
        return "Invalid input"
    if len(set(heights)) == 1:
        return "beautiful"

    diff = heights[1] - heights[0]
    for i in range(2, len(heights)):
        if heights[i] - heights[i-1] != diff:
            return "not beautiful"

    return "beautiful"
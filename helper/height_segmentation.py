def find_rides_arne(height):
    diff = height.diff()
    height_diff = diff.rolling(20).mean().rolling(10).sum()
    return height_diff < -1
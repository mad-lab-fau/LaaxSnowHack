def find_rides_arne(height):
    diff = height.diff()
    height_diff = diff.rolling(10, center=True).mean().rolling(15, center=True).sum()
    return height_diff < -1

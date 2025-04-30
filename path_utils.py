def split_path_into_segments(path):
    segments = []
    if len(path) < 2:
        return segments

    current_dir = get_direction(path[0], path[1])
    current_segment = [path[0]]

    for i in range(1, len(path)):
        new_dir = get_direction(path[i - 1], path[i])
        if new_dir == current_dir:
            current_segment.append(path[i])
        else:
            segments.append(current_segment)
            current_segment = [path[i - 1], path[i]]
            current_dir = new_dir

    segments.append(current_segment)
    return segments

def get_direction(p1, p2):
    dx = p2[1] - p1[1]
    dy = p2[0] - p1[0]
    if dx == 1: return 'right'
    if dx == -1: return 'left'
    if dy == 1: return 'down'
    if dy == -1: return 'up'
    return None

def get_segment_direction(segment):
    if len(segment) < 2:
        return None
    return get_direction(segment[0], segment[1])
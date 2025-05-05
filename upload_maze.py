import pickle


def save_maze(filename, maze_info):
    with open(filename, 'wb') as f:
        pickle.dump(maze_info, f)


def load_maze(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
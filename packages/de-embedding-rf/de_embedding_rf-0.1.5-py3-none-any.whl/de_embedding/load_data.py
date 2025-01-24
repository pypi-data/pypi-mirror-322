import os


def load_example(file_name):
    path = os.path.join(os.path.dirname(__file__), 'data/simulation_ADS', file_name)

    path = os.path.join(os.path.dirname(__file__), 'data', 'simulation_ADS', file_name)
    path = os.path.normpath(path)
    return path
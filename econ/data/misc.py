class DataSniffer:
    '''Guess data type of a set of data by heuristics.'''
    # TODO
    pass

def floatify(value):
    try:
        newval = float(value)
        return newval
    except:
        return value

def floatify_matrix(matrix):
    return [ [ floatify(col) for col in row ] for row in matrix ]


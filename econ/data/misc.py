class DataSniffer:
    '''Guess data type of a set of data by heuristics.'''
    # TODO
    pass

def floatify(value):
    # often numbers have commas in them like 1,030
    if isinstance(value, basestring):
        value = value.replace(',', '')
    try:
        newval = float(value)
        return newval
    except:
        return value

def floatify_matrix(matrix):
    return [ [ floatify(col) for col in row ] for row in matrix ]


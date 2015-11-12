import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    value = record[1][:-10]
    mr.emit_intermediate(value, 0)

def reducer(key, value):
    # key: word
    # value: list of occurrence counts
    mr.emit(key)

    
# Do not modify below this line
# =============================
if __name__ == '__main__':
    #inputdata = open('dna.json')
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)

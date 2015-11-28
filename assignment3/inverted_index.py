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
    key = record[0]
    value = record[1]
    words = value.split()
    for w in words:
      mr.emit_intermediate(w, key)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    documents = set()
    for v in list_of_values:
      documents.add(v)
    mr.emit((key, list(documents)))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    #inputdata = open('books.json')  
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)

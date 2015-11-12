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
    key = record[1]
    value = list([record[0]]) + record[2:]
    mr.emit_intermediate(key, value)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    items = []
    for v in list_of_values:
      if v[0] == 'order':
        order = list([v[0], key]) + v[1:]
      else:
        item = list([v[0], key]) + v[1:]
        items.append(item)
    for item in items:
      mr.emit(order + item)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

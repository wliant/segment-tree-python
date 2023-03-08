from segment_tree import SegmentTree
import random

input_file = "input.txt"

with open(input_file, "r") as infile:
    file = infile.readline()
elements = list(map(int, file.split(" ")))

st = SegmentTree(elements, lambda left_value, right_value: left_value + right_value, lambda x: x)


def find_sum(x, f_index, t_index):
    the_sum = 0
    for i in range(f_index, t_index):
        the_sum += x[i]

    return the_sum


for _ in range(100):
    a = [random.randint(0, len(elements)), random.randint(0, len(elements))]
    a.sort()
    left, right = a
    print("calculating segment {} to {}: {}, verify: {}".format(left, right, st.calc_segment(left, right-1),
          find_sum(elements, left, right)))

print("testing update")
for _ in range(100):
    a = [random.randint(0, len(elements)), random.randint(0, len(elements))]
    a.sort()
    left, right = a
    update_index = random.randint(left, right)
    update_value = random.randint(0, 100)
    print("updating index {} from {} to {}".format(update_index, elements[update_index], update_value))
    elements[update_index] = update_value

    st.update(update_index, update_value)
    print("calculating segment {} to {}: {}, verify: {}".format(left, right-1, st.calc_segment(left, right-1),
          find_sum(elements, left, right)))
    print()

import sys
import random
length = int(sys.argv[1])

result = " ".join([str(random.randint(0, 100)) for _ in range(length)])

with open("input.txt", "w") as outfile:
    outfile.writelines([result])



import random

def countInversions(arr):
    lst = [x for x in arr if x != 0]
    inv = 0
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            if lst[i] > lst[j]:
                inv += 1
    return inv

def isSolvable(arr):
    inv = countInversions(arr)
    zero_index = arr.index(0)
    zero_row = zero_index // 4
    row_from_bottom = 4 - zero_row
    return (inv + row_from_bottom) % 2 == 1

def generateSolvablePuzzle():
    arr = list(range(16))
    while True:
        random.shuffle(arr)
        if isSolvable(arr):
            break
    return [arr[i:i+4] for i in range(0, 16, 4)]

def spitItOut():
    puzzle = generateSolvablePuzzle()
    return puzzle

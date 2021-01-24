# -*- coding: utf-8 -*-
""" @author:  _-=<( // ( Xiana Victoria Laor ) \\ )>=-_ """

# magn = 33
magnum = lambda magn: (magn**2 * (magn**2 + 1)) / 2 * magn
digsum = lambda numb: sum(map(int, str(numb)))
listOfSums_of_digits_of_magNumbers = [None]*69 # we list magnitudes in the element with number, corresponding to digsum of magnum
for magnitude in range (1, 40):
    magical_number = magnum (magnitude)
    svd = digsum(magical_number)
    try:
        if listOfSums_of_digits_of_magNumbers[svd] is None:
            listOfSums_of_digits_of_magNumbers[svd] = [magnitude]
        else:
            listOfSums_of_digits_of_magNumbers[svd].append(magnitude)
    except IndexError:
        print "!!!! Sum ({}) of magnum:{} for pow:{} failed".format(svd, magical_number, magnitude)

########################################################################################################################
def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

def next_set(arr, n):
    j = n - 2
    while j != -1 and arr[j] >= arr[j + 1]: j -= 1
    if j == -1:
        return False
    k = n - 1
    while arr[j] >= arr[k]: k -= 1
    swap(arr, j, k)
    l = j + 1
    r = n - 1
    while l < r:
        swap(arr, l, r)
        l += 1
        r -= 1
    return True
def is_magic(arr, n):
    for i in range(0, n):
        sum1 = 0
        sum2 = 0
        sum3 = 0
        sum4 = 0
    for j in range(0, n):
        sum1 += arr[i * n + j]
        sum2 += arr[j * n + i]
        sum3 += arr[j * n + j]
        sum4 += arr[(n - j - 1) * n + j]
    if sum1 != sum2 or sum1 != sum3 or sum1 != sum4 or sum2 != sum3 or sum2 != sum4 or sum3 != sum4:
        return False
    return True

def show_squares(n):
    N = n * n
    arr = [i + 1 for i in range(N)]
    cnt = 0
    while next_set(arr, N):
        if is_magic(arr, n):
            print(arr)
            cnt += 1
    return cnt
# Требуемая размерность
cnt = show_squares(3)
print("Число вариантов:", cnt)
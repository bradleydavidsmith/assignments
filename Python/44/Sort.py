# The 2 sample list
list1 =  [67, 45, 2, 13, 1, 998]
list2 = [89, 23, 33, 45, 10, 12, 45, 45, 45]

# Print the sorted version of the 2 sample lists
print sorted(list1)
print sorted(list2)

# Sorted, using a bubble sort
def sorted (list):
    
    # copy the list, since we don't want to disturb the original
    tList = list
    
    # Bubble Sort
    for i in range(len(list)-1, 0, -1):
        for j in range(i):
            # compare the last item in the list (i) with each item in turn (j)
            # After each pass, the ith is assumed sorted, and so i is decremented
            if tList[i] < tList[j]:
                # switch them
                (tList[i], tList[j]) = (tList[j], tList[i])
    return tList



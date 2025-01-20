def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations +=1
        mid = (high + low) // 2

        if arr[mid] >= x:
            upper_bound = arr[mid]
            high = mid - 1
        else:
            low = mid + 1

    return iterations, upper_bound

arr = [2.1, 3.3, 4.4, 5.5, 6.6]
x = 4.0
result = binary_search(arr, x)
print(f"Iterations: {result[0]}, Upper Bound: {result[1]}")

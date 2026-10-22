import random
import time
import csv
import matplotlib.pyplot as plt



"""
Linear search function
"""
#Sun Runze
def linearSearch(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1  # Return -1 if the target is not found

"""
Binary search function
"""
#Sun Runze
#Iterative version
def binarySearchIterative(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (right + left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1  # Return -1 if the target is not found

#Recursive version
def binarySearchRecursive(arr, left, right, target):
    if left > right:
        return -1  # Return -1 if the target is not found
    mid = (right + left) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binarySearchRecursive(arr, mid + 1, right, target)
    else:
        return binarySearchRecursive(arr, left, mid - 1, target)

"""
Insertion sort function
"""
#Sun Runze
def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

"""
Bubble sort function
"""
#Sun Runze
def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

"""
Merge sort function
"""
#Sun Runze
def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        mergeSort(L)
        mergeSort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

"""
Quick sort function
"""
#Sun Runze
def quickSort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quickSort(left) + middle + quickSort(right)

"""
Complexity evaluation for searching algorithms
"""

#Experiment settings
sizes = [10, 100, 1000, 10000]
runs = 5

results = []

for n in sizes:

    # Generate random array
    data = [random.randint(0, 100000) for _ in range(n)]
    # Binary search requires sorted data
    sorted_data = sorted(data)
    # Generate random targets
    targets = [random.randint(0, 100000) for _ in range(runs)]

    # Measurement of linear search
    start = time.perf_counter()

    for target in targets:
        linearSearch(data, target)

    end = time.perf_counter()

    linear_time = (end - start) / runs * 1_000_000

    # Measurement of binary search (iterative)
    start = time.perf_counter()
    for target in targets:
        binarySearchIterative(sorted_data, target)

    end = time.perf_counter()

    binary_iterative_time = (end - start) / runs * 1_000_000

    # Measurement of binary search (recursive)
    start = time.perf_counter()
    for target in targets:
        binarySearchRecursive(sorted_data, 0, len(sorted_data) - 1, target)

    end = time.perf_counter()

    binary_recursive_time = (end - start) / runs * 1_000_000

    results.append((n, linear_time, binary_iterative_time, binary_recursive_time))

# Write results to CSV file
with open("search_results.csv", "w", newline="") as file:

    writer = csv.writer(file)

    # Header
    writer.writerow([
        "Array Size",
        "Linear Search (microseconds)",
        "Binary Search (iterative) (microseconds)",
        "Binary Search (recursive) (microseconds)"
    ])

    # Data
    writer.writerows(results)

# Output table to console
print(f"{'Array Size':<12}"
      f"{'Linear Search (μs)':<25}"
      f"{'Binary Search (iterative) (μs)':<25}"
      f"{'Binary Search (recursive) (μs)':<25}")

print("-" * 62)

for row in results:
    print(f"{row[0]:<12}"
          f"{row[1]:<25.3f}"
          f"{row[2]:<25.3f}"
          f"{row[3]:<25.3f}")
    
"""
Complexity evaluation for sorting algorithms
"""

print("Sorting algorithms performance evaluation...")

# Experiment settings
sizes = [10, 100, 1000, 10000]
runs = 5

results = []

# Mearurement of sorting algorithms
for n in sizes:
    # Generate random array
    original = [random.randint(0, 100000) for _ in range(n)]

    # -------------------------
    # Insertion Sort
    # -------------------------
    total_time = 0

    for _ in range(runs):

        data = original.copy()

        start = time.perf_counter()

        insertionSort(data)

        end = time.perf_counter()

        total_time += end - start

    average_time = total_time / runs

    results.append([
        "Insertion Sort",
        n,
        average_time
    ])

    # -------------------------
    # Bubble Sort
    # -------------------------
    total_time = 0

    for _ in range(runs):

        data = original.copy()

        start = time.perf_counter()

        bubbleSort(data)

        end = time.perf_counter()

        total_time += end - start

    average_time = total_time / runs

    results.append([
        "Bubble Sort",
        n,
        average_time
    ])

    # -------------------------
    # Merge Sort
    # -------------------------
    total_time = 0

    for _ in range(runs):

        data = original.copy()

        start = time.perf_counter()

        mergeSort(data)

        end = time.perf_counter()

        total_time += end - start

    average_time = total_time / runs

    results.append([
        "Merge Sort",
        n,
        average_time
    ])

    # -------------------------
    # Quick Sort
    # -------------------------
    total_time = 0

    for _ in range(runs):

        data = original.copy()

        start = time.perf_counter()

        quickSort(data)

        end = time.perf_counter()

        total_time += end - start

    average_time = total_time / runs

    results.append([
        "Quick Sort",
        n,
        average_time
    ])


    # -------------------------
    # Quick Sort - sorted array
    # -------------------------
    #Sun Runze
    sorted_data = sorted(original, reverse=True)

    total_time = 0

    for _ in range(runs):

        data = sorted_data.copy()

        start = time.perf_counter()

        quickSort(data)

        end = time.perf_counter()

        total_time += end - start

    average_time = total_time / runs

    results.append([
        "Quick Sort (Sorted)",
        n,
        average_time
    ])

# Output table
print(f"{'Algorithm':<25}"
      f"{'n':<10}"
      f"{'Average Time (s)':<20}")

print("-" * 55)

for algorithm, n, average_time in results:

    print(f"{algorithm:<25}"
          f"{n:<10}"
          f"{average_time:<20.6f}")

print("Results have been written to 'sorting_results.csv' and plotted.")

# Write results to CSV file
with open("sorting_results.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Algorithm",
        "n",
        "Average Time (s)"
    ])

    writer.writerows(results)

# Plot the results
data = {}

with open("sorting_results.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        algorithm = row["Algorithm"]
        n = int(row["n"])
        time = float(row["Average Time (s)"])

        if algorithm not in data:
            data[algorithm] = {
                "n": [],
                "time": []
            }

        data[algorithm]["n"].append(n)
        data[algorithm]["time"].append(time)


# Draw curves
for algorithm in data:
    plt.plot(
        data[algorithm]["n"],
        data[algorithm]["time"],
        marker="o",
        label=algorithm
    )


plt.xlabel("Input Size (n)")
plt.ylabel("Average Time (seconds)")
plt.title("Sorting Algorithm Performance")

plt.legend()
plt.grid(True)

plt.show()

print("All algorithms completed.")
import csv
import random
import time
from pathlib import Path

import matplotlib.pyplot as plt


# ============================================================
# Searching and Sorting Algorithms Performance Experiment
# Outputs:
#   search_results.csv
#   sorting_results.csv
#   search_performance.png
#   sorting_performance.png
#   quicksort_order_comparison.png
# ============================================================

OUTPUT_DIR = Path(__file__).resolve().parent
SIZES = [10, 100, 1000, 10000]
SEARCH_TARGETS_PER_BATCH = 100
REPEATS = 5
RANDOM_SEED = 42


# -------------------------
# Searching algorithms ----- Sun Runze
# -------------------------
def linearSearch(arr, target):
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1


def binarySearchIterative(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def binarySearchRecursive(arr, left, right, target):
    if left > right:
        return -1
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    if arr[mid] < target:
        return binarySearchRecursive(arr, mid + 1, right, target)
    return binarySearchRecursive(arr, left, mid - 1, target)


# -------------------------
# Sorting algorithms ----- Sun Runze
# -------------------------
def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


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
    return arr

# ----- Sun Runze
def mergeSort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = mergeSort(arr[:mid])
    right = mergeSort(arr[mid:])

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quickSort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quickSort(left) + middle + quickSort(right)


def time_search_batch(search_fn, arr, targets, recursive=False):
    """Return average microseconds per search for one batch."""
    start = time.perf_counter()
    if recursive:
        for target in targets:
            search_fn(arr, 0, len(arr) - 1, target)
    else:
        for target in targets:
            search_fn(arr, target)
    elapsed = time.perf_counter() - start
    return elapsed / len(targets) * 1_000_000


def make_search_targets(data, count, rng):
    """Create a balanced target set: half present, half guaranteed absent."""
    present_count = count // 2
    present = [rng.choice(data) for _ in range(present_count)]

    data_values = set(data)
    absent = []
    candidate = max(data) + 1
    while len(absent) < count - present_count:
        if candidate not in data_values:
            absent.append(candidate)
        candidate += 1

    targets = present + absent
    rng.shuffle(targets)
    return targets


def run_search_experiment(rng):
    results = []

    for n in SIZES:
        data = [rng.randint(0, 100000) for _ in range(n)]
        sorted_data = sorted(data)
        targets = make_search_targets(data, SEARCH_TARGETS_PER_BATCH, rng)

        # Repeat the batch measurement; report the mean time per search.
        measurements = {
            "Linear Search (microseconds)": [],
            "Binary Search (iterative) (microseconds)": [],
            "Binary Search (recursive) (microseconds)": [],
        }

        for _ in range(REPEATS):
            measurements["Linear Search (microseconds)"].append(
                time_search_batch(linearSearch, data, targets)
            )
            measurements["Binary Search (iterative) (microseconds)"].append(
                time_search_batch(binarySearchIterative, sorted_data, targets)
            )
            measurements["Binary Search (recursive) (microseconds)"].append(
                time_search_batch(
                    binarySearchRecursive, sorted_data, targets, recursive=True
                )
            )

        row = {
            "Array Size": n,
            "Linear Search (microseconds)": sum(measurements["Linear Search (microseconds)"]) / REPEATS,
            "Binary Search (iterative) (microseconds)": sum(measurements["Binary Search (iterative) (microseconds)"]) / REPEATS,
            "Binary Search (recursive) (microseconds)": sum(measurements["Binary Search (recursive) (microseconds)"]) / REPEATS,
        }
        results.append(row)

    output = OUTPUT_DIR / "search_results.csv"
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    print("\nSEARCH TIMING TABLE (average microseconds per search)")
    print(f"{'n':>8} {'Linear':>14} {'Binary iterative':>18} {'Binary recursive':>18}")
    for row in results:
        print(
            f"{row['Array Size']:>8} "
            f"{row['Linear Search (microseconds)']:>14.4f} "
            f"{row['Binary Search (iterative) (microseconds)']:>18.4f} "
            f"{row['Binary Search (recursive) (microseconds)']:>18.4f}"
        )

    # Search performance chart
    plt.figure(figsize=(8, 5))
    x = [row["Array Size"] for row in results]
    for key, label in [
        ("Linear Search (microseconds)", "Linear Search"),
        ("Binary Search (iterative) (microseconds)", "Binary Search (Iterative)"),
        ("Binary Search (recursive) (microseconds)", "Binary Search (Recursive)"),
    ]:
        plt.plot(x, [row[key] for row in results], marker="o", label=label)

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Input Size (n)")
    plt.ylabel("Average Time per Search (microseconds)")
    plt.title("Searching Algorithm Performance")
    plt.grid(True, which="both", linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "search_performance.png", dpi=300, bbox_inches="tight")
    plt.close()

    return results


def time_sort(sort_fn, source):
    data = source.copy()
    start = time.perf_counter()
    result = sort_fn(data)
    elapsed = time.perf_counter() - start
    # Validate correctness outside the timed section.
    if result is None:
        result = data
    if result != sorted(source):
        raise ValueError(f"{sort_fn.__name__} produced an incorrect result.")
    return elapsed


def run_sorting_experiment(rng):
    algorithms = [
        ("Insertion Sort", insertionSort),
        ("Bubble Sort", bubbleSort),
        ("Merge Sort", mergeSort),
        ("Quick Sort", quickSort),
    ]
    results = []
    quick_order_results = []

    for n in SIZES:
        # Use the same five random source arrays for each algorithm at this n.
        source_arrays = [
            [rng.randint(0, 100000) for _ in range(n)]
            for _ in range(REPEATS)
        ]

        for name, sort_fn in algorithms:
            times = [time_sort(sort_fn, source) for source in source_arrays]
            results.append({
                "Algorithm": name,
                "n": n,
                "Average Time (s)": sum(times) / len(times),
            })

        # Additional experiment: Quick Sort on Ascending input.
        Ascending_times = []
        for source in source_arrays:
            Ascending = sorted(source)
            Ascending_times.append(time_sort(quickSort, Ascending))
        quick_order_results.append({
            "Algorithm": "Quick Sort (Ascending Input)",
            "n": n,
            "Average Time (s)": sum(Ascending_times) / len(Ascending_times),
        })

    all_sort_rows = results + quick_order_results
    output = OUTPUT_DIR / "sorting_results.csv"
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Algorithm", "n", "Average Time (s)"])
        writer.writeheader()
        writer.writerows(all_sort_rows)

    print("\nSORTING TIMING TABLE (average seconds)")
    print(f"{'Algorithm':<30} {'n':>8} {'Average Time (s)':>18}")
    for row in all_sort_rows:
        print(
            f"{row['Algorithm']:<30} {row['n']:>8} "
            f"{row['Average Time (s)']:>18.8f}"
        )

    # Required curve: at least four sorting algorithms.
    plt.figure(figsize=(8, 5))
    for name, _ in algorithms:
        rows = [row for row in results if row["Algorithm"] == name]
        plt.plot(
            [row["n"] for row in rows],
            [row["Average Time (s)"] for row in rows],
            marker="o",
            label=name,
        )
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Input Size (n)")
    plt.ylabel("Average Sorting Time (seconds)")
    plt.title("Sorting Algorithm Performance")
    plt.grid(True, which="both", linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "sorting_performance.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Separate plot to discuss the effect of input order on Quick Sort.
    plt.figure(figsize=(8, 5))
    random_rows = [row for row in results if row["Algorithm"] == "Quick Sort"]
    plt.plot(
        [row["n"] for row in random_rows],
        [row["Average Time (s)"] for row in random_rows],
        marker="o",
        label="Quick Sort (Random Input)",
    )
    plt.plot(
        [row["n"] for row in quick_order_results],
        [row["Average Time (s)"] for row in quick_order_results],
        marker="o",
        label="Quick Sort (Ascending Input)",
    )
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Input Size (n)")
    plt.ylabel("Average Sorting Time (seconds)")
    plt.title("Quick Sort: Random vs. Ascending Input")
    plt.grid(True, which="both", linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "quicksort_order_comparison.png", dpi=300, bbox_inches="tight")
    plt.close()

    return all_sort_rows


def main():
    rng = random.Random(RANDOM_SEED)
    run_search_experiment(rng)
    run_sorting_experiment(rng)

    print("\nSaved files:")
    for filename in [
        "search_results.csv",
        "sorting_results.csv",
        "search_performance.png",
        "sorting_performance.png",
        "quicksort_order_comparison.png",
    ]:
        print(f"  - {OUTPUT_DIR / filename}")


if __name__ == "__main__":
    main()

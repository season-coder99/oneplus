"""
Sorting Algorithms Implementation

This module provides implementations of various sorting algorithms including:
- Bubble Sort
- Quick Sort  
- Merge Sort
- Selection Sort
- Insertion Sort

Each algorithm includes time complexity information and usage examples.
"""

def bubble_sort(arr):
    """
    Bubble Sort Algorithm
    Time Complexity: O(n²) worst/average case, O(n) best case
    Space Complexity: O(1)
    
    Args:
        arr (list): List of comparable elements to sort
        
    Returns:
        list: Sorted list in ascending order
    """
    if not arr:
        return arr
    
    n = len(arr)
    arr_copy = arr.copy()  # Don't modify original array
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr_copy[j] > arr_copy[j + 1]:
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                swapped = True
        
        # If no swapping occurred, array is already sorted
        if not swapped:
            break
    
    return arr_copy


def quick_sort(arr):
    """
    Quick Sort Algorithm
    Time Complexity: O(n log n) average case, O(n²) worst case
    Space Complexity: O(log n) average case
    
    Args:
        arr (list): List of comparable elements to sort
        
    Returns:
        list: Sorted list in ascending order
    """
    if not arr:
        return arr
    
    arr_copy = arr.copy()
    _quick_sort_helper(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy


def _quick_sort_helper(arr, low, high):
    """Helper function for quick sort"""
    if low < high:
        # Partition the array and get pivot index
        pivot_index = _partition(arr, low, high)
        
        # Recursively sort elements before and after partition
        _quick_sort_helper(arr, low, pivot_index - 1)
        _quick_sort_helper(arr, pivot_index + 1, high)


def _partition(arr, low, high):
    """Partition function for quick sort"""
    # Choose rightmost element as pivot
    pivot = arr[high]
    
    # Index of smaller element
    i = low - 1
    
    for j in range(low, high):
        # If current element is smaller than or equal to pivot
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # Place pivot in correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def merge_sort(arr):
    """
    Merge Sort Algorithm
    Time Complexity: O(n log n) all cases
    Space Complexity: O(n)
    
    Args:
        arr (list): List of comparable elements to sort
        
    Returns:
        list: Sorted list in ascending order
    """
    if not arr:
        return arr
    
    arr_copy = arr.copy()
    _merge_sort_helper(arr_copy)
    return arr_copy


def _merge_sort_helper(arr):
    """Helper function for merge sort"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    _merge_sort_helper(left)
    _merge_sort_helper(right)
    
    # Merge the sorted halves
    _merge(arr, left, right)


def _merge(arr, left, right):
    """Merge function for merge sort"""
    i = j = k = 0
    
    # Merge the arrays back into arr
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    
    # Copy remaining elements
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1


def selection_sort(arr):
    """
    Selection Sort Algorithm
    Time Complexity: O(n²) all cases
    Space Complexity: O(1)
    
    Args:
        arr (list): List of comparable elements to sort
        
    Returns:
        list: Sorted list in ascending order
    """
    if not arr:
        return arr
    
    arr_copy = arr.copy()
    n = len(arr_copy)
    
    for i in range(n):
        # Find minimum element in remaining unsorted array
        min_idx = i
        for j in range(i + 1, n):
            if arr_copy[j] < arr_copy[min_idx]:
                min_idx = j
        
        # Swap found minimum element with first element
        arr_copy[i], arr_copy[min_idx] = arr_copy[min_idx], arr_copy[i]
    
    return arr_copy


def insertion_sort(arr):
    """
    Insertion Sort Algorithm
    Time Complexity: O(n²) worst/average case, O(n) best case
    Space Complexity: O(1)
    
    Args:
        arr (list): List of comparable elements to sort
        
    Returns:
        list: Sorted list in ascending order
    """
    if not arr:
        return arr
    
    arr_copy = arr.copy()
    
    for i in range(1, len(arr_copy)):
        key = arr_copy[i]
        j = i - 1
        
        # Move elements greater than key one position ahead
        while j >= 0 and arr_copy[j] > key:
            arr_copy[j + 1] = arr_copy[j]
            j -= 1
        
        arr_copy[j + 1] = key
    
    return arr_copy


def compare_algorithms(arr, show_steps=False):
    """
    Compare different sorting algorithms on the same input
    
    Args:
        arr (list): List to sort
        show_steps (bool): Whether to show sorting steps
    
    Returns:
        dict: Results from each sorting algorithm
    """
    import time
    
    algorithms = {
        'Bubble Sort': bubble_sort,
        'Quick Sort': quick_sort, 
        'Merge Sort': merge_sort,
        'Selection Sort': selection_sort,
        'Insertion Sort': insertion_sort
    }
    
    results = {}
    
    for name, func in algorithms.items():
        start_time = time.time()
        sorted_arr = func(arr)
        end_time = time.time()
        
        results[name] = {
            'result': sorted_arr,
            'time': end_time - start_time,
            'is_sorted': sorted_arr == sorted(arr)
        }
        
        if show_steps:
            print(f"{name}: {sorted_arr} (Time: {results[name]['time']:.6f}s)")
    
    return results


if __name__ == "__main__":
    # Example usage and demonstration
    print("Sorting Algorithms Demonstration")
    print("=" * 40)
    
    # Test with different types of data
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 4, 6, 1, 3],
        [1],
        [],
        [3, 3, 3, 3],
        [9, 8, 7, 6, 5, 4, 3, 2, 1]
    ]
    
    for i, test_array in enumerate(test_cases):
        print(f"\nTest Case {i + 1}: {test_array}")
        print("-" * 30)
        
        # Test each algorithm
        print(f"Bubble Sort:    {bubble_sort(test_array)}")
        print(f"Quick Sort:     {quick_sort(test_array)}")
        print(f"Merge Sort:     {merge_sort(test_array)}")
        print(f"Selection Sort: {selection_sort(test_array)}")
        print(f"Insertion Sort: {insertion_sort(test_array)}")
        
        # Verify all produce same result
        results = [
            bubble_sort(test_array),
            quick_sort(test_array), 
            merge_sort(test_array),
            selection_sort(test_array),
            insertion_sort(test_array)
        ]
        
        all_same = all(result == results[0] for result in results)
        print(f"All algorithms agree: {all_same}")
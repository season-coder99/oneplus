# oneplus

A readme file that describes my interests

## Sorting Algorithms Implementation

This repository includes a comprehensive implementation of various sorting algorithms in Python. The implementation demonstrates different approaches to sorting with detailed documentation and performance characteristics.

### Available Algorithms

1. **Bubble Sort** - O(n²) time complexity
2. **Quick Sort** - O(n log n) average case, O(n²) worst case
3. **Merge Sort** - O(n log n) guaranteed time complexity
4. **Selection Sort** - O(n²) time complexity
5. **Insertion Sort** - O(n²) worst case, O(n) best case

### Usage

```python
from sorting_algorithms import bubble_sort, quick_sort, merge_sort, selection_sort, insertion_sort

# Sort an array
numbers = [64, 34, 25, 12, 22, 11, 90]

# Use any of the sorting algorithms
sorted_bubble = bubble_sort(numbers)
sorted_quick = quick_sort(numbers)
sorted_merge = merge_sort(numbers)
sorted_selection = selection_sort(numbers)
sorted_insertion = insertion_sort(numbers)

print(sorted_bubble)  # [11, 12, 22, 25, 34, 64, 90]
```

### Running the Code

To see a demonstration of all algorithms:
```bash
python sorting_algorithms.py
```

To run the test suite:
```bash
python test_sorting.py
```

### Features

- **Multiple Algorithms**: Five different sorting algorithms implemented
- **Comprehensive Testing**: Full test suite with edge cases
- **Performance Comparison**: Built-in benchmarking functionality
- **Educational**: Clear documentation with time/space complexity information
- **Safe**: All functions create copies of input arrays (non-destructive)

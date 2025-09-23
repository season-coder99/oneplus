"""
Test Suite for Sorting Algorithms

Simple test cases to verify the correctness of all implemented sorting algorithms.
"""

from sorting_algorithms import (
    bubble_sort, quick_sort, merge_sort, 
    selection_sort, insertion_sort, compare_algorithms
)


def test_sorting_algorithm(sort_func, test_name):
    """
    Test a sorting algorithm with various test cases
    
    Args:
        sort_func: The sorting function to test
        test_name (str): Name of the algorithm being tested
    
    Returns:
        bool: True if all tests pass, False otherwise
    """
    test_cases = [
        # (input, expected_output)
        ([64, 34, 25, 12, 22, 11, 90], [11, 12, 22, 25, 34, 64, 90]),
        ([5, 2, 4, 6, 1, 3], [1, 2, 3, 4, 5, 6]),
        ([1], [1]),
        ([], []),
        ([3, 3, 3, 3], [3, 3, 3, 3]),
        ([9, 8, 7, 6, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),  # Already sorted
        ([-5, -1, -10, 0, 3], [-10, -5, -1, 0, 3]),  # Negative numbers
        ([3.5, 1.2, 4.8, 2.1], [1.2, 2.1, 3.5, 4.8]),  # Floating point
    ]
    
    passed = 0
    total = len(test_cases)
    
    print(f"Testing {test_name}...")
    
    for i, (input_arr, expected) in enumerate(test_cases):
        try:
            result = sort_func(input_arr)
            if result == expected:
                print(f"  ✓ Test {i+1} passed: {input_arr} -> {result}")
                passed += 1
            else:
                print(f"  ✗ Test {i+1} FAILED: {input_arr} -> {result} (expected {expected})")
        except Exception as e:
            print(f"  ✗ Test {i+1} ERROR: {input_arr} -> Exception: {e}")
    
    print(f"  Result: {passed}/{total} tests passed\n")
    return passed == total


def run_all_tests():
    """Run tests for all sorting algorithms"""
    print("Running Sorting Algorithm Tests")
    print("=" * 50)
    
    algorithms = [
        (bubble_sort, "Bubble Sort"),
        (quick_sort, "Quick Sort"),
        (merge_sort, "Merge Sort"), 
        (selection_sort, "Selection Sort"),
        (insertion_sort, "Insertion Sort")
    ]
    
    all_passed = True
    
    for sort_func, name in algorithms:
        passed = test_sorting_algorithm(sort_func, name)
        if not passed:
            all_passed = False
    
    # Test the compare_algorithms function
    print("Testing compare_algorithms function...")
    test_array = [64, 34, 25, 12, 22, 11, 90]
    results = compare_algorithms(test_array)
    
    # Verify all algorithms produce the same result
    sorted_results = [info['result'] for info in results.values()]
    expected = sorted(test_array)
    
    if all(result == expected for result in sorted_results):
        print("  ✓ compare_algorithms test passed")
    else:
        print("  ✗ compare_algorithms test FAILED")
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED! 🎉")
        return True
    else:
        print("❌ SOME TESTS FAILED")
        return False


def performance_test():
    """Simple performance comparison"""
    import random
    import time
    
    print("\nPerformance Test")
    print("=" * 30)
    
    # Generate random test data
    sizes = [100, 500, 1000]
    
    for size in sizes:
        print(f"\nTesting with {size} random integers:")
        test_data = [random.randint(1, 1000) for _ in range(size)]
        
        algorithms = [
            (bubble_sort, "Bubble Sort"),
            (insertion_sort, "Insertion Sort"),
            (selection_sort, "Selection Sort"),
            (merge_sort, "Merge Sort"),
            (quick_sort, "Quick Sort")
        ]
        
        for sort_func, name in algorithms:
            start_time = time.time()
            result = sort_func(test_data)
            end_time = time.time()
            
            # Verify correctness
            is_correct = result == sorted(test_data)
            status = "✓" if is_correct else "✗"
            
            print(f"  {status} {name:15}: {end_time - start_time:.4f}s")


if __name__ == "__main__":
    # Run the test suite
    success = run_all_tests()
    
    # Run performance test if basic tests pass
    if success:
        performance_test()
    
    print(f"\nTest suite completed. Exit code: {0 if success else 1}")
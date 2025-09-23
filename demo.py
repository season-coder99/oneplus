#!/usr/bin/env python3
"""
Interactive Demo for Sorting Algorithms

This script provides an interactive demonstration of the sorting algorithms.
Run it to see examples and compare performance.
"""

from sorting_algorithms import (
    bubble_sort, quick_sort, merge_sort, 
    selection_sort, insertion_sort, compare_algorithms
)
import random


def interactive_demo():
    """Interactive demonstration of sorting algorithms"""
    print("🎯 Sorting Algorithms Interactive Demo")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Demo with predefined arrays")
        print("2. Demo with custom array")
        print("3. Demo with random array")
        print("4. Performance comparison")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            demo_predefined()
        elif choice == '2':
            demo_custom()
        elif choice == '3':
            demo_random()
        elif choice == '4':
            performance_demo()
        elif choice == '5':
            print("👋 Thanks for using the sorting algorithms demo!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-5.")


def demo_predefined():
    """Demo with predefined test cases"""
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 4, 6, 1, 3],
        [9, 8, 7, 6, 5, 4, 3, 2, 1],
        [1, 1, 1, 1, 1],
        [-5, -1, -10, 0, 3]
    ]
    
    print("\n📋 Predefined Test Cases")
    print("-" * 30)
    
    for i, arr in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {arr}")
        
        # Show results from all algorithms
        algorithms = [
            ("Bubble Sort", bubble_sort),
            ("Quick Sort", quick_sort),
            ("Merge Sort", merge_sort),
            ("Selection Sort", selection_sort),
            ("Insertion Sort", insertion_sort)
        ]
        
        for name, func in algorithms:
            result = func(arr)
            print(f"  {name:15}: {result}")


def demo_custom():
    """Demo with user-provided array"""
    print("\n✏️  Custom Array Demo")
    print("-" * 25)
    
    try:
        input_str = input("Enter numbers separated by spaces: ")
        arr = [float(x) if '.' in x else int(x) for x in input_str.split()]
        
        if not arr:
            print("❌ No numbers entered.")
            return
        
        print(f"\nOriginal array: {arr}")
        
        # Ask which algorithm to use
        print("\nChoose sorting algorithm:")
        print("1. Bubble Sort")
        print("2. Quick Sort")
        print("3. Merge Sort")
        print("4. Selection Sort")
        print("5. Insertion Sort")
        print("6. All algorithms")
        
        algo_choice = input("Enter choice (1-6): ").strip()
        
        algorithms = {
            '1': ("Bubble Sort", bubble_sort),
            '2': ("Quick Sort", quick_sort),
            '3': ("Merge Sort", merge_sort),
            '4': ("Selection Sort", selection_sort),
            '5': ("Insertion Sort", insertion_sort)
        }
        
        if algo_choice in algorithms:
            name, func = algorithms[algo_choice]
            result = func(arr)
            print(f"\n{name} result: {result}")
        elif algo_choice == '6':
            print("\nResults from all algorithms:")
            for name, func in algorithms.values():
                result = func(arr)
                print(f"  {name:15}: {result}")
        else:
            print("❌ Invalid choice.")
            
    except ValueError:
        print("❌ Invalid input. Please enter numbers only.")


def demo_random():
    """Demo with randomly generated array"""
    print("\n🎲 Random Array Demo")
    print("-" * 22)
    
    try:
        size = int(input("Enter array size (1-100): "))
        if size < 1 or size > 100:
            print("❌ Size must be between 1 and 100.")
            return
            
        min_val = int(input("Enter minimum value: "))
        max_val = int(input("Enter maximum value: "))
        
        if min_val >= max_val:
            print("❌ Minimum value must be less than maximum value.")
            return
        
        # Generate random array
        arr = [random.randint(min_val, max_val) for _ in range(size)]
        
        print(f"\nGenerated array: {arr}")
        
        # Sort with all algorithms and show results
        print("\nSorting with all algorithms:")
        algorithms = [
            ("Bubble Sort", bubble_sort),
            ("Quick Sort", quick_sort),
            ("Merge Sort", merge_sort),
            ("Selection Sort", selection_sort),
            ("Insertion Sort", insertion_sort)
        ]
        
        for name, func in algorithms:
            result = func(arr)
            print(f"  {name:15}: {result}")
            
    except ValueError:
        print("❌ Invalid input. Please enter valid numbers.")


def performance_demo():
    """Performance comparison demo"""
    print("\n⚡ Performance Comparison")
    print("-" * 30)
    
    try:
        size = int(input("Enter array size for performance test (10-10000): "))
        if size < 10 or size > 10000:
            print("❌ Size must be between 10 and 10000.")
            return
        
        # Generate random test data
        test_data = [random.randint(1, 1000) for _ in range(size)]
        
        print(f"\nTesting with {size} random integers...")
        print("Algorithm       | Time (seconds)")
        print("-" * 35)
        
        # Test each algorithm
        results = compare_algorithms(test_data)
        
        for name, info in results.items():
            time_str = f"{info['time']:.6f}"
            status = "✓" if info['is_sorted'] else "✗"
            print(f"{status} {name:13} | {time_str}")
        
        # Show fastest algorithm
        fastest = min(results.items(), key=lambda x: x[1]['time'])
        print(f"\n🏆 Fastest: {fastest[0]} ({fastest[1]['time']:.6f}s)")
        
    except ValueError:
        print("❌ Invalid input. Please enter a valid number.")


if __name__ == "__main__":
    interactive_demo()
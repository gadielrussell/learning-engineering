# Big O Cheat Sheet

## Credits 
Original work Copyright (c) 2021 ReaVNaiL
Available at: [Big-O Complexity Cheat Sheet GitHub Repo](https://github.com/ReaVNaiL/Big-O-Complexity-Cheat-Sheet).
Licensed under the [MIT License](https://github.com/ReaVNaiL/Big-O-Complexity-Cheat-Sheet/blob/main/LICENSE).


## Introduction:

Welcome to the "Big-O Complexity Cheat Sheet" repository! This cheat sheet is designed to provide a quick reference guide for understanding the time and space complexity of various algorithms and data structures. As a developer, you will often encounter problems that require efficient solutions, and having a solid understanding of Big O notation is essential for writing performant code.

In this repository, you will find a comprehensive list of common algorithms and data structures, along with their time and space complexities. This will serve as a handy resource for developers, computer science students, and anyone interested in learning more about the fundamental concepts of computer science.

Whether you are preparing for a technical interview or simply want to improve your knowledge of algorithmic complexities, this cheat sheet is the perfect starting point for your journey.

---
## Table of Contents:
[Big O Notation:](#introduction)
* [TLDR](#tldr)
* [Time Complexity](#time-complexity)
    * [O(1): Constant time.](#o1-constant-time)
    * [O(log n): Logarithmic time.](#olog-n-logarithmic-time)
    * [O(n): Linear time.](#on-linear-time)
    * [O(n log n): Log-linear time.](#on-log-n-log-linear-time)
    * [O(n^2): Quadratic time.](#on2-quadratic-time)
    * [O(n^3): Cubic time.](#on3-cubic-time)
    * [O(2^n): Exponential time.](#o2n-exponential-time)
    * [O(n!): Factorial time.](#on-factorial-time)
* [Space Complexity](#space-complexity)
    * [O(1): Constant space.](#o1-constant-space)
    * [O(n): Linear space.](#on-linear-space)
    * [O(n^2): Quadratic space.](#on2-quadratic-space)
* [Common Data Structures](#common-data-structures)
    * [Arrays](#arrays)
    * [Linked Lists](#linked-lists)
    * [Stacks](#stacks)
    * [Queues](#queues)
    * [Hash Tables](#hash-tables)

---
## TL;DR:
A very useful complexity chart by: 

[bigocheatsheet.com](https://www.bigocheatsheet.com/)
<p>
   <img  height=600 width=1000 src="https://user-images.githubusercontent.com/59776018/228047115-a23f0f1a-8d32-4225-bbba-a9ee5b00bb7e.png"/>
</p>
<p>
   <img  height=704 width=1000 src="https://www.bigocheatsheet.com/img/big-o-cheat-sheet-poster.png" />
</p>

| Complexity            | Description                                                                                                                                                                                                                                                                              | Example                                  |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| **Constant Time**     | `O(1)` - Execution time remains the same, no matter the input size.                                                                                                                                                                                                                      | Accessing an array element by index      |
| **Logarithmic Time**  | `O(log n)` - Execution time increases slowly as the input size increases, typically by halving the problem at each step. For example, each step reduces the problem size by half.                                                                                                        | Binary search                            |
| **Linear Time**       | `O(n)` - Execution time grows directly in proportion to input size. Each element in the input is processed once.                                                                                                                                                                         | Iterating through an array (single loop) |
| **Linearithmic Time** | `O(n log n)` - A combination of linear and logarithmic growth. For each of the (n) elements, the algorithm performs a logarithmic number of operations, typically dividing the problem size in half at each step.                                                                        | Merge sort, Quick sort                   |
| **Quadratic Time**    | `O(n²)` - Execution time grows as the square of the input size. For each element, the algorithm performs an operation for every other element, resulting in a double loop or nested iteration.                                                                                           | Nested loops (2 loops)                   |
| **Cubic Time**        | `O(n³)` - Execution time grows as the cube of the input size. This happens when there are three nested loops, where each loop iterates over the entire input. Essentially, for every element, the algorithm performs operations for every pair of elements and then repeats this process for each of the pairs.                                                                       | Triple nested loops (3 loops)            |
| **Exponential Time**  | `O(2^n)` - Execution time doubles with each additional input element. This growth is extremely rapid, often leading to infeasibility for even moderate values of (n).                                                                                                                    | Naive recursive Fibonacci                |
| **Factorial Time**    | `O(n!)` - Execution time grows as the factorial of the input size. For each new element, the number of operations multiplies by a decreasing factor, resulting in a very rapid increase in time. This is typical for problems like generating all possible permutations of (n) elements. | Generating all possible permutations     |



---

## Time Complexity:

* ### O(1): Constant time.
    * Constant time means that the execution time of the algorithm does not depend on the size of the input. No matter how large the input grows, the time required stays the same.

    * Example: Accessing an element in an array by its index is 
𝑂
(
1
)
O(1) because you directly jump to the desired position in constant time.
    * Real-World Analogy: Imagine flipping a light switch. No matter how large the room is, the action of flipping the switch is always instantaneous.

```py
def get_first(my_list):
    return my_list[0]
```

* ### O(log n): Logarithmic time.
    * Logarithmic time complexity occurs when the algorithm reduces the problem size by a constant factor (commonly halving it) with each step. As a result, the number of steps grows very slowly as the input size increases.
    * For example, in binary search, the input size is halved at each step, making the number of steps much smaller than the size of the input. If you start with 1,000 elements, it would take only about 10 steps to reduce the problem to 1 element (since 
log
⁡
2
1000
≈
10
log
2 ​
1000≈10).

    * Logarithmic growth is often seen in algorithms that divide the input into smaller parts (like binary search), where each comparison essentially cuts the problem size in half.
    * Example: Binary search.
    * Real-World Analogy: Imagine you're looking for a specific book in a library where books are sorted alphabetically. If you start in the middle of the shelf and check if the book you're looking for is before or after that point, you can eliminate half of the shelf from your search. You then repeat this process with the remaining half. Each time, you're halving the number of books you need to search, which makes the process very efficient.
```py
# Binary search
```

* ### O(n): Linear time.
    * Linear time means that the execution time grows directly in proportion to the input size. If the input doubles, the time taken also doubles. This occurs when the algorithm processes each element in the input exactly once, often in a single loop.
    * Iterating through an array: If you loop through an array of 
𝑛
n items, you perform 
𝑛
n operations.
    * Real-World Analogy: Imagine you’re looking through a list of people’s names and you need to find a specific person. You check one name at a time and you go through the entire list once. The number of checks is directly proportional to the length of the list.

```py
# Iterating through an array
def print_all_elements(my_list):
    for element in my_list:
        print(element)
```

* ### O(n log n): Log-linear time.
    * This complexity combines both linear and logarithmic behaviors. It occurs when an algorithm performs a logarithmic operation repeatedly for each element in the input.
    * It typically happens in algorithms that involve both dividing the problem into smaller parts and then processing each part linearly. Sorting algorithms like Merge Sort or Quick Sort exhibit this time complexity.
    * Merge Sort: Splits the data into smaller subarrays and then merges them in a sorted order. Each splitting is logarithmic, and the merging process happens linearly.
    * Real-World Analogy: Imagine organizing a large stack of papers. You start by dividing them into smaller groups, and then within each group, you repeatedly divide them again (logarithmic). After the divisions, you linearly go through and sort each group. The combination of these steps results in a time complexity of 
𝑂
(
𝑛
log
⁡
𝑛
)
O(nlogn).

```py
# Merge sort
```


* ### O(n^2): Quadratic time.
    * In algorithms with quadratic time complexity, for every input element, the algorithm must compare it to every other element. This typically happens in nested loops. For example, in a bubble sort or selection sort, each item is compared to every other item in the list, resulting in 
𝑛
×
𝑛
=
𝑛
2
n×n=n
2
 comparisons.
    * Example: 2 nested for loops.
    * Real-World Analogy: Imagine you're in a room with 
𝑛
n people, and everyone shakes hands with every other person exactly once. The first person shakes hands with 
𝑛
−
1
n−1 people, the second person shakes hands with 
𝑛
−
2
n−2 people (because they already shook hands with the first person), and so on. This leads to 
𝑛
×
𝑛
=
𝑛
2
n×n=n
2
 handshakes.

```py
# 2 nested for loops
def print_all_possible_ordered_pairs(my_list):
    for first_item in my_list: # O(n)
        for second_item in my_list: # O(n)
            print(first_item, second_item)
```

* ### O(n^3): Cubic time.
    * Execution time grows as the cube of the input size. This happens when there are three nested loops, where each loop iterates over the entire input. Essentially, for every element, the algorithm performs operations for every pair of elements and then repeats this process for each of the pairs.
    * Example: Iterating through a 3D array, or 3 nested for loops.
    * Real-World Analogy: Imagine you are arranging boxes in a 3D grid (like a cubic container). For each layer of boxes (along the first dimension), you need to arrange them in rows (second dimension) and columns (third dimension). The number of operations to arrange all boxes is proportional to the cube of the size of the grid (
𝑛
3
n
3
). The more boxes you have, the exponentially harder it becomes to organize them in all three dimensions.

```py
# 3 nested for loops -- Also use as last resort for 3D arrays
def naive_matrix_mult(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    if cols_A != rows_B:
        raise ValueError("Matrices cannot be multiplied.")
    
    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
```

* ### O(2^n): Exponential time.
    * Exponential time complexity occurs when the execution time doubles with each additional input element. As the size of the input increases, the number of operations grows very rapidly, often making the algorithm impractical for even relatively small inputs.
    * In problems with exponential complexity, the algorithm often explores all possible combinations of a set of elements, leading to an explosion in the number of operations as 
𝑛
n grows.
    * Example: Naive Recursive Fibonacci: A naive recursive implementation of Fibonacci computes the same values multiple times, leading to exponential growth in the number of calls. For each element, you make two recursive calls, resulting in 
2
𝑛
2
n
 calls as the problem size grows.
    * Real-World Analogy: Imagine you are playing a game where at each level, you get to choose from two paths. After one level, you have 2 possible paths. After two levels, you have 4 paths. After three levels, you have 8 paths, and so on. The number of possibilities grows exponentially with each additional decision.

```py
# Iterating through all subsets of a set
def print_all_subsets(my_set):
    all_subsets = [[]]
    for element in my_set:
        for subset in all_subsets:
            all_subsets = all_subsets + [list(subset) + [element]]
    return all_subsets

# or

def naive_fibonacci(n):
    if n <= 1:
        return n
    return naive_fibonacci(n - 1) + naive_fibonacci(n - 2)
```

* ### O(n!): Factorial time.
    * Factorial time complexity occurs when an algorithm generates all possible permutations of the input elements. The number of operations increases very rapidly as the input size increases.
    * The factorial of a number 
𝑛
n (written 
𝑛
!
n!) is the product of all positive integers less than or equal to 
𝑛
n. For example, 
4
!
=
4
×
3
×
2
×
1
=
24
4!=4×3×2×1=24.
    * Example: Generating all possible permutations: If you need to find every possible arrangement of 
𝑛
n items, the time complexity grows factorially.
    * Real-World Analogy: Suppose you have 
𝑛
n people and you want to know all the possible ways to arrange them in a line for a photo. For the first position, you can pick any of the 
𝑛
n people. Once the first person is chosen, you can pick any of the remaining 
𝑛
−
1
n−1 people for the second position, then any of the remaining 
𝑛
−
2
n−2 for the third position, and so on. This results in 
𝑛
!
=
𝑛
×
(
𝑛
−
1
)
×
(
𝑛
−
2
)
×
⋯
×
1
n!=n×(n−1)×(n−2)×⋯×1 possible arrangements. As you increase the number of people, the number of ways to arrange them grows extremely fast.

```py
# Iterating through all permutations of a set
def generate_permutations(arr, start=0):
    if start == len(arr) - 1:
        print(arr)
    for i in range(start, len(arr)):
        arr[start], arr[i] = arr[i], arr[start]
        # Recurse
        generate_permutations(arr, start + 1)
        arr[start], arr[i] = arr[i], arr[start]
```

## Space Complexity:

* ### O(1): Constant space.
    * The algorithm uses a `constant` amount of memory, regardless of the `input size`.
    * Example: `Iterating` through an `array`.
```py
def print_all_elements(my_list):
    for element in my_list:
        print(element)
```

* ### O(n): Linear space.
    * The algorithm uses `linear` amount of memory, proportional to the `input size`.
    * Example: `Iterating` through an `array` and storing the values in a `hash table`.
```py
# O(n) space - Storing all elements in a hash table
def reverse_list(arr):
    reversed_arr = []
    for i in range(len(arr) - 1, -1, -1):
        reversed_arr.append(arr[i])
    return reversed_arr
```


* ### O(n^2): Quadratic space.  
    * The algorithm uses `quadratic` amount of memory, proportional to the `input size`.
    * Example: `Iterating` through an `array` and storing the values in a `2D array`.
```py
# O(n^2) space - Storing all elements in a 2D array
def create_identity_matrix(n):
    identity = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        identity[i][i] = 1
    return identity
```

* ### O(2^n): Exponential space.
    * The algorithm uses `exponential` amount of memory, proportional to the `input size`.
    * Example: `Iterating` through all subsets of a set.
```py
# Exponential Space - O(2^n)
def power_set(arr):
    result = [[]]
    for item in arr:
        result += [subset + [item] for subset in result]
    return result
```
---
## Common Data Structures:

* ### Array
    * **Time** Complexity:
        * **Access**: `O(1)`
        * **Search**: `O(n)`
        * **Insertion**: `O(n)`
        * **Deletion**: `O(n)`
    * **Space** Complexity: `O(n)`
    * **Description**: An `array` is a data structure that stores a collection of elements. Each element is identified by an index, or key. Arrays are used to store a collection of data, but they are not as flexible as other data structures such as linked lists, stacks, and queues. Arrays are best used when you know exactly what data you need to store, and how you will be accessing it.

* ### Linked List
    * **Time** Complexity:
        * **Access**: `O(n)`
        * **Search**: `O(n)`
        * **Insertion**: `O(1)`
        * **Deletion**: `O(1)`
    * **Space** Complexity: `O(n)`
    * **Description**: A `linked list` is a data structure that stores a collection of elements. Each element is a separate object that contains a `pointer or a link to the next object in that list`. Linked lists are **best** used when you need to *add* or *remove* elements from the beginning of the list.

* ### Stack
    * **Time** Complexity:
        * **Access**: `O(n)`
        * **Search**: `O(n)`
        * **Insertion**: `O(1)`
        * **Deletion**: `O(1)`
    * **Space** Complexity: `O(n)`
    * **Description**: A `stack` is a data structure that stores a collection of elements. A `stack` is a `LIFO` (Last In First Out) data structure, meaning that the last element added to the stack will be the first one to be removed. Stacks are best used when you need to *add* or *remove* elements from the beginning of the list.

* ### Queue
    * **Time** Complexity:
        * **Access**: `O(n)`
        * **Search**: `O(n)`
        * **Insertion**: `O(1)`
        * **Deletion**: `O(1)`
    * **Space** Complexity: `O(n)`
    * **Description**: A `queue` is a data structure that stores a collection of elements. A `queue` is a `FIFO` (First In First Out) data structure, meaning that the first element added to the queue will be the first one to be removed. Queues are best used when you need to *add* or *remove* elements from the end of the list.

* ### Hash Table
    * **Time** Complexity:
        * **Access**: `O(1)`
        * **Search**: `O(1)`
        * **Insertion**: `O(1)`
        * **Deletion**: `O(1)`
    * **Space** Complexity: `O(n)`
    * **Description**: A `hash table` is a data structure that stores a collection of elements. A `hash table` is a `key-value` data structure, meaning that each element is identified by a `key`. A `hash function` is used to compute the index at which an element will be stored. Hash tables are best used when you need to *add*, *remove*, or *access* elements in a collection.

"""Demonstration of rpipe functionality."""

from rpipe import P, pipe, TF, TL, partial
from functools import reduce
from toolz import take, drop


def main():
    """Run various rpipe demonstrations."""

    print("=== Basic rpipe Examples ===\n")

    # Basic usage with >>
    result = range(5) >> P(list)
    print(f"range(5) >> P(list) = {result}")

    # Traditional pipe
    result = pipe(range(5), list, sum)
    print(f"pipe(range(5), list, sum) = {result}")

    # Multiple transformations
    result = [1, 2, 3, 4, 5] >> P(sum)
    print(f"[1, 2, 3, 4, 5] >> P(sum) = {result}")

    print("\n=== Thread-first (TF) and Thread-last (TL) ===\n")

    # Thread-first example
    result = TF(
        10,
        (lambda x, y: x / y, 2),  # 10 / 2 = 5
        (lambda x, y: x + y, 3),  # 5 + 3 = 8
        str                        # "8"
    )
    print(f"TF(10, (div, 2), (add, 3), str) = {result}")

    # Thread-last example
    result = TL(
        2,
        (pow, 3),            # pow(3, 2) = 9
        str,                 # "9"
        (lambda s: s.rjust(5, '0'))  # "00009"
    )
    print(f"TL(2, (pow, 3), str, rjust) = {result}")

    print("\n=== Using functools.partial ===\n")

    # Partial application
    add = lambda x, y: x + y
    add_10 = partial(add, 10)

    result = 5 >> P(add_10, lambda x: x * 2)
    print(f"5 >> P(add_10, lambda x: x * 2) = {result}")

    # Complex pipeline with partial
    data = ["apple", "banana", "cherry", "date", "elderberry"]

    result = data >> P(
        partial(filter, lambda x: len(x) > 5),
        list,
        partial(map, str.upper),
        list,
        sorted
    )
    print(f"Fruits longer than 5 chars (uppercase): {result}")

    print("\n=== Comparing Different Pipe Styles ===\n")

    # Same operation, different styles
    numbers = [1, 2, 3, 4, 5]

    # Style 1: Using >> operator
    result1 = numbers >> P(
        partial(map, lambda x: x * 2),
        list,
        sum
    )
    print(f"Style 1 (>>): {result1}")

    # Style 2: Using pipe function
    result2 = pipe(
        numbers,
        partial(map, lambda x: x * 2),
        list,
        sum
    )
    print(f"Style 2 (pipe): {result2}")

    # Style 3: Using thread-first
    # For TF, we need to be careful with functions that return iterators
    result3 = TF(
        numbers,
        (partial(map, lambda x: x * 2),),  # Returns map object
        list,                              # Convert map object to list
        sum
    )
    print(f"Style 3 (TF): {result3}")

    print("\n=== Advanced Examples ===\n")

    # Statistical operations
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    mean = numbers >> P(sum, lambda x: x / len(numbers))
    print(f"Mean of {numbers}: {mean}")

    # Text processing
    text = "The quick brown fox jumps over the lazy dog"

    word_count = text >> P(
        str.lower,
        str.split,
        len
    )
    print(f"Word count: {word_count}")

    # Using with toolz
    result = range(20) >> P(
        partial(drop, 5),
        partial(take, 10),
        list,
        lambda x: [i**2 for i in x],
        sum
    )
    print(f"Sum of squares of numbers 5-14: {result}")

    print("\n=== Real-world Example: Data Processing ===\n")

    # Simulate processing user data
    users = [
        {"name": "Alice", "age": 25, "score": 85},
        {"name": "Bob", "age": 30, "score": 92},
        {"name": "Charlie", "age": 22, "score": 78},
        {"name": "Diana", "age": 28, "score": 95},
        {"name": "Eve", "age": 35, "score": 88},
    ]

    # Get names of high scorers
    high_scorers = users >> P(
        partial(filter, lambda u: u["score"] > 85),
        list,
        partial(map, lambda u: u["name"]),
        list,
        lambda names: ", ".join(names)
    )
    print(f"High scorers (>85): {high_scorers}")

    # Calculate average age
    avg_age = users >> P(
        partial(map, lambda u: u["age"]),
        list,
        lambda ages: sum(ages) / len(ages)
    )
    print(f"Average age: {avg_age}")

    print("\n=== Combining All Styles ===\n")

    # A complex example using multiple styles
    data = range(1, 11)

    # First, use pipe to get even numbers
    evens = pipe(data, partial(filter, lambda x: x % 2 == 0), list)

    # Then process them with >>
    processed = evens >> P(
        partial(map, lambda x: x ** 2),
        list,
        lambda x: sorted(x, reverse=True)
    )

    # Finally use >> to get the result
    result = processed >> P(
        partial(take, 3),
        list,
        sum
    )

    print(f"Sum of top 3 squared even numbers: {result}")
    print(f"  Even numbers: {evens}")
    print(f"  Squared and sorted (desc): {processed}")
    print(f"  Top 3 sum: {result}")


if __name__ == "__main__":
    main()

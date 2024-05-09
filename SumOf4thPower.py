# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 20:53:51 2024

@author: cscholz
"""

import time
from itertools import combinations_with_replacement, combinations
from math import factorial
from tqdm import tqdm

def is_odd(number):
    return number % 2 != 0

# Set minimum and maximum values of search range
Nmin = 353 #651 #5491
Nmax = 353 #651 #5491

# Check that pre-conditions are met
if not (is_odd(Nmin) and is_odd(Nmax) and Nmax >= Nmin):
    raise ValueError("Conditions not met. Nmin and Nmax must be odd, and Nmax must be greater than or equal to Nmin.")

# Generate list of 4th powers
left_side_indices = range(Nmin, Nmax + 1, 2)
left_side_values = [i0**4 for i0 in range(Nmin,Nmax + 1,2)] # due to mod 16 = 0,1 for 4th power, sum of 4 4th powers must be odd or has a common factor, such that it can be reduce by /16

# Generate odd_div_by_5 case
def generate_combinations_with_even_all_divisible_by_5(even_numbers_div_5, odd_numbers_not_div_5):
    for odd_comb in odd_numbers_not_div_5:
        even_combinations = combinations_with_replacement(even_numbers_div_5, 3)  # Generate combinations of odd numbers
        for even_comb in even_combinations:
            yield [odd_comb] + list(even_comb)

# Generate even_div_by_5 case
def generate_combinations_with_odd_even_two_divisible_by_5(even_numbers_div_5, odd_numbers_div_5, even_numbers_not_div_5):
    for even_comb in combinations_with_replacement(even_numbers_div_5, 2):
        for odd_comb_divisible_by_5 in combinations(odd_numbers_div_5, 1):
            for even_comb_not_divisible_by_5 in combinations(even_numbers_not_div_5, 1):
                yield list(even_comb) + list(odd_comb_divisible_by_5) + list(even_comb_not_divisible_by_5)

def calculate_factors(left_side_index, left_side):
    odd_numbers_divisible_by_5 = {i**4 for i in range(1, left_side_index + 1 - 3) if i % 2 != 0 and i % 5 == 0 and any((left_side - i**4) % 16 == r for r in range(4))}
    odd_numbers_not_divisible_by_5 = {i**4 for i in range(1, left_side_index + 1 - 3) if i % 2 != 0 and i % 5 != 0 and (left_side - i**4) % 625 == 0 and any((left_side - i**4) % 16 == r for r in range(4))}
    even_numbers_divisible_by_5 = {i**4 for i in range(2, left_side_index + 1 - 3, 2) if i % 5 == 0}
    even_numbers_not_divisible_by_5 = {i**4 for i in range(2, left_side_index + 1 - 3, 2) if i % 5 != 0 and (left_side - i**4) % 625 == 0}
    return odd_numbers_divisible_by_5, odd_numbers_not_divisible_by_5, even_numbers_divisible_by_5, even_numbers_not_divisible_by_5

# Search for possible solutions
def search_matches(left_side_values, left_side_indices, total_iterations):
    solutions = []  # Initialize an empty list to store solutions
    progress_update_interval = 1000  # Update progress bar after every 1000 iterations
    with tqdm(total=total_iterations) as pbar:
        iteration_count = 0
        for array_index, left_side in enumerate(left_side_values):
            odd_numbers_divisible_by_5, odd_numbers_not_divisible_by_5, even_numbers_divisible_by_5, even_numbers_not_divisible_by_5 = calculate_factors(left_side_indices[array_index], left_side)
            # Calculate for each combination
            combinations = generate_combinations_with_odd_even_two_divisible_by_5(even_numbers_divisible_by_5, odd_numbers_divisible_by_5, even_numbers_not_divisible_by_5)
            for combination in combinations:
                iteration_count += 1
                sum_combination = sum(combination)
                if sum_combination == left_side:
                    print(f'\nfound solution: {left_side} = {" + ".join(str(i) for i in combination)}')
                    solutions.append((left_side, combination))
                if iteration_count % progress_update_interval == 0:
                    pbar.update(progress_update_interval)
            combinations = generate_combinations_with_even_all_divisible_by_5(even_numbers_divisible_by_5, odd_numbers_not_divisible_by_5)
            for combination in combinations:
                iteration_count += 1
                sum_combination = sum(combination)
                if sum_combination == left_side:
                    print(f'\nfound solution: {left_side} = {" + ".join(str(i) for i in combination)}')
                    solutions.append((left_side, combination))
                if iteration_count % progress_update_interval == 0:
                    pbar.update(progress_update_interval)
            print(f"\nLast combination: {combination}")
    return solutions # return the list of solutions

# Run the main script
print(f'Check all powers up to {left_side_indices[-1]}**4')
start_time = time.time()

# Determine total numbers of iterations for time estimate
length1 = 0
length2 = 0
for array_index, left_side in enumerate(left_side_values):
    odd_numbers_divisible_by_5, odd_numbers_not_divisible_by_5, even_numbers_divisible_by_5, even_numbers_not_divisible_by_5 = calculate_factors(left_side_indices[array_index], left_side)
	# Determine length of odd_div_by_5 case
    n = len(list(even_numbers_divisible_by_5))
    k = 3
    length1 += len(list(odd_numbers_not_divisible_by_5)) * factorial(n-1+k)/(factorial(k)*factorial(n-1))
	# determine length of even_div_by_5 case
    n=len(list(even_numbers_divisible_by_5)) 
    k=2
    length2 += factorial(n-1+k)/(factorial(k)*factorial(n-1)) * len(list(odd_numbers_divisible_by_5)) * len(list(even_numbers_not_divisible_by_5))

# start searching for matches
solutions = search_matches(left_side_values, left_side_indices, length1+length2)
end_time = time.time()
total_runtime = end_time - start_time
print(f"Total runtime: {total_runtime:.2f} seconds")
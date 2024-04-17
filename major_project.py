import itertools
from sage.all import *
import numpy as np
import sys
import pickle
import time

verbose = True


def generate_binary_strings(n):
    if verbose:
        print('Starting generating binary strings...')
    start_time = time.time()
    result = [list(bs) for i, bs in enumerate(itertools.product([0, 1], repeat=n))]
    end_time = time.time()
    print(f'Time: {end_time - start_time}')
    # 24.32463002204895
    # 12.116153240203857
    # 5.943586826324463
    if verbose:
        print('Finished generating binary strings')
    return result


def generate_binary_strings_numpy(n):
    if verbose:
        print('Starting generating binary strings...')
    start_time = time.time()

    # Generate all binary numbers from 0 to 2^n - 1
    nums = np.arange(2 ** n, dtype=np.uint8)
    # Convert numbers to binary format and pad with zeros
    binary_strings = ((nums[:, None] & (1 << np.arange(n))) > 0).astype(int)
    # Reverse the order of columns because binary digits are from least significant to most significant
    binary_strings = np.fliplr(binary_strings)

    end_time = time.time()
    if verbose:
        print('Finished generating binary strings')
        print(f'Time: {end_time - start_time}')

    return binary_strings


def generate_set(divisor):
    if verbose:
        print('Starting generating set...')
    primes = list(primes_first_n(100))
    power_of_ten = 10 ** 100
    result = [floor(power_of_ten * (p ** (1 / 3))) for p in primes]
    result_divisor = [r // divisor for r in result]
    if verbose:
        print('Finished generating set')
    return result, result_divisor


def generate_target(id, divisor):
    result = 2 * id * 10**94
    result_divisor = result // divisor
    return result, result_divisor


def get_subset_sums(subset):
    subset_length = len(subset)
    binary_strings = generate_binary_strings(subset_length)
    print('test')
    num_subsets = len(binary_strings)
    subset_sums = {}
    for i in range(num_subsets):
        summ = np.dot(binary_strings[i], subset)
        subset_sums[summ] = binary_strings[i]
        if verbose:
            percentage = ((i + 1) / num_subsets) * 100
            sys.stdout.write("\rCalculating Subset Sums: {:.2f}%".format(percentage))
            sys.stdout.flush()
    if verbose:
        print()
    return subset_sums


if __name__ == '__main__':
    bs = generate_binary_strings(5)
    bs_np = generate_binary_strings_numpy(5)
    time.sleep(5)
    print()
    print()
    print(bs)
    print(bs_np)
    # # Constants used for meet in the middle
    # size_of_m1 = 27
    # divisor_power = 85
    #
    # # Generate target
    # target, target_divisor = generate_target(113499560, 10**divisor_power)
    #
    # # Generate Set
    # m, m_divisor = generate_set(10**divisor_power)
    # m = np.array(m)
    # m_divisor = np.array(m_divisor)
    #
    # # Split set
    # m1 = m[:size_of_m1]
    # m2 = m[size_of_m1:]
    # m1_divisor = m_divisor[:size_of_m1]
    # m2_divisor = m_divisor[size_of_m1:]
    #
    # # Find all subset sums for left set
    # subset_sums = get_subset_sums(m1_divisor)
    #
    # # Store the answer values
    # values = []
    #
    # # Perform meet-in-the-middle attack
    # if verbose:
    #     print('Searching for answer...')
    # while True:
    #     # Generate random bit string for right set
    #     right_binary_string = np.random.randint(2, size=100 - size_of_m1)
    #
    #     # Find sum in random subset
    #     summ = np.dot(m2_divisor, right_binary_string)
    #
    #     # If the sum's complement was found in left subset sums, it is the answer
    #     if target_divisor - summ in subset_sums:
    #         if verbose:
    #             print('Found answer')
    #         left_binary_string = subset_sums[target_divisor - summ]
    #
    #         # Find elements from left
    #         for i in range(len(left_binary_string)):
    #             if left_binary_string[i] == 1:
    #                 values.append(m1[i])
    #
    #         # Find elements from right
    #         for i in range(len(right_binary_string)):
    #             if right_binary_string[i] == 1:
    #                 values.append(m2[i])
    #
    #         # Save the binary string and sum answer
    #         total_binary_string = np.concatenate((left_binary_string, right_binary_string))
    #         answer = np.sum(values)
    #         difference = answer - target
    #
    #         # Output results
    #         print(f'Target: {target}')
    #         print(f'Answer: {answer}')
    #         print(f'Difference: {difference:e}')
    #         print(f'Binary String: {total_binary_string}')
    #
    #         # Save results to pickle file
    #         results = {
    #             'binary_string': total_binary_string,
    #             'values': values,
    #             'target': target,
    #             'answer': answer,
    #             'difference': difference
    #         }
    #         if verbose:
    #             print('Saving results...')
    #         with open(f'results_left_size_{size_of_m1}_divisor_{divisor_power}.pkl', "wb") as fp:
    #             pickle.dump(results, fp)
    #         if verbose:
    #             print('Done.')
    #
    #         break

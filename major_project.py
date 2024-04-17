import itertools
from sage.all import *
import numpy as np
import pickle
import time

verbose = True


def generate_binary_strings(n):
    if verbose:
        print('Starting generating binary strings...')
    start_time = time.time()

    # Generate all binary numbers from 0 to 2^n - 1
    nums = np.arange(2 ** n, dtype=np.uint8)
    # Convert numbers to binary format and pad with zeros
    binary_strings = np.unpackbits(nums.reshape(-1, 1), axis=1, count=n, bitorder='little')
    # Reverse the order of columns because binary digits are from least significant to most significant
    binary_strings = np.fliplr(binary_strings)

    end_time = time.time()
    if verbose:
        print('Finished generating binary strings')
        print(f'Time: {end_time - start_time}')

    return binary_strings


def generate_binary_strings_alt(n):
    if verbose:
        print('Starting generating binary strings...')
    start_time = time.time()

    # Generate all binary numbers from 0 to 2^n - 1
    nums = np.arange(2 ** n, dtype=np.uint32)
    # Convert numbers to binary format and pad with zeros
    binary_strings = ((nums[:, None] & (1 << np.arange(n))) > 0).astype(int)
    # Reverse the order of columns because binary digits are from least significant to most significant
    binary_strings = np.fliplr(binary_strings)

    end_time = time.time()
    if verbose:
        print('Finished generating binary strings')
        print(f'Time: {end_time - start_time}')

    return binary_strings


def generate_binary_strings_alt_alt(n, chunk_size=1000000):
    if verbose:
        print('Starting generating binary strings...')
    start_time = time.time()

    # Determine the correct datatype to hold the numbers
    if n <= 8:
        dtype = np.uint8
    elif n <= 16:
        dtype = np.uint16
    elif n <= 32:
        dtype = np.uint32
    else:
        dtype = np.uint64

    num_total = 2 ** n
    all_binary_strings = []

    for start in range(0, num_total, chunk_size):
        end = min(start + chunk_size, num_total)
        nums = np.arange(start, end, dtype=dtype)

        # Convert numbers to binary format and pad with zeros
        binary_strings = np.unpackbits(nums.view(np.uint8).reshape(-1, 4), axis=1, count=n, bitorder='little')
        # Reverse the order of columns because binary digits are from least significant to most significant
        binary_strings = np.fliplr(binary_strings)

        all_binary_strings.append(binary_strings)

    all_binary_strings = np.vstack(all_binary_strings)

    end_time = time.time()
    if verbose:
        print('Finished generating binary strings')
        print(f'Time: {end_time - start_time}')

    return all_binary_strings


def generate_set(divisor):
    primes = list(primes_first_n(100))
    power_of_ten = 10 ** 100
    result = [floor(power_of_ten * (p ** (1 / 3))) for p in primes]
    result_divisor = [r // divisor for r in result]
    return result, result_divisor


def generate_target(id, divisor):
    result = 2 * id * 10**94
    result_divisor = result // divisor
    return result, result_divisor


def get_subset_sums(subset):
    subset_length = len(subset)
    binary_strings = generate_binary_strings(subset_length)
    num_subsets = len(binary_strings)
    subset_sums = {}
    for i in range(num_subsets):
        print(i)
        summ = np.dot(binary_strings[i], subset)
        if summ in subset_sums:
            print(subset_sums)
            print('collision')
            print(summ)
            print(subset_sums[summ])
            print(binary_strings[i])
            exit(0)
        subset_sums[summ] = binary_strings[i]
        # if verbose:
        #     percentage = ((i + 1) / num_subsets) * 100
        #     sys.stdout.write("\rCalculating Subset Sums: {:.2f}%".format(percentage))
        #     sys.stdout.flush()
    if verbose:
        print()
    return subset_sums
    # subset_length = len(subset)
    # binary_strings = generate_binary_strings(subset_length)
    # subset_sums = {np.dot(binary_strings[i], subset): binary_strings[i] for i in range(len(binary_strings))}
    #
    # return subset_sums


if __name__ == '__main__':
    # bs = generate_binary_strings(20)
    bs_alt = generate_binary_strings_alt_alt(28)
    # print(bs[256])
    print(bs_alt[-1])
    # # Constants used for meet in the middle
    # size_of_m1 = 25
    # divisor_power = 90
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
    # print(len(subset_sums.keys()))
    #
    # # Store the answer values
    # values = []
    #
    # # Perform meet-in-the-middle attack
    # if verbose:
    #     print('Searching for answer...')
    #
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
    #         # Store values used in sum
    #         values = [m1[i] for i in range(len(left_binary_string)) if left_binary_string[i] == 1]
    #         values.extend(m2[i] for i in range(len(right_binary_string)) if right_binary_string[i] == 1)
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

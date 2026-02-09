"""
Additional logic (e.g. first_pass, etc.) use for logs has been added
for educational purposes but is not needed in the actual implementation:

    def binarySearch(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2  # avoid overflow
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1  # not found

"""
def binary_search(arr:list[int], target: int) -> int:
    left, right = 0, len(arr) - 1
    mid = -1
    first_pass = True
    while left <= right:
        prev_mid = mid
        mid = left + (right - left) // 2  # avoid overflow
        if first_pass:
            print(f'Beginning our search for target {target} starting at our middle index of {mid}.\n')
        else:
            if left == mid or right == mid:
                array_txt = f'{left}...{right}'
            else:
                array_txt = f'{left}...{mid}...{right}'

            print(f'Halving search range. Left is now {left}, Right is now {right}, and Mid has been updated from {prev_mid} -> {mid} [{array_txt}].\n')

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            prev_left = left
            left = mid + 1
            print(f'Because the element (at index {mid}) is LESS than target ({arr[mid]} < {target}) we\'ll move the LEFT pointer inward from {prev_left} -> {left} (one greater than {mid}) \n' +
                f'to focus on the right half of our search range [{left}...{right}]. Since the array is sorted, we know our target has to be somewhere between these indices if it exists in our input.\n')
        else:
            prev_right = right
            right = mid - 1
            print(
                f'Because the element (at index {mid}) is GREATER than target ({arr[mid]} > {target}) we\'ll move the RIGHT pointer inward from {prev_right} -> {right} (one less than {mid}) \n' +
                f'to focus on the left half of our search range [{left}...{right}]. Since the array is sorted, we know our target has to be somewhere between these indices if it exists in our input.\n')

        first_pass = False

    print(f'Target not found in list, returning -1')
    return -1  # not found

t = 35
sorted_list = [ 1, 2, 4, 6, 12, 18, 21, 23, 35, 52]
target_index = binary_search(sorted_list, t)

if target_index != -1:
    sorted_list[target_index] = f'[{sorted_list[target_index]}]'
    print(f'Target {t} found at index: {target_index}!: sorted_list: {sorted_list}')
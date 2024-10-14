# Assumes that list is sorted.
# If target isn't found, this returns the index that it would be inserted into.
def binary_search(list: list, target):
        left, right = 0, len(list) - 1
        while left <= right:
            mid = (left + right) // 2
            if list[mid] < target:
                left = mid + 1
            elif list[mid] > target:
                right = mid - 1
            else:
                return mid
        return left
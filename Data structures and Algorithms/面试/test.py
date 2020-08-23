def searchRange(nums, target):
    if not nums or len(nums) == 0:
        return [-1, -1]
    left, right = -1, -1

    # left bounder
    start, end = 0, len(nums) - 1
    while start <= end:
        mid = start + ((end - start) // 2)
        if target < nums[mid]:
            end = mid - 1
        elif target > nums[mid]:
            start = mid + 1
        else:
            end = mid - 1
    left = end + 1
    if left >= len(nums) or nums[left] != target:
        return [-1, -1]

    # right bounder
    start, end = 0, len(nums) - 1
    while start <= end:
        mid = start + ((end - start) // 2)
        if target > nums[mid]:
            start = mid + 1
        elif target < nums[mid]:
            end = mid - 1
        else:
            start = mid + 1
    right = start - 1
    if right < 0 or nums[right] != target:
        return [-1, -1]

    return [left, right]


nums = [5,7,7,8,8,10]
target = 8
print(searchRange(nums, target))

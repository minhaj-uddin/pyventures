def permute(nums):
    result = []

    def backtrack(start=0):
        if start == len(nums):
            print("Permutation complete:", nums)
            result.append(nums[:])
            return

        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            print(f"Swapped positions {start} and {i}: {nums}")
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]
            print(f"Backtracked positions {start} and {i}: {nums}")

    backtrack()
    return result


# Example usage:
nums = [1, 2, 3]
print(permute(nums))

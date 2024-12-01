def FMS_COMPARE(A, low, high):
    if low == high:
        return A[low], A[low], A[low], A[low]
    else:
        mid = (low + high) // 2
        left = FMS_COMPARE(A, low, mid)
        right = FMS_COMPARE(A, mid + 1, high)
        return COMPARE(left, right)

# Function to compare and combine results from left and right parts
def COMPARE(L, R):
    totalSum = L[0] + R[0]
    maxPrefix = max(L[1], L[0] + R[1])
    maxSuffix = max(R[2], R[0] + L[2])
    maxSum = max(L[3], R[3], L[2] + R[1])
    return totalSum, maxPrefix, maxSuffix, maxSum

print(FMS_COMPARE([1, 2, 3, 4, 5, 6, 7, 8, 9], 0, 8))
print(FMS_COMPARE([-2, 1, -3, 4, -1, 2, 1, -5, 4], 0, 8) )
import numpy as np
def strassen_multiply(A, B):

    n = len(A)
    

    if n == 1:
        return A * B
    

    mid = n // 2
    
    A11, A12 = A[:mid, :mid], A[:mid, mid:]
    A21, A22 = A[mid:, :mid], A[mid:, mid:]
    
    B11, B12 = B[:mid, :mid], B[:mid, mid:]
    B21, B22 = B[mid:, :mid], B[mid:, mid:]


    M1 = strassen_multiply(A11 + A22, B11 + B22)
    M2 = strassen_multiply(A21 + A22, B11)
    M3 = strassen_multiply(A11, B12 - B22)
    M4 = strassen_multiply(A22, B21 - B11)
    M5 = strassen_multiply(A11 + A12, B22)
    M6 = strassen_multiply(A21 - A11, B11 + B12)
    M7 = strassen_multiply(A12 - A22, B21 + B22)


    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6


    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
    return C


A = np.array([[1, 2], [2, 3]])
B = np.array([[2, 3], [7, 4]])

result = strassen_multiply(A, B)
print("Resultant Matrix:")
print(result)

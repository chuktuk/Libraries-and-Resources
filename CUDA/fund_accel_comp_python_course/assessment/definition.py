import numpy as np
from numba import cuda, types
@cuda.jit
def mm_shared(A, B, C):
    # Define an array in the shared memory
    # The size and type of the arrays must be known at compile time
    TPB = N
#     sA = cuda.shared.array(shape=(TPB, TPB), dtype=types.float32)
#     sB = cuda.shared.array(shape=(TPB, TPB), dtype=types.float32)

#     x, y = cuda.grid(2)

#     tx = cuda.threadIdx.x
#     ty = cuda.threadIdx.y
#     bpg = cuda.gridDim.x    # blocks per grid

#     if x >= C.shape[0] and y >= C.shape[1]:
#         # Quit if (x, y) is outside of valid C boundary
#         return

#     # Each thread computes one element in the result matrix.
#     # The dot product is chunked into dot products of TPB-long vectors.
#     tmp = 0.
#     for i in range(bpg):
#         # Preload data into shared memory
#         sA[tx, ty] = A[x, ty + i * TPB]
#         sB[tx, ty] = B[tx + i * TPB, y]

#         # Wait until all threads finish preloading
#         cuda.syncthreads()

#         # Computes partial product on the shared memory
#         for j in range(TPB):
#             tmp += sA[tx, j] * sB[j, ty]

#         # Wait until all threads finish computing
#         cuda.syncthreads()

#     C[x, y] = tmp

    sA = cuda.shared.array(shape=(TPB, TPB), dtype=types.float32)
    sB = cuda.shared.array(shape=(TPB, TPB), dtype=types.float32)

    x, y = cuda.grid(2)

    tx = cuda.threadIdx.x
    ty = cuda.threadIdx.y
    bpg = cuda.gridDim.x    # blocks per grid

    # Each thread computes one element in the result matrix.
    # The dot product is chunked into dot products of TPB-long vectors.
#     tmp = float32(0.)
    tmp = 0.
    for i in range(bpg):
        # Preload data into shared memory
        sA[ty, tx] = 0
        sB[ty, tx] = 0
        if y < A.shape[0] and (tx+i*TPB) < A.shape[1]:
            sA[ty, tx] = A[y, tx + i * TPB]
        if x < B.shape[1] and (ty+i*TPB) < B.shape[0]:
            sB[ty, tx] = B[ty + i * TPB, x]

        # Wait until all threads finish preloading
        cuda.syncthreads()

        # Computes partial product on the shared memory
        for j in range(TPB):
            tmp += sA[ty, j] * sB[j, tx]

        # Wait until all threads finish computing
        cuda.syncthreads()
    if y < C.shape[0] and x < C.shape[1]:
        C[y, x] = tmp
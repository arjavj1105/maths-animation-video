"""
Mathematical Verification Script for Gaussian Elimination (3x3 System)
Student Name: Arjav Jain
Student ID: E25B070861
Batch: Ramanujan
Course: Mathematics 3 - Linear Algebra and Calculus
"""

import numpy as np
import sys

def verify():
    print("=" * 70)
    print("MATHEMATICAL VERIFICATION: GAUSSIAN ELIMINATION (3x3 SYSTEM)")
    print("Student: Arjav Jain | ID: E25B070861 | Batch: Ramanujan")
    print("=" * 70)

    # 1. Original coefficient matrix A and constant vector b
    A = np.array([
        [1.0, 1.0, 1.0],
        [2.0, 3.0, 1.0],
        [1.0, 2.0, 3.0]
    ], dtype=np.float64)

    b = np.array([6.0, 11.0, 14.0], dtype=np.float64)

    print("\n1. Coefficient Matrix A:")
    print(A)
    print("\nRight-Hand-Side Vector b:")
    print(b)

    # 2. Check Determinant
    det_A = np.linalg.det(A)
    print(f"\n2. Determinant of A: det(A) = {det_A:.4f}")
    assert not np.isclose(det_A, 0.0), "Error: Matrix A is singular!"
    print("   -> det(A) != 0 confirms A is invertible and system has a UNIQUE solution.")

    # 3. Solve Ax = b using numpy.linalg.solve
    x_numpy = np.linalg.solve(A, b)
    print(f"\n3. numpy.linalg.solve(A, b) result: {x_numpy}")
    expected_x = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    assert np.allclose(x_numpy, expected_x), f"Error: Expected {expected_x}, got {x_numpy}"
    print(f"   -> Exact solution confirmed: x = {x_numpy[0]:.0f}, y = {x_numpy[1]:.0f}, z = {x_numpy[2]:.0f}")

    # 4. Form Initial Augmented Matrix
    M = np.column_stack([A, b])
    print("\n4. Initial Augmented Matrix [A | b]:")
    print(M)

    # 5. Step-by-Step Row Operations
    print("\n5. Step-by-Step Elementary Row Operations:")
    
    # Operation 1: R2 -> R2 - 2*R1
    print("\n--- Operation 1: R2 -> R2 - 2*R1 ---")
    r2_before = M[1].copy()
    r1 = M[0].copy()
    r2_after = r2_before - 2.0 * r1
    M[1] = r2_after
    expected_r2 = np.array([0.0, 1.0, -1.0, -1.0])
    print(f"R2 before: {r2_before}")
    print(f"2 * R1:    {2.0 * r1}")
    print(f"R2 after:  {M[1]}")
    assert np.allclose(M[1], expected_r2), f"Row op 1 mismatch: got {M[1]}, expected {expected_r2}"
    print("   -> Row Operation 1 MATCHES expected: [0, 1, -1 | -1]")

    # Operation 2: R3 -> R3 - R1
    print("\n--- Operation 2: R3 -> R3 - R1 ---")
    r3_before = M[2].copy()
    r3_after = r3_before - r1
    M[2] = r3_after
    expected_r3_step2 = np.array([0.0, 1.0, 2.0, 8.0])
    print(f"R3 before: {r3_before}")
    print(f"R1:        {r1}")
    print(f"R3 after:  {M[2]}")
    assert np.allclose(M[2], expected_r3_step2), f"Row op 2 mismatch: got {M[2]}, expected {expected_r3_step2}"
    print("   -> Row Operation 2 MATCHES expected: [0, 1, 2 | 8]")

    # Operation 3: R3 -> R3 - R2
    print("\n--- Operation 3: R3 -> R3 - R2 ---")
    r3_before_op3 = M[2].copy()
    r2_op3 = M[1].copy()
    r3_after_op3 = r3_before_op3 - r2_op3
    M[2] = r3_after_op3
    expected_r3_step3 = np.array([0.0, 0.0, 3.0, 9.0])
    print(f"R3 before: {r3_before_op3}")
    print(f"R2:        {r2_op3}")
    print(f"R3 after:  {M[2]}")
    assert np.allclose(M[2], expected_r3_step3), f"Row op 3 mismatch: got {M[2]}, expected {expected_r3_step3}"
    print("   -> Row Operation 3 MATCHES expected: [0, 0, 3 | 9]")

    # Final Row Echelon Form (REF)
    print("\n6. Final Row Echelon Matrix [U | c]:")
    print(M)
    expected_final_M = np.array([
        [1.0, 1.0,  1.0,  6.0],
        [0.0, 1.0, -1.0, -1.0],
        [0.0, 0.0,  3.0,  9.0]
    ])
    assert np.allclose(M, expected_final_M), "Final REF matrix does not match expected!"
    print("   -> Final REF matrix matches expected matrix perfectly.")

    # Pivots
    pivots = [M[0, 0], M[1, 1], M[2, 2]]
    print(f"\n   Pivots along diagonal: Pivot 1 = {pivots[0]:.0f}, Pivot 2 = {pivots[1]:.0f}, Pivot 3 = {pivots[2]:.0f}")
    assert pivots == [1.0, 1.0, 3.0], "Pivot mismatch!"
    print("   -> All three pivots are non-zero. Matrix is in upper-triangular echelon form.")

    # 7. Back Substitution
    print("\n7. Back Substitution Execution:")
    z = M[2, 3] / M[2, 2]
    print(f"   From Row 3: 3z = 9  =>  z = 9 / 3 = {z:.0f}")
    
    y = (M[1, 3] - M[1, 2] * z) / M[1, 1]
    print(f"   From Row 2: y - z = -1  =>  y = -1 + ({z:.0f}) = {y:.0f}")

    x = (M[0, 3] - M[0, 1] * y - M[0, 2] * z) / M[0, 0]
    print(f"   From Row 1: x + y + z = 6  =>  x = 6 - ({y:.0f}) - ({z:.0f}) = {x:.0f}")

    sol = np.array([x, y, z])
    assert np.allclose(sol, expected_x), f"Back substitution mismatch: got {sol}, expected {expected_x}"
    print(f"   -> Back substitution solution: (x, y, z) = ({x:.0f}, {y:.0f}, {z:.0f})")

    # 8. Matrix Multiplication Verification: A * x = b
    print("\n8. Verification via Matrix Multiplication (A @ x):")
    Ax = A @ sol
    residuals = Ax - b
    print(f"   A @ x = {Ax}")
    print(f"   b     = {b}")
    print(f"   Residuals (A @ x - b): {residuals}")
    assert np.allclose(residuals, 0.0), "Non-zero residuals in Ax = b!"
    print("   -> All residuals are ZERO. Ax = b is strictly satisfied.")

    # 9. Individual Equation Verifications
    print("\n9. Individual Equation Verification:")
    eq1_lhs = 1.0*x + 1.0*y + 1.0*z
    eq1_rhs = 6.0
    print(f"   Eq 1: x + y + z = {x:.0f} + {y:.0f} + {z:.0f} = {eq1_lhs:.0f} (Expected: {eq1_rhs:.0f}) -> {'PASS [6 = 6]' if np.isclose(eq1_lhs, eq1_rhs) else 'FAIL'}")

    eq2_lhs = 2.0*x + 3.0*y + 1.0*z
    eq2_rhs = 11.0
    print(f"   Eq 2: 2x + 3y + z = 2({x:.0f}) + 3({y:.0f}) + {z:.0f} = {eq2_lhs:.0f} (Expected: {eq2_rhs:.0f}) -> {'PASS [11 = 11]' if np.isclose(eq2_lhs, eq2_rhs) else 'FAIL'}")

    eq3_lhs = 1.0*x + 2.0*y + 3.0*z
    eq3_rhs = 14.0
    print(f"   Eq 3: x + 2y + 3z = {x:.0f} + 2({y:.0f}) + 3({z:.0f}) = {eq3_lhs:.0f} (Expected: {eq3_rhs:.0f}) -> {'PASS [14 = 14]' if np.isclose(eq3_lhs, eq3_rhs) else 'FAIL'}")

    assert np.isclose(eq1_lhs, eq1_rhs) and np.isclose(eq2_lhs, eq2_rhs) and np.isclose(eq3_lhs, eq3_rhs), "Equation check failed!"

    print("\n" + "=" * 70)
    print("ALL MATHEMATICAL VERIFICATION CHECKS PASSED WITH 100% ACCURACY!")
    print("=" * 70)
    return True

if __name__ == "__main__":
    verify()

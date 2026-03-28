import numpy as np

def trimf(x, a, b, c):
    """Triangular membership function"""
    if x <= a or x >= c:
        return 0.0
    elif x == b:
        return 1.0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)

def fuzz_berat(B):
    return {
        'sangat_ringan': trimf(B, 40, 40, 50),
        'rendah': trimf(B, 45, 55, 65),
        'sedang': trimf(B, 60, 75, 90),
        'tinggi': trimf(B, 85, 95, 110),
        'sangat_tinggi': trimf(B, 100, 120, 120)
    }

def fuzz_aktivitas(A):
    return {
        'sangat_rendah': trimf(A, 0, 0, 2),
        'rendah': trimf(A, 1, 2.5, 4),
        'sedang': trimf(A, 3, 5, 7),
        'tinggi': trimf(A, 6, 8, 9),
        'sangat_tinggi': trimf(A, 8, 10, 10)
    }

# Test
B, A = 40, 3
mu_B = fuzz_berat(B)
mu_A = fuzz_aktivitas(A)

print(f"Input: B={B}, A={A}\n")

print("Membership Berat:")
for k, v in mu_B.items():
    if v > 0:
        print(f"  {k}: {v:.3f}")

print("\nMembership Aktivitas:")
for k, v in mu_A.items():
    if v > 0:
        print(f"  {k}: {v:.3f}")

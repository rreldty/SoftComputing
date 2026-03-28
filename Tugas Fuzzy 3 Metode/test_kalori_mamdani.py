import numpy as np
import matplotlib.pyplot as plt

# ===================== MEMBERSHIP FUNCTION HELPER =====================
def trimf(x, a, b, c):
    """Triangular membership function - handles edge cases"""
    # Handle edge case when a == b (peak at left)
    if a == b:
        if x == a:
            return 1.0
        elif a < x < c:
            return (c - x) / (c - a)
        else:
            return 0.0
    # Handle edge case when b == c (peak at right)
    elif b == c:
        if x == b:
            return 1.0
        elif a < x < b:
            return (x - a) / (b - a)
        else:
            return 0.0
    # Normal triangular case
    else:
        if x <= a or x >= c:
            return 0.0
        elif x == b:
            return 1.0
        elif a < x < b:
            return (x - a) / (b - a)
        else:  # b < x < c
            return (c - x) / (c - b)

# ===================== FUZZY INPUT =====================
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

# ===================== FUZZY OUTPUT =====================
def mf_kalori(K, label):
    if label == 'sangat_rendah':
        return trimf(K, 1500, 1500, 1700)
    elif label == 'rendah':
        return trimf(K, 1600, 1850, 2100)
    elif label == 'sedang':
        return trimf(K, 2000, 2500, 3000)
    elif label == 'tinggi':
        return trimf(K, 2800, 3100, 3300)
    elif label == 'sangat_tinggi':
        return trimf(K, 3200, 3500, 3500)

# ===================== RULES & CONSTANTS =====================
berat_levels = ['sangat_ringan','rendah','sedang','tinggi','sangat_tinggi']
aktivitas_levels = ['sangat_rendah','rendah','sedang','tinggi','sangat_tinggi']
kalori_levels = ['sangat_rendah','rendah','sedang','tinggi','sangat_tinggi']

RULES = []
for i, b in enumerate(berat_levels):
    for j, a in enumerate(aktivitas_levels):
        out_index = min(i+j, 4)
        RULES.append((b, a, kalori_levels[out_index]))

# ===================== MAMDANI DEFUZZIFICATION =====================
def mamdani(B, A):
    """Mamdani inference with centroid defuzzification"""
    mu_B = fuzz_berat(B)
    mu_A = fuzz_aktivitas(A)
    
    r_domain = np.linspace(1500, 3500, 1000)
    aggregated = np.zeros_like(r_domain)
    
    for (b_set, a_set, out_set) in RULES:
        w = min(mu_B[b_set], mu_A[a_set])
        aggregated = np.maximum(aggregated, np.array([min(w, mf_kalori(r, out_set)) for r in r_domain]))
    
    # Centroid defuzzification
    numerator = np.sum(r_domain * aggregated)
    denominator = np.sum(aggregated)
    
    if denominator == 0:
        return 0
    return numerator / denominator

# ===================== INPUT USER =====================
berat_input = float(input("Masukkan berat badan (kg): "))
aktivitas_input = float(input("Masukkan jam aktivitas fisik per hari: "))

# ===================== HITUNG =====================
kalori_result = mamdani(berat_input, aktivitas_input)

print("\nKebutuhan Kalori Harian: {:.2f} kcal".format(kalori_result))

# ===================== GRAFIK =====================
x_berat = np.linspace(40, 120, 500)
x_aktivitas = np.linspace(0, 10, 500)
x_kalori = np.linspace(1500, 3500, 500)
colors = ['#e74c3c','#e67e22','#2ecc71','#3498db','#9b59b6']

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for label, color in zip(berat_levels, colors):
    axes[0].plot(x_berat, [fuzz_berat(x)[label] for x in x_berat], color=color, label=label)
axes[0].set_title('Berat (kg)')
axes[0].set_ylabel('Derajat Keanggotaan')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

for label, color in zip(aktivitas_levels, colors):
    axes[1].plot(x_aktivitas, [fuzz_aktivitas(x)[label] for x in x_aktivitas], color=color, label=label)
axes[1].set_title('Aktivitas Fisik (jam/hari)')
axes[1].set_ylabel('Derajat Keanggotaan')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

for label, color in zip(kalori_levels, colors):
    axes[2].plot(x_kalori, [mf_kalori(x, label) for x in x_kalori], color=color, label=label)
axes[2].axvline(kalori_result, color='red', linestyle='--', linewidth=2, label=f'Hasil: {kalori_result:.0f}')
axes[2].set_title('Kalori (kcal)')
axes[2].set_ylabel('Derajat Keanggotaan')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
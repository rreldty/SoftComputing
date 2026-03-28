import numpy as np
import matplotlib.pyplot as plt

# ===========================
# Membership Function Helper
# ===========================
def trimf(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif x == b:
        return 1.0
    elif a < x < b:
        return (x - a)/(b - a)
    elif b < x < c:
        return (c - x)/(c - b)

def trapmf(x, a, b, c, d):
    if x <= a or x >= d:
        return 0.0
    elif b <= x <= c:
        return 1.0
    elif a < x < b:
        return (x - a)/(b - a)
    elif c < x < d:
        return (d - x)/(d - c)

# ===========================
# Fuzzy Input Membership
# ===========================
def fuzz_berat(B):
    return {
        'Sangat Ringan': trimf(B, 40, 40, 50),      # Peak: 40 kg
        'Rendah'      : trimf(B, 45, 55, 60),      # Peak: 55 kg
        'Sedang'      : trimf(B, 55, 60, 75),      # Peak: 60 kg
        'Tinggi'      : trimf(B, 70, 80, 90),      # Peak: 80 kg
        'Sangat Tinggi': trimf(B, 85, 100, 120)    # Peak: 100 kg
    }

def fuzz_aktivitas(A):
    return {
        'Sangat Rendah': trimf(A, 0, 0, 2),        # Peak: 0 jam
        'Rendah'      : trimf(A, 1, 2.5, 4),      # Peak: 2.5 jam
        'Sedang'      : trimf(A, 3, 5, 7),        # Peak: 5 jam
        'Tinggi'      : trimf(A, 6, 8, 9),        # Peak: 8 jam
        'Sangat Tinggi': trimf(A, 8, 10, 10)      # Peak: 10 jam
    }

# ===========================
# Output Membership Kalori (Mamdani)
# ===========================
def mf_kalori(K, label):
    if label=='Sangat Rendah':
        return trimf(K, 1500, 1500, 1700)
    elif label=='Rendah':
        return trimf(K, 1600, 1850, 2100)
    elif label=='Sedang':
        return trimf(K, 2000, 2500, 3000)
    elif label=='Tinggi':
        return trimf(K, 2800, 3100, 3300)
    elif label=='Sangat Tinggi':
        return trimf(K, 3200, 3500, 3500)

# ===========================
# RULES
# ===========================
berat_levels = ['Sangat Ringan','Rendah','Sedang','Tinggi','Sangat Tinggi']
aktivitas_levels = ['Sangat Rendah','Rendah','Sedang','Tinggi','Sangat Tinggi']
kalori_levels = ['Sangat Rendah','Rendah','Sedang','Tinggi','Sangat Tinggi']

CONST_K = {
    'Sangat Rendah': 1500,
    'Rendah'      : 1850,
    'Sedang'      : 2500,
    'Tinggi'      : 3100,
    'Sangat Tinggi': 3500
}

RULES = []
for i, b in enumerate(berat_levels):
    for j, a in enumerate(aktivitas_levels):
        # Gunakan rata-rata index agar mapping lebih logis
        # Contoh: Sedang(2) + Sedang(2) = 4//2 = 2 → Sedang
        out_index = min((i+j)//2, 4)
        RULES.append( (b, a, kalori_levels[out_index]) )

# ===========================
# Metode MAXq
# ===========================
def metode_max(B, A):
    mu_B = fuzz_berat(B)
    mu_A = fuzz_aktivitas(A)
    best_w = -1
    best_out = None
    best_rule = None
    for (b_set, a_set, out_set) in RULES:
        w = min(mu_B[b_set], mu_A[a_set])
        if w > best_w:
            best_w = w
            best_out = CONST_K[out_set]
            best_rule = (b_set, a_set, out_set)
    return best_out, best_rule

# ===========================
# Metode Sugeno
# ===========================
def metode_sugeno(B, A):
    mu_B = fuzz_berat(B)
    mu_A = fuzz_aktivitas(A)
    numerator = 0.0
    denominator = 0.0
    for (b_set, a_set, out_set) in RULES:
        w = min(mu_B[b_set], mu_A[a_set])
        z = CONST_K[out_set]
        numerator += w * z
        denominator += w
    if denominator==0: return 0
    return numerator/denominator

# ===========================
# Metode Mamdani
# ===========================
def metode_mamdani(B, A):
    mu_B = fuzz_berat(B)
    mu_A = fuzz_aktivitas(A)
    r_domain = np.linspace(1500,3500,1000)
    aggregated = np.zeros_like(r_domain)
    for (b_set, a_set, out_set) in RULES:
        w = min(mu_B[b_set], mu_A[a_set])
        aggregated = np.maximum(aggregated, np.array([min(w, mf_kalori(r,out_set)) for r in r_domain]))
    numerator = np.sum(r_domain * aggregated)
    denominator = np.sum(aggregated)
    if denominator==0: return 0
    return numerator/denominator

# ===========================
# Plot Membership Function
# ===========================
def plot_mf():
    x_berat = np.linspace(40,120,500)
    x_aktivitas = np.linspace(0,10,500)
    x_kalori = np.linspace(1500,3500,500)
    colors = ['#e74c3c','#e67e22','#2ecc71','#3498db','#9b59b6']

    # Grafik Berat
    plt.figure("Berat Badan (kg)")
    for label, color in zip(berat_levels, colors):
        plt.plot(x_berat, [fuzz_berat(x)[label] for x in x_berat], color=color, label=label)
    plt.title('Membership Function – Berat (kg)')
    plt.xlabel("Berat (kg)")
    plt.ylabel("Derajat Keanggotaan")
    plt.grid(True)
    plt.legend()
    
    # Grafik Aktivitas
    plt.figure("Aktivitas Fisik (jam/hari)")
    for label, color in zip(aktivitas_levels, colors):
        plt.plot(x_aktivitas, [fuzz_aktivitas(x)[label] for x in x_aktivitas], color=color, label=label)
    plt.title('Membership Function – Aktivitas (jam/hari)')
    plt.xlabel("Jam Aktivitas / hari")
    plt.ylabel("Derajat Keanggotaan")
    plt.grid(True)
    plt.legend()

    # Grafik Kalori
    plt.figure("Kalori (kcal)")
    for label, color in zip(kalori_levels, colors):
        plt.plot(x_kalori, [mf_kalori(x,label) for x in x_kalori], color=color, label=label)
    plt.title('Membership Function – Kalori (kcal)')
    plt.xlabel("Kalori (kcal)")
    plt.ylabel("Derajat Keanggotaan")
    plt.grid(True)
    plt.legend()

    plt.show(block=False)

# ===========================
# MAIN
# ===========================
if __name__=="__main__":
    print("=== FUZZY KALORI – MAX / SUGENO / MAMDANI ===")
    berat_input = float(input("Masukkan berat badan (kg): "))
    aktivitas_input = float(input("Masukkan jam aktivitas fisik per hari: "))

    # Hitung hasil fuzzy
    max_out, max_rule = metode_max(berat_input, aktivitas_input)
    sugeno_out = metode_sugeno(berat_input, aktivitas_input)
    mamdani_out = metode_mamdani(berat_input, aktivitas_input)

    # Tampilkan grafik dan hasil sekaligus
    plot_mf()

    # langsung print hasil fuzzy tanpa harus menutup grafik
    print("\n=== HASIL FUZZY ===")
    print(f"Max      : {max_out} kcal (Rule: {max_rule[0]} & {max_rule[1]} → {max_rule[2]})")
    print(f"Sugeno   : {sugeno_out:.2f} kcal")
    print(f"Mamdani  : {mamdani_out:.2f} kcal")

    input("\nTekan Enter untuk menutup grafik...")  # supaya user bisa lihat grafik dulu
    plt.close()
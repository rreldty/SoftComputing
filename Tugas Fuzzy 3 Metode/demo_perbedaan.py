from kalori import (fuzz_berat, fuzz_aktivitas, berat_levels, aktivitas_levels, 
                    RULES, CONST_K, metode_max, metode_sugeno, metode_mamdani)

# Contoh input yang akan menunjukkan PERBEDAAN
test_cases = [
    (54, 6, "Input Anda"),
    (57, 3.5, "Fuzzy: Banyak rules berbeda"),  
    (73, 6, "Fuzzy: Sedang-Tinggi"),
    (85, 7, "Fuzzy: Tinggi area"),
]

for berat, aktivitas, desc in test_cases:
    print(f"\n{'='*70}")
    print(f"Test: {desc} (Berat={berat}kg, Aktivitas={aktivitas}jam)")
    print('='*70)
    
    mu_B = fuzz_berat(berat)
    mu_A = fuzz_aktivitas(aktivitas)
    
    # Tampilkan membership yang aktif
    print('Membership Berat:', end='')
    for level in berat_levels:
        if mu_B[level] > 0:
            print(f' {level}={mu_B[level]:.2f}', end='')
    
    print('\nMembership Aktivitas:', end='')
    for level in aktivitas_levels:
        if mu_A[level] > 0:
            print(f' {level}={mu_A[level]:.2f}', end='')
    
    print('\n\nRules Aktif:')
    active_rules = []
    for (b_set, a_set, out_set) in RULES:
        w = min(mu_B[b_set], mu_A[a_set])
        if w > 0:
            z = CONST_K[out_set]
            active_rules.append((w, b_set, a_set, out_set, z))
            print(f'  w={w:.3f}: {b_set:15s} & {a_set:15s} → {out_set:15s} ({z} kcal)')
    
    # Cek output unik
    unique_outputs = set([z for _, _, _, _, z in active_rules])
    
    # Hitung hasil
    max_out, max_rule = metode_max(berat, aktivitas)
    sugeno_out = metode_sugeno(berat, aktivitas)
    mamdani_out = metode_mamdani(berat, aktivitas)
    
    print(f'\n📊 HASIL:')
    print(f'  MAX:     {max_out:.2f} kcal')
    print(f'  SUGENO:  {sugeno_out:.2f} kcal')
    print(f'  MAMDANI: {mamdani_out:.2f} kcal')
    
    # Analisis
    if len(active_rules) == 1:
        print(f'\n  ⚠️  Hanya 1 rule aktif → Semua metode SAMA')
    elif len(unique_outputs) == 1:
        print(f'\n  ⚠️  {len(active_rules)} rules aktif tapi output SAMA → Semua metode SAMA')
    else:
        diff = max(max_out, sugeno_out, mamdani_out) - min(max_out, sugeno_out, mamdani_out)
        print(f'\n  ✅ {len(active_rules)} rules dengan {len(unique_outputs)} output berbeda → PERBEDAAN {diff:.2f} kcal!')

print(f"\n{'='*70}")
print("💡 KESIMPULAN:")
print("="*70)
print("Metode menghasilkan nilai SAMA ketika:")
print("  1. Hanya 1 rule yang aktif")
print("  2. Semua rules aktif punya output konsekuen yang sama")
print("\nUntuk melihat PERBEDAAN, gunakan input yang:")
print("  • Berada di PERBATASAN 2-4 kategori (fuzzy)")
print("  • Mengaktifkan rules dengan konsekuen BERBEDA")
print("  • Contoh: berat=57kg aktivitas=3.5jam atau berat=73kg aktivitas=6jam")

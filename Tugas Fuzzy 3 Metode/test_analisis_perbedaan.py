from kalori import (fuzz_berat, fuzz_aktivitas, berat_levels, aktivitas_levels, 
                    RULES, CONST_K, metode_max, metode_sugeno, metode_mamdani)

# Test dengan input di tengah-tengah kategori
test_cases = [
    (60, 5, "Crisp (tepat di peak)"),
    (57.5, 3.5, "Fuzzy (di antara kategori)"),
    (67, 4, "Fuzzy lainnya"),
]

for berat, aktivitas, desc in test_cases:
    print(f"\n{'='*60}")
    print(f"Input: Berat={berat}kg, Aktivitas={aktivitas}jam ({desc})")
    print('='*60)
    
    mu_B = fuzz_berat(berat)
    mu_A = fuzz_aktivitas(aktivitas)
    
    print('\nDerajat Keanggotaan Berat:')
    for level in berat_levels:
        if mu_B[level] > 0:
            print(f'  {level:15s}: {mu_B[level]:.3f}')
    
    print('\nDerajat Keanggotaan Aktivitas:')
    for level in aktivitas_levels:
        if mu_A[level] > 0:
            print(f'  {level:15s}: {mu_A[level]:.3f}')
    
    print('\nRules yang Aktif (w > 0):')
    active_rules = []
    for (b_set, a_set, out_set) in RULES:
        w = min(mu_B[b_set], mu_A[a_set])
        if w > 0:
            z = CONST_K[out_set]
            active_rules.append((w, b_set, a_set, out_set, z))
    
    for w, b, a, o, z in sorted(active_rules, key=lambda x: -x[0]):
        print(f'  w={w:.3f}: {b:15s} & {a:15s} → {o:15s} (z={z})')
    
    # Hitung hasil
    max_out, max_rule = metode_max(berat, aktivitas)
    sugeno_out = metode_sugeno(berat, aktivitas)
    mamdani_out = metode_mamdani(berat, aktivitas)
    
    print('\n--- HASIL ---')
    print(f'MAX:     {max_out:.2f} kcal')
    print(f'SUGENO:  {sugeno_out:.2f} kcal')
    print(f'MAMDANI: {mamdani_out:.2f} kcal')
    
    if len(active_rules) == 1:
        print('\n⚠️  Hanya 1 rule aktif → MAX dan Sugeno pasti sama!')
    else:
        print(f'\n✓ Ada {len(active_rules)} rules aktif → Metode berbeda!')

print(f"\n{'='*60}")
print("KESIMPULAN:")
print("="*60)
print("MAX = SUGENO terjadi ketika:")
print("1. Hanya ada 1 rule yang aktif (input tepat di peak)")
print("2. Atau semua rules aktif punya output yang sama")
print("\nUntuk melihat PERBEDAAN, gunakan input yang:")
print("- Berada di ANTARA dua kategori (fuzzy)")
print("- Mengaktifkan multiple rules dengan output berbeda")

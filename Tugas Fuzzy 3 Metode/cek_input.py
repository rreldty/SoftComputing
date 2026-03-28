from kalori import fuzz_berat, fuzz_aktivitas, berat_levels, aktivitas_levels, RULES, CONST_K

berat, aktivitas = 54, 6

print(f'=== Analisis Input: Berat={berat}kg, Aktivitas={aktivitas}jam ===')
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

print('\n=== Rules yang Aktif (w > 0) ===')
active_rules = []
for (b_set, a_set, out_set) in RULES:
    w = min(mu_B[b_set], mu_A[a_set])
    if w > 0:
        z = CONST_K[out_set]
        active_rules.append((w, b_set, a_set, out_set, z))
        
for w, b, a, o, z in sorted(active_rules, key=lambda x: -x[0]):
    print(f'  w={w:.3f}: {b:15s} & {a:15s} → {o:15s} (z={z})')

print(f'\nJumlah Rules Aktif: {len(active_rules)}')

# Cek apakah semua output sama
unique_outputs = set([z for _, _, _, _, z in active_rules])
print(f'Output berbeda: {unique_outputs}')

if len(unique_outputs) == 1:
    print(f'\n⚠️  SEMUA {len(active_rules)} RULES MENGHASILKAN OUTPUT YANG SAMA!')
    print(f'    Ketika semua rules mengarah ke output yang sama,')
    print(f'    maka MAX = SUGENO = MAMDANI = {list(unique_outputs)[0]} kcal')
    print(f'\n    Ini karena:')
    print(f'    - MAX: pilih output dengan w terbesar → {list(unique_outputs)[0]}')
    print(f'    - SUGENO: weighted average output yang sama → {list(unique_outputs)[0]}')
    print(f'    - MAMDANI: defuzzifikasi MF yang sama → {list(unique_outputs)[0]}')
elif len(active_rules) == 1:
    print(f'\n⚠️  Hanya 1 rule aktif → MAX dan Sugeno pasti sama!')
else:
    print(f'\n✓ Ada {len(active_rules)} rules dengan output berbeda → Metode akan berbeda!')

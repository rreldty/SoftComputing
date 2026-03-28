import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# INPUT VARIABLES
jarak = ctrl.Antecedent(np.arange(0,101,1),'jarak')
frekuensi = ctrl.Antecedent(np.arange(0,8,1),'frekuensi')

# OUTPUT VARIABLE
vo2max = ctrl.Consequent(np.arange(30,71,1),'vo2max')

# MEMBERSHIP FUNCTION JARAK
jarak['rendah'] = fuzz.trimf(jarak.universe,[0,0,40])
jarak['sedang'] = fuzz.trimf(jarak.universe,[30,50,70])
jarak['tinggi'] = fuzz.trimf(jarak.universe,[60,100,100])

# MEMBERSHIP FUNCTION FREKUENSI
frekuensi['jarang'] = fuzz.trimf(frekuensi.universe,[0,0,3])
frekuensi['normal'] = fuzz.trimf(frekuensi.universe,[2,4,6])
frekuensi['sering'] = fuzz.trimf(frekuensi.universe,[5,7,7])

# MEMBERSHIP FUNCTION VO2MAX
vo2max['rendah'] = fuzz.trimf(vo2max.universe,[30,35,45])
vo2max['sedang'] = fuzz.trimf(vo2max.universe,[40,50,60])
vo2max['tinggi'] = fuzz.trimf(vo2max.universe,[55,65,70])

# RULE BASE
rule1 = ctrl.Rule(jarak['rendah'] & frekuensi['jarang'], vo2max['rendah'])
rule2 = ctrl.Rule(jarak['rendah'] & frekuensi['normal'], vo2max['rendah'])

rule3 = ctrl.Rule(jarak['sedang'] & frekuensi['normal'], vo2max['sedang'])
rule4 = ctrl.Rule(jarak['sedang'] & frekuensi['sering'], vo2max['sedang'])

rule5 = ctrl.Rule(jarak['tinggi'] & frekuensi['normal'], vo2max['tinggi'])
rule6 = ctrl.Rule(jarak['tinggi'] & frekuensi['sering'], vo2max['tinggi'])

# SISTEM FUZZY
system = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6])
sim = ctrl.ControlSystemSimulation(system)

# INPUT USER
jarak_input = float(input("Masukkan jarak latihan per minggu (km): "))
frekuensi_input = float(input("Masukkan frekuensi latihan per minggu (hari): "))

sim.input['jarak'] = jarak_input
sim.input['frekuensi'] = frekuensi_input

# HITUNG
sim.compute()

print("\nPrediksi VO2max:", sim.output['vo2max'])

# GRAFIK MEMBERSHIP
jarak.view()
frekuensi.view()
vo2max.view()

plt.show()
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# INPUT
vo2max = ctrl.Antecedent(np.arange(30,71,1),'vo2max')
jarak = ctrl.Antecedent(np.arange(0,101,1),'jarak')

# OUTPUT
pace = ctrl.Consequent(np.arange(3,9,0.1),'pace')

# MEMBERSHIP VO2MAX
vo2max['rendah'] = fuzz.trimf(vo2max.universe,[30,30,45])
vo2max['sedang'] = fuzz.trimf(vo2max.universe,[40,50,60])
vo2max['tinggi'] = fuzz.trimf(vo2max.universe,[55,70,70])

# MEMBERSHIP JARAK
jarak['sedikit'] = fuzz.trimf(jarak.universe,[0,0,40])
jarak['sedang'] = fuzz.trimf(jarak.universe,[30,50,70])
jarak['banyak'] = fuzz.trimf(jarak.universe,[60,100,100])

# MEMBERSHIP PACE
pace['lambat'] = fuzz.trimf(pace.universe,[6,7,8])
pace['sedang'] = fuzz.trimf(pace.universe,[5,6,7])
pace['cepat'] = fuzz.trimf(pace.universe,[4,5,6])
pace['sangat_cepat'] = fuzz.trimf(pace.universe,[3,4,5])

# RULE
rule1 = ctrl.Rule(vo2max['rendah'] & jarak['sedikit'], pace['lambat'])
rule2 = ctrl.Rule(vo2max['sedang'] & jarak['sedang'], pace['sedang'])
rule3 = ctrl.Rule(vo2max['tinggi'] & jarak['banyak'], pace['sangat_cepat'])
rule4 = ctrl.Rule(vo2max['tinggi'] & jarak['sedang'], pace['cepat'])
rule5 = ctrl.Rule(vo2max['sedang'] & jarak['banyak'], pace['cepat'])

# SYSTEM
system = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5])
sim = ctrl.ControlSystemSimulation(system)

# INPUT USER
vo2_input = float(input("Masukkan VO2max: "))
jarak_input = float(input("Masukkan jarak latihan mingguan (km): "))

sim.input['vo2max'] = vo2_input
sim.input['jarak'] = jarak_input

# HITUNG
sim.compute()

print("\nPrediksi Pace Half Marathon:", round(sim.output['pace'],2), "menit/km")

# GRAFIK
vo2max.view()
jarak.view()
pace.view()

plt.show()
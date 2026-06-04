import micropython
from pyb import ADC, Pin, Timer
from time import ticks_ms, ticks_diff

micropython.alloc_emergency_exception_buf(100)

VREF = 3.3
RES = 4095

adc = ADC(Pin('A0'))

N = 100             # Nombre total de mesures
count = 0           # Compteur de mesures
t0 = ticks_ms()

# Variables partagées ISR <-> tâche planifiée
last_raw = 0
last_dt_ms = 0

# Ouverture fichier en global pour pouvoir écrire dedans
f = open('pot.csv', 'w')
f.write('t_ms,voltage\n')

def process(_):
    global count, last_raw, last_dt_ms, f
    voltage = (last_raw * VREF) / RES
    dt = last_dt_ms
    f.write('%d, %.4f\n' % (dt, voltage))
    count += 1
    if count >= N:
        f.close()
        print("Mesures enregistrées dans pot.csv")
        # On peut arrêter le timer ici si besoin
        tim.deinit()

def handler(timer):
    global last_raw, last_dt_ms
    last_raw = adc.read()
    last_dt_ms = ticks_diff(ticks_ms(), t0)
    micropython.schedule(process, 0)

tim = Timer(2, freq=10)  # Timer à 10 Hz (ajuste la fréquence selon besoin)
tim.callback(handler)

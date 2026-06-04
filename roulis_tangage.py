from machine import I2C
import time
from math import sqrt, atan2, degrees
import moduleimu as imu

# Initialisation de l'I2C
i2c = I2C(1)
imu.init_LSM6DSO16IS(i2c)

# --- Offsets de l'accéléromètre ---
offset_A = [0.02935869, -0.03289181, 1.005599]

# Boucle de lecture
N = 1000
for _ in range(N):
    # Lecture et correction des mesures
    ax, ay, az = imu.lire_acceleration(i2c)
    ax_corr = ax - offset_A[0]
    ay_corr = ay - offset_A[1]
    az_corr = az - 0.005599

    # --- Calcul du roulis (alpha) et tangage (beta) ---
    alpha =degrees(-atan2(ay_corr, az_corr))             # roulis
    beta = degrees(atan2(ax_corr, sqrt(ax_corr**2 +ay_corr**2 + az_corr**2)))  # tangage
  
    #beta = degrees(atan2(ax_corr, az_corr))
    

    # Affichage
    print("Roulis α = %.2f° | Tangage β = %.2f°" % (alpha, beta))
    
    time.sleep_ms(500)

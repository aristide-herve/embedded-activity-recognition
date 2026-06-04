from machine import I2C, Pin
import time
from pyb import LED
from math import sqrt, atan2, degrees, radians, cos, sin
import moduleimu as imu

# --- Initialisation I2C et capteurs ---
i2c = I2C(1)
imu.init_LIS2MDL(i2c)
imu.init_LSM6DSO16IS(i2c)

# --- LED pour signaler horizontalité (facultatif ici) ---
ledG = LED(2) 

# --- Offsets connus ---
offset_A = [0.02935869, -0.03289181, 1.005599]

# --- Offsets Hard-Iron  ---
Bx_c = 0.00   # exemple
By_c =  0.00  # exemple

print("➡️ Boussole avec compensation d'inclinaison démarrée...")

while True:
    # --- Lecture accéléromètre et correction ---
    ax, ay, az = imu.lire_acceleration(i2c)
    ax  = ax-offset_A[0]
    ay  = ay-offset_A[1]
    az  = az-.005599

    # --- Calcul du roulis (alpha) et du tangage (beta) ---
    alpha = atan2(ay, az)
    beta = atan2(ax, sqrt(ax**2 + ay**2 + az**2))

    # --- Lecture magnétomètre et correction hard-iron ---
    bx, by, bz = imu.lire_magnetometre(i2c)
    
    #bx -= Bx_c
    #by -= By_c

    # --- Compensation de l’inclinaison ---
    BxT = bx * cos(beta) + bz * sin(beta)
    ByT = bx * sin(alpha) * sin(beta) + by * cos(alpha) - bz * sin(alpha) * cos(beta)

    # --- Calcul de l’azimut corrigé ---
    theta = degrees(atan2(ByT, BxT))
    if theta < 0:
        theta += 360

    # --- LED ON si proche de l’horizontale (optionnel) ---
    if (-10 < degrees(alpha) < 10 and -10 < degrees(beta) < 10) : 

        ledG.on()
    else : 
        ledG.off()

    # --- Affichage ---
    print("α=%.2f° β=%.2f° | θ_compensé=%.2f°" % (degrees(alpha), degrees(beta), theta))

    time.sleep(1)

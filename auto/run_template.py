from os import times

import matplotlib.pyplot as plt
import numpy as np
from pid_template import make_car
from pid_template import update
from pid_template import calculate_desired_acceleration
from pid_template import acceleration_to_throttle_percentage
from pid_tuner import tune, plot_pid

# K_P = 0.07
# K_I = 0.05
# K_D = 0

STEPS = 550

#WRITE CODE HERE

best = tune(
    K_P_range=np.arange(0.2, 3.01, 0.2),
    K_I_range=np.arange(0.0, 2.01, 0.1),
    K_D_range=[0.0, 0.05, 0.1, 0.2],
    TARGET_RANGE=[20, 30, 40, 50],
)

plot_pid(K_P=best[0], K_I=best[1], K_D=best[2], STEPS=STEPS)

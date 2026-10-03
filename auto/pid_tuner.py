
import matplotlib.pyplot as plt

from pid_template import acceleration_to_throttle_percentage
from pid_template import calculate_desired_acceleration
from pid_template import make_car
from pid_template import update


def score_pid(K_P, K_I, K_D, target=20.0, STEPS=550):
    car = make_car(desired_v=target, dt=0.1)
    cost = 0
    for i in range(STEPS):
        a_d, err = calculate_desired_acceleration(car, K_P, K_I, K_D)
        throttle = acceleration_to_throttle_percentage(a_d)
        update(car, throttle)
        cost += car["t"] * abs(err) * car['dt']
    return cost

def tune(K_P_range, K_I_range, K_D_range, TARGET_RANGE):
    best_cost = float('inf')
    best_params = (0, 0, 0)
    for K_P in K_P_range:
        for K_I in K_I_range:
            for K_D in K_D_range:
                cost = 0
                for target in TARGET_RANGE:
                    cost += score_pid(K_P, K_I, K_D, target=target)
                if cost < best_cost:
                    best_cost = cost
                    best_params = (K_P, K_I, K_D)
    return best_params

def plot_pid(K_P, K_I, K_D, target=20.0, STEPS=550):
    car = make_car(desired_v=target, dt=0.1)
    velocities = []
    errors = []
    times = []
    for i in range(STEPS):
        a_d, err = calculate_desired_acceleration(car, K_P, K_I, K_D)
        throttle = acceleration_to_throttle_percentage(a_d)
        update(car, throttle)
        velocities.append(car['v'])
        errors.append(err)
        times.append(car['t'])

    # Velocity graph

    plt.figure()
    plt.plot(times, velocities, label="Velocity")
    plt.axhline(car["desired_v"], color="red", linestyle="--", label="Target")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.title(f"Velocity vs Time with K_P={K_P:.2f}, K_I={K_I:.2f}, K_D={K_D:.2f}")
    plt.legend()
    plt.show()

    # # Error graph
    # plt.figure()
    # plt.plot(times, errors, label="Error")
    # plt.axhline(0, color="red", linestyle="--", label="Target (0 error)")
    # plt.xlabel("Time (s)")
    # plt.ylabel("Error (m/s)")
    # plt.title(f"Error vs Time with K_P={K_P}, K_I={K_I}, K_D={K_D}")
    # plt.legend()
    # plt.show()
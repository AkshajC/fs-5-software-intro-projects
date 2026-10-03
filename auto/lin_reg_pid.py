"""
Optional ML extension: learn the PID controller with linear regression.

Goal: given (current velocity, desired velocity), predict the desired
acceleration the PID controller would output.

Pipeline (same shape as learnpytorch.io sections 00 and 01):
    1. Generate data by running the PID simulation
    2. Turn it into tensors and split into train / test
    3. Build a model (nn.Linear)
    4. Training loop: forward -> loss -> zero_grad -> backward -> step
    5. Evaluate on unseen targets and plot
"""

import matplotlib.pyplot as plt
import torch
from torch import nn

from pid_template import (
    acceleration_to_throttle_percentage,
    calculate_desired_acceleration,
    make_car,
    update,
)

torch.manual_seed(42)

STEPS = 550
TRAIN_TARGETS = [10, 15, 20, 25, 35, 40, 45, 55]
TEST_TARGETS = [30, 50]   # never seen during training


# ---------------------------------------------------------------------------
# 1. Data
# ---------------------------------------------------------------------------
def generate_data(K_P, K_I, K_D, targets, use_integral=False):
    
    X, y, run_ids = [], [], []
    for run, target in enumerate(targets):
        car = make_car(desired_v=target, dt=0.1)
        for _ in range(STEPS):
            features = [car["v"], car["desired_v"]]
            a_d, _ = calculate_desired_acceleration(car, K_P, K_I, K_D)

            if use_integral:
                features.append(car["net_integral"])

            X.append(features)
            y.append([a_d])
            run_ids.append(run)
            update(car, acceleration_to_throttle_percentage(a_d))

    return (torch.tensor(X, dtype=torch.float32),
            torch.tensor(y, dtype=torch.float32),
            torch.tensor(run_ids))


# ---------------------------------------------------------------------------
# 3. Model
# ---------------------------------------------------------------------------
class LinearRegressionModel(nn.Module):
    def __init__(self, n_features):
        super().__init__()
        self.linear = nn.Linear(in_features=n_features, out_features=1)

    def forward(self, x):
        return self.linear(x)


# ---------------------------------------------------------------------------
# 4. Training
# ---------------------------------------------------------------------------
def train(X_train, y_train, X_test, y_test, epochs=2000, lr=0.05):
    #standardize the featues so 1 learning rate is good 
    mean, std = X_train.mean(dim=0), X_train.std(dim=0)
    #in case Null values
    std[std == 0] = 1.0

    model = LinearRegressionModel(X_train.shape[1])
    loss_fn = nn.MSELoss() # MSE better than L1 because big misses should be punished harder
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)

    train_losses, test_losses = [], []
    for epoch in range(epochs):
        model.train()
        y_pred = model((X_train - mean) / std)    # forward pass
        loss = loss_fn(y_pred, y_train)           # how wrong are we?
        optimizer.zero_grad()                     # clear old gradients
        loss.backward()                           # compute new gradients
        optimizer.step()                          # nudge the weights

        model.eval()
        with torch.inference_mode():
            test_loss = loss_fn(model((X_test - mean) / std), y_test)
        train_losses.append(loss.item())
        test_losses.append(test_loss.item())

        if epoch % 500 == 0 or epoch == epochs - 1:
            print(f"  epoch {epoch:4d} | train MSE {loss.item():9.4f} | test MSE {test_loss.item():9.4f}")

    # Undo the standardization so the weights are in real units:
    # pred = sum(w * (x - mean) / std) + b  =  sum((w/std) * x) + (b - sum(w*mean/std))
    w = model.linear.weight.detach()[0]
    b = model.linear.bias.detach()[0]
    real_w = w / std
    real_b = b - (w * mean / std).sum()

    predict = lambda X: model((X - mean) / std).detach()
    return predict, real_w, real_b, train_losses, test_losses


def experiment(name, K_P, K_I, K_D, use_integral=False):
    print(f"\n=== {name}: K_P={K_P}, K_I={K_I}, K_D={K_D} | features: "
          f"{'v, desired_v, net_integral' if use_integral else 'v, desired_v'} ===")
    
    X_train, y_train, _ = generate_data(K_P, K_I, K_D, TRAIN_TARGETS, use_integral)
    X_test, y_test, test_runs = generate_data(K_P, K_I, K_D, TEST_TARGETS, use_integral)
    predict, w, b, train_losses, test_losses = train(X_train, y_train, X_test, y_test)

    names = ["v", "desired_v", "net_integral"][: len(w)]
    learned = " ".join(f"{wi:+.3f}*{n}" for wi, n in zip(w.tolist(), names))
    print(f"  learned: a = {learned} {b.item():+.3f}")

    return dict(name=name, X_test=X_test, y_test=y_test, test_runs=test_runs,
                predict=predict, train_losses=train_losses, test_losses=test_losses)


#DELETE LATER TWIN PUT ALL THIS IN an IPYNB so I results can be displayed better
# ---------------------------------------------------------------------------
# 5. Run experiments and plot
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    results = [
        # P-only: a = K_P*(desired_v - v) is exactly linear, so the model
        # should recover weights of -1.8 on v and +1.8 on desired_v.
        experiment("P only", K_P=1.8, K_I=0.0, K_D=0.0),
        # PI: the integral depends on the car's history, which v and
        # desired_v alone don't capture, so the fit can't be perfect.
        experiment("PI, 2 features", K_P=1.8, K_I=1.0, K_D=0.0),
        # Give the model the integral as a third input: now it's linear again.
        experiment("PI, 3 features", K_P=1.8, K_I=1.0, K_D=0.0, use_integral=True),
    ]

    fig, axes = plt.subplots(2, len(results), figsize=(15, 8))
    for col, r in enumerate(results):
        ax = axes[0, col]
        t = torch.arange(STEPS) * 0.1
        for run, target in enumerate(TEST_TARGETS):
            mask = r["test_runs"] == run
            ax.plot(t, r["y_test"][mask], label=f"PID (target {target})")
            ax.plot(t, r["predict"](r["X_test"][mask]), "--", label=f"model (target {target})")
        ax.set_title(r["name"])
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Desired accel (m/s²)")
        ax.set_ylim(-5, 20)
        ax.legend(fontsize=8)

        ax = axes[1, col]
        ax.plot(r["train_losses"], label="train")
        ax.plot(r["test_losses"], label="test")
        ax.set_yscale("log")
        ax.set_xlabel("Epoch")
        ax.set_ylabel("MSE loss")
        ax.legend(fontsize=8)

    plt.tight_layout()
    plt.show()

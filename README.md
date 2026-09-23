# larzscript-lorenz

Deterministic chaos, written entirely in [Larzscript](https://github.com/larz-scripter/larzscript). `lorenz.lz` is one file. In 1963 Edward Lorenz boiled atmospheric convection down to three equations and found that a completely deterministic system can still be impossible to predict for long: nudge the starting point by a hair and the future changes completely. This tool integrates that system, shows the effect, and measures how fast it happens.

```
dx/dt = sigma (y - x)      sigma = 10
dy/dt = x (rho - z) - y    rho   = 28
dz/dt = x y - beta z       beta  = 8/3
```

Fourth-order Runge-Kutta, dt = 0.01, starting from (1, 1, 1).

```
$ larzscript lorenz.lz run
t=0  x=1 y=1 z=1
t=5  x=-6.512 y=-6.9738 z=23.9242
t=10  x=-4.9028 y=-3.7434 z=24.6919
t=15  x=-4.3853 y=-2.0643 z=25.9042
t=20  x=13.4729 y=12.6915 z=34.3921

$ larzscript lorenz.lz diverge
two starts, (1, 1, 1) and (1 + 1e-08, 1, 1)
t=0  separation=1e-08
t=5  separation=1.24531e-08
t=10  separation=1.75773e-08
t=15  separation=2.36724e-07
t=20  separation=1.06825e-05
t=25  separation=0.0032812
t=30  separation=0.242192

$ larzscript lorenz.lz lyapunov
largest Lyapunov exponent over 100 time units: 0.9147 per unit time
nearby states separate like e^(0.9147 t): a factor of e every 1.0932 time units
```

A difference of one part in a hundred million grows to about a quarter of the attractor's size in 30 time units. That is the butterfly effect, measured. Note the shape of it: almost nothing for the first ten units, then exponential growth until the two paths are unrelated.

## Does it check out?

- **The program is right.** `tools/reference.py` is an independent Python implementation of the same integrator. Every number above - the trajectory, the separations and the exponent - matched to the last printed digit before the tests were written.
- **The exponent is in the right place.** The largest Lyapunov exponent of the classic Lorenz system is commonly quoted as about 0.906 per unit time. The estimate depends on how long you average: 0.9147 over 100 time units here, 0.9007 over 400 in the Python reference, settling toward that value as the averaging window grows. Treat the 100-unit figure as good to about two digits, not four.

## Install

You need the [Larzscript](https://github.com/larz-scripter/larzscript) interpreter and the `cli`, `args` and `orbits` packages (`orbits` supplies `ln`):

```
curl -fsSL https://raw.githubusercontent.com/larz-scripter/larzscript/main/install.sh | sh
larzscript pkg install cli
larzscript pkg install args
larzscript pkg install orbits
```

## Commands

| Command | What it does |
|---|---|
| `run [--steps=N] [--every=N]` | Print the trajectory from (1, 1, 1), every `--every` steps (default 2000 steps, every 500). |
| `diverge [--eps=X]` | Run two trajectories `X` apart in x (default 1e-8) and print how far apart they are every 5 time units. |
| `lyapunov [--time=N]` | Estimate the largest Lyapunov exponent over `N` time units (default 100) by two-trajectory renormalisation. |

## Limits

- **One parameter set.** sigma, rho and beta are fixed at the classic values. Chaos in this system depends on them; for rho below about 24 the orbits eventually settle to fixed points instead.
- **One exponent.** Only the largest Lyapunov exponent is measured, by the two-trajectory method, which is simple but noisier than the QR-based method that gets all three.
- **A model, not the atmosphere.** Lorenz's equations are a drastic truncation of convection. The lesson is qualitative: deterministic does not mean predictable.
- **Integration error.** RK4 at dt = 0.01 is accurate here, but any numerical trajectory in a chaotic system is only a shadow of the true one after a few Lyapunov times - which is itself part of the point.

## Tests

```
sh tests/run_tests.sh
```

Set `LZ="larzscript /path/to/lorenz.lz"` to test another copy. CI runs the same suite on every push.

## Licence

MIT (`LICENSE`).

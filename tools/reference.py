#!/usr/bin/env python3
"""Independent Python reference for lorenz.lz (provenance and cross-check).

    python3 tools/reference.py run 2000 500
    python3 tools/reference.py diverge 1e-8
    python3 tools/reference.py lyapunov 200
"""
import math, sys

SIGMA, RHO, BETA, DT = 10.0, 28.0, 8.0 / 3.0, 0.01

def f(s):
    x, y, z = s
    return (SIGMA * (y - x), x * (RHO - z) - y, x * y - BETA * z)

def rk4(s):
    def add(a, b, k): return tuple(ai + k * bi for ai, bi in zip(a, b))
    k1 = f(s); k2 = f(add(s, k1, DT / 2)); k3 = f(add(s, k2, DT / 2)); k4 = f(add(s, k3, DT))
    return tuple(si + DT / 6 * (a + 2 * b + 2 * c + d) for si, a, b, c, d in zip(s, k1, k2, k3, k4))

def dist(a, b): return math.sqrt(sum((p - q) ** 2 for p, q in zip(a, b)))

def run(steps, every):
    s = (1.0, 1.0, 1.0)
    for i in range(steps + 1):
        if i % every == 0: print("t=%.2f  x=%.4f y=%.4f z=%.4f" % (i * DT, *s))
        s = rk4(s)

def diverge(eps):
    a = (1.0, 1.0, 1.0); b = (1.0 + eps, 1.0, 1.0)
    for i in range(3001):
        if i % 500 == 0: print("t=%.0f  separation=%.6g" % (i * DT, dist(a, b)))
        a = rk4(a); b = rk4(b)

def lyapunov(T):
    a = (1.0, 1.0, 1.0)
    for _ in range(1000): a = rk4(a)          # settle onto the attractor
    d0 = 1e-8; b = (a[0] + d0, a[1], a[2]); total = 0.0; n = int(T)
    for _ in range(n):
        for _ in range(100): a = rk4(a); b = rk4(b)
        d = dist(a, b); total += math.log(d / d0)
        b = tuple(ai + (bi - ai) * d0 / d for ai, bi in zip(a, b))
    print("lambda = %.4f" % (total / n))

if __name__ == "__main__":
    c = sys.argv[1]
    if c == "run": run(int(sys.argv[2]), int(sys.argv[3]))
    elif c == "diverge": diverge(float(sys.argv[2]))
    else: lyapunov(float(sys.argv[2]))

#!/usr/bin/env python3
"""Continuation-Passing Style transformation for lambda calculus."""
import sys

class Var:
    def __init__(self, name): self.name = name
    def __repr__(self): return self.name
class Lam:
    def __init__(self, param, body): self.param, self.body = param, body
    def __repr__(self): return f"(λ{self.param}.{self.body})"
class App:
    def __init__(self, fn, arg): self.fn, self.arg = fn, arg
    def __repr__(self): return f"({self.fn} {self.arg})"

_counter = [0]
def fresh(prefix="k"):
    _counter[0] += 1; return f"{prefix}{_counter[0]}"

def cps_transform(expr, k=None):
    if k is None: k = Var("halt")
    if isinstance(expr, Var): return App(k, expr)
    if isinstance(expr, Lam):
        kp = fresh("k")
        body_cps = cps_transform(expr.body, Var(kp))
        return App(k, Lam(expr.param, Lam(kp, body_cps)))
    if isinstance(expr, App):
        f, e = fresh("f"), fresh("e")
        return cps_transform(expr.fn,
            Lam(f, cps_transform(expr.arg,
                Lam(e, App(App(Var(f), Var(e)), k)))))

if __name__ == "__main__":
    _counter[0] = 0
    # (λx.x) y → CPS
    expr = App(Lam("x", Var("x")), Var("y"))
    print(f"Direct: {expr}")
    print(f"CPS:    {cps_transform(expr)}")
    _counter[0] = 0
    # λf.λx.(f x)
    expr2 = Lam("f", Lam("x", App(Var("f"), Var("x"))))
    print(f"\nDirect: {expr2}")
    print(f"CPS:    {cps_transform(expr2)}")

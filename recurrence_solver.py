import math
import re

def _clean(text: str) -> str:
    text = text.lower().replace(" ", "").replace(" ", "")
    text = text.replace("log(n)", "logn").replace("t(", "t(")
    text = text.replace("×", "*")
    return text

def _big_o_power(power: float) -> str:
    rounded = round(power, 3)
    p = str(int(rounded)) if float(rounded).is_integer() else str(rounded)
    return f"O(n^{p})"

def solve_recurrence(raw: str) -> dict:
    """
    Supports common educational recurrence patterns:
      T(n) = aT(n/b) + f(n), for f(n) in {1, log n, n^k, n^k log n}
      T(n) = T(n-c) + f(n), for f(n) in {1, log n, n^k, 2^n}
      Fibonacci-style T(n)=T(n-1)+T(n-2)+1
    This is a pattern-based educational solver, not a general symbolic algebra system.
    """
    r = _clean(raw)
    # The UI shows "T(n) =" as a fixed prefix, so users may enter only the right-hand side.
    if not r.startswith("t(n)="):
        r = "t(n)=" + r

    if r in {
        "t(n)=t(n-1)+t(n-2)+1",
        "t(n)=t(n-2)+t(n-1)+1",
    }:
        return {
            "ok": True,
            "complexity": "O(φ^n) ≈ O(1.618^n)",
            "method": "Fibonacci-style recurrence",
            "explanation": "Each call branches into two smaller calls, T(n−1) and T(n−2). The recursion tree grows exponentially, with growth rate related to the golden ratio φ."
        }

    rhs = r[5:]
    # Match recursive calls and optional leading integer coefficient:
    # 2t(n/2), t(n/3), 3t(n-1)
    pattern = r"(?<![a-z0-9^])(\d*)t\(n(?:/(\d+)|-(\d+))\)"
    calls = list(re.finditer(pattern, rhs))
    if not calls:
        return {"ok": False, "error": "Unsupported recurrence. Try T(n)=2T(n/2)+n or T(n)=T(n-1)+n."}

    # Only support a single consistent recurrence style and identical arguments.
    styles = set()
    divisors = set()
    decreases = set()
    total_a = 0
    for call in calls:
        coeff_text = call.group(1)
        coeff = int(coeff_text) if coeff_text else 1
        if coeff <= 0:
            return {"ok": False, "error": "Recursive-call coefficients must be positive integers."}
        total_a += coeff
        if call.group(2):
            styles.add("divide")
            divisors.add(int(call.group(2)))
        else:
            styles.add("decrease")
            decreases.add(int(call.group(3)))

    if len(styles) != 1:
        return {"ok": False, "error": "Mixed divide-and-conquer and decrease-by-constant calls are not supported."}

    # Remove recursive call tokens from RHS to inspect f(n).
    work = rhs
    for call in reversed(calls):
        work = work[:call.start()] + work[call.end():]
    work = work.strip("+")
    if not work:
        work = "0"

    if styles == {"decrease"}:
        if len(decreases) != 1 or len(calls) != 1:
            return {"ok": False, "error": "For T(n-c), use exactly one recursive call with a single positive constant c."}
        c = next(iter(decreases))
        if c <= 0:
            return {"ok": False, "error": "The decrement c must be positive."}
        if work == "1":
            complexity = "O(n)"
            explanation = "There is one recursive call per level and about n/c levels, with constant work at each level."
        elif work == "logn":
            complexity = "O(n log n)"
            explanation = "There are Θ(n) levels, and each level performs Θ(log n) non-recursive work."
        elif work == "2^n":
            complexity = "O(2^n)"
            explanation = "The added work grows exponentially; the sum 2^n + 2^(n−c) + … is dominated by its first term."
        else:
            m = re.fullmatch(r"n(?:\^(\d+))?", work)
            if not m:
                return {"ok": False, "error": "Unsupported work function for T(n-c). Try +1, +log(n), +n, +n^2, or +2^n."}
            k = int(m.group(1)) if m.group(1) else 1
            complexity = f"O(n^{k + 1})"
            explanation = f"There are Θ(n) levels and Θ(n^{k}) work per level, so summing the work gives Θ(n^{k + 1})."
        return {"ok": True, "complexity": complexity, "method": "Repeated substitution / summation", "explanation": explanation}

    if len(divisors) != 1:
        return {"ok": False, "error": "All recursive calls must use the same divisor, such as T(n/2)."}
    b = next(iter(divisors))
    if b <= 1:
        return {"ok": False, "error": "The divisor b must be greater than 1."}
    if re.search(r"t\(n/", work):
        return {"ok": False, "error": "Could not parse all recursive calls."}

    # Supported f(n): 1, log n, n^k, n^k log n
    if work == "1":
        k, q = 0, 0
    elif work == "logn":
        k, q = 0, 1
    else:
        m = re.fullmatch(r"n(?:\^(\d+))?(logn)?", work)
        if not m:
            return {"ok": False, "error": "Unsupported work function. Try +1, +log(n), +n, +n^2, or +n^2log(n)."}
        k = int(m.group(1)) if m.group(1) else 1
        q = 1 if m.group(2) else 0

    p = math.log(total_a, b)
    eps = 1e-9
    if abs(p - k) < eps:
        log_power = q + 1
        log_part = "" if log_power == 0 else (" log n" if log_power == 1 else f" log^{log_power} n")
        complexity = f"O(n^{k}{log_part})"
        method = "Master Theorem — Case 2"
        explanation = f"a={total_a}, b={b}, so log_b(a)={p:.3f}. Since f(n) matches n^log_b(a) up to a logarithmic factor, the result gains one power of log n."
    elif p > k:
        complexity = _big_o_power(p)
        method = "Master Theorem — Case 1"
        explanation = f"a={total_a}, b={b}, and log_b(a)={p:.3f} > k={k}. The recursive subproblems dominate the non-recursive work."
    else:
        # For the supported polynomial/log forms, the usual regularity condition
        # is met for the standard classroom cases.
        if q == 1:
            complexity = f"O(n^{k} log n)"
        else:
            complexity = f"O(n^{k})"
        method = "Master Theorem — Case 3"
        explanation = f"f(n) grows polynomially faster than n^log_b(a) for this supported pattern, so the non-recursive work dominates (under the Master Theorem regularity condition)."

    return {
        "ok": True,
        "complexity": complexity,
        "method": method,
        "explanation": explanation,
        "details": {"a": total_a, "b": b, "log_b_a": round(p, 3), "work": work}
    }

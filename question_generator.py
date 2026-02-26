"""
question_generator.py — Randomized Question Generator
Grade 5 CA Common Core Math Standards
Generates fresh questions with random numbers each time.
"""

import random
import math


def _shuffle_choices(answer, wrong):
    """Build a shuffled choice list with the correct answer included."""
    choices = [str(answer)] + [str(w) for w in wrong]
    random.shuffle(choices)
    return choices


def _unique_wrong(correct, gen_func, count=3):
    """Generate 'count' unique wrong answers different from correct."""
    wrong = set()
    attempts = 0
    while len(wrong) < count and attempts < 50:
        w = gen_func()
        if w != correct and w not in wrong:
            wrong.add(w)
        attempts += 1
    # Fallback if stuck
    while len(wrong) < count:
        wrong.add(correct + len(wrong) + 1)
    return list(wrong)


# ═══════════════════════════════════════
# CHAPTER: 5.OA — Operations & Algebraic Thinking
# ═══════════════════════════════════════

def _oa_parentheses_eval():
    """Evaluate expression with parentheses: a x (b + c)"""
    a = random.randint(2, 9)
    b = random.randint(1, 12)
    c = random.randint(1, 12)
    ans = a * (b + c)
    wrong = _unique_wrong(ans, lambda: random.randint(2, 9) * random.randint(2, 20))
    return {
        "type": "multiple_choice",
        "question": f"What is {a} x ({b} + {c})?",
        "choices": _shuffle_choices(ans, wrong),
        "answer": str(ans),
    }


def _oa_write_expression():
    """Match a word description to an expression."""
    a = random.randint(2, 9)
    b = random.randint(1, 12)
    c = random.randint(1, 12)
    correct = f"{a} x ({b} + {c})"
    wrong = [
        f"{b} + {c} x {a}",
        f"({a} x {b}) + {c}",
        f"{a} + {b} x {c}",
    ]
    return {
        "type": "multiple_choice",
        "question": f"Which expression means 'add {b} and {c}, then multiply by {a}'?",
        "choices": _shuffle_choices(correct, wrong),
        "answer": correct,
    }


def _oa_prime_factors():
    """Find the prime factorization of a number."""
    composites = {
        12: "2 x 2 x 3", 18: "2 x 3 x 3", 20: "2 x 2 x 5",
        24: "2 x 2 x 2 x 3", 28: "2 x 2 x 7", 30: "2 x 3 x 5",
        36: "2 x 2 x 3 x 3", 40: "2 x 2 x 2 x 5", 42: "2 x 3 x 7",
        45: "3 x 3 x 5", 48: "2 x 2 x 2 x 2 x 3", 50: "2 x 5 x 5",
    }
    num, ans = random.choice(list(composites.items()))
    # Generate plausible wrong answers
    others = [v for k, v in composites.items() if k != num]
    wrong = random.sample(others, min(3, len(others)))
    return {
        "type": "multiple_choice",
        "question": f"What is the prime factorization of {num}?",
        "choices": _shuffle_choices(ans, wrong),
        "answer": ans,
    }


def _oa_is_prime():
    """True/false: is a number prime?"""
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    not_primes = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 25, 26, 27]
    is_prime = random.choice([True, False])
    num = random.choice(primes if is_prime else not_primes)
    return {
        "type": "true_false",
        "question": f"{num} is a prime number.",
        "answer": "True" if is_prime else "False",
    }


def _oa_pattern_rule():
    """Generate two patterns and ask how they relate."""
    base = random.randint(1, 5)
    mult = random.choice([2, 3, 4])
    rule_a = base
    rule_b = base * mult
    terms_a = [i * rule_a for i in range(5)]
    terms_b = [i * rule_b for i in range(5)]
    correct = f"Rule B terms are {mult} times Rule A terms"
    wrong = [
        f"Rule A terms are {mult} times Rule B terms",
        "They are equal",
        f"Rule B terms are {mult + 1} times Rule A terms",
    ]
    return {
        "type": "multiple_choice",
        "question": (f"Rule A: 'Add {rule_a}' from 0 gives {terms_a[:4]}.\n"
                     f"Rule B: 'Add {rule_b}' from 0 gives {terms_b[:4]}.\n"
                     f"How do they compare?"),
        "choices": _shuffle_choices(correct, wrong),
        "answer": correct,
    }


def _oa_bracket_eval():
    """Evaluate nested brackets: a x [b + (c x d)]"""
    a = random.randint(2, 5)
    b = random.randint(1, 8)
    c = random.randint(2, 5)
    d = random.randint(1, 5)
    ans = a * (b + c * d)
    wrong = _unique_wrong(ans, lambda: random.randint(10, 100))
    return {
        "type": "multiple_choice",
        "question": f"What is {a} x [{b} + ({c} x {d})]?",
        "choices": _shuffle_choices(ans, wrong),
        "answer": str(ans),
    }


OA_GENERATORS = [
    _oa_parentheses_eval, _oa_write_expression, _oa_prime_factors,
    _oa_is_prime, _oa_pattern_rule, _oa_bracket_eval,
]


# ═══════════════════════════════════════
# CHAPTER: 5.NBT — Number & Operations in Base Ten
# ═══════════════════════════════════════

def _nbt_place_value():
    """What is the value of a digit in a number?"""
    places = [
        (1, "ones"), (10, "tens"), (100, "hundreds"), (1000, "thousands"),
    ]
    val, name = random.choice(places)
    digit = random.randint(1, 9)
    # Build a number with that digit in that place
    num = digit * val + random.randint(0, val - 1) + random.randint(1, 9) * val * 10
    actual = digit * val
    wrong = _unique_wrong(actual, lambda: random.choice([1, 10, 100, 1000]) * digit)
    return {
        "type": "multiple_choice",
        "question": f"In the number {num:,}, what is the value of the digit {digit} in the {name} place?",
        "choices": _shuffle_choices(actual, wrong),
        "answer": str(actual),
    }


def _nbt_multiply_power10():
    """Multiply a decimal by a power of 10."""
    dec = round(random.uniform(0.5, 9.9), 1)
    power = random.choice([10, 100, 1000])
    ans = round(dec * power, 2)
    # Clean up float display
    ans_str = f"{ans:g}"
    wrong_strs = []
    for _ in range(3):
        w = round(dec * random.choice([10, 100, 1000]), 2)
        ws = f"{w:g}"
        if ws != ans_str and ws not in wrong_strs:
            wrong_strs.append(ws)
    while len(wrong_strs) < 3:
        wrong_strs.append(f"{round(ans * random.uniform(0.1, 10), 1):g}")
    return {
        "type": "multiple_choice",
        "question": f"What is {dec} x {power}?",
        "choices": _shuffle_choices(ans_str, wrong_strs),
        "answer": ans_str,
    }


def _nbt_compare_decimals():
    """Which decimal is greater?"""
    a = round(random.uniform(0.1, 9.9), random.randint(1, 3))
    b = a + round(random.uniform(0.001, 0.1), 3)
    b = round(b, 3)
    if random.choice([True, False]):
        a, b = b, a
    bigger = a if a > b else b
    return {
        "type": "multiple_choice",
        "question": f"Which is greater: {a} or {b}?",
        "choices": _shuffle_choices(str(bigger), [str(min(a, b)), "They are equal"]),
        "answer": str(bigger),
    }


def _nbt_round_decimal():
    """Round a decimal to the nearest tenth."""
    num = round(random.uniform(1.01, 19.99), 2)
    ans = round(num, 1)
    ans_str = f"{ans:.1f}"
    wrong = _unique_wrong(ans_str, lambda: f"{round(num + random.uniform(-0.5, 0.5), 1):.1f}")
    return {
        "type": "multiple_choice",
        "question": f"Round {num} to the nearest tenth.",
        "choices": _shuffle_choices(ans_str, wrong),
        "answer": ans_str,
    }


def _nbt_add_decimals():
    """Add two decimals."""
    a = round(random.uniform(1.0, 30.0), 2)
    b = round(random.uniform(1.0, 20.0), 2)
    ans = round(a + b, 2)
    ans_str = f"{ans:g}"
    wrong = _unique_wrong(ans_str, lambda: f"{round(a + b + random.uniform(-3, 3), 2):g}")
    return {
        "type": "multiple_choice",
        "question": f"What is {a} + {b}?",
        "choices": _shuffle_choices(ans_str, wrong),
        "answer": ans_str,
    }


def _nbt_subtract_decimals():
    """Subtract two decimals."""
    a = round(random.uniform(5.0, 30.0), 2)
    b = round(random.uniform(1.0, a - 0.5), 2)
    ans = round(a - b, 2)
    ans_str = f"{ans:g}"
    wrong = _unique_wrong(ans_str, lambda: f"{round(a - b + random.uniform(-2, 2), 2):g}")
    return {
        "type": "multiple_choice",
        "question": f"What is {a} - {b}?",
        "choices": _shuffle_choices(ans_str, wrong),
        "answer": ans_str,
    }


def _nbt_powers_of_10():
    """What is 10 to a power?"""
    exp = random.randint(1, 5)
    ans = 10 ** exp
    wrong = _unique_wrong(ans, lambda: 10 ** random.randint(1, 5))
    return {
        "type": "multiple_choice",
        "question": f"What is 10 to the power of {exp} (10^{exp})?",
        "choices": _shuffle_choices(f"{ans:,}", [f"{w:,}" for w in wrong]),
        "answer": f"{ans:,}",
    }


def _nbt_place_value_tf():
    """True/false about place value."""
    return {
        "type": "true_false",
        "question": "In a multi-digit number, each place is 10 times the place to its right.",
        "answer": "True",
    }


NBT_GENERATORS = [
    _nbt_place_value, _nbt_multiply_power10, _nbt_compare_decimals,
    _nbt_round_decimal, _nbt_add_decimals, _nbt_subtract_decimals,
    _nbt_powers_of_10, _nbt_place_value_tf,
]


# ═══════════════════════════════════════
# CHAPTER: 5.NF — Fractions
# ═══════════════════════════════════════

def _frac_str(n, d):
    """Simplify and return a fraction string."""
    g = math.gcd(abs(n), abs(d))
    n, d = n // g, d // g
    if d == 1:
        return str(n)
    return f"{n}/{d}"


def _nf_add_fractions():
    """Add two fractions with unlike denominators."""
    d1 = random.choice([2, 3, 4, 5, 6, 8])
    d2 = random.choice([d for d in [2, 3, 4, 5, 6, 8] if d != d1])
    n1 = random.randint(1, d1 - 1)
    n2 = random.randint(1, d2 - 1)
    # Compute answer
    num = n1 * d2 + n2 * d1
    den = d1 * d2
    ans = _frac_str(num, den)
    wrong = _unique_wrong(ans, lambda: _frac_str(
        random.randint(1, 15), random.choice([2, 3, 4, 5, 6, 8, 10, 12])
    ))
    return {
        "type": "multiple_choice",
        "question": f"What is {n1}/{d1} + {n2}/{d2}?",
        "choices": _shuffle_choices(ans, wrong),
        "answer": ans,
    }


def _nf_subtract_fractions():
    """Subtract two fractions."""
    d1 = random.choice([2, 3, 4, 5, 6, 8])
    d2 = random.choice([d for d in [2, 3, 4, 5, 6, 8] if d != d1])
    n1 = random.randint(1, d1 - 1)
    n2 = random.randint(1, d2 - 1)
    num = n1 * d2 - n2 * d1
    den = d1 * d2
    # Make sure positive
    if num <= 0:
        n1, n2 = n2, n1
        d1, d2 = d2, d1
        num = n1 * d2 - n2 * d1
        den = d1 * d2
    if num <= 0:
        return _nf_add_fractions()  # fallback
    ans = _frac_str(num, den)
    wrong = _unique_wrong(ans, lambda: _frac_str(
        random.randint(1, 10), random.choice([2, 3, 4, 5, 6, 8, 10, 12])
    ))
    return {
        "type": "multiple_choice",
        "question": f"What is {n1}/{d1} - {n2}/{d2}?",
        "choices": _shuffle_choices(ans, wrong),
        "answer": ans,
    }


def _nf_multiply_frac_whole():
    """Multiply a fraction by a whole number."""
    d = random.choice([2, 3, 4, 5, 6])
    n = random.randint(1, d - 1)
    w = random.randint(2, 10)
    num = n * w
    ans = _frac_str(num, d)
    wrong = _unique_wrong(ans, lambda: _frac_str(
        random.randint(1, 20), random.choice([1, 2, 3, 4, 5, 6])
    ))
    return {
        "type": "multiple_choice",
        "question": f"What is {n}/{d} x {w}?",
        "choices": _shuffle_choices(ans, wrong),
        "answer": ans,
    }


def _nf_multiply_frac_frac():
    """Multiply two fractions."""
    d1 = random.choice([2, 3, 4, 5])
    d2 = random.choice([2, 3, 4, 5])
    n1 = random.randint(1, d1 - 1)
    n2 = random.randint(1, d2 - 1)
    ans = _frac_str(n1 * n2, d1 * d2)
    wrong = _unique_wrong(ans, lambda: _frac_str(
        random.randint(1, 10), random.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
    ))
    return {
        "type": "multiple_choice",
        "question": f"What is {n1}/{d1} x {n2}/{d2}?",
        "choices": _shuffle_choices(ans, wrong),
        "answer": ans,
    }


def _nf_divide_unit_frac_by_whole():
    """Divide a unit fraction by a whole number."""
    d = random.choice([2, 3, 4, 5, 6])
    w = random.randint(2, 6)
    ans = _frac_str(1, d * w)
    wrong = _unique_wrong(ans, lambda: _frac_str(1, random.randint(2, 36)))
    return {
        "type": "multiple_choice",
        "question": f"What is (1/{d}) divided by {w}?",
        "choices": _shuffle_choices(ans, wrong),
        "answer": ans,
    }


def _nf_divide_whole_by_unit_frac():
    """Divide a whole number by a unit fraction."""
    w = random.randint(2, 8)
    d = random.choice([2, 3, 4, 5, 6])
    ans = w * d
    wrong = _unique_wrong(ans, lambda: random.randint(2, 50))
    return {
        "type": "multiple_choice",
        "question": f"What is {w} divided by (1/{d})?",
        "choices": _shuffle_choices(ans, wrong),
        "answer": str(ans),
    }


def _nf_scaling_tf():
    """True/false about multiplying by fractions."""
    greater = random.choice([True, False])
    if greater:
        n = random.randint(3, 9)
        d = random.randint(2, n - 1)
        return {
            "type": "true_false",
            "question": f"Multiplying a number by {n}/{d} makes it bigger.",
            "answer": "True",
        }
    else:
        d = random.randint(3, 8)
        n = random.randint(1, d - 1)
        return {
            "type": "true_false",
            "question": f"Multiplying a number by {n}/{d} makes it bigger.",
            "answer": "False",
        }


def _nf_fraction_is_division():
    """Fraction as division: a/b = a divided by b."""
    a = random.randint(1, 10)
    b = random.randint(2, 8)
    return {
        "type": "true_false",
        "question": f"{a}/{b} means {a} divided by {b}.",
        "answer": "True",
    }


def _nf_word_problem_share():
    """Word problem: sharing equally."""
    people = random.randint(2, 6)
    d = random.choice([2, 3, 4, 5])
    ans = _frac_str(1, d * people)
    wrong = _unique_wrong(ans, lambda: _frac_str(1, random.randint(2, 30)))
    food = random.choice(["pizza", "candy", "cake", "pie", "chocolate"])
    return {
        "type": "multiple_choice",
        "question": f"If {people} people share 1/{d} pound of {food} equally, how much does each person get?",
        "choices": _shuffle_choices(f"{ans} pound", [f"{w} pound" for w in wrong]),
        "answer": f"{ans} pound",
    }


NF_GENERATORS = [
    _nf_add_fractions, _nf_subtract_fractions, _nf_multiply_frac_whole,
    _nf_multiply_frac_frac, _nf_divide_unit_frac_by_whole,
    _nf_divide_whole_by_unit_frac, _nf_scaling_tf, _nf_fraction_is_division,
    _nf_word_problem_share,
]


# ═══════════════════════════════════════
# CHAPTER: 5.MD — Measurement & Data
# ═══════════════════════════════════════

def _md_unit_conversion():
    """Convert between measurement units."""
    conversions = [
        ("cm", "m", 100, lambda v: f"{v} cm", lambda v: f"{v / 100:g} m"),
        ("m", "cm", 0.01, lambda v: f"{v} m", lambda v: f"{int(v * 100)} cm"),
        ("g", "kg", 1000, lambda v: f"{v:,} g", lambda v: f"{v / 1000:g} kg"),
        ("kg", "g", 0.001, lambda v: f"{v} kg", lambda v: f"{int(v * 1000):,} g"),
        ("mL", "L", 1000, lambda v: f"{v:,} mL", lambda v: f"{v / 1000:g} L"),
        ("ft", "yd", 3, lambda v: f"{v} ft", lambda v: f"{v // 3} yd"),
    ]
    from_u, to_u, factor, fmt_q, fmt_a = random.choice(conversions)
    val = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) * int(max(factor, 1))
    if factor < 1:
        val = random.choice([1, 2, 3, 5, 10])
    q_str = fmt_q(val)
    a_str = fmt_a(val)
    wrong = _unique_wrong(a_str, lambda: fmt_a(
        random.choice([1, 2, 3, 5, 10]) * int(max(factor, 1)) if factor >= 1
        else random.choice([1, 2, 3, 5, 10])
    ))
    return {
        "type": "multiple_choice",
        "question": f"Convert {q_str} to {to_u}.",
        "choices": _shuffle_choices(a_str, wrong),
        "answer": a_str,
    }


def _md_volume_rect_prism():
    """Find volume of a rectangular prism."""
    l = random.randint(2, 10)
    w = random.randint(2, 10)
    h = random.randint(2, 10)
    ans = l * w * h
    unit = random.choice(["cubic cm", "cubic in", "cubic ft"])
    wrong = _unique_wrong(ans, lambda: random.randint(8, 200))
    return {
        "type": "multiple_choice",
        "question": f"A box is {l} x {w} x {h}. What is its volume?",
        "choices": _shuffle_choices(f"{ans} {unit}", [f"{w} {unit}" for w in wrong]),
        "answer": f"{ans} {unit}",
    }


def _md_volume_cube():
    """Volume of a cube."""
    s = random.randint(2, 8)
    ans = s ** 3
    unit = random.choice(["cubic cm", "cubic in", "cubic ft"])
    wrong = _unique_wrong(ans, lambda: random.randint(4, 200))
    return {
        "type": "multiple_choice",
        "question": f"A cube has sides of {s} units. What is its volume?",
        "choices": _shuffle_choices(f"{ans} {unit}", [f"{w} {unit}" for w in wrong]),
        "answer": f"{ans} {unit}",
    }


def _md_volume_base_area():
    """Volume using V = base area x height."""
    base = random.randint(4, 20)
    h = random.randint(2, 10)
    ans = base * h
    unit = random.choice(["cubic cm", "cubic ft", "cubic in"])
    wrong = _unique_wrong(ans, lambda: random.randint(10, 200))
    return {
        "type": "multiple_choice",
        "question": f"A prism has a base area of {base} sq units and height {h}. What is its volume?",
        "choices": _shuffle_choices(f"{ans} {unit}", [f"{w} {unit}" for w in wrong]),
        "answer": f"{ans} {unit}",
    }


def _md_volume_formula():
    """Which formula finds volume?"""
    correct = "V = l x w x h"
    wrong = ["V = l + w + h", "V = l x w", "V = 2(l + w)"]
    return {
        "type": "multiple_choice",
        "question": "Which formula finds the volume of a rectangular prism?",
        "choices": _shuffle_choices(correct, wrong),
        "answer": correct,
    }


def _md_volume_tf():
    """True/false about volume."""
    qs = [
        ("Volume is measured in cubic units.", "True"),
        ("Volume is measured in square units.", "False"),
        ("A unit cube has a volume of 1 cubic unit.", "True"),
        ("You can find the volume of an L-shape by adding volumes of two rectangular prisms.", "True"),
    ]
    q, a = random.choice(qs)
    return {"type": "true_false", "question": q, "answer": a}


def _md_composite_volume():
    """Volume of L-shaped figure (two prisms)."""
    l1, w1, h1 = random.randint(2, 6), random.randint(2, 6), random.randint(2, 6)
    l2, w2, h2 = random.randint(2, 6), random.randint(2, 6), random.randint(2, 6)
    v1, v2 = l1 * w1 * h1, l2 * w2 * h2
    ans = v1 + v2
    wrong = _unique_wrong(ans, lambda: random.randint(20, 300))
    return {
        "type": "multiple_choice",
        "question": (f"An L-shaped solid is made of two boxes:\n"
                     f"Box A: {l1} x {w1} x {h1}\n"
                     f"Box B: {l2} x {w2} x {h2}\n"
                     f"What is the total volume?"),
        "choices": _shuffle_choices(f"{ans} cubic units", [f"{w} cubic units" for w in wrong]),
        "answer": f"{ans} cubic units",
    }


MD_GENERATORS = [
    _md_unit_conversion, _md_volume_rect_prism, _md_volume_cube,
    _md_volume_base_area, _md_volume_formula, _md_volume_tf,
    _md_composite_volume,
]


# ═══════════════════════════════════════
# CHAPTER: 5.G — Geometry
# ═══════════════════════════════════════

def _g_identify_point():
    """What ordered pair is at (x, y)?"""
    x = random.randint(1, 10)
    y = random.randint(1, 10)
    correct = f"({x}, {y})"
    wrong = [f"({y}, {x})", f"({x + 1}, {y - 1})", f"({x}, {x})"]
    return {
        "type": "multiple_choice",
        "question": f"What ordered pair is {x} right and {y} up from the origin?",
        "choices": _shuffle_choices(correct, wrong),
        "answer": correct,
    }


def _g_x_coordinate():
    """How far right/left from origin."""
    x = random.randint(1, 12)
    y = random.randint(1, 12)
    wrong = _unique_wrong(x, lambda: random.randint(1, 12))
    return {
        "type": "multiple_choice",
        "question": f"Point A is at ({x}, {y}). How far right of the origin is it?",
        "choices": _shuffle_choices(f"{x} units", [f"{w} units" for w in wrong]),
        "answer": f"{x} units",
    }


def _g_y_coordinate():
    """Which number tells how far up."""
    x = random.randint(1, 12)
    y = random.randint(1, 12)
    correct = str(y)
    wrong = [str(x), str(x + y), str(abs(x - y))]
    return {
        "type": "multiple_choice",
        "question": f"In the ordered pair ({x}, {y}), which number tells how far UP?",
        "choices": _shuffle_choices(correct, wrong),
        "answer": correct,
    }


def _g_origin():
    """What is (0,0) called?"""
    correct = "The origin"
    wrong = ["The vertex", "The endpoint", "The center"]
    return {
        "type": "multiple_choice",
        "question": "What is the point (0, 0) called on a coordinate plane?",
        "choices": _shuffle_choices(correct, wrong),
        "answer": correct,
    }


def _g_shape_classification_tf():
    """True/false about shape properties."""
    qs = [
        ("A square is always a rectangle.", "True"),
        ("A rectangle is always a square.", "False"),
        ("All rhombuses have 4 equal sides.", "True"),
        ("All rectangles have 4 right angles.", "True"),
        ("A triangle is a quadrilateral.", "False"),
        ("All squares have 4 right angles because they are rectangles.", "True"),
        ("A trapezoid has exactly 2 parallel sides.", "True"),
    ]
    q, a = random.choice(qs)
    return {"type": "true_false", "question": q, "answer": a}


def _g_which_axis():
    """Which axis goes which direction?"""
    horiz = random.choice([True, False])
    if horiz:
        return {
            "type": "multiple_choice",
            "question": "On a coordinate plane, which axis goes left to right?",
            "choices": _shuffle_choices("x-axis", ["y-axis", "z-axis", "origin"]),
            "answer": "x-axis",
        }
    else:
        return {
            "type": "multiple_choice",
            "question": "On a coordinate plane, which axis goes up and down?",
            "choices": _shuffle_choices("y-axis", ["x-axis", "z-axis", "origin"]),
            "answer": "y-axis",
        }


def _g_not_quadrilateral():
    """Which shape is NOT a quadrilateral?"""
    non_quads = ["Triangle", "Circle", "Pentagon", "Hexagon"]
    quads = ["Rectangle", "Square", "Trapezoid", "Rhombus", "Parallelogram"]
    correct = random.choice(non_quads)
    wrong = random.sample(quads, 3)
    return {
        "type": "multiple_choice",
        "question": f"Which of these is NOT a quadrilateral?",
        "choices": _shuffle_choices(correct, wrong),
        "answer": correct,
    }


def _g_shape_properties():
    """Which shape has specific properties?"""
    shapes = [
        ("has exactly 4 right angles and 4 equal sides", "Square",
         ["Trapezoid", "Rhombus", "Triangle"]),
        ("has 4 sides with opposite sides parallel", "Parallelogram",
         ["Triangle", "Pentagon", "Circle"]),
        ("has exactly 3 sides", "Triangle",
         ["Square", "Rectangle", "Pentagon"]),
    ]
    desc, correct, wrong = random.choice(shapes)
    return {
        "type": "multiple_choice",
        "question": f"Which shape {desc}?",
        "choices": _shuffle_choices(correct, wrong),
        "answer": correct,
    }


G_GENERATORS = [
    _g_identify_point, _g_x_coordinate, _g_y_coordinate, _g_origin,
    _g_shape_classification_tf, _g_which_axis, _g_not_quadrilateral,
    _g_shape_properties,
]


# ═══════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════

CHAPTER_DEFS = [
    {
        "id": "5OA",
        "title": "Operations & Algebraic Thinking",
        "subtitle": "Expressions, patterns, prime factors",
        "icon": "+-x",
        "generators": OA_GENERATORS,
    },
    {
        "id": "5NBT",
        "title": "Number & Operations in Base Ten",
        "subtitle": "Place value, decimals, multi-digit ops",
        "icon": "123",
        "generators": NBT_GENERATORS,
    },
    {
        "id": "5NF",
        "title": "Number & Operations - Fractions",
        "subtitle": "Add, subtract, multiply & divide fractions",
        "icon": "a/b",
        "generators": NF_GENERATORS,
    },
    {
        "id": "5MD",
        "title": "Measurement & Data",
        "subtitle": "Conversions, volume & line plots",
        "icon": "cm3",
        "generators": MD_GENERATORS,
    },
    {
        "id": "5G",
        "title": "Geometry",
        "subtitle": "Coordinate plane & 2D figures",
        "icon": "XY",
        "generators": G_GENERATORS,
    },
]


def get_chapter_list():
    """Return chapter metadata (without generators) for the UI."""
    return [
        {
            "id": ch["id"],
            "title": ch["title"],
            "subtitle": ch["subtitle"],
            "icon": ch["icon"],
        }
        for ch in CHAPTER_DEFS
    ]


def generate_questions(chapter_id="all", count=10):
    """
    Generate 'count' random questions for the given chapter.
    If chapter_id is 'all', mix questions from every chapter.
    Returns a list of question dicts.
    """
    if chapter_id == "all":
        gens = []
        for ch in CHAPTER_DEFS:
            gens.extend(ch["generators"])
    else:
        gens = []
        for ch in CHAPTER_DEFS:
            if ch["id"] == chapter_id:
                gens = ch["generators"]
                break

    if not gens:
        gens = CHAPTER_DEFS[0]["generators"]

    questions = []
    for i in range(count):
        gen = random.choice(gens)
        try:
            q = gen()
            questions.append(q)
        except Exception as e:
            print(f"[WARN] Question gen failed: {e}")
            # Fallback question
            questions.append({
                "type": "true_false",
                "question": "Is 2 + 2 equal to 4?",
                "answer": "True",
            })
    return questions

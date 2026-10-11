#!/usr/bin/env python3
"""Python mirror of engine.js - regenerates expected.json. Exact float-for-float mirror."""
import json, math, os

def r0(x): return math.floor(x + 0.5)
def r1(x): return math.floor(x * 10 + 0.5) / 10
def r2(x): return math.floor(x * 100 + 0.5) / 100
def jsnum(x):
    if isinstance(x, float) and x == int(x): return int(x)
    return x
def fmt(x): return repr(jsnum(x))
def pos(nums, msg):
    for n in nums:
        if not (n > 0) or n != n or n == float('inf'): return {"error": msg}
    return None

def holdPlan(weightG, absorbX, spillMl):
    bad = pos([weightG, absorbX, spillMl], "weight, absorbency and spill must be positive")
    if bad: return bad
    held = weightG * absorbX
    wrings = math.ceil(spillMl / held)
    return {"heldMl": r0(held), "wrings": wrings}

def replacePlan(swapsWeeks, priceEach):
    bad = pos([swapsWeeks, priceEach], "swap pace and price must be positive")
    if bad: return bad
    perYear = 52 / swapsWeeks
    return {"spongesYear": jsnum(r1(perYear)), "costYear": jsnum(r2(perYear * priceEach))}

def packPlan(packSize, packPrice, swapsWeeks):
    bad = pos([packSize, packPrice, swapsWeeks], "pack size, price and swap pace must be positive")
    if bad: return bad
    perSponge = r2(packPrice / packSize)
    months = r1(packSize / (52 / swapsWeeks) * 12)
    return {"perSponge": jsnum(perSponge), "months": jsnum(months)}

def plural(n, w): return fmt(n) + " " + w + ("" if n == 1 else "s")

def renderHold(r, weightG, absorbX):
    return "A " + fmt(weightG) + " g sponge holds about " + str(r["heldMl"]) + " mL at a labeled " + fmt(absorbX) + "x absorbency - the spill takes " + plural(r["wrings"], "wring") + "."

def renderReplace(r, swapsWeeks):
    return "Swapping every " + plural(swapsWeeks, "week") + " is " + plural(r["spongesYear"], "sponge") + " a year - about " + fmt(r["costYear"]) + " at your price."

def renderPack(r, packSize):
    return "That pack works out to " + fmt(r["perSponge"]) + " a sponge - at your swap pace " + plural(packSize, "sponge") + (" lasts" if packSize == 1 else " last") + " about " + plural(r["months"], "month") + "."

cases = []
hold_args = [(12,8,250),(10,10,200),(15,8,300),(12,8,90),(8,6,150),(14,9,400),
             (12,8,96),(20,12,500),(11,7,180),(13,8,220),(9,5,100),(16,10,350),
             (0,8,250),(12,0,250),(12,8,0)]
for a in hold_args:
    r = holdPlan(*a)
    case = {"fn": "holdPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderHold(r, a[0], a[1])
    cases.append(case)
replace_args = [(2,1.2),(1,0.8),(4,1.5),(2,1),(3,2),(1.5,1.1),(52,1.2),(6,0.9),
                (2.5,1.3),(8,0.75),(1,2.5),(12,1),(0,1.2),(2,0)]
for a in replace_args:
    r = replacePlan(*a)
    case = {"fn": "replacePlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderReplace(r, a[0])
    cases.append(case)
pack_args = [(6,4.5,2),(8,6,2),(4,3,1),(10,8,4),(6,5,2),(12,9,3),(3,2.4,1),
             (1,1.2,2),(24,15,2),(5,4,1.5),(9,6.3,6),(15,10,2),(0,4.5,2),(6,0,2),(6,4.5,0)]
for a in pack_args:
    r = packPlan(*a)
    case = {"fn": "packPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderPack(r, a[0])
    cases.append(case)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expected.json")
with open(out, "w") as f:
    json.dump(cases, f, separators=(",", ":"))
    f.write("\n")
print("wrote", len(cases), "cases")

# Sponge math

How much a sponge actually holds, how many wrings a spill takes, what your swap pace costs per year, and how long a multipack lasts. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/spongemath/

## The three tools

- **Hold plan** - `holdPlan(weightG, absorbX, spillMl)`: mL held and wrings per spill.
- **Replace plan** - `replacePlan(swapsWeeks, priceEach)`: sponges and cost per year.
- **Pack plan** - `packPlan(packSize, packPrice, swapsWeeks)`: price per sponge and months a pack lasts.

## Labeled norms (illustrative references, not rules)

- Absorbency: a cellulose sponge holds about 8 times its own weight; 1 g of water is 1 mL.
- Sponge: 12 g dry. Swap pace: every 2 weeks. Your sponge, spills and standards decide the real numbers.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (44 cases, 116 checks)

Regenerate the oracle expectations: `python3 oracle.py`

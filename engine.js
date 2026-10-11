// Sponge math - pure arithmetic engine, runs in browser and node.
(function(root){
"use strict";
function r0(x){ return Math.round(x); }
function r1(x){ return Math.round(x*10)/10; }
function r2(x){ return Math.round(x*100)/100; }
function pos(nums, msg){
  for (var i=0;i<nums.length;i++){ if (!isFinite(nums[i]) || nums[i] <= 0) return { error: msg }; }
  return null;
}
function holdPlan(weightG, absorbX, spillMl){
  var bad = pos([weightG, absorbX, spillMl], "weight, absorbency and spill must be positive");
  if (bad) return bad;
  var held = weightG * absorbX; // 1 g of water is 1 mL, labeled
  var wrings = Math.ceil(spillMl / held);
  return { heldMl: r0(held), wrings: wrings };
}
function replacePlan(swapsWeeks, priceEach){
  var bad = pos([swapsWeeks, priceEach], "swap pace and price must be positive");
  if (bad) return bad;
  var perYear = 52 / swapsWeeks;
  return { spongesYear: r1(perYear), costYear: r2(perYear * priceEach) };
}
function packPlan(packSize, packPrice, swapsWeeks){
  var bad = pos([packSize, packPrice, swapsWeeks], "pack size, price and swap pace must be positive");
  if (bad) return bad;
  var perSponge = r2(packPrice / packSize);
  var months = r1(packSize / (52 / swapsWeeks) * 12);
  return { perSponge: perSponge, months: months };
}
function plural(n, w){ return n + " " + w + (n === 1 ? "" : "s"); }
function renderHold(r, weightG, absorbX){
  return "A " + weightG + " g sponge holds about " + r.heldMl + " mL at a labeled " + absorbX + "x absorbency - the spill takes " + plural(r.wrings, "wring") + ".";
}
function renderReplace(r, swapsWeeks){
  return "Swapping every " + plural(swapsWeeks, "week") + " is " + plural(r.spongesYear, "sponge") + " a year - about " + r.costYear + " at your price.";
}
function renderPack(r, packSize){
  return "That pack works out to " + r.perSponge + " a sponge - at your swap pace " + plural(packSize, "sponge") + (packSize === 1 ? " lasts" : " last") + " about " + plural(r.months, "month") + ".";
}
var api = { holdPlan: holdPlan, replacePlan: replacePlan, packPlan: packPlan,
  renderHold: renderHold, renderReplace: renderReplace, renderPack: renderPack };
if (typeof module !== "undefined" && module.exports) module.exports = api;
root.SpongeMath = api;
})(typeof window !== "undefined" ? window : globalThis);

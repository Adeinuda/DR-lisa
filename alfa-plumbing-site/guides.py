# -*- coding: utf-8 -*-
"""The 20 published Alfa Plumbing DIY guides. Titles, dates, categories, lead copy and steps are
taken from the live alfaplumbingservices.com posts; wording is tightened, facts are not."""

UP = "https://alfaplumbingservices.com/wp-content/uploads"

GUIDES = [
 dict(
  slug="7-reasons-hot-water-goes-cold-quickly",
  title="7 Reasons Your Hot Water Goes Cold Quickly",
  date="2020-08-15", cat="DIY Tutorial", mins=4,
  img=f"{UP}/2018/04/baytown-tx-water-heater-repair.jpg",
  lede="A short shower is rarely a mystery. Work through these seven causes in order and you will usually land on it in ten minutes.",
  body="""
<h2>The seven usual causes</h2>
<ol class="steps">
<li><b>Burned-out heating element (electric).</b> The lower element does most of the work and dies first. Power off at the breaker, pull the element and check it with a continuity tester — no continuity means replacement.</li>
<li><b>Tank too small for the household.</b> If the shower goes cold the moment someone runs the kitchen tap, the tank is undersized for your demand, not broken.</li>
<li><b>Sediment in the bottom of the tank.</b> A foot of scale insulates the water from the burner or element. It shows up as knocking first, then as a longer recovery time.</li>
<li><b>Broken dip tube (older tanks).</b> Cold inlet water stops rising through the tank and short-circuits straight to the hot outlet. Plastic fragments in your faucet aerators or appliance filters are the tell.</li>
<li><b>Thermostat set too low or failing.</b> We set tanks to 120°F — that is hot enough for the house and low enough to avoid scalds. Test with a thermometer, not by elbow.</li>
<li><b>Gas pilot went out.</b> Relight per the manufacturer's instructions on the control panel. If it will not stay lit, the thermocouple is the $20 part that fixes it.</li>
<li><b>Old, worn tank.</b> Past ten years, a tank that needs both an element and a thermostat is telling you to replace it.</li>
</ol>
<h2>What we check on a diagnostic call</h2>
<p>Age of the unit, the symptoms above, and whether the tank has ever been flushed. If the answer is a repair, we do the repair. If the tank is on borrowed time we say so and quote the replacement in the same visit, so you choose once.</p>""",
  related=[("Water heater repair","water-heaters.html#water-heater-repair")],
 ),
 dict(
  slug="kitchen-sink-leaking-from-drain-5-min-fix",
  title="Kitchen Sink Leaking from the Drain: 5-Minute Fix You Can DIY",
  date="2020-08-13", cat="DIY Tutorial", mins=3,
  img=f"{UP}/2020/08/kitchen-sink-leaking.jpg",
  lede="A wet cabinet with no dripping faucet almost always means the seal between the sink and the drain strainer has let go. One adjustable wrench and plumber's putty will sort it.",
  body="""
<h2>What you need</h2>
<ul class="ticks">
<li>Adjustable wrench</li>
<li>Plumber's putty</li>
<li>New rubber drain gasket</li>
<li>New strainer (worth doing while you are in there)</li>
<li>A pan to catch the water still in the trap</li>
</ul>
<h2>The fix</h2>
<ol class="steps">
<li><b>Clear the cabinet</b> so you have unrestricted access to the drain, and put the pan under the trap.</li>
<li><b>Unthread the slip nuts</b> by hand on modern PVC; if your plumbing predates the upgrade, use the wrench and turn counter-clockwise.</li>
<li><b>Photograph the tailpiece and nuts as they come off</b> so reassembly is obvious — keep the washers in the order they came off.</li>
<li><b>Remove the big locking nut</b> under the sink. A flat-head screwdriver and a tap on the tabs breaks it loose; an adjustable wrench works too.</li>
<li><b>Scrape the old putty off the sink</b> with a paper towel or a scraper, without scratching the surface.</li>
<li><b>Roll a rope of putty</b> and lay it around the strainer flange, then set the strainer in and press until a little squeezes out.</li>
<li><b>Rebuild underneath:</b> paper friction ring, rubber gasket, strainer body, brass nut — hand tight, then a snug with the wrench while you hold the tailpiece so the strainer does not spin.</li>
<li><b>Reconnect the drain pipe,</b> wipe off the excess putty (keep it for the next job), run the water and check for a dry joint.</li>
</ol>
<aside class="tip"><span class="tag-mono">Alfa tip</span><p>If the putty does not stop it, the sink flange itself is cracked or the drain body has a hairline split — that is a strainer replacement, not a reseal.</p></aside>""",
  related=[("Faucet &amp; fixture repair","leaks-gas-repairs.html#faucet-repair")],
 ),
 dict(
  slug="why-is-my-water-bill-so-high",
  title="Why Is My Water Bill So High? 5 Causes and 5 Easy Solutions",
  date="2020-08-12", cat="Plumbing Tips", mins=4,
  img=f"{UP}/2018/04/baytown-tx-plumber-services.jpg",
  lede="A bill that jumps with nothing wet on the floor is nearly always one of these five. Four of them you can confirm yourself before you call anyone.",
  body="""
<h2>The five causes</h2>
<ol class="steps">
<li><b>A faulty flapper valve.</b> The number one cause of a high bill. Sediment gets under the flapper, it stops sealing, and the tank refills all day long. Put a few drops of food colouring in the tank: colour in the bowl within a few minutes means a leak.</li>
<li><b>Fill tube or float set too high.</b> Water spilling into the overflow keeps running silently. On ball-and-arm floats, bend the arm or turn the screw so the level sits about half an inch below the top of the fill tube.</li>
<li><b>Dripping faucets.</b> One drip a second is a surprising amount of water over a month, and it is a washer or cartridge, not a faucet.</li>
<li><b>A change in how you use water.</b> More people home, more laundry, a new habit — check the meter reading against last month before you blame the fixture.</li>
<li><b>An irrigation leak.</b> A zone head that will not seal or a cracked lateral keeps running when nobody is outside. Watch the meter with everything off; if the triangle turns, you have a leak in the house or the yard.</li>
</ol>
<h2>Prove it on the meter first</h2>
<p>Turn every tap and appliance off, then watch the meter's low-flow indicator. If it moves, water is going somewhere it should not — and that is worth a repair call the same week, before the next bill argues about it.</p>
<aside class="tip"><span class="tag-mono">Alfa tip</span><p>Fix the flapper first. It costs a few dollars, takes ten minutes, and it is the single most common thing we find on high-bill calls.</p></aside>""",
  related=[("Toilet repair","leaks-gas-repairs.html#toilet-repair"),("Water leak detection","leaks-gas-repairs.html#water-leak-detection")],
 ),
 dict(
  slug="water-heater-knocking-easy-5-min-fix",
  title="Water Heater Knocking? An Easy 5-Minute Fix",
  date="2020-08-02", cat="Plumbing Tips", mins=4,
  img=f"{UP}/2018/04/baytown-tx-water-heater-replacement.jpg",
  lede="Ninety-nine percent of the time that popping or knocking is water trapped under sediment boiling up through it. Draining the tank fixes it and buys you years of life.",
  body="""
<h2>Why it knocks</h2>
<p>Minerals settle on the bottom of the tank. On a gas unit the burner heats through that layer and steam bubbles form under it; when they break the surface they bang. Electric tanks get the same noise from element efficiency dropping off. Left alone, the deposits hold heat against the steel, corrode the lining and finish as a leak or a burst.</p>
<h2>How to flush it</h2>
<ol class="steps">
<li>Work gloves on. Turn a gas unit to <b>Pilot</b> (or off) — an electric unit to <b>off at the breaker</b>.</li>
<li><b>Close the cold inlet</b> valve on top of the tank.</li>
<li>Let it cool about <b>30 minutes</b> — you are draining near-scalding water.</li>
<li>Run a <b>garden hose to the bottom drain valve</b> and put the other end in a floor drain or outside.</li>
<li><b>Open a hot faucet</b> somewhere in the house to break the vacuum, or nothing will flow.</li>
<li>Open the drain valve with a screwdriver in its slot, and <b>lift the tab on the pressure-relief valve</b> to let air in. Muddy water, then clearer.</li>
<li>Once it slows, <b>crack the cold inlet open</b> to stir and flush the tank until the water runs clear.</li>
<li>Close the drain, remove the hose, refill the tank, and <b>leave a hot tap open until water runs</b> before you restore gas or power — an element fired up dry is a dead element.</li>
</ol>
<h2>How often, and what else helps</h2>
<p>Flush once a year. In our water, a salt-based softener or a filtration system reduces the build-up in the first place.</p>""",
  related=[("Water heater maintenance","water-heaters.html#water-heater-maintenance")],
 ),
 dict(
  slug="septic-tank-services",
  title="Septic Tank Services: What Baytown Homes Off Sewer Need to Know",
  date="2020-08-01", cat="Services", mins=3,
  img=f"{UP}/2018/04/sewer-line-repair-baytown.jpg",
  lede="East of the city sewer line, a septic system is not an option you choose — it is the only option. Which means the maintenance is not optional either.",
  body="""
<h2>Pump it every five years</h2>
<p>Solids that stay in the tank travel out to the drain field and clog it. A pump-out is a modest, scheduled expense; a failed field is an excavation. We pump, inspect the baffles and Tee, and tell you what we saw.</p>
<h2>Signs you are past due</h2>
<ul class="ticks">
<li>Slow drains and gurgling in more than one fixture</li>
<li>Damp or sour-smelling ground over the tank or field</li>
<li>Standing water above the tank after rain</li>
<li>A system that has not been pumped in five years or more</li>
</ul>
<h2>Replacement and permits</h2>
<p>When a system is beyond pumping, the design has to be sized to the soil and the house. Alfa pulls the county permit, installs the system and files the as-built, so the paperwork lands with the property record rather than in a drawer.</p>
<aside class="tip"><span class="tag-mono">Alfa tip</span><p>No bleach tablets or blue deodorizers in the bowl. They eat the rubber in the tank and they kill the bacteria you need out there.</p></aside>""",
  related=[("Septic service","drains-sewer.html#septic-tank-services")],
 ),
 dict(
  slug="baytown-tankless-water-heater",
  title="Baytown Tankless Water Heaters: Is On-Demand Right for Your House?",
  date="2020-07-31", cat="Plumbing Tips", mins=3,
  img=f"{UP}/2018/04/baytown-tx-plumber-services.jpg",
  lede="Since 2003 the case we have made to Baytown households for tankless is simple: you stop running out of hot water, and you stop paying to keep 50 gallons hot all night.",
  body="""
<h2>What it does well</h2>
<ul class="ticks">
<li><b>Endless hot water on demand</b> — no capacity limit, so a big family's evening stops being a queue.</li>
<li><b>Efficiency.</b> Energy Star models cut standby loss; the savings show on the gas bill rather than the invoice.</li>
<li><b>Space.</b> Wall-hung, the size of a carry-on suitcase, in the closet where a tank would not fit.</li>
<li><b>Life.</b> A serviced unit outlives a tank, and the heat exchanger is usually the warrantable part.</li>
</ul>
<h2>What it costs and what it needs</h2>
<p>Baytown averages run from about <b>$1,000 for an electric point-of-use</b> to <b>$3,000 for a whole-house gas install</b>, unit included. Gas retrofits need the right vent material and often a heavier gas line — that is why we quote a walk-through, not a phone number. Whole-home systems also want soft water and an annual descale, or the heat exchanger silts up exactly like a tank would.</p>
<h2>When we would not sell it to you</h2>
<p>If two bathrooms never run at once and the existing tank is five years old, a tankless conversion is money spent for elegance, not need. We say that out loud on the estimate.</p>""",
  related=[("Tankless installs","water-heaters.html#tankless-water-heaters")],
 ),
 dict(
  slug="plumbing-101-diy-10-quick-fixes",
  title="Plumbing 101: DIY Repairs — 10 Quick Fixes That Save You a Service Call",
  date="2020-07-30", cat="Plumbing Tips", mins=5,
  img=f"{UP}/2018/11/ed35b70628f21c22d2524518b7494097e377ffd41cb5134697f6c67ea2_640.jpg",
  lede="As a master plumber I get called out to fix things most people can do themselves. Here are the ten that save around $150 a visit.",
  body="""
<h2>The ten</h2>
<ol class="steps">
<li><b>Re-caulk around a sink or tub.</b> Scrape out the cracked bead with a utility knife and a chisel, clean it, then run a fresh bead from a caulking gun with the tip cut at 45° and smooth it with a wet finger. Let it cure a few hours.</li>
<li><b>Replace a leaky shower head.</b> Usually one nut. Stuck? Vice grips or a pipe wrench, and new tape on the threads.</li>
<li><b>Fix a leaky faucet.</b> Drip from the spout or leak at the base — cartridge, washer or O-ring. See our Delta faucet walkthrough.</li>
<li><b>Install a new bathroom faucet.</b> Shut the supply under the cabinet, unscrew the supply lines with channel locks, drop the old faucet out, reverse the steps.</li>
<li><b>Stop a running toilet.</b> Nine times in ten it is a worn flapper; the other one is a float set too high.</li>
<li><b>Chase a water-pressure problem from the bottom up.</b> Mineral build-up is the usual cause — start at the fixture aerators and work back to the shut-off.</li>
<li><b>Replace washing machine hoses.</b> Rubber hoses swell and burst. Braided steel, changed every few years, is the cheapest insurance in the house.</li>
<li><b>Unclog a drain.</b> Plunger first, hand auger second. Skip the chemical openers.</li>
<li><b>Get the garbage disposal working again.</b> Press the reset button on the bottom, then clear a jam with an Allen key in the shaft — after the switch is off.</li>
<li><b>Change a bathtub spout.</b> Most unscrew by hand with a rag for grip; a stuck one gets a wrench on the flats, padded.</li>
</ol>
<aside class="tip"><span class="tag-mono">Where the DIY stops</span><p>If re-caulking does not stop the leak, if the pressure problem is whole-house, or if the job needs a new line inside a wall or slab — that is licensed work. A repipe is never a DIY project.</p></aside>""",
  related=[("Faucet repair","leaks-gas-repairs.html#faucet-repair"),("Drain cleaning","drains-sewer.html#drain-cleaning")],
 ),
 dict(
  slug="professional-plumbing-services-10-tips-hiring-local",
  title="Professional Plumbing Services: 10 Tips for Hiring Local",
  date="2020-07-25", cat="Plumbing Tips", mins=4,
  img=f"{UP}/2018/04/baytown-tx-plumber-team.jpg",
  lede="Hiring is hardest when the ceiling is wet and you have ten minutes. These are the ten checks we would want a customer to run on anyone — including us.",
  body="""
<h2>The ten checks</h2>
<ul class="ticks">
<li><b>Licensed and insured.</b> Ask for the Texas Master Plumber licence and the certificate of insurance, not a promise.</li>
<li><b>Local.</b> A company with a shop in Baytown is the one that will answer when the repair needs warranty work in November.</li>
<li><b>Written estimate before work starts.</b> We price repipes, remodels, sewer repairs and water heater replacements on a free walk-through.</li>
<li><b>Diagnosis first, parts second.</b> Anyone replacing a water heater before they have looked at the flapper, breaker or pilot is guessing.</li>
<li><b>Camera before concrete.</b> Sewer and underground water line work should start with a camera or an electronic trace, not with a backhoe in your yard.</li>
<li><b>Permits in writing.</b> Septic replacement and sewer work need county permits and as-builts. The one who pulls them is the one accountable for the installation.</li>
<li><b>Know the warranty.</b> Parts come from the manufacturer; workmanship should be guaranteed by the plumber who did it.</li>
<li><b>Ask what else they saw.</b> A plumber under your sink who notices a sweating tank or an unvalved joint is worth more than one who does not.</li>
<li><b>Emergency availability.</b> Confirm a 24-hour number before you need it, and text is fine.</li>
<li><b>Reviews with names and jobs in them.</b> Judge the pattern of what the work was, not the star.</li>
</ul>""",
  related=[("Reviews","reviews.html"),("Service areas","service-areas.html")],
 ),
 dict(
  slug="how-to-fix-your-toilet-from-running",
  title="How to Fix Your Toilet from Running: 3 Fixes for 3 Situations",
  date="2020-06-20", cat="Plumbing Tips", mins=4,
  img=f"{UP}/2020/06/stopper-valve.jpg",
  lede="A running toilet can cost hundreds on your water bill and the fix usually costs under ten dollars. All you need is a flat-head screwdriver, pliers and ten minutes.",
  body="""
<h2>Situation 1 — the flapper</h2>
<ol class="steps">
<li>Shut the water off at the wall — follow the supply line and turn the knob clockwise.</li>
<li>Before you flush, <b>press down on the centre of the stopper</b>. If the running stops, the flapper is your problem.</li>
<li>Flush to empty the tank, unclip the chain from the lever and lift the stopper off its two side posts.</li>
<li>Take the old stopper to the store and match it. Reinstall the new one the way it came off, turn the water back on counter-clockwise, done.</li>
</ol>
<h2>Situation 2 — water running over the fill tube</h2>
<p>Look at the overflow tube. If water is spilling into it, the level is set too high. Turn the adjustment screw counter-clockwise to lower the float (clockwise to raise) until the water sits about <b>half an inch below the top of the fill tube</b>. On the old ball-on-a-metal-rod valves it is the same idea — bend or screw the arm down.</p>
<h2>Situation 3 — a push-button cistern</h2>
<p>Take the lid off and confirm nothing is running over the fill tube; adjust the screw if it is. Otherwise, grab the cylinder under the two buttons, give it a quarter turn clockwise and pull it out. On the bottom is a rubber gasket: take it off, flip it around and refit it — that alone stops most push-button leaks.</p>""",
  related=[("Toilet repair","leaks-gas-repairs.html#toilet-repair")],
 ),
 dict(
  slug="why-do-i-run-out-of-hot-water-so-fast",
  title="Why Do I Run Out of Hot Water So Fast?",
  date="2019-05-07", cat="Plumbing Tips", mins=3,
  img=f"{UP}/2018/04/baytown-tx-water-heater-repair.jpg",
  lede="Five to ten minutes of hot water and then cold is one of the most common calls we take, and it is almost never the water utility's fault.",
  body="""
<h2>What we find</h2>
<ul class="ticks">
<li><b>A crossed-over or failing dip tube.</b> Cold inlet water shoots straight to the hot outlet, so the tank reads full but delivers lukewarm and short showers.</li>
<li><b>The lower element burned out (electric).</b> Only the top element works, so you get a few gallons of hot and then cold.</li>
<li><b>Sediment.</b> A tank half full of scale only has half the capacity it was rated for, and the recovery time stretches.</li>
<li><b>Thermostat set too low</b> or a tankless unit whose flow is above its temperature-rise rating — in Texas winter that alone will make a 9-minute shower into a 3-minute one.</li>
<li><b>Demand genuinely bigger than the tank.</b> Two bathrooms and a kitchen running at 6pm on a 40-gallon tank is not a fault, it is sizing.</li>
</ul>
<h2>Try this before you call</h2>
<p>Time a hot shower with everything else off, then repeat with the kitchen tap running. If it goes from eight minutes to three, you have a capacity or short-circuit problem rather than a broken part — and the answer is usually a flush, an element, or a bigger tank or tankless unit.</p>""",
  related=[("Water heater repair","water-heaters.html#water-heater-repair"),("7 reasons hot water goes cold","7-reasons-hot-water-goes-cold-quickly.html")],
 ),
 dict(
  slug="how-to-apply-teflon-tape",
  title="How to Apply Teflon Tape Correctly",
  date="2019-05-03", cat="Plumbing Tips", mins=4,
  img=f"{UP}/2020/07/Plumbers-putty-1024x576.jpg",
  lede="Tape applied the wrong way leaks and breaks valves. Three turns the right direction beats ten the wrong one — and the colour matters more than most people think.",
  body="""
<h2>Pick the right tape</h2>
<ul class="ticks">
<li><b>White</b> — standard PTFE for NPT water and air threads up to 3/8".</li>
<li><b>Yellow</b> — gas threads, 1/2" to 2". Use this on any gas fitting, never white.</li>
<li><b>Pink</b> — heavier weight for potable water pipe.</li>
<li><b>Green</b> — oil-free and oxygen service.</li>
<li><b>Grey</b> — nickel anti-seize, for stainless that wants to gall and seize.</li>
<li><b>Copper</b> — an anti-seize lubricant, not a thread sealant.</li>
<li><b>Blue</b> — thicker general-purpose PTFE.</li>
</ul>
<h2>How to wrap it</h2>
<ol class="steps">
<li>Start at the <b>edge of the pipe</b>, holding the tape snug and keeping light tension.</li>
<li>Wrap <b>clockwise</b> — the same direction the fitting tightens. Counter-clockwise wrapping unrolls itself into the joint.</li>
<li>Wrap only to the <b>first thread</b>, so no tape goes past the end where it can break off and plug a valve.</li>
<li><b>Three turns</b> is right on most residential water joints. Never more than six. Gas, oxygen and steam systems follow their own code requirements — check before you wrap.</li>
<li>Press the wrapped threads with a finger so the tape conforms, make up the joint tight, then <b>test with water before you close the wall up</b>.</li>
</ol>
<h2>Why tape fails</h2>
<p>PTFE seals by filling the gap between mating threads; it needs a connector that actually pulls tight to work. Loose or cross-threaded joints leak no matter how much tape is on them. The tape itself is a wide-band material — good from roughly -450°F to +500°F. US military specs are MIL-T-27730A (at least 3.5 mil thick, 99% PTFE) and A-A-58092, which adds a density requirement of at least 1.2 g/cm³.</p>""",
  related=[("Gas line repair","leaks-gas-repairs.html#gas-line-repair")],
 ),
 dict(
  slug="how-to-fix-a-leaky-faucet",
  title="How to Fix a Leaky Faucet (Delta Single-Handle Valve in 10 Steps)",
  date="2018-12-23", cat="DIY Tutorial", mins=5,
  img=f"{UP}/2018/09/shutterstock_143795752-1024x599.jpg",
  lede="The ball-type Delta single valve leaks for one of two reasons: the rubber seats and springs are worn, or the cam assembly is. The kit is three to five dollars at any hardware store — in the faucet aisle, not the toilet aisle.",
  body="""
<h2>Before you start</h2>
<p>Buy a <b>Delta repair kit</b> for the faucet (seats, springs, O-rings; add the cam and ball assembly for a few dollars more if the handle is worn), a Phillips and a flat-head screwdriver, an Allen key, channel locks and a small towel. <b>Drop a plate or rag over the drain</b> — a dropped set screw into an open drain is the reason these jobs take an hour instead of twenty minutes.</p>
<h2>The ten steps</h2>
<ol class="steps">
<li>Shut off the <b>hot and cold supply valves</b> under the sink and open the handle to bleed the pressure.</li>
<li>Remove the <b>handle set screw</b> with the Allen key and lift the handle off.</li>
<li>Unscrew the <b>domed cap and the ball</b> by hand or with channel locks padded by a cloth. Do not put a pipe wrench on a Delta dome — it will mark it.</li>
<li>Lift out the <b>plastic cam assembly and the rubber seats and springs</b>.</li>
<li>Take the old seals and spring out, and <b>load the new springs into the new seats narrow-end first</b>, keeping their orientation exactly as they came out.</li>
<li>Drop the new seats and springs into the valve body.</li>
<li>Refit the <b>cam assembly</b> with its tabs in the notches, then the ball, and the cap.</li>
<li>Reassemble the handle and tighten the <b>set screw</b> snug — that is what holds the whole thing indexed.</li>
<li>Turn the water back on and <b>test both hot and cold at full pressure</b> for a leak around the base and from the spout.</li>
<li>Let the water run <b>one to two minutes</b> into a bucket to clear any sediment or discoloured residue the repair shook loose.</li>
</ol>
<aside class="tip"><span class="tag-mono">Still dripping?</span><p>A leak at the base after a good rebuild usually means the valve body itself is scored, or the faucet is old enough that the replacement costs less than the second repair.</p></aside>""",
  related=[("Faucet repair","leaks-gas-repairs.html#faucet-repair")],
 ),
 dict(
  slug="the-complete-plumbing-guide",
  title="The Complete Plumbing Guide",
  date="2018-12-20", cat="DIY Tutorial", mins=6,
  img=f"{UP}/2018/04/baytown-tx-plumber-truck.jpg",
  lede="The one-page map of a house: where your water comes in, where it goes out, what to shut off, and what to never touch.",
  body="""
<h2>Know your house in five minutes</h2>
<ul class="ticks">
<li><b>Main shut-off.</b> Follow the pipe from the meter to where it enters the wall. Find it, label it, and make sure everyone in the house can work it. If it will not turn, service it now — a burst pipe with a stuck valve is a much bigger job.</li>
<li><b>Fixture stops.</b> Every sink and toilet has its own; the tub usually does not. Water heater, softener, ice maker and washing machine should each have their own too.</li>
<li><b>Water heater.</b> Set to 120°F, T&amp;P valve piped to within six inches of the floor, a drain flush once a year, and a pan under it if it lives over living space or in your garage.</li>
<li><b>Drain-waste-vent.</b> Every fixture needs air as well as fall. A gurgling sink or a slow tub after the neighbours flush is a vent or main-line signal, not a clog you can pour away.</li>
<li><b>Sewer cleanout.</b> Find the capped tee where the house line leaves. Every drain machine and every camera goes in there.</li>
<li><b>Gas.</b> Know the shut-off at the meter. If you smell gas, do not light anything or work switches — get out and phone from outside.</li>
</ul>
<h2>The maintenance calendar we run our own houses on</h2>
<ol class="steps">
<li><b>Monthly:</b> run water in any fixture nobody uses, so the trap seal does not dry out and let sewer gas in.</li>
<li><b>Seasonally:</b> check under sinks with a flashlight for staining, feel washing machine hoses, look at the water heater base for rust blooms.</li>
<li><b>Yearly:</b> flush the water heater, test the T&amp;P valve, test sump pump if you have one, and pump a septic tank on its five-year clock.</li>
<li><b>Every few years:</b> replace rubber appliance hoses, and have a main-line camera look if the house is more than twenty years old.</li>
</ol>""",
  related=[("Water heater maintenance","water-heaters.html#water-heater-maintenance"),("Drain cleaning","drains-sewer.html#drain-cleaning")],
 ),
 dict(
  slug="how-to-use-plumbers-putty",
  title="How to Use Plumber's Putty — and When Not to",
  date="2018-12-08", cat="Plumbing Tips", mins=4,
  img=f"{UP}/2020/07/Plumbers-putty-1024x576.jpg",
  lede="Putty is what seals a drain to a sink. It is also the wrong answer in four very common situations, and using it there costs you the fixture.",
  body="""
<h2>How to apply it like a pro</h2>
<ol class="steps">
<li>Tear off a golf-ball size of putty and <b>roll it warm in your hands</b> until it is pliable.</li>
<li>Roll it into a snake long enough to go around the drain collar.</li>
<li><b>Clean and dry the surface</b> first — putty will not seal to a wet or greasy sink.</li>
<li>Lay the rope where the seal has to sit and press it into place.</li>
<li>Install the part, snug it, and <b>wipe away the squeeze-out</b>. Keep the excess in the tub for next time.</li>
</ol>
<h2>What putty is for</h2>
<p>Watertight seals between a sink, tub or drain flange and the fixture — the joint under the faucet base or around a strainer. It stays soft, so it never needs drying time; run water as soon as the fixture is installed. If the putty in your tub is hard or cracks when you roll it, it is too old — throw it out and buy fresh, and keep the lid sealed.</p>
<h2>When not to use it</h2>
<ul class="ticks">
<li><b>Where you need adhesive strength.</b> Putty does not glue anything.</li>
<li><b>Exposed beads.</b> It is not a caulk — it will smear and crumble in a visible joint between wall and sink.</li>
<li><b>Plastic.</b> Most putty is petroleum-based and degrades rigid plastics — shower drains and fittings go brittle and crack. Use silicone caulk on ABS, PVC or plastic-body drains.</li>
<li><b>Threaded metal joints.</b> That is tape or pipe dope.</li>
<li><b>Underwater.</b> Putty is not a bonding sealant and will not cure under water.</li>
<li><b>Stone.</b> Petroleum-based putty can stain granite and other porous surfaces; those need a stain-free product or silicone.</li>
</ul>""",
  related=[("Kitchen sink leaking fix","kitchen-sink-leaking-from-drain-5-min-fix.html"),("Teflon tape","how-to-apply-teflon-tape.html")],
 ),
 dict(
  slug="should-i-repipe-my-house",
  title="Should I Repipe My House? 3 Things to Know First",
  date="2018-12-04", cat="Plumbing Tips", mins=4,
  img=f"{UP}/2018/11/ed35b70628f21c22d2524518b7494097e377ffd41cb5134697f6c67ea2_640.jpg",
  lede="A repipe is one of the best-value jobs you can do in an older house and one of the worst things to do early. Answer these three questions before anyone quotes you.",
  body="""
<h2>1. Has it already been repiped, and with what?</h2>
<p>Ask the previous owner, look in the garage or utility room where the lines come out of the wall, and check at the water heater. Homes repiped with copper behave very differently from ones done in CPVC or PEX, and a partial repipe is common — some rooms new, the rest original.</p>
<h2>2. What year was the house built?</h2>
<ul class="ticks">
<li><b>Before 1970:</b> galvanized steel supply lines are likely original, and they rust from the inside out until the pressure drops and discolouration shows.</li>
<li><b>1978 to 1995:</b> check for polybutylene — grey plastic with a credit-card-coloured crimp. Those fittings fail and that plumbing needs replacing regardless of how it performs today.</li>
<li><b>Post-1970:</b> copper, then CPVC and PEX. Copper lasts but pinholes where it touches concrete or in aggressive water.</li>
</ul>
<h2>3. What is failing right now?</h2>
<p>A single pinhole in an otherwise sound copper line is a repair. Multiple leaks, visible rust at the nipples, pressure you notice dropping when two taps run, or a fixture count growing on undersized 1/2" lines — that is a whole-house conversation. Slab leaks follow the same rule: two spots under a slab means the third is a matter of time.</p>
<h2>What it costs and what it involves</h2>
<p>We quote repipes per house after a walk-through, and the estimate says what is included: the number of fixtures, new shut-off valves, patching or no patching, and how many days. A typical whole-house change-out is two days with water off in stages, not days of no water at all.</p>""",
  related=[("House repiping","repiping-remodels.html#house-repiping")],
 ),
 dict(
  slug="how-you-can-stop-a-leaky-faucet-yourself",
  title="How You Can Stop a Leaky Faucet Yourself",
  date="2018-11-23", cat="Plumbing Tips", mins=3,
  img=f"{UP}/2018/09/shutterstock_143795752-1024x599.jpg",
  lede="Three things fix the vast majority of dripping faucets, and all three are a trip to the hardware store rather than a service call.",
  body="""
<h2>1. Replace the washer, O-ring or gasket</h2>
<p>Take the tap apart, look at the rubber on the valve seat, and match it at the store with the old pieces in your hand — sizes vary more than you would think. Springs that have lost tension get replaced at the same time.</p>
<h2>2. Soak the corroded parts</h2>
<p>Calcium crust on a valve body or a stuck handle comes off with a soak: white vinegar for a couple of hours, or a paste of baking soda and water on the parts, then a rinse and a dry. Scrub the seat with an old toothbrush before fitting new rubber, or the new seal fails on the same crust.</p>
<h2>3. Replace what is worn</h2>
<p>A grooved valve seat or a scored cartridge will leak with new seals too. That is a replacement part, not a repair job you can tune. Cartridges usually pull straight out and cost more than rebuild kits but take a tenth of the time.</p>
<aside class="tip"><span class="tag-mono">And while you are under there</span><p>Service your septic tank at least every five years — a backup that finds the lowest drain in the house is a far more expensive call than a pump-out, and a dripping faucet is not the only cheap fix with a high payoff.</p></aside>""",
  related=[("Delta faucet in 10 steps","how-to-fix-a-leaky-faucet.html"),("Septic service","drains-sewer.html#septic-tank-services")],
 ),
 dict(
  slug="how-to-keep-drains-clear-naturally",
  title="How to Keep Drains Clear Naturally: Tips from the Alfa Pros",
  date="2018-10-05", cat="Plumbing Tips", mins=5,
  img=f"{UP}/2018/10/e834b00b21fd003ed1584d05fb1d4390e277e2c818b4124993f8c67aaee4_640.jpg",
  lede="Almost every clog we cut out is something that a two-minute habit would have prevented. Here is the routine we run ourselves.",
  body="""
<h2>Every month</h2>
<ul class="ticks">
<li><b>Baking soda and vinegar in the bathtub and sink drains.</b> Equal parts, plug it, let the reaction run, then flush with a kettle of boiling water. It moves hair and soap scum before they bridge the pipe.</li>
<li><b>Enzyme cleaner overnight</b> instead of a caustic opener. Enzymes eat the organic film; lye-based products eat older pipes and the rubber in your toilet.</li>
<li><b>Clear the overflow holes</b> in every sink — a packed overflow is why a partly clogged sink also drains slowly.</li>
<li><b>Screens in every drain.</b> Hair out of a screen is easy; hair out of a bend is a machine.</li>
<li><b>Run water in unused fixtures</b> so the trap does not dry out, and never put grease, coffee grounds or fat down the disposal. Cold water and a little dish soap while it runs keeps the blades and the drain clean.</li>
</ul>
<h2>Every season</h2>
<ul class="ticks">
<li><b>Check outdoor faucets for drips before winter.</b> A weeping bib left open freezes and splits the pipe it is teed from.</li>
<li><b>Insulate the exposed lines</b> and do not let an empty house drop below freezing. If a pipe freezes, open the nearest tap so the thaw has somewhere to go — the pressure is what bursts the pipe, not the ice.</li>
<li><b>Anchor exposed pipes.</b> Noisy pipes are usually just loose ones; a strap is a five-minute fix.</li>
<li><b>Look at the floor around the toilet base.</b> Soft spots mean a leak you have not seen yet.</li>
</ul>
<h2>What does not work</h2>
<p>Chemical drain openers on a full clog — they sit on top of it and burn the stuff they touch; and flushable wipes, which do not flush. If two or more drains are slow at once, stop pouring things down them and call: that is the main line, and it wants a cable or a jet.</p>""",
  related=[("Drain cleaning","drains-sewer.html#drain-cleaning"),("Sewer line services","drains-sewer.html#sewer-line-services")],
 ),
 dict(
  slug="brown-water-from-your-faucet",
  title="Brown Water Running from Your Faucet",
  date="2018-09-03", cat="Plumbing Tips", mins=4,
  img=f"{UP}/2018/09/9D2705C3-794D-4DE7-9BD5-F6E7B5AF7749.jpeg",
  lede="Brown water is the pipe telling you something: rust, sediment, a dying water heater or a stir-up in the street. Here is how to tell which — and when it stops being a wait-and-see.",
  body="""
<h2>Start here: whose water is brown?</h2>
<ul class="ticks">
<li><b>Neighbours too?</b> Then it is the municipal main — a hydrant flush, a water break or work on the system. Call the city's water department and it settles within hours.</li>
<li><b>Only your house, only the hot side?</b> The tank is corroding inside. Have a plumber evaluate it before you replace it, but a tank over ten or fifteen years with rusty hot water is usually a tank to replace.</li>
<li><b>Only one faucet?</b> That fixture's line or its aerator — sediment caught in the screen, or a rusted galvanized stub.</li>
<li><b>Only cold, whole house, and it keeps happening?</b> Rust in your own supply piping or the service line. It clogs the pipes and gives bacteria somewhere to live.</li>
</ul>
<h2>What to do first</h2>
<p>Turn the cold tap on for about 20 minutes and let it run to waste — water the lawn with it rather than the drain. If the colour clears, note when it came back and on which tap; that pattern is the diagnosis.</p>
<h2>Is it safe?</h2>
<p>We would not drink it, cook with it, wash a baby's bottle in it or run laundry — rust stains clothes. In a bind, a shower and a flush will not hurt you. Persistent discolouration is not a cosmetic problem: find the cause before it finds your fixtures.</p>
<aside class="tip"><span class="tag-mono">If iron is the cause</span><p>Pink or orange stains in the tub from a well mean iron in the water, which is a softener or filtration problem rather than a plumbing repair — but the staining will keep eating your lines until it is dealt with.</p></aside>""",
  related=[("Water line repair","leaks-gas-repairs.html#water-line-repair"),("Water heater replacement","water-heaters.html#water-heater-installation")],
 ),
 dict(
  slug="gas-line-repair-baytown",
  title="Gas Line Repair in Baytown: What to Do When You Smell Gas",
  date="2018-08-17", cat="Emergency", mins=3,
  img=f"{UP}/2018/04/baytown-tx-plumbing-repair-247.jpg",
  lede="A gas smell is the one plumbing call where what you do in the first minute matters more than how fast we get there.",
  body="""
<h2>Do this now</h2>
<ol class="steps">
<li><b>Put the flame out and do not light anything.</b> No match, no candle, no lighter.</li>
<li><b>Do not work switches, thermostats or doorbells</b> — leave the lights as they are. A spark the size of a click is enough.</li>
<li><b>Open a door or window on the way out</b> to ventilate, and take the household and the pets with you.</li>
<li><b>From outside, call your gas utility and then us</b> on (713) 992-9257. If the smell is strong or you hear hissing, call 911 first.</li>
<li>Do not go back inside for anything until the line has been checked.</li>
</ol>
<h2>What we do on a gas call</h2>
<p>Manometer and leak-detection fluid at every joint from the meter in, so the leak is found rather than assumed; then the repair — a fitting, a section of line, a shut-off valve that failed. If black dust or soot is coming from a joint, tell us before we start, because it means the leak has been open a while and the pipe needs replacing, not patching.</p>
<h2>New appliance? Same rules</h2>
<p>Gas dryers, ranges, generators, pool heaters and outdoor kitchens all need a properly sized line, a sediment trap ahead of the appliance and a pressure test on the finished run. We run those with the utility on the other end of the phone if the service has to be isolated.</p>""",
  related=[("Gas line repair","leaks-gas-repairs.html#gas-line-repair"),("Emergency plumber","leaks-gas-repairs.html#emergency-plumber")],
 ),
 dict(
  slug="water-line-repair-underground-leak-detection",
  title="Water Line Repair and Underground Leak Detection",
  date="2018-08-10", cat="Emergency", mins=3,
  img=f"{UP}/2018/04/baytown-tx-drain-cleaning.jpg",
  lede="You cannot repair what you cannot locate. Underground leaks are almost never visible above ground, which is why the dig-first approach costs homeowners so much.",
  body="""
<h2>The four signs of a service-line leak</h2>
<ul class="ticks">
<li>Usage on the bill that no habit explains — the meter keeps turning with everything off.</li>
<li>A soft, wet or greener-than-the-rest patch of lawn between the meter and the house.</li>
<li>Pressure that dropped across the whole house at the same time.</li>
<li>The sound of running water at the slab or the wall with every fixture closed.</li>
</ul>
<h2>How we find it</h2>
<p>Isolate and section the line to prove which run leaks, listen for it with ground amplification, then trace it electronically so the dig is a hole, not a trench. Under slab, we pressurise and trace the hot water and cold separately, then decide between excavating and rerouting — in Baytown the reroute is usually the cheaper, better repair.</p>
<h2>Why it should not wait</h2>
<p>A service line leak washes the bedding and the soil out from under a slab and grows as it erodes. The water bill is the smallest number in the problem; the settlement damage and the second repair are not.</p>""",
  related=[("Leak detection","leaks-gas-repairs.html#water-leak-detection"),("Water line repair","leaks-gas-repairs.html#water-line-repair")],
 ),
]

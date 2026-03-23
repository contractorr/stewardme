# Nuclear Energy

## Overview

Nuclear energy harnesses the enormous power locked in atomic nuclei through controlled fission reactions — releasing roughly 2 million times more energy per kilogram than fossil fuels. It provides approximately 10% of global electricity (26% in the US, 70% in France) with near-zero carbon emissions during operation. Understanding nuclear physics fundamentals, reactor design principles, the fuel cycle, safety systems, waste management challenges, economic constraints, and advanced reactor concepts is essential for evaluating nuclear power's role in decarbonization.

Nuclear energy is unique among energy sources: it's based on Einstein's mass-energy equivalence rather than chemical bonds, operates at energy densities orders of magnitude beyond anything chemical, produces waste that remains hazardous for millennia, and carries catastrophic failure risks (Chernobyl, Fukushima) alongside an excellent safety record (fewest deaths per TWh of any major energy source). This combination of extraordinary capability and profound responsibility makes nuclear power one of humanity's most consequential technological achievements.

## Nuclear Physics Basics

### Mass-Energy Equivalence

Einstein's special relativity (1905) revealed that mass and energy are interconvertible:

```
E = mc²
```

Where:
- E = energy (joules)
- m = mass (kilograms)
- c = speed of light (299,792,458 m/s)

**Implication**: A tiny mass converts to enormous energy.

1 kg of mass → E = 1 × (3×10⁸)² = 9×10¹⁶ J = 90 PJ

This is equivalent to:
- 21.5 megatons of TNT explosive
- 25,000 GWh of electricity
- Burning ~3 million tonnes of coal

In practice, nuclear reactors convert ~0.09% of fuel mass to energy (not 100% — that would require matter-antimatter annihilation). Still, this means 1 kg of uranium-235 releases ~80,000 MJ — roughly 2 million times the energy of burning 1 kg of coal (~32 MJ).

### Nuclear Structure and Forces

**Atomic nucleus**: Protons (positive charge) + neutrons (neutral), bound by the **strong nuclear force**.

- **Electromagnetic repulsion**: Protons repel each other (positive-positive). This force scales with 1/r² and acts at all distances.
- **Strong force**: Attracts all nucleons (protons and neutrons) but only at extremely short range (femtometers, 10⁻¹⁵ m). Much stronger than electromagnetic force at nuclear distances.

For light nuclei (H, He, C, O), adding neutrons increases stability by diluting proton-proton repulsion. For heavy nuclei (U, Pu), neutron excess is essential — U-238 has 92 protons and 146 neutrons (ratio 1.59:1).

### Binding Energy

When nucleons combine into a nucleus, the mass of the nucleus is *less* than the sum of individual nucleon masses. The "missing mass" has been converted to **binding energy** — the energy holding the nucleus together.

**Binding energy per nucleon** varies across elements:
- Hydrogen-2 (deuterium): ~1.1 MeV per nucleon
- Iron-56: ~8.8 MeV per nucleon (peak binding energy — most stable nucleus)
- Uranium-235: ~7.6 MeV per nucleon

**Energy release mechanisms**:
- **Fusion**: Light nuclei (H, He) fuse → heavier nucleus closer to iron peak → releases energy
- **Fission**: Heavy nuclei (U, Pu) split → lighter nuclei closer to iron peak → releases energy

Iron-56 sits at the binding energy maximum — you can't extract energy from iron by either fusion or fission. This is why stars produce iron as their final fusion product before collapse.

### Fission Reaction

A heavy nucleus (typically U-235 or Pu-239) absorbs a neutron, becomes unstable, and splits into two lighter **fission fragments** (daughter nuclei) plus 2-3 neutrons plus energy.

**Example fission reaction** (one of many possible):
```
²³⁵U + n → ⁹²Kr + ¹⁴¹Ba + 3n + ~200 MeV
```

But fission is probabilistic — hundreds of possible fragment combinations. Most common mass numbers: ~95 and ~140 (asymmetric split).

**Energy distribution per fission** (~200 MeV total):
- Kinetic energy of fission fragments: ~168 MeV (83%) — becomes heat
- Kinetic energy of neutrons: ~5 MeV (2.5%)
- Prompt gamma rays: ~7 MeV (3.5%)
- Beta particles from radioactive decay: ~7 MeV (3.5%)
- Gamma rays from radioactive decay: ~6 MeV (3%)
- Neutrinos: ~10 MeV (5% — escapes, not captured)

**Heat generation**: ~190 MeV per fission becomes heat in the reactor core (neutrinos escape). This heat boils water → steam → turbine → electricity.

**Comparison to chemical reactions**:
- Coal combustion: ~4 eV per carbon atom
- Nuclear fission: ~200 MeV per uranium atom
- Ratio: 200 MeV / 4 eV = 50 million times more energy per atom

### Chain Reactions and Criticality

Each fission releases 2-3 neutrons (average 2.5 for U-235). These neutrons can trigger more fissions, creating a chain reaction.

**Criticality states**:

**Multiplication factor** k = (neutrons in generation n+1) / (neutrons in generation n)

| k value | State | Behavior | Application |
|---------|-------|----------|-------------|
| k < 1 | **Subcritical** | Reaction dies out | Reactor shutdown |
| k = 1 | **Critical** | Steady-state | Normal reactor operation |
| k > 1 | **Supercritical** | Exponentially increasing | Reactor startup, nuclear weapon |

**Reactor operation**: Maintain k = 1.000 ± 0.001 through precise control rod positioning, coolant flow, and fuel geometry.

**Weapon**: k >> 1 (highly supercritical). Weapon-grade U-235 (~90% enrichment) or Pu-239 in a compact geometry allows uncontrolled exponential chain reaction, releasing enormous energy in microseconds. Requires extreme precision and specialized design — reactor-grade fuel (3-5% enrichment) cannot create a nuclear explosion.

**Delayed neutrons** (~0.65% of fission neutrons, released seconds to minutes after fission from radioactive fission fragments) provide crucial controllability. Without delayed neutrons, reactors would be impossible to control — power would respond to changes in milliseconds rather than seconds, too fast for mechanical systems.

### Isotopes and Radioactive Decay

**Isotopes**: Same element (same protons) but different neutron counts. Example: uranium has three natural isotopes:
- U-234: 92 protons, 142 neutrons (0.0054% of natural uranium)
- U-235: 92 protons, 143 neutrons (0.72%) — fissile
- U-238: 92 protons, 146 neutrons (99.27%) — not fissile

**Fissile** (can sustain chain reaction with thermal neutrons): U-233, U-235, Pu-239, Pu-241
**Fertile** (can become fissile by neutron capture): U-238 → Pu-239, Th-232 → U-233

**Radioactive decay**: Unstable nuclei emit particles/energy to reach stability.
- **Alpha decay**: Nucleus emits He-4 (2 protons + 2 neutrons). Stopped by paper, skin.
- **Beta decay**: Neutron → proton + electron + antineutrino (or vice versa). Stopped by aluminum foil.
- **Gamma decay**: Nucleus emits high-energy photon. Requires thick lead or concrete shielding.

**Half-life**: Time for half the radioactive atoms to decay. Ranges from microseconds to billions of years.

## Reactor Types and Designs

Global nuclear fleet (2024): ~440 reactors, ~390 GW capacity, generating ~2,800 TWh/year

| Type | Coolant | Moderator | Fuel | Countries | Reactors | Share |
|------|---------|-----------|------|-----------|----------|-------|
| **PWR** (Pressurized Water Reactor) | Pressurized light water | Light water | Enriched UO₂ (3-5%) | US, France, China, Russia, South Korea | ~300 | ~67% |
| **BWR** (Boiling Water Reactor) | Boiling light water | Light water | Enriched UO₂ (3-5%) | US, Japan, Sweden | ~65 | ~15% |
| **PHWR** (Pressurized Heavy Water, CANDU) | Heavy water | Heavy water | Natural UO₂ (0.7% U-235) | Canada, India, South Korea, China | ~50 | ~11% |
| **RBMK** (graphite-moderated boiling water) | Light water | Graphite | Enriched UO₂ (2-3%) | Russia (legacy) | ~10 | ~2% |
| **AGR** (Advanced Gas-Cooled Reactor) | CO₂ gas | Graphite | Enriched UO₂ | UK (legacy) | ~4 | ~1% |
| **FBR** (Fast Breeder Reactor) | Liquid sodium | None | PuO₂ or MOX | Russia, India | ~2 | <1% |
| **Other** | Various | Various | Various | Research, experimental | ~10 | ~2% |

### PWR (Pressurized Water Reactor) — Dominant Design

**Operating principle**:
1. **Primary loop**: Water at ~155 bar (2,250 psi) pressure circulates through reactor core. Heated to ~315°C but remains liquid (high pressure prevents boiling).
2. **Steam generator**: Primary loop water transfers heat to secondary loop through thousands of thin tubes (heat exchanger).
3. **Secondary loop**: Water at lower pressure (~70 bar) boils to steam at ~280°C.
4. **Turbine**: Steam drives turbine-generator. Exhaust steam condenses back to water.
5. **Containment**: Two barriers between radioactive fuel and turbine (primary loop and steam generator tubes).

**Advantages**:
- Clean steam (no radioactive contamination in turbine)
- Negative temperature coefficient (reactor power naturally decreases if coolant heats up — inherent safety)
- Compact core (high power density)
- Proven technology (>11,000 reactor-years of operating experience)

**Disadvantages**:
- Requires enriched fuel
- High pressure vessels expensive and complex
- Lower thermal efficiency (~33%) due to modest steam temperature (280°C vs 540°C+ for fossil plants)

**Example reactors**:
- Westinghouse AP1000 (US, China): 1,100 MW electric, Generation III+ design with passive safety
- EPR (European Pressurized Reactor, France/Finland): 1,650 MW, double containment
- Russian VVER series: 1,000-1,200 MW, similar design to Western PWRs

### BWR (Boiling Water Reactor)

**Operating principle**:
Water boils directly in the reactor core at ~285°C and ~70 bar. Radioactive steam goes directly to turbine (single loop).

**Advantages**:
- Simpler design (no steam generator)
- Lower operating pressure than PWR
- Higher thermal efficiency (~34%) due to eliminating steam generator heat transfer loss

**Disadvantages**:
- Radioactive steam in turbine (requires shielding, increases maintenance dose)
- Positive void coefficient possible (bubbles in core → less moderation → potential power increase)
- More complex control (steam quality affects reactivity)

**Example reactors**:
- GE BWR/6, ABWR (Advanced BWR): 1,300-1,350 MW
- Fukushima Daiichi units 1-4: 460-784 MW (BWR/3-4 — older design)

### CANDU (Canada Deuterium Uranium)

**Operating principle**:
Uses heavy water (D₂O) as both coolant and moderator. Heavy water absorbs far fewer neutrons than light water, allowing use of natural uranium (0.7% U-235) without enrichment.

**Advantages**:
- No enrichment required (fuel cycle independence)
- On-line refueling (doesn't shut down to replace fuel)
- Can burn thorium, spent fuel from light-water reactors

**Disadvantages**:
- Requires large quantities of heavy water (expensive: ~$500/kg)
- Larger core than PWR/BWR (lower power density)
- Horizontal pressure tubes (vs single large vessel) more complex

**Deployment**: Canada (19 reactors), India (18 reactors, plus indigenous variants), South Korea, China, Romania, Argentina.

### RBMK (Chernobyl Design)

**Operating principle**:
Graphite moderates neutrons; water cools fuel and produces steam. Positive void coefficient — if water boils away, reactivity increases (opposite of PWR).

**Fatal flaw**: Loss of coolant increases power rather than decreasing it. Combined with weak containment, this led to Chernobyl disaster. No RBMKs built after 1986; remaining units heavily modified or shut down.

### Fast Breeder Reactors

**Operating principle**:
No moderator — neutrons remain at high energy ("fast" neutrons, ~2 MeV vs ~0.025 eV for thermal neutrons). Fast neutrons can cause fertile U-238 to capture neutrons and become fissile Pu-239:

```
²³⁸U + n → ²³⁹U → ²³⁹Np + β⁻ → ²³⁹Pu + β⁻
(23 minutes)   (2.4 days)
```

**Breeding ratio**: If > 1.0, reactor creates more fissile material than it consumes, "breeding" new fuel.

**Coolant**: Liquid sodium (melts at 98°C, boils at 883°C). Excellent heat transfer, low pressure, doesn't moderate neutrons. But chemically reactive (burns in air, explodes in water).

**Promise**: Could extract 60-70x more energy from uranium (use U-238, not just U-235). Effectively unlimited fuel for thousands of years. Can also burn actinides from spent fuel (waste reduction).

**Challenge**: Sodium handling, higher capital costs, weapons proliferation concern (produces Pu-239), limited commercial deployment.

**Operating reactors**: BN-800 (Russia, 880 MW), experimental units in India. France, UK, US, Japan built prototypes but abandoned commercial deployment due to high costs and proliferation concerns.

## Nuclear Fuel Cycle

```
Mining → Milling → Conversion → Enrichment → Fabrication → Reactor → Interim Storage → Reprocessing or Disposal
```

### Mining and Milling

**Uranium ore** typically contains 0.1-2% uranium oxide (U₃O₈, "yellowcake"). Mined via:
- **Open pit**: Large surface excavations (Olympic Dam, Australia)
- **Underground**: Shaft and tunnel mining (McArthur River, Canada)
- **In-situ leaching**: Inject oxidizing solution, pump uranium-bearing liquid to surface (Kazakhstan — now 45% of global production)

**Major producers** (2023):
- Kazakhstan: 21,227 tonnes U (~43% of global)
- Canada: 7,351 tonnes (~15%)
- Australia: 4,610 tonnes (~9%)
- Namibia: 3,654 tonnes (~7%)
- Uzbekistan: 3,500 tonnes (~7%)
- **Total global**: ~49,000 tonnes U

**Milling**: Crush ore, leach with acid or alkali, precipitate uranium oxide (U₃O₈). This "yellowcake" is ~80% uranium.

### Conversion

Convert U₃O₈ to uranium hexafluoride (UF₆), the feedstock for enrichment. UF₆ is solid at room temperature, sublimes to gas at 56°C.

**Process**: U₃O₈ → UO₃ → UF₄ → UF₆

**Major facilities**: Cameco (Canada), Converdyn (US), Rosatom (Russia), CNNC (China), Orano (France)

### Enrichment

Natural uranium: 99.27% U-238, 0.72% U-235. Most reactors need 3-5% U-235 (LEU — Low Enriched Uranium). Weapons require >90% (HEU — Highly Enriched Uranium).

**Separation challenge**: U-235 and U-238 are chemically identical (same element). Only difference is mass (235 vs 238 atomic mass units — 1.3% lighter).

**Gas centrifuge** (modern standard):
1. UF₆ gas spins at 50,000-70,000 RPM in a cylinder
2. Heavier U-238 concentrates at outer edge; lighter U-235 near center
3. Extract slightly enriched stream from center, depleted stream from edge
4. Single centrifuge enriches by only ~1% → requires thousands in series (cascades)

**Separative Work Unit (SWU)**: Measure of enrichment effort (not a physical unit). Depends on feed, product, and waste concentrations.

Example: Producing 1 kg of 4.5% enriched uranium from natural (0.72%) uranium:
- Feed required: ~8.9 kg natural uranium
- Enrichment work: ~6.6 SWU
- Tails (depleted uranium, 0.3% U-235): ~7.9 kg

**Global enrichment capacity** (2023): ~66 million SWU/year
- Russia: ~28 million SWU (~42%)
- China: ~13 million SWU (~20%)
- France (Orano): ~7.5 million SWU (~11%)
- UK (Urenco): ~7.5 million SWU (~11%)
- US (Urenco USA): ~5 million SWU (~8%)

**Proliferation concern**: Centrifuge technology for 5% enrichment can also enrich to 90% (weapons-grade). Only quantity/time differs. This is the Iran/North Korea nuclear program concern — "civilian" enrichment provides path to weapons capability.

### Fuel Fabrication

Convert enriched UF₆ to ceramic uranium dioxide (UO₂) pellets:
1. Convert UF₆ to UO₂ powder
2. Press powder into cylindrical pellets (~1 cm diameter, 1-2 cm long)
3. Sinter (heat to 1,700°C to densify)
4. Grind to precise dimensions
5. Load pellets into zirconium alloy tubes (cladding)
6. Seal tubes and bundle into fuel assemblies

**Fuel assembly** (PWR example):
- ~200-300 fuel rods per assembly
- Each rod contains ~350 pellets (~4 meters long)
- Total fuel: ~450 kg uranium per assembly
- Reactor core: ~150-200 fuel assemblies (~80-100 tonnes uranium)

**In-core lifetime**: 3-6 years (typically 18-month cycles, replacing 1/3 of core each cycle)

### Reactor Operation

**Power output**: 1,000 MW electric plant requires ~2,900 MW thermal (34% efficiency). At 92% capacity factor:
- Annual electricity: ~8 TWh
- Annual uranium consumption: ~25 tonnes U-235 fissioned
- This requires ~190 tonnes fresh fuel (4.5% enrichment) replacing ~60 tonnes spent fuel

**Fuel burnup**: Measured in megawatt-days per tonne of uranium (MWd/t). Modern PWRs achieve 50,000-60,000 MWd/t. Higher burnup means more energy per tonne of uranium but increases fuel degradation and fission product accumulation.

### Spent Fuel and Storage

After 3-6 years in-core, fuel assemblies are "spent" — too many fission products absorb neutrons, impeding chain reaction. But spent fuel contains:
- Unused uranium: ~95% (~94% U-238, ~1% U-235)
- Fission products: ~3.5% (highly radioactive, short-to-medium half-lives)
- Transuranic actinides (Pu, Am, Cm, Np): ~1.5% (long half-lives, radiotoxic)

**Decay heat**: Fission products continue radioactive decay, generating heat. Spent fuel must be actively cooled:
- 1 day after shutdown: ~1% of operating power (~30 MW for 3 GW reactor)
- 1 year after shutdown: ~0.1% (~3 MW)
- 10 years: ~0.01% (~300 kW)
- 100 years: ~0.001% (~30 kW)

**Spent fuel pool** (interim storage):
- Water-filled pool at reactor site
- Water provides cooling and radiation shielding (~5 meters water stops gamma rays)
- Fuel stored 5-10 years until cool enough for dry storage
- **Fukushima vulnerability**: Spent fuel pools lost cooling after tsunami → hydrogen buildup

**Dry cask storage** (longer-term interim):
- Transfer cooled fuel to steel/concrete casks
- Passive air cooling (no pumps required)
- Licensed for 60+ years (likely good for centuries)
- ~100,000 tonnes in dry cask storage globally

**Disposal** (final, permanent):
- Deep geological repository: 300-1,000 meters underground in stable rock formations
- Isolation for 100,000+ years
- **Challenge**: Institutional timescales far exceed human political/organizational lifespans

## Safety Systems and Accidents

### Defense in Depth

Nuclear safety philosophy: Multiple independent barriers prevent radioactive release.

**Five barriers**:
1. **Fuel pellet**: Ceramic UO₂ matrix retains most fission products
2. **Fuel cladding**: Zirconium alloy tubes seal fuel (prevent coolant contamination)
3. **Reactor vessel**: 20-30 cm thick steel pressure vessel contains core
4. **Containment building**: 1-2 meter thick reinforced concrete, steel liner (prevents external release)
5. **Exclusion zone**: Distance from public

**Safety systems** (PWR example):
- **Passive safety**: Negative temperature/void coefficients — power naturally drops if coolant heats up
- **Active safety**: Control rods (absorb neutrons), boron injection (emergency shutdown), emergency core cooling (backup water injection)
- **Containment spray**: Cool containment atmosphere, remove radioactive particles
- **Filtered venting**: Relieve containment pressure while filtering radioactive material
- **Backup power**: Multiple diesel generators, batteries (prevent station blackout)

**Chernobyl lacking**: No containment building, positive void coefficient, inadequate safety culture

**Fukushima lacking**: Backup generators vulnerable to flooding, insufficient battery capacity

### Major Accidents and Lessons

| Accident | Date | Location | Type | Cause | Deaths (Direct) | INES Level | Lessons |
|----------|------|----------|------|-------|-----------------|-----------|---------|
| **Three Mile Island** | 1979 | US | PWR | Valve failure + operator error | 0 | 5 | Containment worked; operator training critical |
| **Chernobyl** | 1986 | Ukraine | RBMK | Design flaw + safety test violations | ~30 acute, ~4,000 cancer (disputed) | 7 | Positive void coefficient fatal; containment essential |
| **Fukushima Daiichi** | 2011 | Japan | BWR | 9.0 quake + 14m tsunami → station blackout | 1 (radiation), ~2,200 (evacuation stress) | 7 | Backup power must be flooding-resistant; passive safety |

**Three Mile Island** (March 28, 1979):
- **Sequence**: Valve stuck open → primary loop lost water → core partially uncovered → partial meltdown
- **Operator error**: Misread instruments, shut off emergency cooling (thought core was flooded — it wasn't)
- **Outcome**: ~50% core melted; containment intact; ~0 public radiation dose; no deaths
- **Impact**: Destroyed public confidence; no new US reactors ordered for 30 years; stricter regulations

**Chernobyl** (April 26, 1986):
- **Design flaw**: RBMK with positive void coefficient (losing coolant increases reactivity)
- **Trigger**: Safety test — operators disabled safety systems, withdrew too many control rods
- **Sequence**: Power surged to 100x normal in seconds → steam explosion → graphite fire
- **Outcome**: Reactor destroyed; radioactive material spread across Europe; 30 immediate deaths; ~4,000-60,000 eventual cancer deaths (estimates vary widely); 350,000 evacuated permanently
- **Impact**: Largest nuclear accident; demonstrated catastrophic potential; RBMK design abandoned

**Fukushima Daiichi** (March 11, 2011):
- **Trigger**: Magnitude 9.0 earthquake → reactors automatically shut down → tsunami (14 meters) flooded site
- **Sequence**: Backup diesel generators flooded → station blackout → loss of cooling → three core meltdowns (units 1, 2, 3) → hydrogen explosions damaged buildings (units 1, 3, 4)
- **Outcome**: ~100,000 evacuated (many permanently); ~1 cancer death attributed to radiation (WHO estimate); ~2,200 deaths from evacuation stress (elderly)
- **Lessons**: Defense-in-depth failed at "beyond design basis" event; passive safety systems crucial; backup power must be flooding-proof

**Safety statistics** (deaths per TWh, lifecycle):
- Coal: ~25 deaths/TWh (air pollution, mining accidents)
- Oil: ~18 deaths/TWh
- Natural gas: ~3 deaths/TWh
- Hydroelectric: ~1.3 deaths/TWh (Banqiao Dam failure 1975: 171,000 deaths in one event)
- Nuclear: ~0.03 deaths/TWh (including Chernobyl and Fukushima)

Nuclear has the lowest mortality rate per unit energy of any major source — but risk is concentrated in rare, catastrophic events rather than distributed across operations.

## Nuclear Waste Management

### Waste Classification

| Category | Radioactivity | Volume | Management | Examples |
|----------|---------------|--------|------------|----------|
| **Low-level** (LLW) | < 4 GBq/m³ | ~90% | Shallow burial (30m), 300 years | Contaminated clothing, tools, filters |
| **Intermediate-level** (ILW) | 4 GBq/m³ - 4 TBq/m³ | ~7% | Geological disposal or engineered surface storage | Reactor components, resins, chemical sludges |
| **High-level** (HLW) | > 4 TBq/m³ | ~3% (by volume), 95% (by radioactivity) | Deep geological disposal | Spent fuel, reprocessing waste |

**Global spent fuel**: ~400,000 tonnes as of 2023, growing by ~10,000 tonnes/year. All spent fuel ever produced would fit on a single American football field stacked ~10 meters high.

### Radiotoxicity and Half-Lives

| Isotope | Half-Life | Radiation Type | Primary Hazard | Decay Time to Background |
|---------|-----------|----------------|----------------|--------------------------|
| **Iodine-131** | 8 days | Beta, gamma | Thyroid cancer (acute) | ~80 days |
| **Strontium-90** | 29 years | Beta | Bone cancer | ~300 years |
| **Cesium-137** | 30 years | Beta, gamma | Ground contamination | ~300 years |
| **Plutonium-239** | 24,100 years | Alpha | Inhalation hazard, long-term | ~250,000 years |
| **Iodine-129** | 15.7 million years | Beta | Thyroid (very long-term) | >100 million years |
| **Technetium-99** | 211,000 years | Beta | Mobile in groundwater | >2 million years |

**Radiotoxicity timeline**:
- First 100 years: Dominated by fission products (Sr-90, Cs-137) — heat and gamma radiation
- 100-10,000 years: Transuranic actinides (Pu, Am, Cm) dominate — alpha emitters
- 10,000-1,000,000 years: Pu-239, long-lived fission products — very slowly declining

After ~300 years, spent fuel radiotoxicity drops below natural uranium ore. But actinides keep it significantly above background for 100,000+ years.

### Reprocessing

**PUREX process** (Plutonium Uranium Redox EXtraction):
1. Dissolve spent fuel in nitric acid
2. Chemically separate uranium (~95%), plutonium (~1%), and fission products/actinides (~4%)
3. Fabricate mixed oxide (MOX) fuel: UO₂ + PuO₂
4. Vitrify high-level waste (fission products + actinides) in glass

**Advantages**:
- Recovers ~95% of uranium for re-enrichment and reuse
- Plutonium becomes fuel (MOX) rather than waste
- Reduces volume of high-level waste ~4x

**Disadvantages**:
- Expensive: ~$2,000-3,000 per kg vs ~$100/kg fresh fuel
- Proliferation risk: Separates weapon-usable plutonium
- Waste remains highly radioactive

**Countries reprocessing**: France (La Hague, 1,700 tonnes/year), UK (Sellafield, closing), Russia, India, China, Japan (Rokkasho, not yet operating at full capacity)

**US policy**: Banned reprocessing 1977-1981 (Carter administration, proliferation concerns); currently allowed but uneconomic (cheap uranium makes reprocessing financially unattractive)

### Geological Disposal

**Design concept** (multi-barrier):
1. **Waste form**: Vitrified glass or spent fuel pellets (immobilizes radionuclides)
2. **Canister**: Corrosion-resistant metal (copper in Sweden/Finland, steel elsewhere)
3. **Buffer**: Bentonite clay (swells when wet, seals cracks, absorbs radionuclides)
4. **Backfill**: Crushed rock (structural support)
5. **Host rock**: Granite (Finland, Sweden), clay (France, Switzerland), tuff (US), salt (Germany)

**Site requirements**:
- Geologically stable (no earthquakes, volcanism)
- Low groundwater flow (minimize radionuclide transport)
- Depth: 300-1,000 meters (isolation from surface processes)
- Far from resources (prevent future humans drilling into repository)

**Status of geological repositories**:

| Country | Site | Rock Type | Status | Capacity | Expected Operation |
|---------|------|-----------|--------|----------|-------------------|
| **Finland** | Onkalo (Olkiluoto) | Granite | Under construction | 6,500 tonnes | ~2025 |
| **Sweden** | Forsmark | Granite | Licensed (2022) | 12,000 tonnes | ~2030s |
| **France** | Bure (Cigéo) | Clay | Planning/approval | 80,000 m³ | ~2035 |
| **US** | Yucca Mountain | Tuff (volcanic) | Licensed (2002), politically blocked | 70,000 tonnes | Indefinite |
| **Canada** | TBD (Ignace or South Bruce) | Granite | Site selection | ~200,000 fuel bundles | 2040s |
| **UK** | TBD | TBD | Community consultation | TBD | 2040s+ |

**Yucca Mountain saga** (US):
- Designated 1987 by Congress (only site studied)
- Licensed by NRC 2002 (met safety requirements)
- Blocked 2009 by Obama administration (political opposition from Nevada)
- Spent fuel accumulates at reactor sites in dry casks (90+ sites nationwide)
- Taxpayers pay $500M+ annually to utilities (government failed to meet disposal contract)

**Finland's success**: Strong public consultation, stable government support, co-location with Olkiluoto nuclear plant (locals already accept nuclear), transparent process. Demonstrates repository is technically achievable — politics/trust are the hard parts.

## Advanced Reactors and Generation IV

### Generations of Nuclear Reactors

| Generation | Era | Description | Examples |
|------------|-----|-------------|----------|
| **Gen I** | 1950s-1970s | Early prototypes | Shippingport, Magnox |
| **Gen II** | 1970s-2000s | Commercial fleet | Most current PWRs, BWRs, CANDUs |
| **Gen III / III+** | 1990s-present | Evolutionary improvements, passive safety | AP1000, EPR, APR-1400, VVER-1200 |
| **Gen IV** | 2030s+ | Revolutionary designs, higher temps, better fuel use | Molten salt, sodium fast, high-temp gas |

### Small Modular Reactors (SMRs)

**Concept**: Factory-built reactors (<300 MW), shipped to site, requiring less capital per unit.

**Advantages**:
- Lower upfront capital (<$2B vs $10-20B for large reactor)
- Faster construction (factory assembly, 3-4 years vs 7-12 years)
- Scalable (add modules as demand grows)
- Potential for mass production (learning curve cost reduction)
- Passive safety (smaller cores easier to cool)

**Disadvantages**:
- Higher cost per kW (lose economies of scale)
- First-of-a-kind costs still high (no learning curve yet)
- Regulatory approval for new designs expensive and slow

**Leading designs**:
- **NuScale** (US): 77 MW PWR modules, NRC approved 2020, targeting 2029 deployment (UAMPS project in Idaho canceled due to cost overruns, seeking new customers)
- **Rolls-Royce SMR** (UK): 470 MW PWR, seeking approval, targeting 2030s
- **BWRX-300** (GE Hitachi): 300 MW BWR, passive safety, Canada pursuing deployment
- **VOYGR** (NuScale's current design): up to 462 MW (6 modules × 77 MW)

**Economics uncertain**: SMRs promise lower cost through factory production, but first projects face cost overruns. Mass production could achieve 30-40% cost reduction by 10th unit.

### Molten Salt Reactors (MSRs)

**Concept**: Fuel dissolved in molten fluoride salt coolant (~650-700°C). Liquid fuel, not solid fuel rods.

**Advantages**:
- **Cannot melt down**: Fuel already molten; emergency drain tanks passively cool fuel if power lost
- **Low pressure**: Operates near atmospheric pressure (salt boiling point ~1,400°C)
- **High temperature**: ~700°C enables 45% thermal efficiency vs 33% for PWR
- **Continuous fission product removal**: Can extract fission products online, improving neutron economy
- **Can burn thorium**: Th-232 → U-233 breeding cycle, more abundant than uranium

**Disadvantages**:
- **Materials challenge**: Fluoride salts corrode most alloys; developing corrosion-resistant materials critical
- **Tritium production**: Fluoride salts + neutrons → tritium (radioactive, leaks through metals)
- **Reprocessing online**: Chemically separating fission products complex and expensive
- **No operating commercial reactor**: Prototype only (MSRE, Oak Ridge, 1960s)

**Leading efforts**: Terrestrial Energy (Canada), ThorCon (Indonesia), Copenhagen Atomics (Denmark), Seaborg (Denmark), various Chinese programs

### Sodium-Cooled Fast Reactors (SFRs)

**Concept**: Liquid sodium coolant, no moderator (fast neutron spectrum), breeds Pu-239 from U-238.

**Advantages**:
- **Fuel breeding**: Can produce more fuel than consumed (breeding ratio >1.0), extending uranium resources 60-100x
- **Waste burning**: Can fission long-lived actinides from LWR spent fuel
- **High temperature**: ~550°C sodium outlet enables ~40% efficiency
- **Low pressure**: Sodium boils at 883°C, so operates ~atmospheric pressure

**Disadvantages**:
- **Sodium reactivity**: Burns in air, explodes in water — complex safety engineering
- **Proliferation**: Produces separated Pu-239
- **Economics**: Higher capital costs than LWRs, cheap uranium makes breeding economically unnecessary

**Operating reactors**: BN-800 (Russia, 880 MW), PFBR (India, 500 MW), experimental units in China and Russia

**Historical programs**: France (Superphénix, 1,200 MW, closed 1998), UK (Dounreay, closed 1994), US (Fermi-1, EBR-II, closed), Japan (Monju, closed 2016 after sodium fire and accidents)

### High-Temperature Gas Reactors (HTGRs)

**Concept**: Helium coolant, graphite moderator, TRISO fuel particles (ceramic-coated fuel pellets), 750-1,000°C outlet temperature.

**Advantages**:
- **Very high temperature**: 950°C enables industrial process heat (hydrogen production, steel, chemicals)
- **Passive safety**: TRISO fuel withstands 1,600°C; core geometry prevents overheating even without cooling
- **Efficiency**: ~45-50% electricity generation, or high-temperature steam for industry

**Disadvantages**:
- **Graphite dust**: Activated graphite particles in coolant complicate maintenance
- **Size limits**: Passive safety relies on surface-to-volume ratio, limiting size to ~200-300 MW
- **Fuel reprocessing difficult**: TRISO particles hard to separate for reprocessing

**Operating**: HTR-PM (China, 2 × 250 MW, operational 2023), earlier prototypes in Germany, Japan, US

### Fusion — The Distant Promise

**Reaction**: Deuterium + Tritium → Helium-4 + neutron + 17.6 MeV

```
²H + ³H → ⁴He (3.5 MeV) + n (14.1 MeV)
```

**Requirements**:
- Temperature: >100 million °C (10 keV) to overcome electromagnetic repulsion
- Pressure: >5 atmospheres in plasma
- Confinement time: >1 second (Lawson criterion: n·τ·T > 5×10²¹ m⁻³·s·keV)

**Approaches**:

**1. Magnetic confinement** (tokamak):
- Magnetic field (5-10 Tesla) confines plasma in torus shape
- Heat plasma with neutral beam injection, radiofrequency, ohmic heating
- **ITER** (France): 23,000 tonne tokamak, 25,000 m³ vacuum vessel, first plasma ~2035, fusion power ~2040, cost ~$25B+
- **Target**: Q = 10 (fusion power / input power = 10x gain)

**2. Inertial confinement** (NIF):
- 192 lasers (4 MJ) compress fuel pellet to extreme density/temperature
- **NIF** (National Ignition Facility, US) achieved ignition December 2022: fusion energy > laser energy (Q ~1.5)
- But total facility energy >> laser energy → Q_total ~0.01
- Path to power plant unclear (need ~10-30 ignitions per second, laser systems can't fire that fast)

**3. Private fusion ventures**:
- Commonwealth Fusion (high-temperature superconductor magnets → smaller tokamak)
- TAE Technologies (beam-driven field-reversed configuration)
- Helion (pulsed magnetic compression)
- Claims of 2030s deployment, but skepticism high — physics demonstrated, engineering enormous

**Challenges**:
- Plasma physics: Instabilities, energy confinement time
- Materials: Neutron bombardment damages reactor materials (10-20 MW/m² neutron flux)
- Tritium: Radioactive, scarce (must breed from lithium blanket)
- Economics: Even if physics works, will cost be competitive?

**Fusion timeline** (realistic): First demonstration power plant 2040s-2050s. Commercial deployment 2060s+, if ever.

## Nuclear Economics and Policy

### Capital Costs and Construction

| Reactor | Country | Capacity (MW) | Overnight Cost ($/kW) | Total Cost | Construction Time | Status |
|---------|---------|--------------|---------------------|-----------|-------------------|--------|
| **Vogtle 3&4** | US | 2,234 | ~$16,000/kW | ~$35B (from $14B estimate) | 15 years (from 7 estimated) | Operating 2023-2024 |
| **V.C. Summer 2&3** | US | 2,234 | N/A | ~$9B spent before cancellation | Abandoned 2017 | Canceled |
| **Hinkley Point C** | UK | 3,200 | ~$10,000/kW | ~£32B (~$40B) | 12+ years (ongoing) | Under construction |
| **Flamanville 3 (EPR)** | France | 1,650 | ~$12,000/kW | ~€19B (~$21B) | 17 years (started 2007, operational 2024) | Recently operational |
| **Barakah 1-4** | UAE | 5,600 | ~$4,000/kW | $24.4B | 9 years (on time) | Operating 2020-2024 |
| **Shin-Kori 3&4** | South Korea | 2,800 | ~$3,000/kW | ~$8.5B | 6 years (on time, on budget) | Operating 2016-2019 |
| **AP1000 (China)** | China | 1,100 each | ~$3,500/kW | ~$4B each | 9 years (first), 5-6 years (subsequent) | Multiple operating |

**Why such variance?**

**Success factors** (South Korea, China, UAE):
- Standardized designs (same reactor built multiple times)
- Sustained construction programs (workforce retention, learning curve)
- Streamlined regulatory processes (but not compromised safety)
- Government support and financing

**Failure factors** (US, Western Europe):
- **Regulatory instability**: Changing requirements mid-construction
- **Loss of skills**: No construction for 30+ years → workforce lost expertise
- **First-of-a-kind**: Every Western plant is custom or new design
- **Financing challenges**: Long construction + high capital → financing costs dominate

**Learning curves**: South Korea reduced cost 30% from 1st to 5th reactor. China building multiple AP1000s in 5-6 years after first took 9 years. France built 56 reactors in 15 years (1975-1990) on time/budget.

**Current reality**: Western nuclear construction costs $10,000-16,000/kW. East Asian costs $3,000-5,000/kW. This 3-5x difference determines nuclear's economic viability.

### Operating Costs and LCOE

**Operating costs** (mature plants):
- Fuel: $5-7/MWh (cheap — uranium price barely matters)
- Operations & maintenance: $20-30/MWh
- Total: $25-37/MWh

**Levelized Cost of Energy (LCOE)** (lifetime average cost per MWh):

| Source | LCOE ($/MWh) | Capacity Factor | Notes |
|--------|--------------|----------------|-------|
| Nuclear (Western new build) | $120-180 | 90% | Dominated by capital costs |
| Nuclear (East Asian new build) | $60-90 | 90% | Lower construction costs |
| Nuclear (existing plants) | $30-40 | 90% | Capital already paid off |
| Natural gas CCGT | $45-80 | 40-60% | Fuel price dependent |
| Onshore wind | $30-60 | 35% | No fuel costs |
| Solar PV (utility scale) | $30-50 | 25% | No fuel costs |
| Solar PV + 4hr battery | $50-80 | ~25% | Storage adds cost |

**Key insight**: New Western nuclear is expensive ($120-180/MWh). But existing nuclear is cheap ($30-40/MWh) — extends plant life to 60-80 years is economically attractive. The question is whether new builds can match East Asian costs or whether renewables + storage outcompete even cheap nuclear.

### Carbon Emissions

**Lifecycle emissions** (g CO₂-eq per kWh):
- Coal: ~900-1,000 g/kWh
- Natural gas: ~400-500 g/kWh
- Nuclear: ~12 g/kWh (uranium mining, enrichment, construction)
- Wind: ~11 g/kWh
- Solar PV: ~40 g/kWh (manufacturing, installation)
- Hydroelectric: ~24 g/kWh

Nuclear lifecycle emissions are comparable to renewables — orders of magnitude below fossil fuels.

### The Nuclear Dilemma

**Advantages**:
- Low-carbon baseload power (24/7, weather-independent)
- Extremely high energy density (small land footprint)
- Proven technology (11,000+ reactor-years experience)
- Low fuel costs (immune to commodity price swings)

**Disadvantages**:
- Very high capital costs (Western builds)
- Long construction times (Western builds)
- Catastrophic accident potential (even if rare)
- Unsolved waste disposal (politically, not technically)
- Proliferation risks (enrichment/reprocessing technology)
- Public opposition (post-Fukushima, NIMBY)

**Role in decarbonization**: Scenarios achieving net-zero emissions typically include nuclear providing 10-20% of electricity (double current ~10%). France demonstrates feasibility (70% nuclear, 10% hydro, 15% gas, 5% renewables → very low-carbon grid at ~40g CO₂/kWh vs ~400g for US or Germany).

But whether nuclear expands depends on solving construction cost and time problems. If Western nuclear remains $120-180/MWh, renewables + storage will dominate. If costs drop to East Asian levels ($60-90/MWh) through standardization and sustained programs, nuclear remains competitive as firm low-carbon power.

## Key Terms

- **Fission**: Splitting heavy nuclei (U-235, Pu-239), releasing ~200 MeV per atom
- **Fusion**: Combining light nuclei (D, T), releasing ~17.6 MeV per reaction
- **Critical**: Chain reaction sustaining itself (k = 1.000)
- **Supercritical**: Chain reaction increasing (k > 1)
- **Subcritical**: Chain reaction decreasing (k < 1)
- **Enrichment**: Increasing U-235 concentration above natural 0.72%
- **LEU**: Low Enriched Uranium (<20% U-235, typically 3-5% for reactors)
- **HEU**: Highly Enriched Uranium (>20% U-235, >90% for weapons)
- **SWU**: Separative Work Unit — measure of enrichment effort
- **Half-Life**: Time for half of radioactive atoms to decay
- **Spent Fuel**: Used nuclear fuel containing fission products, actinides, unused uranium
- **Defense in Depth**: Multiple independent safety barriers (fuel pellet, cladding, vessel, containment, distance)
- **LCOE**: Levelized Cost of Energy — lifetime average cost per MWh
- **PWR**: Pressurized Water Reactor — most common reactor type (~67% of global fleet)
- **BWR**: Boiling Water Reactor — water boils in core (~15% of fleet)
- **SMR**: Small Modular Reactor — factory-built, <300 MW
- **Breeding**: Creating more fissile material than consumed (e.g., U-238 → Pu-239)
- **Tokamak**: Magnetic confinement fusion device (toroidal shape)
- **TRISO**: Tri-structural isotropic fuel particle (ceramic-coated, high-temperature stable)
- **Yucca Mountain**: US designated geological repository (licensed but politically blocked)

## Summary

Nuclear energy harnesses atomic binding energy through fission, releasing ~2 million times more energy per kg than fossil fuels. Fission reactors maintain controlled chain reactions (k = 1), with PWRs dominating globally (~67% of 440 reactors worldwide). The fuel cycle from mining through enrichment (natural 0.72% U-235 → 3-5% LEU) to disposal raises proliferation concerns and waste management challenges.

Three major accidents — Three Mile Island (1979, zero public deaths, containment worked), Chernobyl (1986, ~30 acute deaths + 4,000 cancer deaths, design flaw + operator error), Fukushima (2011, ~1 radiation death, tsunami → station blackout) — demonstrate both nuclear's risks and that defense-in-depth can work when properly implemented. Statistical analysis shows nuclear has lowest mortality per TWh (~0.03 deaths/TWh vs ~25 for coal), but risk concentrates in rare catastrophic events.

Spent fuel contains ~95% unused uranium, ~3.5% fission products, ~1.5% transuranic actinides. After 300 years, radiotoxicity drops below natural uranium ore, but actinides keep it above background for 100,000+ years. Geological repositories (Finland's Onkalo under construction, Sweden's Forsmark approved, US Yucca Mountain politically blocked) provide technical solution, but political/public acceptance remains challenging.

Advanced reactors — SMRs (factory-built, <300 MW), molten salt (liquid fuel, cannot melt down), sodium fast breeders (extend uranium 60x, burn waste), high-temp gas (950°C for industrial heat) — promise improved safety, economics, and fuel efficiency. But first-of-a-kind costs remain high. Fusion remains decades away despite recent NIF ignition achievement (December 2022) — physics demonstrated, engineering and economics unproven.

Nuclear economics vary dramatically: Western new builds cost $120-180/MWh (Vogtle: $35B for 2.2 GW), East Asian builds $60-90/MWh (South Korea on-time/on-budget at $3,000/kW). Existing plants are cheap ($30-40/MWh) — extending plant life to 60-80 years is economically attractive. The industry's future depends on solving construction cost/time problems through standardization, sustained programs, and regulatory stability — or being outcompeted by renewables + storage.

Nuclear's role in decarbonization remains contested. It provides proven low-carbon baseload power but faces high costs (Western markets), waste disposal politics, proliferation concerns, and public opposition. Whether it expands beyond current ~10% of global electricity depends on matching East Asian construction performance and public acceptance that benefits (climate, energy security) outweigh risks (accidents, waste, proliferation).


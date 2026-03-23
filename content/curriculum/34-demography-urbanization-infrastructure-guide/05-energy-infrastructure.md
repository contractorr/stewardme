# Energy Infrastructure

## Power Grid Architecture

### Generation → Transmission → Distribution

**Generation (power plants):**
- Convert primary energy (coal, gas, nuclear, hydro, wind, solar) → electricity
- Typical large plant: 500-1,000 MW
- Global capacity: ~8,500 GW installed (2023)

**Transmission (high voltage, long distance):**
- Step up voltage to 115-765 kV to reduce losses (P = I²R; higher V → lower I → lower loss)
- High-voltage lines, towers, substations
- Typical loss: 2-6% over transmission
- HVDC (High Voltage Direct Current): Better for very long distances, undersea cables (e.g., NordLink: Norway-Germany, 623 km)

**Distribution (medium/low voltage, local):**
- Step down: 4-35 kV → 120/240V (residential)
- Poles, underground cables, transformers
- "Last mile" to homes and businesses
- Typical loss: 2-6% in distribution

**Total losses:** ~8-15% generation to consumption

### Grid Architecture Types
- **Centralized:** Large power plants → transmission network → distribution → consumers (traditional model)
- **Distributed:** Generation at or near point of use (rooftop solar, micro-wind, fuel cells)
- **Microgrid:** Self-contained local grid; can disconnect from main grid; military bases, campuses, island communities
- **Smart grid:** Digital communication overlaid on physical grid; real-time monitoring, demand response, bidirectional power flow

### Grid Operations: Technical Detail

**Frequency and Voltage Regulation**
- Grid frequency must stay at exactly 50 Hz (Europe/Asia/Africa) or 60 Hz (Americas/parts of Asia) ±0.5%
- Frequency drops when demand > supply (generators slow down); rises when supply > demand
- Deviation beyond ±2.5% → automatic load shedding or generator trip → potential blackout
- **Primary frequency response:** Automatic (governors on generators adjust within seconds)
- **Secondary (AGC):** Automatic Generation Control rebalances within minutes; centralised dispatch
- **Tertiary:** Manual dispatch of reserves; 10-30 minutes

**Voltage regulation:** Maintained through reactive power management; capacitor banks, synchronous condensers, tap-changing transformers; voltage sags/swells damage equipment

**Grid Interconnections**
- US has 3 separate grids: Eastern Interconnection, Western Interconnection, ERCOT (Texas); limited DC ties between them
- Europe: ENTSO-E synchronous area covers ~35 countries; one of world's largest synchronized machines
- Benefits of interconnection: Share reserves, smooth demand variations, access diverse generation; Texas isolation during Winter Storm Uri (2021) meant no help from neighbors
- HVDC links increasingly used to connect asynchronous grids: NordLink (Norway-Germany), IFA (UK-France), proposed Australia-Singapore Sun Cable (4,200 km)

**Electricity Markets**
- Wholesale markets: Day-ahead and real-time; generators bid to supply; cheapest dispatched first ("merit order")
- Merit order effect: Renewables bid at $0 marginal cost → push expensive gas/coal off the stack → lower wholesale prices; but intermittency complicates
- Capacity markets: Pay generators to be available (not just for energy produced); ensures reliability
- Ancillary services market: Frequency regulation, voltage support, black start capability — increasingly provided by batteries
- Retail rates: Residential customers pay $0.05-0.40/kWh depending on country; includes generation, transmission, distribution, taxes

**Demand Response**
- Shift electricity consumption to match supply rather than vice versa
- Industrial: Aluminum smelters, data centers can adjust load; paid to reduce consumption during peaks
- Residential: Smart thermostats, EV charging scheduled for off-peak; aggregated by virtual power plants
- Potential: 10-20% of peak demand shiftable; equivalent to building fewer peaking plants

---

## Global Energy Mix

### Primary Energy by Source (2023)

| Source | Share | Trend |
|---|---|---|
| Oil | ~31% | Slowly declining as % |
| Coal | ~26% | Declining in OECD; still growing in Asia |
| Natural gas | ~23% | Growing (bridge fuel narrative) |
| Hydroelectric | ~7% | Mature; limited growth potential |
| Nuclear | ~4% | Flat/declining; some new builds (China) |
| Wind | ~4% | Fastest growing |
| Solar | ~3% | Fastest cost decline |
| Bioenergy | ~2% | Biomass, biofuels |
| Other renewables | <1% | Geothermal, tidal, etc. |

**Fossil fuels still = ~80% of primary energy.** But declining as share; renewables growing exponentially.

### Electricity Generation (Different from Primary Energy)

| Source | Share of Global Electricity (2023) |
|---|---|
| Coal | ~35% |
| Natural gas | ~22% |
| Hydroelectric | ~15% |
| Nuclear | ~10% |
| Wind | ~8% |
| Solar | ~6% |
| Oil | ~3% |
| Other | ~1% |

**Renewables + nuclear = ~40% of electricity** (2023). Solar + wind growing ~20% annually.

---

## Base Load, Peak Load, and Dispatchability

| Concept | Definition | Technologies |
|---|---|---|
| **Base load** | Minimum constant demand (~40-60% of peak) | Nuclear, coal, gas (combined cycle), hydro |
| **Intermediate** | Follows daily demand curve | Gas (combined cycle), hydro |
| **Peak** | Maximum demand (hot afternoons, cold evenings) | Gas (peakers), hydro, batteries |
| **Variable/intermittent** | Output depends on weather/time | Solar, wind |
| **Dispatchable** | Can be turned on/off on demand | Gas, hydro, nuclear, batteries, biomass |

### The Duck Curve (California)
- Solar generation peaks midday → net demand drops
- Solar drops at sunset → net demand spikes (everyone turns on lights/AC)
- Creates steep "ramp" that dispatchable sources must fill
- Solution: batteries (store midday solar for evening), demand response, grid interconnection

---

## Renewable Integration Challenges

### Intermittency
- Solar: 0% at night; varies with clouds; capacity factor ~15-25%
- Wind: Varies with weather; capacity factor ~25-45%
- Compare: Nuclear ~90%, coal ~50-80%, gas ~30-60% capacity factor

### Storage Solutions

| Technology | Duration | Cost Trend | Status |
|---|---|---|---|
| Lithium-ion batteries | 1-4 hours | ↓ 90% since 2010 | Deployed at scale; dominant for short-duration |
| Pumped hydro | 8-24+ hours | Mature | ~95% of global storage; geography-limited |
| Iron-air batteries | 100+ hours | Early stage | Form Energy; potentially cheap long-duration |
| Compressed air (CAES) | 8-24 hours | Mature | Few installations; geology-dependent |
| Hydrogen (green) | Seasonal | Expensive; declining | Electrolysis + storage + fuel cell; ~30% round-trip efficiency |
| Gravity storage | 4-8 hours | Pilot stage | Energy Vault; crane/block systems |

### Grid Stability
- Grid must maintain 50/60 Hz frequency at all times
- Traditional: Large spinning generators provide inertia (resist frequency changes); spinning mass of turbine resists frequency deviations like a flywheel
- Renewables: Inverter-based; no inherent inertia → synthetic inertia needed; as renewable share rises, total system inertia falls → frequency more volatile
- Solutions: Grid-forming inverters (mimic synchronous generator behavior), synchronous condensers (spinning machines that provide inertia without generating), battery fast-frequency response (can respond in milliseconds vs seconds for thermal)
- **South Australia case study:** World's highest renewable penetration (~70%+ of electricity); installed Hornsdale Power Reserve (Tesla "big battery," 150 MW); battery responds to frequency deviations 100x faster than gas turbines; stabilized grid; paid for itself in ~2 years through ancillary services revenue
- **Ireland/Great Britain:** SNSP (System Non-Synchronous Penetration) limit — maximum instantaneous share of renewable/non-synchronous generation grid can handle while remaining stable; was 50%, raised to 75%; targeting higher; requires grid-forming inverter deployment
- **Curtailment:** When renewable output exceeds what grid can absorb → must be "curtailed" (wasted); California curtails ~5% of solar; Germany curtails wind; signals need for storage, transmission, demand flexibility

### Renewable Integration: Advanced Topics

**The "Three Ds" of Grid Transformation**
1. **Decarbonization:** Replacing fossil fuels with clean sources
2. **Decentralization:** From a few large plants to millions of small generators (rooftop solar, batteries, EVs)
3. **Digitalization:** Smart meters, SCADA systems, AI-based forecasting, automated grid management

**Transmission Buildout Challenge**
- Renewable resources often far from demand centers (wind in Great Plains, solar in deserts; demand in cities)
- US needs to roughly double transmission capacity by 2035 for net-zero pathway (DOE)
- Average US transmission line takes 10+ years from proposal to energization (permitting, land rights, NIMBYism)
- Germany's Energiewende bottleneck: Offshore wind in North Sea, demand in southern industry; north-south transmission lines years behind schedule; wind curtailment in north while coal burns in south
- China builds faster: ~40,000 km of UHV (ultra-high voltage) lines; transmits hydro from southwest, wind from northwest to coastal demand centers; authoritarian advantage in land acquisition

**Vehicle-to-Grid (V2G)**
- EVs as mobile batteries; 100M EVs with 60 kWh each = 6,000 GWh of distributed storage (vs ~100 GWh of utility-scale battery storage installed globally)
- Bidirectional charging: Car discharges to grid during peak demand; charges during off-peak/surplus renewable
- Technical barriers: Battery degradation concerns (mitigated by LFP chemistry), standardization, metering/billing complexity
- Pilots: UK, Netherlands, Japan; early but promising

**Seasonal Storage Problem**
- Daily storage (solar noon → evening peak) solvable with 4-hour lithium-ion
- Weekly storage (wind drought lasting days) needs 100+ hour storage
- Seasonal storage (summer surplus → winter demand) needs weeks-months; only candidates: hydrogen (electrolysis → storage → fuel cell), pumped hydro at huge scale, compressed air in salt caverns
- Hydrogen round-trip efficiency ~30-40% (electrolysis losses + compression + fuel cell); expensive but may be only option for seasonal balancing
- Alternative: Overbuild renewables + transmission interconnection across climate zones; Scandinavian hydro balances European wind/solar

---

## Nuclear Power

### How It Works
- Uranium-235 fission → heat → steam → turbine → electricity
- ~440 reactors in 32 countries; ~10% of global electricity
- Capacity factor ~90% (highest of any source); zero direct CO₂ emissions
- Fuel: Uranium enriched to 3-5% U-235 (natural uranium is 0.7% U-235)

### Safety
- **Three Mile Island (1979):** Partial meltdown; no deaths; led to improved safety culture
- **Chernobyl (1986):** Full meltdown + explosion; ~30 direct deaths; long-term cancer estimates debated (WHO: ~4,000 eventual; Greenpeace: much higher)
- **Fukushima (2011):** Tsunami overwhelmed backup power; 3 meltdowns; 1 direct death from radiation; ~2,200 deaths from evacuation stress
- Modern designs (Gen III+): Passive safety (shut down without power/human action); AP1000, EPR, VVER-1200

### Waste
- High-level waste: ~3,000 tonnes/year globally; highly radioactive for ~10,000+ years
- No permanent geological repository operating (Finland's Onkalo first, opening ~2025)
- Volume is small: All US nuclear waste ever produced fits on a football field ~10m deep
- Reprocessing: France recycles ~96% of spent fuel; US doesn't (proliferation concerns)

### Nuclear Renaissance?
- China building ~20+ reactors; India, UAE, Turkey, Egypt, Poland building
- Small Modular Reactors (SMRs): 50-300 MW; factory-built; potentially cheaper/faster; NuScale, Rolls-Royce SMR, X-energy
- Advanced reactors: Molten salt, high-temperature gas, sodium-cooled fast reactors
- Fusion: Still ~20 years away (as always); ITER under construction; private companies (Commonwealth Fusion, Helion)

---

## Coal

### Still Dominant in Electricity
- ~35% of global electricity; single largest source; ~8B tonnes mined/year
- China: ~50% of global coal consumption; 1,100+ coal plants; still building new ones (permits accelerated 2022-23)
- India: 2nd largest consumer; coal provides ~70% of electricity; abundant domestic reserves (less import-dependent than oil/gas)
- US: Coal dropped from ~50% of electricity (2005) → ~16% (2023); natural gas and renewables displaced
- EU: Coal declining sharply; Germany's Energiewende; UK went from 40% coal (2012) → <2% (2023); Poland still ~65% coal

### Coal Economics
- Cheapest fuel for baseload in many developing countries (if externalities unpriced)
- With carbon pricing: Uncompetitive vs renewables almost everywhere
- Stranded asset risk: $1T+ in coal infrastructure may be retired early; China's young fleet (average age ~14 years vs 40+ years in US) makes early retirement politically/financially harder
- Employment: ~6M direct coal jobs globally; transition politically difficult (Appalachia, Polish Silesia, Indian Jharkhand)
- "Just transition": Compensating coal communities for economic loss; $40B EU Just Transition Fund; US Inflation Reduction Act targeted at energy communities

---

## Oil & Gas Infrastructure

### Upstream (Extraction)
- Conventional: Drill wells into reservoirs; primary, secondary (water/gas injection), tertiary (enhanced) recovery
- Unconventional: Hydraulic fracturing (fracking) + horizontal drilling; unlocked US shale revolution (~2008-present)
- Offshore: Deepwater platforms (Gulf of Mexico, North Sea, Brazil pre-salt); expensive, technically challenging
- ~100M barrels/day global oil production (2023)

### Midstream (Transport)
- Pipelines: ~2.6M km globally; cheapest for large volumes over land; Keystone, Druzhba, Nord Stream
- Tankers: ~4,000 oil tankers; VLCCs carry ~2M barrels; maritime shipping handles ~60% of global oil trade
- LNG (Liquefied Natural Gas): Cool to -162°C → 1/600th volume; LNG terminals; fast-growing (Qatar, Australia, US top exporters)

### Downstream (Refining)
- Crude oil → gasoline, diesel, jet fuel, petrochemicals, plastics
- ~700 refineries globally; largest: Jamnagar (India) at 1.24M barrels/day
- Petrochemical industry: ~$600B/year; plastics, fertilizers, pharmaceuticals, synthetic materials

### Energy Security & Geopolitics
- OPEC+ controls ~40% of global supply; Saudi Arabia as swing producer
- Strait of Hormuz: ~21% of global oil passes through (20.5M barrels/day)
- Russia-Europe gas dependency: Nord Stream; weaponized in Ukraine war
- US shale: Made US world's largest oil/gas producer; reduced import dependence
- Petrostates: Countries dependent on oil revenue → Dutch disease, institutional weakness

---

## The Energy Transition

### Key Trends
- Solar cost: ↓ 99% since 1976; now cheapest electricity in history in many locations ($20-40/MWh)
- Wind cost: ↓ 70% since 2009
- Battery cost: ↓ 90% since 2010 ($1,100/kWh → ~$140/kWh)
- EV adoption: ~14% of global new car sales (2022); ~18% (2023)

### Challenges
- **Intermittency** (see above)
- **Grid infrastructure:** Built for centralized generation; needs massive investment for distributed renewables
- **Materials:** Lithium, cobalt, nickel, rare earths for batteries/magnets; concentrated supply chains (Congo cobalt, China rare earth processing)
- **Permitting/NIMBYism:** Transmission lines, wind farms, solar farms face local opposition
- **Developing world:** 675M without electricity; need energy growth + clean transition simultaneously
- **Industrial heat:** Steel, cement, chemicals need high temperatures; hard to electrify
- **Aviation/shipping:** No viable battery solution; hydrogen or synthetic fuels needed

### Hard-to-Abate Sectors

| Sector | % of Global Emissions | Why Hard | Leading Solutions |
|---|---|---|---|
| Steel | ~7% | 1,500°C+ needed; coking coal reduces iron ore | Green hydrogen DRI (HYBRIT, Sweden); electric arc furnaces with scrap |
| Cement | ~8% | Process emissions from limestone calcination (not just fuel) | Carbon capture; novel chemistries (LC3, geopolymer); efficiency |
| Chemicals/plastics | ~6% | Fossil feedstock (not just fuel) | Bio-based feedstock; electrification; green hydrogen |
| Aviation | ~2.5% | Energy density requires liquid fuel | SAF (sustainable aviation fuel); green hydrogen for short-haul |
| Shipping | ~3% | Long distances; heavy loads | Ammonia, methanol, LNG (transition); wind-assist (sails returning) |
| Agriculture | ~12% | Biological processes (methane, N₂O) | Methane inhibitors for cattle; precision fertilizer; diet change |

### Country Energy Transition Profiles

**China:** Largest emitter AND largest clean energy investor; installs more solar/wind than rest of world combined; but also building coal plants as backup/energy security; approach: "build everything" not "transition from"

**India:** 1.4B people; per-capita emissions 1/8th of US; energy demand growing 5%/year; committed to net-zero by 2070; massive solar buildout but coal dominant for decades; can't be expected to decarbonize at same pace as wealthy nations

**US:** 2nd largest emitter; Inflation Reduction Act ($370B clean energy subsidies) accelerated transition; but politically polarized; state-level variation enormous (Texas leads in both oil/gas AND wind)

**EU:** Most aggressive regulatory framework (EU ETS, Fit for 55, Carbon Border Adjustment Mechanism); per-capita emissions falling; but energy-intensive industry relocating ("carbon leakage"); dependency on imported gas exposed by Russia-Ukraine war

### Net Zero Pathways (IEA)
- Requires: ~$4 trillion/year clean energy investment by 2030 (up from ~$1.8T in 2023)
- No new fossil fuel exploration (controversial)
- Triple renewable capacity by 2030
- Double energy efficiency improvement rate
- Phase down unabated coal by 2040
- Net zero electricity in advanced economies by 2035
- **Reality check (Smil):** Every prior energy transition (wood→coal, coal→oil) took 50-70 years and the old fuel was never fully replaced; fossil fuels at 80% of primary energy; getting to 50% would be unprecedented speed; net-zero by 2050 requires transformation at pace never achieved

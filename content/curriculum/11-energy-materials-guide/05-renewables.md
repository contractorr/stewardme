# Renewable Energy

## Overview

Renewable energy — solar, wind, hydro, geothermal, biomass — harnesses natural energy flows rather than depleting finite fossil fuel stocks. Over the past 15 years, solar photovoltaics and wind turbines have experienced unprecedented cost declines, transforming them from expensive niche technologies to the cheapest sources of new electricity generation in most regions globally. But intermittency (sun doesn't always shine, wind doesn't always blow), energy storage limitations, and grid integration challenges remain fundamental constraints on achieving very high renewable penetration.

Understanding the physics of renewable energy conversion (photovoltaic effect, aerodynamic lift, hydr

ology), the engineering of generation systems (solar cells, wind turbines, turbines), the economics of rapidly declining costs, and the grid integration challenges is essential for evaluating decarbonization pathways and energy policy.

## Solar Photovoltaics

### The Photovoltaic Effect

Discovered by Edmond Becquerel in 1839 and explained by Einstein in 1905 (for which he won the Nobel Prize in 1921, not for relativity), the photovoltaic effect converts light directly to electricity via quantum mechanics.

**Mechanism**:
1. Photon with energy E = hf (h = Planck's constant, f = frequency) strikes semiconductor
2. If photon energy exceeds band gap (E_photon > E_gap), electron absorbs photon and jumps from valence band to conduction band
3. This creates electron-hole pair (electron in conduction band, hole in valence band)
4. Built-in electric field at p-n junction separates electron and hole before they recombine
5. Electrons flow to n-type side, holes to p-type side → voltage difference → current flows through external circuit

**Key insight**: This is quantum mechanical energy conversion, not thermal. Solar PV converts light to electricity without intermediate heat step, avoiding Carnot efficiency limits. But it faces different limits (Shockley-Queisser).

### Solar Cell Technologies

| Technology | Efficiency (lab/commercial) | Cost Trend | Material | Market Share | Notes |
|-----------|---------------------------|-----------|----------|--------------|-------|
| **Monocrystalline Si** | 26.7% / 20-22% | Dominant, falling | Single-crystal silicon | ~40% | High efficiency, established |
| **Polycrystalline Si** | 23.3% / 17-19% | Being replaced | Multi-crystal silicon | ~15% | Lower cost than mono (historically) |
| **PERC (mono)** | 25% / 22-23% | Growing fast | Si with passivated rear contact | ~30% | Efficiency boost over standard mono |
| **TOPCon** | 26% / 24-25% | Emerging | Tunnel oxide passivated contact | ~5% | Higher efficiency than PERC |
| **HJT (Heterojunction)** | 26.7% / 24-25% | Emerging | Si with a-Si:H layers | ~2% | High efficiency, low temp coefficient |
| **Thin-film CdTe** | 22.1% / 17-19% | Niche | Cadmium telluride | ~3% | First Solar, cheaper $/W |
| **CIGS** | 23.4% / 15-18% | Niche | Copper indium gallium selenide | <2% | Flexible substrates possible |
| **Perovskite** | 26.1% / ~18% | Research/pilot | Hybrid organic-inorganic | <1% | Rapid efficiency gains but stability issues |
| **Multi-junction** | 47.1% / 35-40% | Space, concentrators | III-V semiconductors (GaInP/GaAs/Ge) | <1% | Expensive (~$300/W), used in space |
| **Organic PV** | ~18% / ~10% | Research | Carbon-based | Negligible | Flexible, lightweight but low efficiency |

**Silicon dominance**: Crystalline silicon represents ~85% of global solar PV market. Advantages: abundant material (silicon is 2nd most abundant element in Earth's crust after oxygen), mature manufacturing, steadily improving efficiency. The industry has standardized on 166-210mm wafers, ~180-200μm thick.

**Module efficiency vs cell efficiency**: A cell achieves higher efficiency than a full module because modules include:
- Frame (aluminum)
- Glass (front cover)
- Encapsulant (EVA or POE)
- Backsheet (polymer or glass)
- Junction box and wiring
- Gaps between cells

Module efficiency typically ~90-95% of cell efficiency. Commercial module: 370-550W from ~2 m² → 18.5-27.5% module efficiency.

### Shockley-Queisser Limit

Fundamental physics limits single-junction solar cells. William Shockley and Hans Queisser (1961) calculated maximum efficiency for ideal single-junction cell under AM1.5 solar spectrum (standard terrestrial sunlight).

**Maximum efficiency**: ~33.7% for optimal bandgap (~1.34 eV, close to GaAs)

Silicon (bandgap 1.12 eV) has theoretical maximum ~32%. Best lab cell: 26.7% (2017, Kaneka). Commercial modules: 20-22%.

**Loss mechanisms**:
1. **Sub-bandgap photons** (~23% loss): Photons with energy below bandgap pass through without generating current. A silicon cell (1.12 eV bandgap) cannot absorb infrared photons with E < 1.12 eV (~1,100 nm wavelength).

2. **Above-bandgap excess energy** (~33% loss): Photons with E > E_gap generate electron-hole pairs, but excess energy (E_photon - E_gap) is lost as heat (phonons). A 3 eV photon (UV) generates the same single electron as a 1.2 eV photon (near-IR), wasting 1.8 eV as heat.

3. **Radiative recombination** (~7% loss): Some electron-hole pairs recombine, emitting photons that escape the cell. This is thermodynamically required (detailed balance).

4. **Thermodynamic losses** (~3% loss): Entropy generation from hot electrons thermalizing, contact resistance, etc.

**Exceeding Shockley-Queisser**:

**Multi-junction cells**: Stack semiconductors with different bandgaps. Top layer (wide bandgap) absorbs high-energy photons; lower layers absorb lower-energy photons that passed through. Each layer operates near its optimal bandgap, reducing thermalization losses.

GaInP (1.9 eV) / GaAs (1.4 eV) / Ge (0.7 eV) triple-junction: 39% efficiency (commercial), 47.1% (lab record, NREL). Used in space (where $/W matters less than W/kg) and concentrating PV (lenses focus sunlight 500-1000x onto tiny expensive cells).

**Tandem perovskite/silicon**: Perovskite top cell (1.6-1.8 eV bandgap) + silicon bottom (1.12 eV). Lab efficiency: 33.9% (2023), exceeding silicon's S-Q limit. If stability and manufacturing issues are solved, could reach 35-40% commercially at modest cost premium.

### Solar PV Economics and Swanson's Law

**Swanson's Law** (named after Richard Swanson, SunPower founder): Solar module prices fall ~20-24% for every doubling of cumulative production.

**Price decline**:
- 1976: ~$76/W (early satellites)
- 1980: ~$20/W
- 2000: ~$3.5/W
- 2010: ~$1.50/W
- 2020: ~$0.25/W
- 2023: ~$0.18-0.22/W (utility-scale modules)

**99.7% price reduction over 47 years**. This is one of the fastest cost declines in technological history, comparable to Moore's Law for semiconductors.

**Drivers**:
1. **Manufacturing scale**: Global production ~450 GW/year (2023) vs ~1 GW/year (2000) — 450x increase
2. **Module efficiency gains**: 15% → 21% average module efficiency doubles power per m²
3. **Wafer thickness**: 300μm → 180μm → reduces silicon material cost
4. **Supply chain integration**: Polysilicon production, ingot growth, wafering, cell fabrication, module assembly increasingly integrated and automated
5. **China's manufacturing dominance**: ~80% of global solar manufacturing capacity, driving economies of scale and competition

**Levelized Cost of Energy (LCOE)** (2023, utility-scale, unsubsidized):
- Best sites (sunny, cheap land): $24-36/MWh
- Average sites: $30-60/MWh
- Poor sites (cloudy, expensive land): $50-96/MWh

Compare to:
- New natural gas CCGT: $45-80/MWh (fuel price dependent)
- New coal: $65-150/MWh
- New nuclear: $120-180/MWh (Western builds)
- Existing nuclear/coal/gas: $25-50/MWh (capital already paid)

**Solar is now the cheapest new electricity source in regions with good solar resources**. But this ignores integration costs at high penetration (storage, backup capacity, transmission).

### Solar Capacity Factor and Intermittency

**Capacity factor**: Actual annual energy output / (nameplate capacity × 8,760 hours)

| Location | Capacity Factor | Annual kWh per kW installed | Equivalent full-sun hours/day |
|----------|----------------|---------------------------|------------------------------|
| Atacama Desert, Chile | ~28% | ~2,450 | 6.7 |
| Phoenix, Arizona | ~27% | ~2,365 | 6.5 |
| Southern California | ~26% | ~2,280 | 6.2 |
| Texas | ~24% | ~2,100 | 5.8 |
| North Carolina | ~20% | ~1,750 | 4.8 |
| Germany | ~12% | ~1,050 | 2.9 |
| UK | ~11% | ~965 | 2.6 |
| Equatorial regions (consistent) | ~18-22% | ~1,575-1,925 | 4.3-5.3 |

**Intermittency challenges**:
- **Diurnal**: Zero output at night (obviously). Peak output at solar noon (when sun is highest).
- **Seasonal**: Higher output in summer (longer days, higher sun angle); lower in winter.
- **Weather**: Clouds reduce output 50-90%. Heavy clouds: ~10-20% of clear-sky output.
- **Dust/soiling**: 1-5% annual degradation from dust, bird droppings, pollution.

**Duck curve** (California ISO's famous graph): Net load (demand minus solar/wind) creates duck-shaped curve:
- **Belly** (midday): Solar floods grid, net load drops, wholesale prices crash (sometimes negative)
- **Neck** (sunset, 5-8pm): Solar drops to zero, demand stays high, requires rapid ramping of gas plants
- **Head** (evening peak): Maximum conventional generation needed

California curtailed ~2.5 TWh (~5% of solar generation) in 2022 because midday generation exceeded demand + export capacity + storage capacity.

## Wind Energy

### Aerodynamics and Power Extraction

Wind turbines extract kinetic energy from moving air via aerodynamic lift on rotor blades (same principle as airplane wings).

**Power available in wind**:
```
P = ½ρAv³
```
Where:
- ρ = air density (~1.225 kg/m³ at sea level, 15°C)
- A = swept area of rotor (πr², where r = blade length)
- v = wind speed (m/s)

**Critical insight**: Power scales with **cube of wind speed**. Doubling wind speed → 8x power. This is why turbine size and height matter enormously — winds are stronger and more consistent at higher altitudes.

**Example**: 3 MW turbine, 100m rotor diameter (A = 7,854 m²)
- At 7 m/s wind: P_available = ½ × 1.225 × 7,854 × 7³ = 1.6 MW
- At 10 m/s wind: P_available = ½ × 1.225 × 7,854 × 10³ = 4.8 MW
- At 14 m/s wind: P_available = ½ × 1.225 × 7,854 × 14³ = 13.2 MW

But turbine is rated 3 MW — it reaches maximum power at ~11-12 m/s (rated wind speed) and then pitch control limits power to prevent overload.

### Betz Limit

**Albert Betz** (1919) calculated maximum fraction of wind's kinetic energy that a turbine can extract: **59.3%** (or 16/27).

**Derivation**: If turbine extracted 100% of wind's kinetic energy, air would stop moving behind turbine → no mass flow → no power. If turbine extracted 0%, it's not there. Optimal is removing enough energy to slow wind but maintaining flow. Calculus finds maximum at 16/27.

```
η_Betz = 16/27 ≈ 0.593 = 59.3%
```

**Real turbines**: Modern large turbines achieve ~45-50% of wind's kinetic energy (75-85% of Betz limit). Losses from:
- Blade aerodynamic imperfections
- Tip vortices (air flowing around blade tips)
- Gearbox and generator losses (~3-5%)
- Yaw and pitch control energy consumption

### Turbine Design Evolution

| Era | Rotor Diameter | Rated Power | Hub Height | Capacity Factor (onshore) | Typical Cost |
|-----|---------------|-------------|-----------|--------------------------|--------------|
| **1980s** | 15-30m | 50-150 kW | 25-40m | 20-25% | ~$2,000/kW |
| **1990s** | 30-50m | 500-750 kW | 40-60m | 22-28% | ~$1,500/kW |
| **2000s** | 50-80m | 1.5-2.5 MW | 60-100m | 25-32% | ~$1,200/kW |
| **2010s** | 80-120m | 2.5-4.5 MW | 80-140m | 28-38% | ~$1,000/kW |
| **2020s onshore** | 120-170m | 4-7 MW | 100-180m | 35-45% | ~$900/kW |
| **2020s offshore** | 160-240m | 8-15 MW | 100-150m | 42-55% | ~$1,500-2,000/kW |

**Size matters**: Larger turbines capture more energy for several reasons:
1. **Swept area scales as r²**: Doubling rotor diameter quadruples swept area
2. **Higher hub height**: Wind speed increases with height (wind shear). Rough rule: ~10-15% increase per 30m height.
3. **Economies of scale**: Power output grows faster than cost. A 5 MW turbine costs ~2x a 2.5 MW turbine but generates 2x power.

**Current giants**:
- **MingYang MySE 16-260**: 260m rotor diameter, 16 MW (offshore)
- **Vestas V236-15**: 236m rotor diameter, 15 MW (offshore)
- **GE Haliade-X**: 220m rotor diameter, 14 MW (offshore)

A single Vestas V236 rotation (one blade passing a point) sweeps ~43,700 m² — larger than 6 American football fields. At 45% capacity factor, one turbine generates ~59 GWh/year, equivalent to powering ~5,000 US homes.

### Onshore vs Offshore Wind

| Feature | Onshore | Offshore | Explanation |
|---------|---------|----------|-------------|
| **Turbine size** | 4-7 MW, up to 170m rotor | 8-15 MW, up to 260m rotor | Offshore: no transport limits, stronger structures |
| **Hub height** | 100-180m | 100-150m above sea level | Offshore water already provides elevation |
| **Capacity factor** | 30-45% (avg ~35%) | 42-55% (avg ~48%) | Offshore: stronger, more consistent winds |
| **LCOE** | $24-60/MWh | $60-120/MWh | Offshore: higher construction/maintenance costs |
| **Installation time** | 3-12 months | 12-24 months | Offshore: specialized vessels, weather delays |
| **Visual impact** | Significant (local opposition) | Minimal (20-100 km from shore) | Offshore: out of sight |
| **Maintenance** | Road accessible | Requires vessels, weather windows | Offshore: higher operating costs |
| **Grid connection** | Straightforward | Subsea HVAC or HVDC cables | Offshore: expensive undersea cables |
| **Environmental** | Bird/bat strikes, noise | Marine life disruption, fishing conflicts | Trade-offs differ |

**Offshore wind growth**: Global offshore capacity ~65 GW (2023), growing ~20-30% annually. Major markets: China (~50% of global), Europe (UK, Germany, Netherlands), Taiwan. US offshore is nascent (~40 MW operational, ~40 GW in development pipeline).

**Floating offshore wind** (emerging): For water depths >60m where fixed-bottom foundations become uneconomic. Floating platforms (spar, semi-submersible, tension-leg) can deploy in deep water (up to 1,000m). Opens vast ocean areas. Current cost: ~$130-200/MWh, target ~$60-90/MWh by 2030s.

### Wind Capacity Factor and Variability

**Wind speed distribution** follows **Weibull distribution** (not normal distribution). Most hours have moderate winds; rare hours have very high or very low winds.

**Power curve**: Turbine power output vs wind speed:
- **Cut-in speed** (~3-4 m/s): Turbine starts generating
- **Rated speed** (~11-13 m/s): Reaches maximum power
- **Cut-out speed** (~25-30 m/s): Turbine shuts down (storm protection)

**Variability challenges**:
- **Temporal**: Wind varies minute-to-minute (gusts), hour-to-hour (weather patterns), season-to-season (winter windier than summer in many regions)
- **Geographic**: Wind at different locations has different patterns — geographic diversity helps smooth output
- **Forecasting**: Modern forecasts predict wind output 1-48 hours ahead with ~5-10% error (RMSE). This allows grid operators to prepare but doesn't eliminate need for backup capacity.

**Wind droughts**: Multi-day periods of low wind across large regions. Example: European "Dunkelflaute" (dark doldrums) in January — simultaneous low wind and low solar in winter. Requires long-duration energy storage or firm backup power.

## Hydroelectric Power

### Types and Operating Principles

| Type | Description | Capacity Factor | Flexibility | Environmental Impact |
|------|-------------|----------------|-------------|---------------------|
| **Run-of-river** | Diverts river flow through turbines, minimal storage | 35-50% | Low (depends on river flow) | Low to moderate |
| **Reservoir (dam)** | Stores water behind dam, releases through turbines | 40-70% | High (dispatchable on demand) | High (flooding, fish migration, sediment) |
| **Pumped hydro storage** | Two reservoirs at different elevations | N/A (storage, not generation) | Very high (charge/discharge on demand) | Moderate (two reservoirs needed) |

**Conversion efficiency**: Hydro turbines are extremely efficient (~90-95%) compared to thermal plants (~33-60%). Potential energy of elevated water converts directly to mechanical energy without heat cycle.

**Power equation**:
```
P = ηρgQH
```
Where:
- η = turbine efficiency (~0.9)
- ρ = water density (1,000 kg/m³)
- g = gravitational acceleration (9.81 m/s²)
- Q = flow rate (m³/s)
- H = head (height difference, meters)

**Example — Hoover Dam**:
- Height: 221m (head)
- Maximum flow: 1,110 m³/s
- Efficiency: ~90%
- Power: 0.9 × 1,000 × 9.81 × 1,110 × 221 = **2,170 MW**
- Actual capacity: 2,080 MW (close to calculated)

### Global Hydroelectric Deployment

**Installed capacity** (2023): ~1,400 GW globally, generating ~4,200 TWh/year (~15% of global electricity)

**Top countries by capacity**:
1. China: ~400 GW (~30% of global capacity)
2. Brazil: ~110 GW
3. United States: ~102 GW
4. Canada: ~82 GW
5. India: ~52 GW

**Largest projects**:
- **Three Gorges Dam** (China): 22.5 GW capacity, 185m dam height, 663 km reservoir, ~100 TWh/year
- **Itaipu Dam** (Brazil/Paraguay): 14 GW, ~90 TWh/year
- **Belo Monte** (Brazil): 11.2 GW
- **Guri Dam** (Venezuela): 10.2 GW

**Resource constraints**: Most large-river sites in developed countries already exploited. Remaining potential is primarily in:
- Developing Asia (Himalayas, Mekong, Brahmaputra)
- Africa (Congo, Nile, Zambezi)
- South America (Amazon basin)

But these face environmental opposition, displacement concerns, and international water conflict risks (dams affect downstream countries).

### Pumped Hydro Storage

**Concept**: Use excess electricity to pump water uphill to upper reservoir. When electricity is needed, release water downhill through turbines.

**Round-trip efficiency**: 75-85% (best among large-scale storage technologies)

**Global capacity**: ~160 GW, representing ~95% of global grid-scale energy storage (by energy capacity, not power).

**Duration**: Typically 4-12 hours of storage at full power, but can be designed for longer (days to weeks) if reservoirs are large enough.

**Examples**:
- **Bath County** (Virginia, US): 3 GW power, 24 GWh energy (~8 hours), 850 ft elevation difference
- **Dinorwig** (Wales, UK): 1.7 GW, 9 GWh, 1,700 ft elevation
- **Tianhuangping** (China): 1.8 GW, 12 GWh

**Challenges**:
- Requires specific geography (two sites at different elevations, sufficient water)
- Large land area (reservoirs)
- Long development time (10-15 years including permitting, construction)
- Environmental impact (flooding, ecology)

**Emerging**: Closed-loop pumped hydro (no river connection), underground pumped hydro (abandoned mines), seawater pumped hydro (coastal cliffs).

## Geothermal Energy

### Resource Types

| Type | Temperature | Depth | Technology | Applications |
|------|-------------|-------|------------|--------------|
| **Hydrothermal** | 150-350°C | 1-3 km | Steam/flash plants | Electricity (baseload) |
| **Enhanced Geothermal Systems (EGS)** | 150-250°C | 3-10 km | Hydraulic fracturing of hot dry rock | Electricity (anywhere) |
| **Low-temperature** | 50-150°C | 0.2-2 km | Binary cycle, heat pumps | Electricity, direct heating |
| **Ground-source heat pumps** | 10-20°C | 2-100m | Heat exchangers | Building heating/cooling |

**Geothermal gradient**: Earth's temperature increases ~25-30°C per km depth (average). Higher in volcanic/tectonic regions (60-100°C/km), lower in stable cratons (15-20°C/km).

### Geothermal Electricity Generation

**Conventional hydrothermal** (steam/flash):
- Requires naturally occurring geothermal reservoir (fractured rock + water + heat)
- Typically along tectonic plate boundaries (Ring of Fire)
- Water at 200-350°C flashes to steam when pressure drops
- Steam drives turbines → electricity

**Enhanced Geothermal Systems (EGS)**:
- Drill into hot dry rock (3-10 km depth)
- Hydraulically fracture rock (similar to oil/gas fracking)
- Inject water; it circulates through fractures, heats up, returns to surface
- Extract heat via heat exchangers → binary cycle turbine

**Advantage**: Not limited to volcanic regions. Could work anywhere if drilling deep enough. US Department of Energy estimates >100 GW potential in US alone.

**Challenges**: Deep drilling expensive ($10-30M per well), induced seismicity concerns (fracturing can trigger small earthquakes), scaling/corrosion from mineral-rich fluids.

**Global capacity** (2023): ~16 GW, generating ~95 TWh/year (~0.3% of global electricity)

**Top countries**:
1. United States: ~3.7 GW (The Geysers in California: 1.5 GW)
2. Indonesia: ~2.3 GW
3. Philippines: ~1.9 GW
4. Turkey: ~1.7 GW
5. New Zealand: ~1.0 GW
6. Kenya: ~0.9 GW

**Capacity factor**: 85-95% (baseload operation, similar to nuclear). Geothermal is the only renewable besides hydro that provides dispatchable baseload power.

## Biomass and Biofuels

### EROEI Problems

Biofuels face fundamental thermodynamic and agricultural constraints. Photosynthesis is only 3-6% efficient at converting sunlight to chemical energy (stored in plant tissues). Further processing to liquid fuels adds energy costs.

| Biofuel | EROEI | Energy Input Sources | CO₂ Lifecycle (vs gasoline) | Assessment |
|---------|-------|---------------------|---------------------------|------------|
| **Corn ethanol (US)** | 1.0-1.6:1 | Diesel (tractors), natural gas (fertilizer, distillation) | ~10% reduction | Barely net-positive; policy-driven |
| **Sugarcane ethanol (Brazil)** | 5-8:1 | Mechanization, sugarcane bagasse burned for process heat | ~70% reduction | Much better due to tropical growing conditions |
| **Soybean biodiesel (US)** | 1.5-3:1 | Similar to corn | ~40% reduction | Land-intensive |
| **Cellulosic ethanol** | 2-6:1 (estimated) | Process heat, enzymes | ~80% reduction | Promises higher EROEI but commercially elusive |
| **Algae biodiesel** | 0.7-2:1 (current) | Cultivation, harvesting, oil extraction | Depends on input energy | Early stage; high hopes but low performance |

**Corn ethanol controversy**: US produces ~15 billion gallons/year of corn ethanol (~10% of gasoline pool by volume, ~7% by energy). Requires ~35-40% of US corn crop. Critics argue net energy gain is small, emissions reduction modest, and food price impact significant. Proponents argue it supports farmers, reduces petroleum dependence, and improves with technology.

**Brazil's success**: Sugarcane ethanol achieves EROEI 5-8:1 because:
- No irrigation needed (tropical rainfall)
- Bagasse (fibrous residue) burned for process heat (no external nat gas)
- More favorable growing season (year-round production possible)
- Higher sugar content than corn starch

Brazil's light vehicle fleet runs on flex-fuel engines (any ratio gasoline/ethanol). Ethanol provides ~40-45% of light vehicle fuel energy.

### Land Use Constraints

**Energy density of biofuel crops** (annual yield per hectare):

| Crop | Yield (tonnes/ha/year) | Energy Content (GJ/ha/year) | Gasoline Equivalent (barrels/ha/year) | Gallons ethanol/ha/year |
|------|----------------------|-------------------------|--------------------------------------|----------------------|
| Corn (US, for ethanol) | 10-12 (grain) | ~40-50 | ~7-8 | ~900-1,100 |
| Sugarcane (Brazil) | 70-80 | ~200-230 | ~33-38 | ~1,700-2,000 |
| Switchgrass (cellulosic, estimated) | 10-15 (dry biomass) | ~160-240 | ~26-40 | ~1,400-2,100 |
| Oil palm (biodiesel) | 4-5 (oil) | ~160-200 | ~26-33 | N/A (biodiesel) |
| Algae (optimistic projection) | ~50 (oil, theoretical) | ~1,800 | ~300 | N/A |

**Comparison to solar PV**:
- 1 hectare of solar PV in moderate location: ~1,500 MWh/year = 5,400 GJ/year = **100-270x more energy per hectare than corn ethanol**
- Even poor solar sites (Germany) produce ~15-30x more energy per hectare than best biofuel crops

**Implication**: Dedicating agricultural land to biofuels is far less efficient than solar PV for energy production. Biofuels only make sense where:
1. Using waste (crop residues, municipal waste, landfill gas)
2. High-value liquid fuel needed (aviation, where batteries don't work)
3. Agricultural co-benefits (nitrogen fixation, soil improvement)

**Global biofuel production** (2023): ~160 billion liters (~40 billion gallons) ethanol, ~55 billion liters biodiesel. Represents ~4% of global transport fuel.

**Sustainable Aviation Fuel (SAF)**: Aviation industry pursues biofuels because battery-electric aircraft face severe range/payload constraints. SAF from waste feedstocks (used cooking oil, agricultural residues, municipal waste) can reduce lifecycle emissions 60-80% vs jet fuel. But scaling to meet 10-30% of aviation fuel demand by 2030-2050 faces feedstock availability limits.

## The Intermittency Problem and Solutions

### The Duck Curve (California Example)

California's net load curve (demand minus solar/wind) creates famous "duck curve":

**Typical spring day**:
- 6am: Net load ~20 GW (low demand, no solar)
- 12pm: Net load ~12 GW (solar peak ~10 GW, demand ~22 GW) — **"belly"**
- 5pm: Net load ~20 GW (solar declining fast, demand steady)
- 8pm: Net load ~32 GW (solar zero, demand peaks) — **"head/neck"**

**Ramping requirement**: ~20 GW in 3 hours (5pm-8pm), ~100 MW/minute. This requires gas plants that can ramp quickly. Baseload plants (nuclear, coal) can't ramp fast enough.

**Curtailment**: On low-demand days (spring, mild weather), solar output midday exceeds demand + export + storage. California curtailed ~2.5 TWh in 2022 (~5% of solar generation). This represents wasted energy — built capacity that produces electricity nobody wants at that moment.

**Price impacts**: Wholesale electricity prices at solar peak drop to $0-20/MWh, sometimes negative (grid pays consumers to take power). Evening prices spike to $50-150/MWh. This "price arbitrage" opportunity drives battery storage deployment.

### Solutions to Intermittency

| Solution | Mechanism | Timescale | Status | Cost Impact |
|----------|-----------|-----------|--------|-------------|
| **Battery storage** | Store excess, discharge later | Hours (2-8h typical) | Rapidly scaling | +$10-30/MWh |
| **Long-duration storage** | Iron-air, flow batteries, hydrogen | Days to weeks | Early stage | +$30-80/MWh (projected) |
| **Demand response** | Shift load to match generation | Minutes to hours | Growing | -$5-15/MWh (saves cost) |
| **Geographic diversity** | Wind/solar different locations | Real-time smoothing | Requires transmission | +$5-15/MWh |
| **Overbuilding + curtailment** | Build excess capacity, waste surplus | Accept losses | Increasingly economic | +$10-25/MWh |
| **Firm clean power** | Nuclear, geothermal, hydro | Continuous baseload | Limited expansion | Depends on source |
| **Natural gas backup** | Keep gas plants for low-renewable periods | As needed | Current practice | Emissions compromise |

### Energy Storage Technologies

#### Lithium-Ion Batteries

| Chemistry | Cathode | Energy Density (Wh/kg) | Cycle Life | Cost ($/kWh) | Notes |
|-----------|---------|----------------------|------------|--------------|-------|
| **NMC (811)** | Ni₀.₈Mn₀.₁Co₀.₁O₂ | 200-260 | 1,000-2,000 | $130-180 | High energy density, EVs |
| **NMC (622)** | Ni₀.₆Mn₀.₂Co₀.₂O₂ | 180-220 | 1,500-2,500 | $130-170 | Balance of energy/life/cost |
| **NCA** | Ni₀.₈Co₀.₁₅Al₀.₀₅O₂ | 220-260 | 500-1,000 | $140-190 | Tesla, high energy density |
| **LFP** | LiFePO₄ | 130-160 | 3,000-10,000 | $90-130 | Long life, safe, no cobalt — **winning for grid** |
| **LTO (anode)** | Li₄Ti₅O₁₂ (vs graphite) | 70-100 | 10,000-20,000 | $200-350 | Ultra-long life, low energy density |

**LFP dominance in grid storage**: Lithium iron phosphate (LFP) has won the grid storage market despite lower energy density than NMC/NCA because:
1. **Cycle life**: 6,000-10,000 cycles vs 1,500-3,000 for NMC → lasts 15-25 years
2. **Safety**: Thermal runaway temp ~270°C vs ~210°C for NMC → safer
3. **Cost**: ~$90-130/kWh vs ~$130-180/kWh for NMC → cheaper
4. **No cobalt**: Avoids supply chain risk and human rights concerns (DRC cobalt mining)

**Weight doesn't matter for stationary storage** → LFP's lower energy density is irrelevant.

**Grid storage deployment**:
- 2015: ~1 GW / 1 GWh globally
- 2020: ~10 GW / 20 GWh
- 2023: ~40 GW / 100 GWh
- Projected 2030: ~300-500 GW / 800-1,500 GWh

**Duration**: Most grid batteries provide 2-4 hours storage (e.g., 100 MW / 400 MWh = 4 hours at full power). Some projects up to 8 hours. This is enough to shift solar from midday to evening peak but not to manage multi-day wind droughts.

#### Beyond Lithium-Ion

| Technology | Duration | Efficiency | Capital Cost ($/kWh) | Maturity | Advantages/Disadvantages |
|-----------|----------|-----------|---------------------|----------|------------------------|
| **Pumped hydro** | 4-24h | 75-85% | $50-200 | Mature | Proven technology; requires specific geography |
| **Compressed air (CAES)** | 8-24h | 50-70% | $50-150 | Commercial (2 plants) | Large scale possible; low efficiency, requires underground cavern |
| **Liquid air (LAES)** | 4-12h | 50-70% | $100-250 | Pilot stage | No geography limits; cryogenic complexity |
| **Flow batteries (vanadium)** | 4-12h | 65-80% | $150-400 | Commercial | Decoupled power/energy, long life; expensive, low energy density |
| **Iron-air battery** | 100+ hours | ~50% | Target $20 (long-term) | Prototype (Form Energy) | Extremely cheap per kWh; low efficiency, slow response |
| **Hydrogen (electrolysis + fuel cell)** | Days to months | 30-40% (round-trip) | $300-600 | Pilot | Seasonal storage; terrible efficiency, expensive |
| **Hydrogen (electrolysis + combustion)** | Days to months | 30-35% | $200-400 | Proven (existing gas turbines) | Can use existing infrastructure; emissions compromise if not 100% H₂ |
| **Thermal storage (molten salt)** | 6-18h | 90%+ (heat-heat) | $15-50 | Commercial (CSP plants) | High efficiency for heat storage; not suitable for general grid storage |

**The duration gap**: Lithium-ion handles 2-6 hours economically. Pumped hydro can do 8-24 hours but requires geography. Multi-day to seasonal storage (managing winter solar shortfall, multi-day wind droughts) remains expensive and inefficient.

**Hydrogen for seasonal storage**: Excess summer solar → electrolysis → hydrogen storage → winter combustion or fuel cells. Round-trip efficiency ~30-40% is terrible compared to batteries (~90%), but for seasonal storage, low cycle frequency (10-50 cycles/year vs 300+ for daily cycling) makes per-cycle cost acceptable. Key challenge: cost (electrolyzers, storage, fuel cells).

## Key Terms

- **Photovoltaic Effect**: Light generating electricity in semiconductors via electron excitation across bandgap
- **Shockley-Queisser Limit**: ~33.7% maximum efficiency for single-junction solar cells
- **Swanson's Law**: Solar module costs fall ~20% per doubling of cumulative production
- **Betz Limit**: ~59.3% (16/27) maximum fraction of wind's kinetic energy extractable by turbine
- **Capacity Factor**: Actual annual energy output / (nameplate capacity × 8,760 hours)
- **LCOE**: Levelized Cost of Energy — total lifetime cost per MWh
- **Duck Curve**: Net load shape with solar midday dip and steep evening ramp
- **Curtailment**: Wasting excess renewable generation when it exceeds demand + exports + storage
- **LFP**: Lithium Iron Phosphate — dominant grid storage chemistry (long life, safe, cheap)
- **Pumped Hydro**: ~95% of global grid-scale storage by energy capacity
- **EROEI**: Energy Return on Energy Invested — critical for biofuels
- **Intermittency**: Variable output of renewables depending on weather/time
- **Firm Power**: Generation that can reliably deliver on demand (nuclear, hydro, geothermal, gas)
- **Demand Response**: Shifting electricity consumption in time to match renewable generation
- **Geographic Diversity**: Wind and solar in different locations provide smoother aggregate output

## Summary

Solar PV and wind turbines have experienced unprecedented cost declines over 15 years, making them the cheapest new electricity sources in most regions. Solar module prices fell 99.7% since 1976 (Swanson's Law: ~20% per doubling of production), reaching $0.18-0.22/W in 2023. LCOE for utility solar: $24-60/MWh; onshore wind: $24-60/MWh — often cheaper than fossil alternatives.

Solar PV converts light directly to electricity via the photovoltaic effect, avoiding Carnot limits but facing Shockley-Queisser limit (~33.7% for single-junction cells). Best commercial silicon modules achieve 20-22% efficiency, approaching the 32% theoretical maximum. Multi-junction cells (47% lab record) exceed S-Q by using multiple bandgaps but cost 100-1000x more per watt.

Wind turbines extract kinetic energy from moving air. Power scales as velocity cubed (P ∝ v³), so doubling wind speed yields 8x power — height and site selection are critical. Betz limit caps extraction at 59.3%; modern turbines achieve 45-50%. Turbine size has grown dramatically: 1980s (50 kW, 15m rotor) → 2020s onshore (6 MW, 170m) → 2020s offshore (15 MW, 240m). Larger turbines achieve higher capacity factors (offshore: 48%, good onshore sites: 40%).

Hydroelectric provides ~15% of global electricity (4,200 TWh/year) with very high efficiency (~90-95% turbine efficiency) and flexibility. But most large-river sites in developed countries are already exploited. Pumped hydro represents ~95% of grid-scale energy storage (160 GW globally) with 75-85% round-trip efficiency, but requires specific geography.

Geothermal provides baseload power (85-95% capacity factor) but limited to specific geographies (conventional) or expensive deep drilling (EGS). Current deployment: ~16 GW globally (~0.3% of electricity). Enhanced Geothermal Systems could unlock >100 GW in US alone if deep drilling costs decline.

Biofuels face hard EROEI and land-use constraints. Corn ethanol (US): 1.0-1.6:1 EROEI, barely net-positive, uses 35% of US corn crop. Sugarcane ethanol (Brazil): 5-8:1 EROEI, much better due to tropical conditions. Solar PV on the same land produces 100-270x more energy than biofuel crops — biofuels only make sense for hard-to-electrify sectors (aviation) or waste feedstocks.

Intermittency is the central challenge: solar produces nothing at night, wind varies unpredictably. California's "duck curve" demonstrates the problem — midday solar surplus (curtailment) followed by rapid evening ramp. Solutions include battery storage (rapidly scaling: 40 GW / 100 GWh globally in 2023), demand response, geographic diversity, overbuilding + curtailment, and firm clean power (nuclear, geothermal, hydro).

Lithium-ion batteries (especially LFP) dominate short-duration storage (2-6 hours, round-trip efficiency ~90%). Long-duration storage (days to weeks) for managing multi-day wind droughts or winter solar shortfalls remains expensive and inefficient. Hydrogen, flow batteries, compressed air, and iron-air batteries compete for this niche, with round-trip efficiencies 30-70%.

Achieving 80-100% renewable electricity requires solving storage and grid integration at unprecedented scale. Portfolios combining multiple solutions (batteries, hydrogen, geographic diversity, demand response, overbuilding, firm clean backup) will likely be necessary rather than any single technology.


# Natural Hazards

## Overview

Geological hazards kill tens of thousands annually, displace millions, and cause hundreds of billions in economic losses. Understanding these hazards enables better prediction, mitigation, and response.

**Major geological hazards by annual average deaths** (2000-2020):
1. Earthquakes: ~40,000/year (highly variable—dominated by rare megaquakes)
2. Floods: ~6,000/year (many triggered by geological factors)
3. Landslides: ~5,000/year
4. Volcanic eruptions: ~600/year (average—massive outliers possible)
5. Tsunamis: ~6,000/year (dominated by 2004 event)

**Economic losses**: $100-300 billion/year on average, with exceptional years exceeding $500 billion.

## Earthquakes

### Mechanisms and Measurement

**Elastic rebound theory**:
1. Tectonic forces gradually bend rock across fault
2. Friction prevents slip → stress accumulates
3. Stress exceeds friction → sudden rupture
4. Rock snaps back to unstrained shape
5. Energy released as seismic waves

**Seismic waves**:
- **P-waves** (primary): Compress-expand, travel through all materials, fastest (5-14 km/s), least damaging
- **S-waves** (secondary): Shear, solids only, slower (3-7 km/s), more damaging
- **Surface waves**: Slowest, largest amplitude, cause most damage
  - Love waves: Horizontal shearing
  - Rayleigh waves: Rolling motion

**Moment magnitude (Mw)**:
```
Mw = (2/3) log₁₀(M₀) - 10.7
M₀ = μ × A × D
```
Where M₀ = seismic moment, μ = rock rigidity, A = fault area, D = slip

**Energy scaling**: Each magnitude unit = 32× more energy
- M5: ~1,000 per year globally
- M6: ~150 per year
- M7: ~15 per year
- M8: ~1-2 per year
- M9: ~1 per decade

**Historic megaquakes**:
| Event | Year | Magnitude | Deaths | Key Impact |
|-------|------|-----------|--------|------------|
| **Valdivia, Chile** | 1960 | 9.5 | ~6,000 | Largest recorded; tsunami reached Hawaii, Japan |
| **Prince William Sound, Alaska** | 1964 | 9.2 | 131 | Tsunami, ground liquefaction |
| **Sumatra-Andaman** | 2004 | 9.1 | ~230,000 | Indian Ocean tsunami; 14 countries affected |
| **Tōhoku, Japan** | 2011 | 9.1 | ~18,500 | 40m tsunami, Fukushima nuclear disaster |
| **Kamchatka, Russia** | 1952 | 9.0 | 0 | Remote location, tsunami |
| **Cascadia** | 1700 | ~9.0 | Unknown | Geological record + Japanese tsunami records |
| **Lisbon, Portugal** | 1755 | ~8.5-9.0 | 60,000 | Destroyed city, tsunami, fires |

### Earthquake Hazards

**1. Ground shaking**:
- **Intensity** (Modified Mercalli scale I-XII): Qualitative damage assessment
  - IV: Felt widely, dishes rattle
  - VI: Slight structural damage
  - VIII: Substantial damage to buildings
  - X: Most buildings destroyed
  - XII: Total devastation, objects thrown into air
- **Peak Ground Acceleration (PGA)**: Maximum acceleration as % of g
  - <10% g: Minor damage
  - 10-30% g: Moderate damage to unreinforced structures
  - >50% g: Severe damage even to well-built structures
- **Duration**: Long shaking (60-90 seconds for M9) causes cumulative damage

**2. Liquefaction**:
- Saturated loose sediment (sand) loses strength during shaking
- Pore water pressure increases → grains separate → behaves as liquid
- **Effects**:
  - Buildings sink, tilt, collapse
  - Underground tanks float upward
  - Lateral spreading on slopes
- **1964 Niigata, Japan**: Apartment buildings toppled intact onto sides
- **1989 Loma Prieta, California**: Marina District built on fill liquefied
- **Mitigation**: Avoid building on unconsolidated sediment, or use deep foundations (piles to bedrock)

**3. Landslides**:
- Shaking triggers slope failures
- **2008 Wenchuan, China (M7.9)**: >15,000 landslides, blocked rivers → landslide dams → outburst floods
- **1970 Ancash, Peru (M7.9)**: Avalanche buried town of Yungay, 70,000 deaths
- **Secondary hazard**: Landslide dams can collapse weeks-months later

**4. Fire**:
- Ruptured gas lines ignite
- Water mains broken → firefighting impossible
- **1906 San Francisco (M7.9)**: Fire caused 90% of damage; burned 3 days; 80% of city destroyed; ~3,000 deaths
- **1923 Great Kanto, Tokyo (M7.9)**: Firestorms from cooking fires (lunchtime quake), 105,000 deaths (mostly burns/asphyxiation)

**5. Tsunamis** (covered separately below)

### Earthquake Prediction vs Forecasting

**Short-term prediction** (days-weeks): **Not currently possible with reliability**

**Why it's hard**:
- Faults are complex, heterogeneous
- Triggering mechanisms not fully understood
- Precursors (foreshocks, radon emissions, animal behavior) are unreliable
- **False alarm problem**: High false alarm rate destroys credibility, economic disruption

**Rare successes**:
- **1975 Haicheng, China**: Foreshock swarm → evacuation ordered → M7.3 quake hours later → many lives saved
  - **But**: Next major quake (1976 Tangshan, M7.6) had no foreshocks, 240,000 died, no warning
  - Foreshocks are not universal precursors

**Failures and controversies**:
- **2009 L'Aquila, Italy**: Scientists convicted (later acquitted) for downplaying risk before M6.3 quake (309 deaths)
  - **Issue**: Not charged with failing to predict, but with "false reassurance" causing residents to stay indoors

**Long-term forecasting** (decades): **Possible via probability**

**Methods**:
1. **Seismic gap theory**: Segments of fault that haven't ruptured in long time are "overdue"
   - **Cascadia subduction zone**: Last rupture 1700, recurrence ~300-600 years → high probability next few centuries
   - **Nankai Trough, Japan**: ~100-150 year cycle, last ruptured 1946 → elevated risk
2. **Paleoseismology**: Study prehistoric earthquakes via trenching, dating offset layers
   - San Andreas (Carrizo Plain): 1857, 1812, ~1400s pattern → ~100-150 year recurrence
3. **Probabilistic hazard maps**: "X% chance of M≥Y in Z years"
   - USGS: "70% chance of M≥6.7 in Bay Area in next 30 years"
   - Used for building codes, insurance rates

**Earthquake early warning** (seconds to tens of seconds):
- Detect P-waves (fast, weak) → warn before S-waves/surface waves (slow, damaging) arrive
- **Lead time**: Seconds to ~minute depending on distance
- **Uses**: Stop trains, close gas valves, duck-cover-hold, pause surgeries
- **Systems**:
  - **Japan**: Operational since 2007; warned 8-30 seconds before Tōhoku 2011 shaking
  - **ShakeAlert (US West Coast)**: Operational 2021; California, Oregon, Washington

### Mitigation

**Building codes**: Most effective mitigation
- **Seismic design principles**:
  - **Strength**: Resist moderate shaking without damage
  - **Ductility**: Bend without breaking during severe shaking
  - **Redundancy**: Multiple load paths
- **Techniques**:
  - Reinforced concrete/steel frames
  - Shear walls, cross-bracing
  - Base isolation (building sits on flexible pads)
  - Dampers (absorb energy)
- **Success**: 1989 Loma Prieta (M6.9) killed 63; 1988 Armenia (M6.9) killed 25,000—difference is building quality

**Land use planning**:
- Avoid building on:
  - Active fault traces (surface rupture)
  - Liquefiable soils
  - Steep slopes (landslide prone)
  - Soft sediments (amplify shaking)

**Emergency preparedness**:
- Earthquake drills (ShakeOut)
- Emergency supplies (water, food, medical, radio)
- Communication plans

## Volcanic Eruptions

### Types and Explosivity

**Volcanic Explosivity Index (VEI)**: 0-8 logarithmic scale

| VEI | Ejecta Volume | Plume Height | Description | Frequency | Examples |
|-----|---------------|--------------|-------------|-----------|----------|
| 0 | <10⁴ m³ | <100 m | Effusive | Daily | Kilauea (Hawaii) continuous |
| 1 | >10⁴ m³ | 100-1,000 m | Gentle | Daily | Stromboli (Italy) |
| 2 | >10⁶ m³ | 1-5 km | Explosive | Weekly | Piton de la Fournaise |
| 3 | >10⁷ m³ | 3-15 km | Severe | 1/month | Ruiz (Colombia) 1985 |
| 4 | >0.1 km³ | 10-25 km | Cataclysmic | ~15/year | Eyjafjallajökull 2010 |
| 5 | >1 km³ | >25 km | Paroxysmal | ~2/decade | Mt. St. Helens 1980, Pinatubo 1991 |
| 6 | >10 km³ | >25 km | Colossal | ~1/century | Krakatoa 1883, Novarupta 1912 |
| 7 | >100 km³ | >25 km | Super-colossal | ~1/1,000 yr | Tambora 1815 (last VEI-7) |
| 8 | >1,000 km³ | >25 km | Apocalyptic | ~1/100,000 yr | Yellowstone 640ka, Toba 74ka |

**What controls explosivity?**

**1. Magma composition**:
- **Felsic** (rhyolite, >70% SiO₂): High viscosity, traps gases → explosive
  - Mt. St. Helens, Pinatubo, Yellowstone
- **Intermediate** (andesite, 55-65% SiO₂): Moderate viscosity → variable explosivity
  - Cascades, Andes, Japan
- **Mafic** (basalt, <52% SiO₂): Low viscosity, gases escape easily → effusive
  - Hawaii, Iceland, mid-ocean ridges

**2. Gas content**:
- H₂O, CO₂, SO₂ dissolved under pressure
- At surface, pressure drops → gases exsolve (like opening soda bottle)
- High gas → fragmentation → explosive eruption
- Low gas → lava flows

**3. Vent geometry**:
- Open vent → gas escapes → effusive
- Blocked vent → pressure builds → explosive

### Volcanic Hazards

**1. Pyroclastic flows** (most lethal):
- Avalanche of hot gas, ash, rock fragments (500-1,000°C)
- Speed: 100-700 km/h
- Density: Denser than air, follows valleys
- **Incineration**: Everything in path destroyed
- **79 CE Pompeii/Herculaneum**: Mt. Vesuvius pyroclastic flow buried cities, ~16,000 deaths
- **1902 Mt. Pelée, Martinique**: Pyroclastic flow destroyed St. Pierre, 29,000 deaths (only 2 survivors in entire city)
- **1991 Unzen, Japan**: Pyroclastic flow killed 43 (including volcanologists Harry Glicken, Katia & Maurice Krafft)

**2. Lahars** (volcanic mudflows):
- Mixture of water + volcanic debris (ash, rock)
- Triggered by:
  - Eruption melts snow/ice (glaciated volcanoes)
  - Heavy rain mobilizes loose ash
  - Crater lake breach
- Speed: 30-60 km/h in valleys
- Consistency: Wet concrete
- **1985 Nevado del Ruiz, Colombia**: Small eruption melted glaciers → lahar traveled 100 km → buried town of Armero → 23,000 deaths
  - **Tragedy**: Scientists issued warnings, but authorities failed to evacuate

**3. Ashfall**:
- Tiny rock/glass fragments ejected into atmosphere
- **Immediate impacts**:
  - Collapses roofs (ash is heavy: 1 m ash = 1,000 kg/m²)
  - Respiratory problems
  - Contaminates water
  - Blocks roads
  - Clogs machinery
- **Aviation hazard**: Ash melts in jet engines (1,400°C), refreezes on turbine blades → engine failure
  - **1982 British Airways Flight 9**: Boeing 747 flew through Galunggung (Indonesia) ash cloud → all 4 engines failed → glided 25 minutes before restarting engines below cloud
  - **2010 Eyjafjallajökull, Iceland**: 100,000 flights canceled, 10 million passengers stranded, $1.7 billion economic loss
- **Climate impacts**: Sulfate aerosols reflect sunlight → cooling (1-3 years)

**4. Lava flows**:
- Slow (1-30 km/h) but unstoppable
- Destroy everything in path (burn, crush, bury)
- Rarely kill people (can outrun) but destroy property
- **2018 Kilauea, Hawaii**: Lower Puna eruption destroyed 700 homes, $800 million damage

**5. Volcanic gases**:
- **CO₂**: Heavier than air, accumulates in low areas, asphyxiation
  - **1986 Lake Nyos, Cameroon**: CO₂ erupted from crater lake (limnic eruption) → dense cloud flowed downhill → 1,700 deaths (suffocation in sleep)
- **SO₂**: Acid rain, respiratory irritation
- **H₂S**: Toxic at high concentrations
- **HF**: Toxic, contaminates vegetation (livestock poisoning)

**6. Tsunamis**:
- Submarine/coastal eruptions displace water
- **1883 Krakatoa, Indonesia**: Eruption + caldera collapse → tsunami 40 m high → 36,000 deaths
- **1792 Unzen, Japan**: Flank collapse → tsunami → 15,000 deaths (worst volcanic disaster in Japan)

### Super-Eruptions and Climate

**Super-eruptions** (VEI-7/8): Eject >100 km³ material

**Known VEI-8 eruptions** (last 2 Ma):
- **Toba, Indonesia** (74,000 years ago): 2,800 km³ ejecta
  - **Volcanic winter**: ~10-15 years of cooling
  - **Genetic bottleneck hypothesis**: Human population crashed to ~1,000-10,000 individuals (debated)
- **Yellowstone**:
  - Huckleberry Ridge (2.1 Ma): 2,500 km³
  - Mesa Falls (1.3 Ma): 280 km³
  - Lava Creek (640 ka): 1,000 km³
  - **Pattern**: ~600-800 ka recurrence (but not predictable like clockwork)
  - **Current hazard**: Low probability (~0.001% per year), but catastrophic if occurs

**Volcanic winter mechanism**:
1. Explosive eruption injects SO₂ into stratosphere (>10 km altitude)
2. SO₂ + H₂O → sulfate aerosols (H₂SO₄ droplets)
3. Aerosols reflect sunlight → surface cooling
4. Stratospheric aerosols persist 1-3 years (tropospheric rain out quickly)
5. **Cooling**: 0.5-5°C depending on eruption size

**Historic examples**:
- **1815 Tambora, Indonesia (VEI-7)**: 160 km³ ejecta
  - **1816 "Year Without Summer"**: Crop failures, famine in Europe/North America, snow in June (northeastern US)
  - Global cooling ~0.5-0.7°C
  - 71,000 direct deaths (pyroclastic flows, ash), ~100,000 indirect (famine, disease)
- **1883 Krakatoa (VEI-6)**: 20 km³ ejecta
  - Global cooling ~0.3°C for 1 year
  - Vivid sunsets globally (aerosols scatter light)
  - Inspiring Edvard Munch's "The Scream"
- **1991 Pinatubo, Philippines (VEI-6)**: 10 km³ ejecta
  - 20 million tonnes SO₂ → stratosphere
  - Global cooling ~0.5°C for 2 years
  - Ozone depletion
  - 847 deaths (lahars, roof collapses, disease)

### Monitoring and Forecasting

**Volcanic precursors** (days to months):

**1. Seismicity**:
- Magma movement fractures rock → earthquakes
- **Types**:
  - Long-period (LP): Resonating fluid-filled cracks
  - Volcanic tremor: Continuous shaking
  - Volcano-tectonic (VT): Rock fracture
- **Pattern**: Increasing frequency + amplitude = magma rising

**2. Ground deformation**:
- Magma inflation swells volcano
- Measured by GPS, tiltmeters, InSAR (satellite radar)
- **1980 Mt. St. Helens**: North flank bulged 140 m (2 m/day in late April)

**3. Gas emissions**:
- Increasing SO₂, CO₂ = fresh magma degassing
- Remote sensing (COSPEC, DOAS instruments)

**4. Thermal anomalies**:
- Hot springs increase temperature
- Fumaroles (steam vents) activate
- Satellite thermal imaging

**Success stories**:
- **1991 Pinatubo**: 75,000 evacuated based on seismicity, deformation, gas → saved ~5,000-20,000 lives
- **2010 Eyjafjallajökull**: Aviation warnings based on seismicity → no plane crashes

**Challenges**:
- **False alarms**: Many unrest episodes don't lead to eruption
- **Short timescales**: Explosions can occur hours after warning signs
- **Social factors**: Evacuation fatigue, economic pressure to stay

## Landslides and Mass Wasting

**Mass wasting**: Downslope movement of rock, soil, debris under gravity.

### Types

**Classification** by speed and material:

| Type | Speed | Material | Water Content | Trigger |
|------|-------|----------|---------------|---------|
| **Rock fall** | Very fast (m/s) | Bedrock | Dry | Weathering, seismic shaking |
| **Rock avalanche** | Very fast (10-100+ m/s) | Fragmented bedrock | Dry-moist | Earthquakes, oversteepening |
| **Debris avalanche** | Very fast (10-50 m/s) | Mixed rock, soil, vegetation | Moist | Volcanoes, earthquakes |
| **Debris flow** | Fast (1-10 m/s) | Mixed debris | Saturated | Heavy rain, snowmelt |
| **Mudflow** | Fast-moderate (0.1-10 m/s) | Fine sediment (clay, silt) | Very wet | Heavy rain, volcanic |
| **Slump** | Slow (cm-m/day) | Coherent mass | Variable | Saturation, undercutting |
| **Earth flow** | Slow (mm-m/day) | Clay-rich soil | Wet | Saturation, thawing |
| **Creep** | Very slow (mm/year) | Soil, regolith | Variable | Cycles (freeze-thaw, wet-dry) |

### Factors Controlling Slope Stability

**Driving force**: Gravity (weight of material)
**Resisting force**: Friction + cohesion

**Factor of Safety (FS)**:
```
FS = Resisting Forces / Driving Forces
FS > 1: Stable
FS = 1: Critically stable
FS < 1: Failure
```

**What decreases stability (decreases FS)?**

**1. Slope angle**:
- Steeper slope → larger component of gravity parallel to slope
- **Angle of repose**: Maximum stable angle (dry sand ~32-34°, wet clay ~10-20°)

**2. Water**:
- Lubricates grains (reduces friction)
- Increases weight
- **Pore pressure**: Water pressure pushes grains apart, reduces effective stress
  - **Critical**: Rain-saturated slopes most prone

**3. Undercutting**:
- Rivers erode toe of slope → removes support
- Ocean waves erode coastal cliffs

**4. Overloading**:
- Add weight at top (buildings, fill)
- Increases driving force

**5. Vegetation removal**:
- Roots bind soil, absorb water
- Deforestation → increased landslides

**6. Earthquakes**:
- Seismic shaking reduces friction temporarily
- Triggers landslides on marginally stable slopes

**7. Weathering**:
- Weakens rock
- Clay minerals expand when wet (reduce strength)

### Notable Disasters

**1970 Ancash, Peru**:
- M7.9 earthquake → Huascarán ice/rock avalanche
- 50-100 million m³ material
- Traveled 14 km in 3-4 minutes (average 300 km/h, peak 400 km/h)
- Buried town of Yungay (3 m of debris)
- **18,000-25,000 deaths** (entire town)
- Only survivors: 300 people in cemetery on hill above town

**1963 Vajont Dam, Italy**:
- 260 million m³ rock slide into reservoir
- Displaced water → 250 m wave overtopped dam (still intact!)
- Wave destroyed villages below
- **1,900 deaths**
- **Cause**: Reservoir filling activated ancient landslide; engineers ignored warnings

**2014 Oso, Washington**:
- Rainfall-triggered debris avalanche
- 7.6 million m³ moved 1 km
- Buried neighborhood
- 43 deaths
- **Cause**: Known slide-prone area (previous slides 1949, 1951, 1967, 2006), river undercut toe, clearcut logging removed trees

**2017 Mocoa, Colombia**:
- Heavy rain (130 mm in hours) → debris flows from 3 rivers
- Boulders, mud, trees swept through city at night
- 329 deaths, 300+ missing
- **Lesson**: Deforestation on steep slopes + intense rainfall = catastrophic

### Mitigation

**Engineering solutions**:
- **Retaining walls**: Hold slope in place
- **Rock bolts**: Anchor unstable rock
- **Drainage**: Remove water (reduces pore pressure)
- **Slope reduction**: Flatten angle (reduce driving force)
- **Vegetation**: Plant deep-rooted species

**Monitoring**:
- Extensometers (measure crack widening)
- Inclinometers (measure subsurface movement)
- GPS, InSAR (track deformation)

**Land use**:
- Avoid building on/below steep slopes
- Hazard zoning (restrict development)
- Setbacks from cliffs

## Tsunamis

**Tsunami** (Japanese: "harbor wave"): Series of ocean waves generated by sudden vertical displacement of water.

### Causes

**1. Submarine earthquakes** (90% of tsunamis):
- Megathrust earthquakes (M8.5+) at subduction zones
- Vertical seafloor displacement → water column displaced
- **Requirement**: Significant vertical motion (thrust faults, not strike-slip)
- **Most dangerous**: Shallow (<70 km depth), M>7.5, near coast

**2. Submarine landslides**:
- Earthquake-triggered or spontaneous
- Displaces large water volume
- Can be disproportionately large for earthquake size
- **1998 Papua New Guinea**: M7.0 quake → underwater landslide → 15 m tsunami → 2,200 deaths

**3. Volcanic eruptions**:
- Submarine explosions
- Caldera collapse
- Pyroclastic flows into water
- **1883 Krakatoa**: Caldera collapse → 40 m tsunami

**4. Meteorite impacts**:
- No historic examples (pre-human era)
- Chicxulub impact (66 Ma) generated mega-tsunami 100+ m

### Wave Characteristics

**Open ocean**:
- Wavelength: 100-500 km
- Wave height: <1 m (undetectable by ships)
- Wave period: 10-60 minutes
- Speed: ~700-900 km/h (depends on depth)
  - `v = √(gd)` where g=9.8 m/s², d=depth
  - 4,000 m depth → 700 km/h

**Approaching shore**:
- Wave slows (shallower water)
- Wavelength decreases
- Wave height increases dramatically
- **Drawdown**: Water recedes (trough arrives first) — WARNING SIGN
  - Exposed sea floor
  - Fish flopping
  - **Never go look**: Wave arrives minutes later

**Run-up**:
- Maximum height above sea level
- Depends on:
  - Wave energy
  - Seafloor bathymetry (shape)
  - Coastline shape (V-shaped bays amplify)
- **2011 Tōhoku**: Up to 40 m run-up (some locations)

**Multiple waves**:
- **NOT a single wave**: Series of waves over hours
- First wave not necessarily largest
- **Stay evacuated** until all-clear given

### Historic Disasters

**2004 Indian Ocean** (M9.1 Sumatra-Andaman earthquake):
- **Deaths**: ~230,000 (14 countries)
- Indonesia (170,000), Sri Lanka (35,000), India (16,000), Thailand (8,000)
- **No warning system** in Indian Ocean (now established)
- Run-up to 30 m (Banda Aceh)
- Waves reached Somalia (7 hours later), South Africa

**2011 Tōhoku, Japan** (M9.1):
- **Deaths**: ~18,500 (most from tsunami, not quake)
- 40 m run-up (Miyako)
- Waves overtopped seawalls designed for 10 m
- **Fukushima Daiichi nuclear disaster**: 15 m wave flooded reactors → meltdown
- $220 billion damage (costliest natural disaster ever)
- **Warning**: Minutes for near-source areas (many died despite warnings—underestimated size, stayed to secure belongings)

**1755 Lisbon, Portugal** (M~8.5-9.0):
- Earthquake destroyed Lisbon
- 40 minutes later, tsunami (up to 15 m) inundated city
- Fires raged for days
- **60,000 deaths** (~1/4 of population)
- **Impact**: Enlightenment philosophy (Voltaire's *Candide* questioned optimistic worldview), birth of modern seismology

**1960 Chilean Tsunami** (M9.5 Valdivia quake):
- Tsunami crossed Pacific
- Chile: 25 m waves, ~2,000 deaths
- Hawaii (15 hours later): 10 m waves, 61 deaths, $75M damage
- Japan (22 hours later): 6 m waves, 142 deaths
- **Lesson**: Distant tsunamis can be deadly—trans-Pacific propagation

**1700 Cascadia**:
- M~9.0 megathrust (Juan de Fuca subduction)
- **No written records** in North America (pre-European)
- **Discovered via**:
  - Tsunami records in Japan (orphan tsunami: no local earthquake)
  - Native American oral histories (flood legends)
  - Ghost forests (drowned trees dated to 1700)
  - Turbidite (underwater landslide) layers
- **Dating**: Tree rings + Japanese tsunami records → January 26, 1700, ~9pm
- **Recurrence**: ~300-600 years (last 10,000 years: ~19 events)
- **Future threat**: Pacific Northwest (Seattle, Portland, Vancouver) at risk

### Warning Systems

**Components**:
1. **Seismic networks**: Detect earthquakes, estimate location, magnitude
2. **Tsunami detection**:
   - DART buoys (Deep-ocean Assessment and Reporting of Tsunamis): Measure sea level pressure changes
   - Coastal tide gauges
3. **Modeling**: Predict wave arrival times, heights
4. **Dissemination**: Alerts to authorities, public (sirens, mobile alerts, TV/radio)

**Lead time**:
- **Near-source** (within 100 km): Minutes (insufficient for evacuation alerts—rely on earthquake as natural warning)
- **Distant**: Hours (Pacific-wide system provides adequate warning)

**Pacific Tsunami Warning System** (since 1949):
- After 1946 Aleutian tsunami killed 165 in Hawaii
- 26 member nations
- DART buoys, seismic stations across Pacific

**Mitigation**:
- **Coastal defenses**: Seawalls, tsunami gates (Japan)
- **Vertical evacuation**: Tall reinforced structures, hills
- **Zoning**: Restrict development in inundation zones
- **Education**: Recognize natural warnings (strong shaking, water recession)
  - "Felt a quake? Head for high ground!"
- **Drills**: Regular evacuation practice

## Subsidence and Sinkholes

**Subsidence**: Gradual or sudden sinking of ground surface.

### Causes

**1. Groundwater extraction**:
- Removing water → pore pressure drops → sediments compact
- **Irreversible** (compaction is permanent)
- **San Joaquin Valley, California**: 9 m subsidence (1925-1970s) from agricultural pumping
- **Mexico City**: 10 m subsidence since 1900; built on drained lake (soft sediments)
- **Bangkok, Thailand**: 2 m subsidence; sinking 2-5 cm/year

**2. Oil and gas extraction**:
- Removing fluids → reservoir compaction
- **Long Beach, California**: 9 m subsidence (1926-1960s) from oil extraction; now halted (water injection)
- **Venice, Italy**: Subsidence + sea level rise = frequent flooding (acqua alta)

**3. Mining**:
- Underground mines collapse → surface subsides
- **Abandoned mines**: Voids eventually collapse decades later

**4. Karst processes** (sinkholes):
- **Limestone/dolomite dissolution** by acidic water:
  ```
  CaCO₃ + H₂O + CO₂ → Ca²⁺ + 2HCO₃⁻ (dissolved in water)
  ```
- Creates subsurface voids (caves)
- Roof collapses → sinkhole
- **Types**:
  - **Dissolution**: Slow, gradual depression
  - **Cover-subsidence**: Soil gradually filters into voids
  - **Cover-collapse**: Sudden collapse (most dramatic)
- **Florida**: 10,000+ sinkholes; limestone bedrock; prone to collapse
  - **2013 Seffner sinkhole**: Swallowed bedroom, 1 death
- **China**: Massive sinkholes in karst regions (some 500+ m deep)

**5. Thawing permafrost** (thermokarst):
- Ice-rich permafrost melts → ground collapses
- **Arctic regions**: Accelerating due to climate warming
- Damages infrastructure (buildings tilt, roads buckle, pipelines rupture)

### Mitigation

- **Groundwater management**: Regulated pumping, artificial recharge
- **Oil/gas**: Water injection to maintain reservoir pressure
- **Geotechnical surveys**: Identify voids before construction
- **Grouting**: Fill subsurface voids with concrete

## Key Terms

- **Elastic rebound**: Earthquake mechanism—stored strain released during fault rupture
- **Moment magnitude (Mw)**: Logarithmic scale measuring earthquake energy release
- **Liquefaction**: Saturated sediment loses strength during shaking, behaves as liquid
- **Peak Ground Acceleration (PGA)**: Maximum shaking intensity (% of g)
- **Megathrust**: Shallow-dipping fault at subduction zone; generates largest earthquakes
- **Volcanic Explosivity Index (VEI)**: 0-8 logarithmic scale of eruption size
- **Pyroclastic flow**: Avalanche of hot gas and rock fragments (500-1,000°C, 100-700 km/h)
- **Lahar**: Volcanic mudflow (water + volcanic debris)
- **Volcanic winter**: Cooling caused by stratospheric sulfate aerosols reflecting sunlight
- **Mass wasting**: Downslope movement of rock/soil under gravity
- **Debris flow**: Rapid flow of water-saturated debris (10-50 m/s)
- **Angle of repose**: Maximum stable slope angle for loose material
- **Factor of Safety**: Ratio of resisting forces to driving forces (>1 stable, <1 fails)
- **Tsunami**: Series of ocean waves from sudden water displacement
- **Run-up**: Maximum height tsunami reaches above normal sea level
- **Subsidence**: Gradual or sudden sinking of ground surface
- **Sinkhole**: Collapse of ground into subsurface void (typically karst terrain)
- **Karst**: Landscape shaped by dissolution of soluble rocks (limestone, gypsum)

## Summary

Geological hazards cause tens of thousands of deaths and hundreds of billions in economic losses annually. Earthquakes result from elastic rebound—accumulated tectonic strain released during fault rupture. Moment magnitude scales exponentially (each unit = 32× energy); megaquakes (M9+) occur ~once per decade. Hazards include ground shaking, liquefaction, landslides, fires, and tsunamis. Short-term prediction remains impossible; mitigation relies on building codes, land-use planning, and early warning systems (seconds to minutes lead time).

Volcanic eruptions range from effusive (Hawaii) to cataclysmic (VEI-8 super-eruptions). Explosivity depends on magma viscosity and gas content. Hazards: pyroclastic flows (most lethal, 500-1,000°C, 100-700 km/h), lahars (volcanic mudflows), ashfall (collapses roofs, grounds aircraft), gases (CO₂ asphyxiation), and volcanic winter (sulfate aerosols cool climate 1-3 years). Monitoring precursors (seismicity, deformation, gases) enables forecasting days to weeks ahead. VEI-7+ eruptions can cause global cooling and crop failures.

Landslides are driven by gravity, resisted by friction. Factors decreasing stability: steep slopes, water (lubricates, increases weight, raises pore pressure), undercutting, vegetation removal, earthquakes. Types range from rock falls (m/s) to soil creep (mm/year). Deadliest events involve rapid debris avalanches (1970 Peru: 18,000 deaths in 3 minutes). Mitigation: drainage, retaining walls, slope reduction, hazard zoning.

Tsunamis are generated primarily by megathrust earthquakes displacing seafloor (also landslides, volcanoes). Open-ocean waves (<1 m height, 700 km/h speed) become multi-meter run-up waves at coast. 2004 Indian Ocean tsunami killed ~230,000; 2011 Tōhoku tsunami killed ~18,500, triggered Fukushima disaster. Warning systems provide hours for distant tsunamis, but near-source events require recognizing natural warnings (strong shaking, water recession). Subsidence from groundwater/oil extraction (San Joaquin Valley: 9 m; Mexico City: 10 m) and karst sinkholes (limestone dissolution creates voids) cause infrastructure damage. Understanding these hazards enables societies to mitigate risk through engineering, monitoring, zoning, and education.

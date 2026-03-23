# Deep Time & Earth History

## Discovering Earth's Age

For most of human history, Earth's age was grossly underestimated. Determining the true age revolutionized geology and unlocked understanding of evolutionary, tectonic, and climatic processes.

### Pre-Scientific Estimates

**Biblical chronology**: Archbishop James Ussher (1650) calculated Creation occurred on October 23, 4004 BCE—giving Earth ~6,000 years. This calculation, based on Biblical genealogies, dominated Western thought for centuries.

**Problem**: 6,000 years cannot explain:
- Thickness of sedimentary sequences (kilometers)
- Mountain range formation and erosion
- Fossil record showing extinct species and evolutionary transitions
- Salt accumulation in oceans
- Observed rates of geological processes

### Early Scientific Attempts

**Georges-Louis Leclerc, Comte de Buffon (1779)**:
- Heated iron spheres and measured cooling rates
- Extrapolated to Earth-sized body
- **Estimate**: 75,000 years (published), 500,000 years (private notes)
- **Limitation**: Didn't know about internal heat from radioactivity

**Charles Lyell (1830s)**:
- Calculated sedimentation rates
- Measured erosion of Niagara Falls
- **Conclusion**: Earth must be hundreds of millions of years old
- **Problem**: No precision, but correctly identified vast age

**Lord Kelvin (1862)**:
- Calculated Earth's cooling from molten state
- Assumed no internal heat source
- **Estimate**: 20-40 million years (later revised to 100 million)
- **Flaw**: Unknown radioactive decay generates continuous heat
- **Impact**: Created conflict with Darwin (evolution needs more time than Kelvin allowed)

**John Joly (1899)**:
- Measured sodium in ocean
- Calculated input rate from rivers
- **Estimate**: 80-90 million years
- **Flaw**: Didn't account for sodium recycling through subduction, evaporites

### Breakthrough: Radiometric Dating

**Discovery of radioactivity** (1896-1900s):
- Henri Becquerel (1896): Discovered uranium emits radiation
- Marie & Pierre Curie (1898): Isolated radium, studied radioactive decay
- Ernest Rutherford (1905): Proposed using radioactive decay as "atomic clock"

**Key principle**: Radioactive isotopes decay at constant, measurable rates unaffected by temperature, pressure, chemical state.

**First radiometric dates**:
- Boltwood (1907): Uranium-lead dating of minerals → 400 million to 2.2 billion years
- Holmes (1913): Refined methods, dated rocks to 1.6 billion years
- **Conclusion**: Earth is orders of magnitude older than Kelvin's estimate

**Current accepted age**: **4.54 ± 0.05 billion years**
- Based on radiometric dating of meteorites (oldest materials in solar system)
- Confirmed by lunar samples, Earth's oldest minerals (zircons ~4.4 Ga)
- Multiple independent isotope systems agree

## Radiometric Dating Principles

### Radioactive Decay

Unstable atomic nuclei spontaneously transform into different elements by emitting particles/energy.

**Types of decay**:

**Alpha decay**: Nucleus emits helium nucleus (2 protons + 2 neutrons)
```
²³⁸U → ²³⁴Th + ⁴He (alpha particle)
Atomic number decreases by 2, mass number by 4
```

**Beta decay**: Neutron converts to proton (or vice versa), emits electron/positron
```
¹⁴C → ¹⁴N + e⁻ (electron) + antineutrino
Atomic number increases by 1, mass number unchanged
```

**Electron capture**: Nucleus captures inner electron, proton converts to neutron
```
⁴⁰K + e⁻ → ⁴⁰Ar + neutrino
```

### Decay Constants and Half-Lives

**Decay follows exponential law**:
```
N(t) = N₀ e^(-λt)
```
- N(t) = number of parent atoms at time t
- N₀ = initial number of parent atoms
- λ = decay constant (probability of decay per unit time)
- t = time elapsed

**Half-life** (t₁/₂): Time for half of parent atoms to decay
```
t₁/₂ = ln(2)/λ = 0.693/λ
```

**Dating equation** (using parent/daughter ratio):
```
t = (1/λ) × ln(1 + D/P)
```
- t = age
- D = number of daughter atoms
- P = number of parent atoms
- λ = decay constant

### Major Dating Systems

| Parent → Daughter | Half-life | Useful Range | Applications |
|-------------------|----------|--------------|--------------|
| **Uranium-238 → Lead-206** | 4.47 Ga | 1 Ma to 4.5 Ga | Oldest rocks, Earth's age, zircons |
| **Uranium-235 → Lead-207** | 704 Ma | 10 Ma to 4.5 Ga | Cross-check with U-238 system |
| **Thorium-232 → Lead-208** | 14.0 Ga | 10 Ma to 4.5 Ga | Ancient rocks, meteorites |
| **Rubidium-87 → Strontium-87** | 48.8 Ga | 10 Ma to 4.5 Ga | Igneous/metamorphic rocks, micas |
| **Potassium-40 → Argon-40** | 1.25 Ga | 100 ka to 4.5 Ga | Volcanic rocks, mineral ages |
| **Samarium-147 → Neodymium-143** | 106 Ga | 100 Ma to 4.5 Ga | Mantle rocks, meteorites |
| **Carbon-14 → Nitrogen-14** | 5,730 years | 100 to 50,000 years | Organic materials, archaeology |

### Radiocarbon Dating (¹⁴C)

**How ¹⁴C forms**:
1. Cosmic rays hit atmosphere → neutrons
2. Neutrons hit ¹⁴N: ¹⁴N + n → ¹⁴C + p
3. ¹⁴C oxidizes to ¹⁴CO₂
4. Plants absorb ¹⁴CO₂ via photosynthesis
5. Animals eat plants
6. **Result**: All living things have same ¹⁴C/¹²C ratio as atmosphere (~1.3 × 10⁻¹²)

**After death**:
- Organism stops exchanging carbon with environment
- ¹⁴C decays: ¹⁴C → ¹⁴N + e⁻ (beta decay)
- ¹⁴C/¹²C ratio decreases exponentially

**Age calculation**:
```
t = (1/λ) × ln(N₀/N)
t = 8,033 × ln(A₀/A) years
```
Where A₀ = initial activity, A = current activity

**Useful range**: 100-50,000 years (after ~10 half-lives, too little ¹⁴C remains)

**Calibration**: Tree rings, coral bands, lake varves provide calibration (atmospheric ¹⁴C varies due to solar activity, magnetic field changes, fossil fuel burning)

**Applications**:
- Archaeology (human artifacts, mummies, settlements)
- Paleoclimate (organic material in sediments)
- Forensics (determine time of death)
- Art authentication (detect modern forgeries)

### Requirements for Accurate Radiometric Dating

**1. Closed system**: No gain/loss of parent or daughter after formation
- **Violation**: Weathering can remove lead from uranium minerals → erroneously young age
- **Mitigation**: Date fresh, unweathered minerals; use multiple isotope systems

**2. Known initial conditions**: Must know or correct for initial daughter isotopes
- **Example**: Rock may contain non-radiogenic lead at formation
- **Solution**: Isochron method compares minerals with different parent/daughter ratios

**3. Constant decay rates**: Decay constant doesn't change over time
- **Confirmed**: Laboratory tests show decay rates unaffected by temperature, pressure, chemical state
- **Exception**: Extreme stellar conditions (not relevant to Earth)

**4. Appropriate mineral selection**: Mineral must incorporate parent but exclude daughter
- **Example**: Zircon (ZrSiO₄) incorporates uranium but excludes lead → excellent for U-Pb dating
- **Example**: K-feldspar incorporates potassium but minimal argon → good for K-Ar dating

## The Precambrian: 4.54 Ga - 541 Ma

Precambrian time comprises ~88% of Earth history yet has sparse fossil record (mostly microbial). Divided into three eons: Hadean, Archean, Proterozoic.

### Hadean Eon (4.54-4.0 Ga): "Hell-like"

Named for Hades (Greek underworld)—reflecting early Earth's extreme conditions.

**Characteristics**:
- No rock record survives (oldest known rocks: 4.03 Ga, Acasta Gneiss, Canada)
- Heavy bombardment by asteroids/comets
- Surface molten or repeatedly re-melted
- No continents, no oceans initially
- No atmosphere like today's

**Timeline of events**:

**~4.54 Ga**: Earth forms from planetesimal accretion
- Entirely molten from impact energy + radioactive heating
- Iron catastrophe: metal sinks to form core over ~30 million years

**~4.51 Ga**: Giant impact (Theia collision)
- Moon forms from ejected debris
- Earth re-melted

**~4.4 Ga**: Surface solidifies
- Oldest minerals: Detrital zircons (Jack Hills, Australia) dated to 4.404 Ga
- Zircon oxygen isotopes suggest liquid water present (implies oceans!)
- Temperature cool enough for crust formation

**4.1-3.8 Ga**: Late Heavy Bombardment
- Spike in asteroid/comet impacts (evidence from Moon craters)
- May have sterilized surface if life had emerged
- Delivered water and organic compounds

**~4.0 Ga**: Hadean ends
- Crust stabilizes enough to preserve rocks
- Oceans established
- Conditions suitable for life

### Archean Eon (4.0-2.5 Ga): "Ancient"

First eon with preserved rock record. Earth becomes recognizably planet-like.

**Key developments**:

**First continents** (~4.0-3.5 Ga):
- Small proto-continents (cratons) form
- Granite-like crust differentiates from basaltic crust
- Preserved examples: Kaapvaal Craton (South Africa), Pilbara Craton (Australia)

**Origin of life** (~3.8-3.5 Ga):
- Oldest possible evidence: 3.95 Ga graphite (carbon) in Labrador with light isotope signature (possible biogenic)
- **Stromatolites** (3.48 Ga, Pilbara, Australia): Layered structures built by microbial mats (cyanobacteria)
- By 3.5 Ga: Life definitely exists—single-celled prokaryotes (bacteria, archaea)

**Atmosphere composition**:
- **No free oxygen** (O₂ <1% of present levels)
- Reducing atmosphere: methane (CH₄), ammonia (NH₃), hydrogen (H₂), water vapor (H₂O)
- CO₂ levels ~10-100× modern (greenhouse effect compensated for weaker early Sun)

**Climate**:
- **Faint Young Sun Paradox**: Sun was 25-30% dimmer than today
- Earth should have been frozen but wasn't
- **Solution**: Greenhouse gases (CO₂, CH₄) kept planet warm
- Evidence of liquid water in zircons, sedimentary rocks

**Tectonic style**:
- Higher mantle temperatures → more vigorous convection
- Uncertain if modern-style plate tectonics operated
- Possible "stagnant lid" or "squishy lid" tectonics initially
- True plate tectonics likely began sometime in late Archean

**Archean rocks**:
- **Greenstone belts**: Volcanic and sedimentary sequences, often metamorphosed
- **Komatiites**: Ultra-high temperature lavas (>1,600°C) that don't form today (mantle too cool)
- **Banded Iron Formations** (BIFs): Begin to form as oxygen from photosynthesis starts reacting with dissolved iron

### Proterozoic Eon (2.5 Ga - 541 Ma): "Earlier Life"

Massive changes in atmosphere, oceans, and life.

**Great Oxidation Event (GOE)** (~2.45-2.0 Ga):

**Cause**: Cyanobacteria (blue-green algae) evolved oxygenic photosynthesis:
```
6 CO₂ + 6 H₂O + sunlight → C₆H₁₂O₆ + 6 O₂
```

**Timeline**:
1. **Pre-2.4 Ga**: Oxygen produced but immediately consumed by reduced minerals (iron, sulfur) and dissolved ocean iron
2. **~2.45 Ga**: Oxygen "sinks" saturated → free O₂ accumulates in atmosphere
3. **2.4-2.0 Ga**: Atmospheric oxygen rises from <0.001% to 1-10%
4. **After 2.0 Ga**: Oxygen levels stabilize at ~10-40% of present (debate ongoing)
5. **Neoproterozoic (~600 Ma)**: Oxygen approaches modern levels (~21%)

**Evidence**:
- **Detrital uraninite/pyrite**: Roundeddgrains in pre-2.3 Ga river deposits (wouldn't survive transport in oxygenated atmosphere)
- **Red beds**: Iron-rich red sediments appear ~2.3 Ga (oxidized iron)
- **Manganese oxides**: Require oxygen, absent before 2.4 Ga
- **Sulfur isotope anomaly**: Disappears at 2.45 Ga (mass-independent fractionation only occurs without oxygen)

**Consequences**:
1. **Oxygen catastrophe**: Anaerobic organisms die or retreat to oxygen-poor environments
2. **Methane collapse**: Oxygen reacts with atmospheric methane → CO₂ (weaker greenhouse)
3. **First Snowball Earth** (Huronian glaciation, 2.4-2.1 Ga): Planet freezes due to methane loss
4. **New metabolic possibilities**: Aerobic respiration evolves (15× more energy than anaerobic)
5. **Ozone layer forms**: O₃ shields surface from UV radiation, enabling eventual land colonization

**Eukaryote evolution** (~2.1-1.8 Ga):
- Cells with nucleus and organelles
- **Endosymbiosis**: Mitochondria originated from engulfed bacteria; chloroplasts from cyanobacteria
- Evidence: Oldest eukaryote fossils ~1.9 Ga (Grypania, coiled ribbon-like organism)

**Supercontinent cycles**:
- **Columbia/Nuna** (~1.8-1.5 Ga): First supercontinent
- **Rodinia** (~1.1-0.75 Ga): Better documented supercontinent
- Supercontinents assemble, persist ~100 Ma, break apart → cycle repeats every ~400-600 Ma

**Snowball Earth events** (Neoproterozoic, ~720 and ~635 Ma):
- **Sturtian glaciation** (720-660 Ma): Global glaciation, evidence of glacial deposits at equator
- **Marinoan glaciation** (650-635 Ma): Even more severe
- **Cause**: Runaway ice-albedo feedback (ice reflects sunlight → cools planet → more ice)
- **End**: Volcanic CO₂ accumulates (ice cover prevents weathering removal) → super-greenhouse → rapid melting
- **Cap carbonates**: Thick limestone layers deposited rapidly after melt (carbonate precipitation from warm CO₂-rich oceans)

**Ediacaran biota** (~575-541 Ma):
- First large, complex multicellular organisms
- Soft-bodied (no hard parts initially)
- Strange morphologies (fronds, discs, quilted forms)
- Mostly extinct by Cambrian; unclear relationship to modern animals

## Phanerozoic Eon (541 Ma - Present): "Visible Life"

### Paleozoic Era (541-252 Ma)

**Cambrian Explosion** (541-485 Ma):

**Event**: Rapid diversification of animal life over ~20-40 million years.

**What appeared**:
- All major animal phyla (body plans) originate
- Hard parts (shells, exoskeletons) evolve—finally abundant fossils
- Trilobites dominate oceans
- First chordates (ancestors of vertebrates)
- Complex ecosystems with predators, filter feeders, burrowers

**Causes** (debated):
- Oxygen levels reach threshold for active metabolism
- Evolution of genetic toolkits (Hox genes) enabling body plan diversity
- Predation arms race (hard parts as defense)
- Environmental changes (ocean chemistry, temperature)

**Burgess Shale** (508 Ma, Canada): Exceptional fossil preservation shows Cambrian diversity—many bizarre forms went extinct.

**Ordovician** (485-444 Ma):
- Marine biodiversity peaks
- First land plants (mosses, liverworts)
- Coral reefs become common
- **Mass extinction** (444 Ma): 85% of marine species die; caused by glaciation + sea level drop

**Silurian** (444-419 Ma):
- Recovery from Ordovician extinction
- First jawed fish (placoderms)
- First vascular plants (conduct water/nutrients)
- Millipedes, centipedes colonize land

**Devonian** (419-359 Ma): "Age of Fishes"
- Fish diversity explodes: armored fish, sharks, lobe-finned fish
- First forests (tree-sized plants with woody tissue)
- **Tetrapods evolve** (~385 Ma): Fish with fleshy fins transition to land (Tiktaalik, Ichthyostega)
- First wingless insects, spiders, mites
- **Late Devonian extinction** (375-359 Ma): 70-75% species die; causes include anoxia, climate cooling

**Carboniferous** (359-299 Ma):
- **Coal age**: Vast swamp forests of tree-sized ferns, lycopods, horsetails
- High oxygen levels (~35%, vs 21% today) → gigantism in arthropods (dragonflies 70 cm wingspan, millipedes 2 m long)
- First reptiles evolve (~320 Ma)—amniotic egg enables full terrestrial life
- Amphibians diversify

**Permian** (299-252 Ma):
- Supercontinent **Pangea** fully assembled (~300 Ma)
- Interior deserts (far from moisture sources)
- Synapsids (mammal ancestors) dominate
- First conifers (drought-adapted)
- **Permian-Triassic extinction** (252 Ma): **Largest mass extinction** — 96% marine species, 70% terrestrial vertebrates die
  - **Cause**: Siberian Traps flood basalt eruptions (massive volcanism) → global warming, ocean anoxia, acidification
  - CO₂ spike, methane release from warming oceans
  - Took 10 million years for ecosystems to recover

### Mesozoic Era (252-66 Ma): "Age of Reptiles"

**Triassic** (252-201 Ma):
- Recovery from Permian extinction
- Archosaurs diversify → dinosaurs, pterosaurs, crocodilians
- First dinosaurs (~230 Ma): small, bipedal
- First mammals (~225 Ma): small, nocturnal, shrew-like
- Pangea begins rifting
- **Triassic-Jurassic extinction** (201 Ma): 50-80% species die; CAMP volcanism (Central Atlantic Magmatic Province) as cause

**Jurassic** (201-145 Ma):
- Dinosaurs dominate terrestrial ecosystems
- Sauropods (long-necked plant-eaters) reach enormous sizes: Brachiosaurus, Diplodocus
- First birds (~150 Ma): Archaeopteryx (feathered, transitional between dinosaurs and birds)
- Pterosaurs soar (flying reptiles, not dinosaurs)
- Marine reptiles: ichthyosaurs, plesiosaurs
- Pangea continues breaking → Atlantic Ocean opens
- Warm, humid climate globally

**Cretaceous** (145-66 Ma):
- Peak dinosaur diversity: T. rex, Triceratops, Velociraptor
- **Flowering plants** (angiosperms) evolve and spread rapidly (~130 Ma) → co-evolution with pollinating insects
- Social insects appear: ants, termites, advanced bees
- Continents approach modern positions
- Highest sea levels in Phanerozoic (shallow seas cover continents)
- Very warm climate (no polar ice, palm trees in Arctic)
- **Cretaceous-Paleogene extinction** (66 Ma): **Dinosaur extinction** (except birds), 75% species die
  - **Cause**: Chicxulub asteroid impact (Yucatan, Mexico) — 10 km diameter, ~100 million megatons energy
  - Impact winter: dust blocks sunlight → photosynthesis collapses → food chain collapse
  - Additional: Deccan Traps volcanism (India) may have stressed ecosystems beforehand

### Cenozoic Era (66 Ma - Present): "Age of Mammals"

**Paleogene** (66-23 Ma):
- Mammals rapidly diversify into niches vacated by dinosaurs
- Modern mammal groups appear: primates, rodents, whales, bats
- **Birds diversify**: Modern bird orders originate
- India collides with Asia (~50 Ma) → Himalaya formation begins
- **PETM** (Paleocene-Eocene Thermal Maximum, 56 Ma): Rapid warming event (~5-8°C increase in 20,000 years)
  - Cause: Massive carbon release (methane hydrates? volcanism?)
  - Mammal dwarfing (Eocene horses size of dogs)
  - Ocean acidification, deep-sea extinctions
- Climate cools through Eocene-Oligocene

**Neogene** (23-2.6 Ma):
- Continued cooling trend
- Grasslands expand (due to cooler, drier climates) → grazing mammals diversify (horses, bison, antelopes)
- Great apes diversify in Africa
- **Hominid evolution**: Human lineage splits from chimpanzee lineage ~6-7 Ma
- Australopithecines (~4-2 Ma): Upright walking
- Genus *Homo* appears ~2.8 Ma

**Quaternary** (2.6 Ma - Present):

**Pleistocene** (2.6 Ma - 11.7 ka): Ice Age
- Glacial-interglacial cycles driven by Milankovitch orbital variations
- Ice sheets cover much of North America, Europe, northern Asia
- Sea level fluctuates 120 m (low during glacials, high during interglacials)
- **Megafauna**: Giant mammals (mammoths, saber-toothed cats, giant sloths)
- **Human evolution**: *Homo erectus*, *Homo neanderthalensis*, *Homo sapiens*
- *Homo sapiens* evolves ~300 ka (thousand years ago) in Africa, spreads globally ~70 ka
- **Megafauna extinctions** (~50-10 ka): Human hunting + climate change likely causes

**Holocene** (11.7 ka - present):
- Current interglacial period (warmer, ice sheets retreat)
- Agriculture begins ~12 ka (Fertile Crescent)
- Civilizations arise (Mesopotamia, Egypt, Indus, China, Mesoamerica)
- Industrial Revolution (~250 years ago): Fossil fuel use, CO₂ rise, anthropogenic climate change
- **Proposed Anthropocene**: Some scientists argue human impacts define new epoch

## Mass Extinctions

Major biodiversity collapses that reshape life on Earth.

### The "Big Five" Mass Extinctions

| Event | Time (Ma) | Marine Extinction % | Cause(s) | Duration | Recovery Time |
|-------|----------|-------------------|----------|----------|---------------|
| **Ordovician-Silurian** | 444 | 85% | Glaciation, sea level fall, anoxia | ~1 Ma | ~5 Ma |
| **Late Devonian** | 375-359 | 75% | Anoxia, climate cooling, bolide impacts? | ~20 Ma | ~10 Ma |
| **Permian-Triassic** | 252 | 96% | Siberian Traps volcanism, warming, anoxia | ~60 ka | ~10 Ma |
| **Triassic-Jurassic** | 201 | 80% | CAMP volcanism, acidification | ~600 ka | ~10 Ma |
| **Cretaceous-Paleogene** | 66 | 75% | Chicxulub impact + Deccan volcanism | ~10-100 ka | ~10 Ma |

**Sixth mass extinction** (ongoing?): Human-caused extinctions since ~1500 CE. Extinction rates ~100-1,000× background rate. IUCN Red List: 28% assessed species threatened.

### Common Extinction Mechanisms

**Volcanism** (flood basalts):
- Massive eruptions over ~1 million years
- CO₂ spike → warming → ocean stratification → anoxia
- SO₂ → sulfate aerosols → short-term cooling
- Acid rain

**Bolide impacts**:
- Asteroid/comet collision
- Impact winter (dust blocks sun)
- Wildfires, tsunami, earthquakes
- Acid rain, ozone depletion

**Climate change**:
- Rapid warming/cooling
- Sea level changes (drowning/exposing habitats)
- Ocean anoxia (oxygen-depleted waters)
- Ocean acidification (dissolves carbonate shells)

**Anoxia**:
- Oxygen-poor oceans kill marine life
- Often triggered by warming (warm water holds less O₂) + stratification

## Paleoclimate Proxies

How do we know ancient climates?

### Isotope Proxies

**Oxygen isotopes** (δ¹⁸O):
- Ocean water: ¹⁶O (lighter) and ¹⁸O (heavier)
- Evaporation preferentially removes ¹⁶O
- During ice ages: ¹⁶O locked in ice sheets → ocean enriched in ¹⁸O
- Foraminifera (marine plankton) shells record ocean δ¹⁸O
- **Measure**: δ¹⁸O in foram shells → ice volume + temperature

**Carbon isotopes** (δ¹³C):
- Plants prefer ¹²C during photosynthesis
- Organic-rich sediments depleted in ¹³C
- Carbonate rocks record ocean δ¹³C
- Sudden negative δ¹³C excursion → massive organic carbon burial or methane release

### Biological Proxies

**Fossils**:
- Species distributions indicate climate (e.g., coral reefs = warm shallow seas)
- Leaf morphology: Large leaves with smooth edges = warm, wet; small leaves with toothed edges = cool, dry

**Pollen**:
- Preserved in lake sediments, peat bogs
- Identifies past vegetation → climate

**Alkenones**:
- Organic molecules from marine algae
- Ratio of unsaturated/saturated forms correlates with temperature

### Sedimentological Proxies

**Ice-rafted debris (IRD)**:
- Rocks dropped by melting icebergs into ocean sediments
- Indicates glacial activity

**Evaporites** (gypsum, halite):
- Form in arid, evaporative environments
- Indicate hot, dry climate

**Coal deposits**:
- Require swampy, warm, wet conditions

**Glacial features** (dropstones, tillites, striations):
- Direct evidence of past glaciation

### Geochemical Proxies

**Boron isotopes**:
- pH proxy → ocean acidification events

**Mg/Ca ratios** in foraminifera:
- Temperature proxy (more Mg at higher temps)

**Strontium isotopes** (⁸⁷Sr/⁸⁶Sr):
- Weathering vs volcanic input ratio → tectonic activity, climate

### Ice Cores

**Best high-resolution climate record** (last ~800 ka):

**What they preserve**:
- **Bubbles**: Ancient atmosphere (CO₂, CH₄, N₂O concentrations)
- **δ¹⁸O in ice**: Temperature proxy
- **Dust**: Aridity, wind strength
- **Volcanic ash**: Dating marker
- **Isotopes**: Solar activity, cosmic ray flux

**Major sites**:
- **Vostok** (Antarctica): 420 ka record
- **EPICA Dome C** (Antarctica): 800 ka record—covers 8 glacial cycles
- **Greenland** (GRIP, GISP2): Higher resolution but shorter (~100 ka)

**Key findings**:
- CO₂ ranged 180-300 ppm during glacial-interglacial cycles (pre-industrial)
- Temperature and CO₂ tightly correlated
- Rapid climate shifts possible (Younger Dryas: ~5°C in decades)

## Key Terms

- **Deep Time**: Vast geological timescales (millions to billions of years)
- **Radiometric Dating**: Age determination using radioactive decay of isotopes
- **Half-life**: Time for half of radioactive parent atoms to decay
- **Closed System**: No gain/loss of parent or daughter isotopes after formation
- **Isochron**: Plot of isotope ratios that yields age from slope
- **Hadean**: 4.54-4.0 Ga; molten Earth, heavy bombardment, no surviving rocks
- **Archean**: 4.0-2.5 Ga; first continents, origin of life, stromatolites
- **Proterozoic**: 2.5-0.541 Ga; Great Oxidation Event, eukaryotes, Snowball Earth
- **Great Oxidation Event (GOE)**: ~2.4 Ga, atmospheric oxygen rises from oxygenic photosynthesis
- **Snowball Earth**: Global glaciation events (~720 and ~635 Ma)
- **Phanerozoic**: 541 Ma-present; "visible life," abundant fossils
- **Cambrian Explosion**: Rapid animal diversification ~541 Ma
- **Mass Extinction**: Events where >75% species die over geologically short period
- **Permian-Triassic Extinction**: Largest mass extinction (252 Ma), 96% marine species die
- **Cretaceous-Paleogene Extinction**: Dinosaur extinction (66 Ma) from asteroid impact
- **Paleoclimate Proxies**: Indicators of past climate (isotopes, fossils, ice cores, sediments)
- **Ice Core**: Cylindrical sample from ice sheet preserving ancient atmosphere and climate
- **δ¹⁸O (delta-O-18)**: Oxygen isotope ratio used as temperature/ice volume proxy

## Summary

Determining Earth's age required overcoming pre-scientific underestimates (6,000 years) and early scientific attempts (Kelvin's 20-100 Ma). Radiometric dating, based on constant radioactive decay rates, established Earth's age at 4.54 billion years—deep time beyond human intuition. Multiple isotope systems (U-Pb, K-Ar, Rb-Sr, C-14) date rocks from thousands to billions of years old by measuring parent/daughter ratios.

Earth's 4.54-billion-year history divides into Hadean (4.54-4.0 Ga: molten Earth, heavy bombardment), Archean (4.0-2.5 Ga: first continents, origin of life, anoxic atmosphere), Proterozoic (2.5-0.541 Ga: Great Oxidation Event, eukaryotes, Snowball Earth), and Phanerozoic (541 Ma-present: abundant fossils). The Phanerozoic divides into Paleozoic (Cambrian explosion, colonization of land, Permian mass extinction), Mesozoic (dinosaur dominance, flowering plants, asteroid impact), and Cenozoic (mammal diversification, human evolution, ice ages).

Five major mass extinctions punctuate the fossil record, caused by volcanism, asteroid impacts, climate change, and ocean anoxia. Recovery takes millions of years. Paleoclimate proxies—isotopes, fossils, ice cores, sediments—reveal ancient temperatures, CO₂ levels, and climate shifts. Ice cores provide 800,000-year records showing tight correlation between CO₂ and temperature across glacial-interglacial cycles. Understanding deep time and Earth history provides context for current rapid environmental changes and informs predictions about future climate and ecosystem responses.

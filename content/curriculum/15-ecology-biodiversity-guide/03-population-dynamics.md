# Population Dynamics

## Overview

Population ecology examines factors controlling population size, distribution, and change over time. Understanding population dynamics is critical for conservation (endangered species), resource management (fisheries, forestry), and controlling pests and invasives.

---

## Population Characteristics

### Basic Measures

**Abundance**
- **Population size (N)**: Total number of individuals
- **Density**: Number per unit area or volume
- **Biomass**: Total mass of all individuals

**Distribution**
- **Range**: Geographic area occupied
- **Dispersion pattern**: Spatial arrangement
  - Random: Independent of others
  - Uniform: Evenly spaced (territorial behavior, competition)
  - Clumped: Aggregated (resource patches, social behavior)

**Demographics**
- **Age structure**: Proportion in each age class
- **Sex ratio**: Males to females
- **Birth/death rates**: Per capita rates

---

## Population Growth Models

### Exponential Growth

**Model:** dN/dt = rN

Where:
- N = population size
- r = intrinsic rate of increase (birth rate - death rate)
- t = time

**Characteristics:**
- J-shaped curve
- No resource limits
- Rare in nature except short-term (invasive species, bacteria in fresh media)

**When It Occurs:**
- After colonization of new habitat
- After population bottleneck
- Favorable conditions with low density

### Logistic Growth

**Model:** dN/dt = rN(1 - N/K)

Where:
- K = carrying capacity (maximum sustainable population)
- (1 - N/K) = proportion of unused resources

**Characteristics:**
- S-shaped curve
- Growth slows as approaches K
- More realistic than exponential for most populations

**Real Example:**
- Fur seals on Pribilof Islands after overhunting stopped
- Rebound from ~200,000 (1911) to ~1,000,000 (1950s) following logistic curve

### Limits to Logistic Model

**Assumptions often violated:**
- K is not constant (varies with environment)
- No time lags (organisms respond instantly)
- No immigration/emigration
- Density dependence is smooth (not always true)

---

## Density Dependence

### Density-Dependent Factors

Effects that intensify as population density increases

**Competition for Resources**
- Food, water, nesting sites, mates
- Reduces per capita birth rates or increases death rates
- Example: Salmon fry growth rates decline with density

**Predation**
- Predators may form search image for abundant prey
- Example: Lynx predation on snowshoe hares increases when hares abundant

**Disease Transmission**
- Higher contact rates at high density
- Example: Chronic wasting disease in deer spreads faster in dense populations

**Territoriality**
- Individuals excluded from breeding at high densities
- Example: Wolf packs defend territories; surplus individuals don't breed

**Waste Accumulation**
- Toxic metabolites build up
- Example: Algae growth limited by self-shading and oxygen depletion

### Density-Independent Factors

Effects unrelated to population density

**Weather/Climate**
- Frost kills organisms regardless of density
- Drought affects all individuals similarly

**Natural Disasters**
- Floods, fires, hurricanes
- Mass mortality not related to crowding

**Human Impacts**
- Habitat destruction affects all individuals
- Pollution, overharvesting

---

## Life History Strategies

### r vs. K Selection

**r-selected species** (maximize growth rate)
- Small body size, short lifespan
- Early maturity, many offspring
- Little parental care
- Thrive in unstable, disturbed environments
- Examples: Insects, rodents, annual plants, bacteria

**K-selected species** (maximize competitive ability near K)
- Large body size, long lifespan
- Late maturity, few offspring
- Extensive parental care
- Thrive in stable, crowded environments
- Examples: Elephants, whales, oak trees, humans

| Trait | r-selected | K-selected |
|-------|------------|------------|
| Lifespan | Short | Long |
| Offspring number | Many | Few |
| Offspring size | Small | Large |
| Parental care | Minimal | Extensive |
| Maturation | Rapid | Slow |
| Mortality | Type III (high juvenile) | Type I (high old age) |

**Reality:** Most species fall on continuum, not strict dichotomy

### Survivorship Curves

**Type I** - K-selected pattern
- Low juvenile mortality, high old-age mortality
- Examples: Humans, elephants, most large mammals

**Type II** - Constant mortality rate
- Equal probability of death at any age
- Examples: Some birds, rodents, lizards

**Type III** - r-selected pattern
- Very high juvenile mortality, survivors live longer
- Examples: Fish, marine invertebrates, plants producing many seeds

---

## Population Regulation

### Intraspecific Competition

Competition among members of same species

**Resource Competition**
- Scramble: All share resources equally → all may suffer
- Contest: Dominant individuals get resources → winners/losers

**Self-Thinning in Plants**
- Seedlings germinate densely → competition → death of smaller individuals
- Final density inversely related to plant size
- -3/2 self-thinning law: log(density) vs. log(biomass) slope ≈ -3/2

### Metapopulation Dynamics

**Metapopulation** = set of discrete populations connected by dispersal

**Dynamics:**
- Local populations go extinct (disturbance, stochasticity)
- Recolonization from other patches
- Regional persistence despite local instability

**Requirements:**
- Multiple habitat patches
- Dispersal between patches (but not too much)
- Asynchronous dynamics across patches

**Example: Butterflies on meadows**
- Individual meadows may lose butterfly population
- Recolonization from nearby meadows maintains regional presence
- Corridor preservation critical

---

## Population Cycles and Oscillations

### Predator-Prey Cycles

**Lotka-Volterra Model**
- Predator and prey populations oscillate
- Prey increase → predators increase (more food)
- Predators overconsume prey → prey crash
- Predators decline (starvation) → prey recover
- Repeat

**Classic Example: Lynx and Snowshoe Hare**
- Hudson's Bay Company fur records (1845-1935)
- ~10-year cycles in both populations
- Hare peak precedes lynx peak by 1-2 years

**Complications:**
- Hare cycles continue without lynx present
- Multiple factors: predation + food quality + stress
- Not pure Lotka-Volterra

### Other Cyclic Patterns

**Lemming Cycles**
- 3-4 year cycles in Arctic rodents
- Causes debated: predation, food quality, social stress

**Periodic Cicadas**
- 13- or 17-year emergence cycles
- Prime numbers reduce encounter with predators on different cycles
- Predator satiation strategy (emerge in huge numbers)

---

## Population Viability Analysis (PVA)

### Small Population Challenges

**Genetic Problems**
- Inbreeding depression (reduced fitness from mating with relatives)
- Loss of genetic variation → reduced adaptability
- Genetic drift stronger in small populations

**Demographic Stochasticity**
- Random variation in births/deaths
- Sex ratio imbalances
- More severe in small populations

**Environmental Stochasticity**
- Random variation in environmental conditions
- Bad years can push small populations to extinction

**Allee Effects**
- Positive density dependence at low densities
- Mate finding difficult
- Reduced cooperative behavior (hunting, predator vigilance)
- Example: Passenger pigeons needed large flocks for breeding → extinction

### Minimum Viable Population (MVP)

**MVP** = smallest population that has X% probability of surviving Y years

**Rules of Thumb:**
- **50/500 rule**: Ne = 50 to avoid inbreeding, Ne = 500 for evolutionary potential
- (Ne = effective population size, usually smaller than census size)

**Factors Determining MVP:**
- Species life history (r vs. K)
- Environmental variability
- Genetic diversity
- Habitat quality and connectivity

---

## Applied Population Ecology

### Sustainable Harvesting

**Maximum Sustainable Yield (MSY)**
- Harvest at rate equal to population growth
- Theory: Harvest at K/2 where growth rate maximized
- Reality: Difficult to estimate K, r; populations fluctuate

**Fisheries Collapse**
- Grand Banks cod fishery (collapsed 1992)
- Overfishing drove population below recovery threshold
- Failed to account for age structure (removed large, productive individuals)

**Improved Approaches:**
- Ecosystem-based management
- Precautionary principle (uncertainty → conservative harvest)
- Marine Protected Areas (no-take zones for reproduction)

### Invasive Species Management

**Exponential Growth Phase**
- Early detection critical (easier to eradicate when small)
- Example: Nutria eradication in UK successful, failed in US Gulf Coast (detected too late)

**Established Populations**
- Control becomes ongoing management, not eradication
- Example: Burmese pythons in Everglades (10,000s present, impossible to eradicate)

**Prevention Best Strategy**
- Border controls, ballast water treatment
- Cost-effective compared to control efforts

### Endangered Species Recovery

**Bottleneck Recovery Examples:**

**Northern Elephant Seals**
- Hunted to ~20 individuals (1890s)
- Protected → exponential growth → 200,000+ today
- Success but low genetic diversity (all descended from bottleneck survivors)

**California Condors**
- Declined to 27 individuals (1987)
- All captured for captive breeding
- Gradual reintroduction → ~500 individuals (2023)
- Requires ongoing management (lead poisoning threat)

---

## Key Terms

| Term | Definition |
|------|------------|
| **Carrying capacity (K)** | Maximum population size environment can sustain |
| **Density dependence** | Effects that change with population density |
| **r-selection** | Strategy favoring rapid growth (many offspring, short life) |
| **K-selection** | Strategy favoring competitive ability (few offspring, long life) |
| **Metapopulation** | Set of discrete populations connected by dispersal |
| **Allee effect** | Positive relationship between fitness and density at low densities |
| **MVP** | Minimum viable population - smallest size for persistence |

---

## Summary

- Population size changes through births, deaths, immigration, and emigration
- Exponential growth (J-curve) occurs without limits; logistic growth (S-curve) incorporates carrying capacity
- Density-dependent factors (competition, predation, disease) regulate populations near K
- Life history strategies range from r-selected (many offspring, short life) to K-selected (few offspring, long life)
- Small populations face genetic, demographic, and environmental challenges requiring MVP thresholds
- Predator-prey systems can oscillate cyclically (lynx-hare example)
- Applied population ecology informs fisheries management, invasive species control, and endangered species recovery
- Sustainable management requires understanding growth rates, age structure, and environmental variability

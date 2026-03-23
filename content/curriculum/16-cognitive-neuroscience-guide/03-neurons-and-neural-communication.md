# Neurons and Neural Communication

## Overview

The neuron is the fundamental unit of brain function. Approximately 86 billion neurons communicate through electrical and chemical signals, forming the basis of all cognition. This chapter covers neuron structure, how signals propagate within neurons (action potentials), how neurons communicate at synapses, and how neurotransmitters modulate brain function.

## Key Concepts

### Neuron Structure

**Basic Components:**

```
         Dendrites
            │││
            ▼▼▼
    ┌───────────────┐
    │   Cell Body   │ ← Soma (contains nucleus)
    │    (Soma)     │
    └───────┬───────┘
            │
      Axon Hillock
            │
            ▼
    ┌───────────────┐
    │     Axon      │ ← Can be very long (up to 1m)
    │  (myelinated) │
    └───────┬───────┘
            │
            ▼
     Axon Terminals
        (boutons)
            │
            ▼
       Synapses → Next neuron
```

| Component | Function |
|-----------|----------|
| **Dendrites** | Receive input from other neurons |
| **Soma (cell body)** | Contains nucleus, integrates signals |
| **Axon hillock** | Where action potential initiates |
| **Axon** | Conducts signal away from soma |
| **Myelin sheath** | Insulates axon, speeds conduction |
| **Nodes of Ranvier** | Gaps in myelin where signal regenerates |
| **Axon terminals** | Release neurotransmitters at synapses |

### Types of Neurons

**By Function:**
- **Sensory (afferent)** - Carry info toward CNS
- **Motor (efferent)** - Carry commands away from CNS
- **Interneurons** - Local processing within CNS

**By Structure:**
- **Multipolar** - Many dendrites, one axon (most common)
- **Bipolar** - One dendrite, one axon (sensory)
- **Unipolar** - Single process splits (sensory)

### Glial Cells

Support cells outnumber neurons ~1:1

| Type | Function |
|------|----------|
| **Astrocytes** | Nutrient supply, blood-brain barrier, synaptic regulation |
| **Oligodendrocytes** | Form myelin in CNS |
| **Schwann cells** | Form myelin in PNS |
| **Microglia** | Immune function, debris cleanup |
| **Ependymal cells** | Line ventricles, produce CSF |

### Resting Membrane Potential

**At rest, neurons maintain ~-70mV potential (inside negative relative to outside)**

**Ionic Basis:**
- **Na⁺ (sodium)** - Higher outside cell
- **K⁺ (potassium)** - Higher inside cell
- **Cl⁻ (chloride)** - Higher outside
- **Organic anions (A⁻)** - Inside cell (proteins)

**Maintained by:**
- **Na⁺/K⁺-ATPase pump** - 3 Na⁺ out, 2 K⁺ in (uses ATP)
- **Selective permeability** - Membrane more permeable to K⁺ at rest
- **Electrochemical gradients**

### The Action Potential

**All-or-none electrical signal propagating down axon**

**Phases:**

| Phase | Membrane Potential | Ion Channels |
|-------|-------------------|--------------|
| 1. Resting | -70mV | K⁺ leak channels open |
| 2. Depolarization | -70 → +30mV | Voltage-gated Na⁺ channels open |
| 3. Repolarization | +30 → -70mV | Na⁺ channels inactivate, K⁺ channels open |
| 4. Hyperpolarization | Below -70mV | K⁺ channels slow to close |
| 5. Return to rest | -70mV | Na⁺/K⁺ pump restores gradients |

**Key Properties:**
- **Threshold** - Must reach ~-55mV to trigger
- **All-or-none** - Once triggered, full amplitude regardless of stimulus strength
- **Refractory periods:**
  - Absolute: Cannot fire another AP
  - Relative: Can fire but requires stronger stimulus
- **Frequency coding** - Stimulus intensity encoded by firing rate, not amplitude

### Propagation of Action Potentials

**Unmyelinated axons:**
- Continuous conduction
- Slow (0.5-2 m/s)
- AP regenerates at each point

**Myelinated axons:**
- **Saltatory conduction** - Signal "jumps" between nodes of Ranvier
- Fast (up to 120 m/s)
- More energy efficient

### Synaptic Transmission

**The Synapse:**

```
PRESYNAPTIC NEURON
        │
  Axon Terminal
        │
   Synaptic vesicles (contain neurotransmitter)
        │
        ▼
═══════════════════  ← Synaptic cleft (~20nm)
        ▼
   Receptors on...
        │
  POSTSYNAPTIC NEURON (dendrite/soma)
```

**Steps of Chemical Synaptic Transmission:**

1. **Action potential arrives** at axon terminal
2. **Voltage-gated Ca²⁺ channels open** → Ca²⁺ enters
3. **Ca²⁺ triggers vesicle fusion** with membrane (exocytosis)
4. **Neurotransmitter released** into synaptic cleft
5. **NT binds receptors** on postsynaptic membrane
6. **Ion channels open/close** → postsynaptic potential
7. **NT cleared** by reuptake, enzymatic degradation, or diffusion

### Postsynaptic Potentials

| Type | Effect | Ion Flow | Neurotransmitter Example |
|------|--------|----------|-------------------------|
| **EPSP** (excitatory) | Depolarization (toward threshold) | Na⁺ in | Glutamate |
| **IPSP** (inhibitory) | Hyperpolarization (away from threshold) | Cl⁻ in or K⁺ out | GABA |

**Summation:**
- **Temporal** - Multiple signals from same synapse over time
- **Spatial** - Signals from multiple synapses simultaneously
- If sum at axon hillock reaches threshold → action potential

### Major Neurotransmitters

#### Amino Acids

| NT | Type | Functions |
|----|------|-----------|
| **Glutamate** | Excitatory | Main excitatory NT; learning, memory |
| **GABA** | Inhibitory | Main inhibitory NT; reduces neural activity |
| **Glycine** | Inhibitory | Inhibition in spinal cord, brainstem |

#### Monoamines

| NT | Functions | Clinical Relevance |
|----|-----------|-------------------|
| **Dopamine** | Reward, motivation, motor control | Parkinson's, addiction, schizophrenia |
| **Serotonin (5-HT)** | Mood, sleep, appetite | Depression, anxiety |
| **Norepinephrine** | Arousal, attention, stress response | ADHD, depression |

#### Acetylcholine (ACh)
- Muscle contraction (neuromuscular junction)
- Attention, learning, memory
- **Clinical:** Alzheimer's (ACh deficit), myasthenia gravis

#### Neuropeptides
- Larger molecules, slower acting, modulatory
- **Examples:** Endorphins (pain, pleasure), oxytocin (bonding), substance P (pain)

### Receptor Types

**Ionotropic (Ligand-gated ion channels):**
- NT binding directly opens ion channel
- Fast (milliseconds)
- Examples: AMPA, NMDA (glutamate), GABA-A, nicotinic ACh

**Metabotropic (G-protein coupled receptors):**
- NT binding activates second messenger cascade
- Slower but longer-lasting effects
- Can modulate many cellular processes
- Examples: Dopamine receptors, muscarinic ACh, metabotropic glutamate

### Neural Plasticity

**Hebbian Learning:** "Neurons that fire together, wire together"

**Long-Term Potentiation (LTP):**
- Persistent strengthening of synapses
- Cellular basis of learning and memory
- Requires coincident pre- and postsynaptic activity
- NMDA receptors critical (coincidence detectors)

**Long-Term Depression (LTD):**
- Weakening of synaptic connections
- Important for refining circuits

## Real-World Examples

- **Multiple sclerosis:** Demyelination → slowed/blocked conduction → motor and sensory deficits
- **Parkinson's disease:** Loss of dopamine neurons in substantia nigra → motor symptoms
- **Antidepressants (SSRIs):** Block serotonin reuptake → more serotonin in synapse
- **Anesthetics:** Often enhance GABA inhibition → loss of consciousness
- **Nerve agents:** Block acetylcholinesterase → excess ACh → muscle paralysis

---

## Key Terms

| Term | Definition |
|------|------------|
| **Action potential** | All-or-none electrical signal in neurons |
| **Synapse** | Junction where neurons communicate |
| **Neurotransmitter** | Chemical messenger between neurons |
| **EPSP/IPSP** | Excitatory/inhibitory postsynaptic potential |
| **Myelin** | Insulating sheath speeding conduction |
| **Reuptake** | Recycling of neurotransmitter back into presynaptic terminal |
| **LTP** | Long-term potentiation; synaptic strengthening |
| **Receptor** | Protein that binds neurotransmitter |

---

## Summary

Neurons communicate through electrical signals (action potentials) within the cell and chemical signals (neurotransmitters) between cells. The action potential is an all-or-none wave of depolarization propagating down the axon. At synapses, neurotransmitters bind receptors to produce excitatory or inhibitory effects. Major neurotransmitter systems (glutamate, GABA, dopamine, serotonin, acetylcholine) modulate different aspects of cognition. Synaptic plasticity—strengthening or weakening of connections—underlies learning and memory.

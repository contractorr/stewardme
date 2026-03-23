# Mutations and Genetic Variation

## Overview

Mutations are changes in DNA sequence, serving as both the source of genetic variation and the cause of many diseases. While often associated with harmful effects, mutations drive evolution and create the diversity within and between species. Understanding mutation types, their causes, and consequences is essential for genetics, medicine, and biotechnology.

## What is a Mutation?

### Definition

A mutation is any permanent change in DNA sequence. Mutations can occur in:
- **Somatic cells**: Affect only the individual, not passed to offspring
- **Germ cells**: Heritable, transmitted to next generation

### Mutation vs Polymorphism

**Mutation**: Rare change (typically <1% population frequency)

**Polymorphism**: Common variant (>1% frequency), often neutral or beneficial

**Single Nucleotide Polymorphism (SNP)**: Single base-pair variation; most common type of genetic variation in humans (~10 million SNPs in human genome)

## Types of Mutations by Scale

### Small-Scale Mutations (Gene Mutations)

**Point Mutations**: Single nucleotide change

| Type | Description | Example |
|------|-------------|---------|
| Silent (Synonymous) | Changes codon but not amino acid | GAA → GAG (both = glutamic acid) |
| Missense (Nonsynonymous) | Changes amino acid | GAA → GTA (glutamic acid → valine) |
| Nonsense | Creates stop codon | UAC → UAG (tyrosine → STOP) |

**Insertions and Deletions (Indels)**: Addition or removal of nucleotides

**Frameshift mutations**: Indels not in multiples of 3
- Shifts reading frame
- Changes all downstream amino acids
- Often creates premature stop codon

**In-frame indels**: Multiples of 3 nucleotides
- Adds or removes amino acids
- Maintains reading frame

### Large-Scale Mutations (Chromosomal Mutations)

**Deletions**: Loss of chromosome segment

**Duplications**: Segment copied, often tandem

**Inversions**: Segment flipped 180°

**Translocations**: Segment moved to different chromosome
- **Reciprocal**: Exchange between two chromosomes
- **Non-reciprocal**: One-way transfer

**Chromosome number changes**:
- **Aneuploidy**: Abnormal chromosome number (2n ± chromosomes)
- **Polyploidy**: Complete extra chromosome sets (3n, 4n, etc.)

### Comparison of Mutation Effects

| Mutation Type | Severity | Frequency | Examples |
|---------------|----------|-----------|----------|
| Silent | None | High | ~25% of point mutations |
| Missense | Variable | Moderate | Sickle cell (severe), many benign |
| Nonsense | Usually severe | Low | β-thalassemia, Duchenne MD |
| Frameshift | Usually severe | Low | Tay-Sachs, cystic fibrosis |
| Large deletions | Severe | Rare | Duchenne MD, Prader-Willi |
| Duplications | Variable | Moderate | Gene families, some diseases |

## Causes of Mutations

### Spontaneous Mutations

Occur naturally without external agents.

**DNA Replication Errors**:
- DNA polymerase occasionally inserts wrong nucleotide
- Proofreading reduces but doesn't eliminate errors
- Replication rate: ~10^-10 errors per base pair per cell division

**Spontaneous DNA Damage**:
- **Depurination**: Loss of purine base (~5000 per human cell per day)
- **Deamination**: Cytosine → Uracil (~100 per cell per day)
- **Oxidative damage**: Reactive oxygen species modify bases

**Transposable Elements**:
- DNA sequences that move within genome
- ~45% of human genome consists of transposable element sequences
- Can insert into genes, disrupting function

**Replication Slippage**:
- In repetitive sequences (microsatellites)
- DNA polymerase slips, adding or removing repeats
- Causes trinucleotide repeat expansion diseases

### Induced Mutations

Caused by external agents (mutagens).

**Chemical Mutagens**:

| Mutagen | Mechanism | Example Disease/Effect |
|---------|-----------|----------------------|
| Base analogs | Incorporated into DNA, mispair | 5-bromouracil research tool |
| Alkylating agents | Add alkyl groups to bases | Chemotherapy drugs, tobacco |
| Deaminating agents | Convert bases to different forms | Nitrous acid, nitrites |
| Intercalating agents | Insert between bases, cause indels | Ethidium bromide, aflatoxin |
| Oxidizing agents | Create DNA lesions | Hydrogen peroxide, cigarette smoke |

**Physical Mutagens**:

**UV Radiation**:
- Creates thymine dimers (covalent bonds between adjacent thymines)
- Major cause of skin cancer
- UVB (280-320 nm) most mutagenic

**Ionizing Radiation**:
- X-rays, gamma rays, alpha/beta particles
- Breaks DNA strands, creates free radicals
- Medical imaging, nuclear accidents, cosmic radiation

**Temperature**:
- Heat increases depurination rate
- Can denature DNA repair enzymes

**Biological Mutagens**:
- **Viruses**: Insert into genome (HIV, HPV)
- **Transposons**: Mobile genetic elements

## Mutation Rates

### Variation by Organism

| Organism | Mutations per Genome per Generation |
|----------|-----------------------------------|
| RNA viruses (HIV) | 0.1 - 1 |
| Bacteria (E. coli) | 0.001 - 0.01 |
| Yeast | 0.003 |
| C. elegans | 0.03 |
| Drosophila | 0.6 |
| Mouse | 0.5 |
| Human | 60 - 100 |

### Factors Affecting Mutation Rate

**Genome size**: Larger genomes accumulate more mutations

**Generation time**: Longer-lived organisms have more cell divisions

**DNA repair efficiency**: Better repair = lower mutation rate

**Environmental exposure**: Radiation, chemicals increase rate

**Replication fidelity**: Error rate of DNA polymerase

**Parental age**: Human paternal age effect (more mutations from older fathers)

## DNA Repair Mechanisms

Cells have multiple systems to detect and fix DNA damage.

### Direct Repair

**Photoreactivation**: Photolyase enzyme directly reverses thymine dimers using light energy (not in humans)

**Alkyltransferases**: Remove alkyl groups from guanine

### Excision Repair

**Base Excision Repair (BER)**:
1. DNA glycosylase removes damaged base
2. AP endonuclease cuts sugar-phosphate backbone
3. DNA polymerase fills gap
4. DNA ligase seals nick

**Nucleotide Excision Repair (NER)**:
1. Recognizes bulky lesions (thymine dimers, chemical adducts)
2. Endonucleases cut DNA on both sides of lesion
3. Helicase removes damaged segment (12-24 nucleotides)
4. DNA polymerase fills gap
5. DNA ligase seals

**Defects cause diseases**:
- **Xeroderma pigmentosum**: NER defect, extreme UV sensitivity, high skin cancer risk

### Mismatch Repair (MMR)

Corrects base-pairing errors after replication:
1. MutS protein recognizes mismatch
2. MutL recruits other enzymes
3. Strand discrimination (newly synthesized strand identified)
4. Exonuclease removes segment containing error
5. DNA polymerase resynthesizes
6. DNA ligase seals

**Defects cause**:
- **Lynch syndrome**: Hereditary colorectal cancer
- Microsatellite instability in tumors

### Double-Strand Break Repair

**Non-Homologous End Joining (NHEJ)**:
- Directly rejoins broken ends
- Fast but error-prone (may lose/add nucleotides)
- Primary mechanism in mammals

**Homologous Recombination (HR)**:
- Uses sister chromatid as template
- Accurate but requires homologous sequence
- Active in S/G2 phases

**Defects cause**:
- **BRCA1/BRCA2 mutations**: Impaired HR, breast/ovarian cancer predisposition

## Mutation Effects on Fitness

### Deleterious Mutations

Reduce organism's fitness (survival/reproduction).

**Recessive lethal**: Fatal in homozygotes, hidden in heterozygotes (e.g., cystic fibrosis)

**Dominant lethal**: Fatal even in heterozygotes; selected against immediately unless late-acting (Huntington's)

**Mildly deleterious**: Small fitness reduction, gradually eliminated by selection

**Most mutations**: Slightly deleterious or neutral

### Beneficial Mutations

Increase fitness; rare but crucial for evolution.

**Examples**:
- **Lactase persistence**: Continued lactose digestion in adulthood (selected in dairy-farming populations)
- **CCR5-Δ32**: HIV resistance (32-base deletion)
- **Tibetan altitude adaptation**: EPAS1 variants
- **Antibiotic resistance**: Mutations in bacterial target genes

### Neutral Mutations

No effect on fitness; neither selected for nor against.

**Silent mutations**: Most are neutral

**Intron mutations**: Usually neutral unless affecting splicing

**Synonymous codon changes**: May affect translation speed but often minimal fitness effect

**Molecular clock**: Neutral mutations accumulate at constant rate, used for evolutionary dating

## Sources of Genetic Variation

### New Mutations

Provide raw material for evolution.

**Per-generation mutation rate**: ~1.2 × 10^-8 per nucleotide in humans

**Human genome**: ~3 billion base pairs → 60-100 new mutations per person

### Sexual Reproduction

Reshuffles existing variation.

**Crossing over**: Recombines alleles on same chromosome (~50 crossovers per meiosis)

**Independent assortment**: Random distribution of chromosomes (2^23 = 8 million combinations in humans)

**Random fertilization**: Any sperm + any egg

**Combined effect**: Virtually unlimited genetic combinations

### Gene Flow (Migration)

Introduces alleles from other populations, increasing variation.

**Example**: Human migrations spreading genetic variants globally

### Polyploidy

Whole-genome duplication; common in plants, rare in animals.

**Autopolyploidy**: Duplication within species

**Allopolyploidy**: Hybridization + duplication of genomes from different species

**Importance**:
- ~70% of flowering plants have polyploid ancestry
- Wheat (hexaploid), cotton (tetraploid)
- Provides genetic material for evolution

### Horizontal Gene Transfer

Gene transfer between organisms without reproduction; common in bacteria.

**Mechanisms**:
- **Transformation**: Uptake of naked DNA
- **Transduction**: Viral transfer
- **Conjugation**: Direct cell-to-cell transfer

**Example**: Antibiotic resistance genes spread among bacteria

## Special Types of Mutations

### Trinucleotide Repeat Expansions

Repetitive three-nucleotide sequences (like CAG) can expand during replication.

**Mechanism**: DNA polymerase slippage in repeat regions

**Diseases**:

| Disease | Gene | Repeat | Normal Range | Disease Range |
|---------|------|--------|--------------|---------------|
| Huntington's | HTT | CAG | 6-35 | 36-250+ |
| Fragile X syndrome | FMR1 | CGG | 6-54 | 200-2000+ |
| Myotonic dystrophy | DMPK | CTG | 5-37 | 50-4000+ |

**Anticipation**: Disease severity increases/onset earlier in successive generations as repeats expand

### Mitochondrial Mutations

Mitochondrial DNA (mtDNA) has its own genome (~16,500 bp, 37 genes).

**Features**:
- Maternal inheritance (sperm mitochondria excluded at fertilization)
- High mutation rate (10× nuclear DNA; less efficient repair, oxidative damage)
- **Heteroplasmy**: Mix of mutant and normal mtDNA in cell
- **Threshold effect**: Disease when mutant percentage exceeds threshold

**Diseases**: LHON (Leber's hereditary optic neuropathy), MELAS, mitochondrial myopathies

### Germline Mosaicism

Mutation arises during germ cell development; some gametes affected, others normal.

**Consequence**: Parent unaffected but multiple offspring can inherit mutation

**Example**: Some Duchenne muscular dystrophy cases from germline mosaic mothers

### Somatic Mutations

Occur in body cells, not inherited.

**Cancer**: Accumulation of somatic mutations in oncogenes and tumor suppressors

**Aging**: Somatic mutation accumulation may contribute to aging

**Mosaicism**: Individual has populations of cells with different genotypes

## Real-World Examples

**Example 1: Sickle Cell Anemia**
Point mutation (A→T) in β-globin gene (GAG→GTG) changes glutamic acid to valine at position 6. Demonstrates how single nucleotide change causes severe disease. Heterozygote advantage in malaria-endemic regions maintains allele.

**Example 2: Chronic Myeloid Leukemia**
Philadelphia chromosome: reciprocal translocation between chromosomes 9 and 22 creates BCR-ABL fusion gene, producing constitutively active tyrosine kinase. Targeted therapy (imatinib) blocks this kinase.

**Example 3: Lactose Intolerance**
Most mammals lose lactase expression after weaning. Mutations in regulatory region allowed continued expression in some human populations. Strong positive selection where dairy farming practiced. Example of recent evolutionary change.

**Example 4: Antibiotic Resistance**
Bacteria rapidly evolve resistance through mutations and horizontal gene transfer. MRSA (methicillin-resistant *Staphylococcus aureus*) has mutations altering penicillin-binding protein. Demonstrates evolution in real time.

**Example 5: CRISPR-Cas9 Off-Target Effects**
Gene editing can create unintended mutations at similar DNA sequences. Understanding mutation mechanisms helps predict and minimize off-target effects, improving precision medicine safety.

## Mutation and Evolution

### Mutation-Selection Balance

Deleterious alleles persist because mutation continually reintroduces them despite selection removing them.

**Equilibrium frequency** depends on mutation rate and selection strength.

### Neutral Theory

Most molecular evolution involves neutral or nearly neutral mutations fixed by genetic drift, not selection.

**Implications**:
- Constant molecular clock (useful for dating evolutionary events)
- Most protein differences between species functionally equivalent
- Genome contains much neutral variation

### Adaptive Evolution

Rare beneficial mutations spread through positive selection.

**Selective sweep**: Beneficial mutation rises to high frequency, reducing variation nearby

**Balancing selection**: Maintains multiple alleles (heterozygote advantage, frequency-dependent selection)

## Key Terms

**Mutation**: Permanent change in DNA sequence

**Point Mutation**: Single nucleotide change

**Frameshift Mutation**: Insertion/deletion causing reading frame shift

**Aneuploidy**: Abnormal chromosome number

**Mutagen**: Agent causing mutations

**DNA Repair**: Cellular mechanisms correcting DNA damage

**Heteroplasmy**: Mix of different mitochondrial genomes in cell

**Germline Mutation**: Heritable mutation in reproductive cells

**Somatic Mutation**: Non-heritable mutation in body cells

**Polymorphism**: Common genetic variant (>1% frequency)

**SNP**: Single Nucleotide Polymorphism, most common variation type

**Trinucleotide Repeat**: Repetitive three-base sequence that can expand

## Summary

Mutations are the ultimate source of genetic variation, arising from replication errors, spontaneous DNA damage, and environmental mutagens. They range from single-nucleotide changes to large chromosomal rearrangements, with effects spanning from silent to lethal. While most mutations are neutral or slightly deleterious, rare beneficial mutations drive adaptation and evolution. Sophisticated DNA repair mechanisms reduce but cannot eliminate mutations, balancing genome stability with the variation necessary for evolution. Understanding mutations is crucial for comprehending genetic diseases, cancer development, antibiotic resistance, and evolutionary processes. Sexual reproduction, gene flow, and other mechanisms amplify variation created by mutations, generating the diversity within and between species. The study of mutations connects molecular genetics to medicine, evolution, and biotechnology applications.

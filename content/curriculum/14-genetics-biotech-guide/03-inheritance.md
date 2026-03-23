# Patterns of Inheritance

## Overview

Inheritance explains how traits pass from parents to offspring through genetic material. While molecular genetics examines genes themselves, this chapter explores how genes behave during reproduction and development. From Mendel's pea plants to modern understanding of chromosomal mechanisms, inheritance patterns reveal the rules governing biological variation.

## Mendelian Genetics

### Mendel's Experiments

Gregor Mendel (1822-1884) studied garden peas, choosing them for:
- Distinct, observable traits (seed shape, color, height)
- Short generation time
- Easy controlled breeding
- True-breeding varieties (self-fertilization produces identical offspring)

**Experimental Design**:
1. Established true-breeding parental (P) lines
2. Cross-pollinated to create F1 (first filial) generation
3. Self-fertilized F1 to produce F2 generation
4. Counted ratios of different traits

### Mendel's Laws

**Law of Segregation (First Law)**
- Each parent has two copies of each gene (alleles)
- Alleles separate during gamete formation
- Each gamete receives one allele
- Offspring inherit one allele from each parent

**Law of Independent Assortment (Second Law)**
- Genes for different traits segregate independently
- Applies to genes on different chromosomes or far apart on same chromosome
- Creates new allele combinations

### Key Terminology

| Term | Definition | Example |
|------|------------|---------|
| Gene | Unit of heredity at specific chromosome location | Gene for seed color |
| Allele | Alternative form of a gene | Yellow (Y) or green (y) |
| Homozygous | Two identical alleles | YY or yy |
| Heterozygous | Two different alleles | Yy |
| Dominant | Allele expressed in heterozygotes | Y (yellow) |
| Recessive | Allele masked in heterozygotes | y (green) |
| Genotype | Genetic makeup | Yy |
| Phenotype | Observable trait | Yellow seeds |

### Monohybrid Crosses

Cross involving one trait. Example: Seed color (Y = yellow, dominant; y = green, recessive)

**P generation**: YY × yy

**F1 generation**: All Yy (yellow, because Y is dominant)

**F2 generation** (F1 × F1):
- Genotypic ratio: 1 YY : 2 Yy : 1 yy
- Phenotypic ratio: 3 yellow : 1 green

**Punnett Square**:
```
        Y      y
    -----------
  Y | YY  | Yy |
    -----------
  y | Yy  | yy |
    -----------
```

### Dihybrid Crosses

Cross involving two traits. Example: Seed color (Y/y) and seed shape (R/r, round/wrinkled)

**P generation**: YYRR × yyrr

**F1 generation**: All YyRr (yellow, round)

**F2 generation**: 9:3:3:1 ratio
- 9 yellow, round (Y_R_)
- 3 yellow, wrinkled (Y_rr)
- 3 green, round (yyR_)
- 1 green, wrinkled (yyrr)

This 9:3:3:1 ratio confirms independent assortment.

### Test Cross

Cross between individual of unknown genotype and homozygous recessive individual to determine genotype.

**If unknown is homozygous (YY × yy)**: All offspring heterozygous (Yy)

**If unknown is heterozygous (Yy × yy)**: 1:1 ratio (Yy : yy)

## Beyond Simple Dominance

### Incomplete Dominance

Neither allele completely dominant; heterozygote shows intermediate phenotype.

**Example: Snapdragon flower color**
- RR = red
- RW = pink (intermediate)
- WW = white

F1 (RR × WW) = all pink

F2 (pink × pink) = 1 red : 2 pink : 1 white

### Codominance

Both alleles fully expressed in heterozygote.

**Example: Human ABO blood type**
- IAIA or IAi = Type A
- IBIB or IBi = Type B
- IAIB = Type AB (both A and B antigens expressed)
- ii = Type O

**Blood Type Genetics Table**:

| Parents | Possible Offspring Blood Types |
|---------|-------------------------------|
| A × A | A, O |
| A × B | A, B, AB, O |
| A × AB | A, B, AB |
| A × O | A, O |
| B × B | B, O |
| B × AB | A, B, AB |
| B × O | B, O |
| AB × AB | A, B, AB |
| AB × O | A, B |
| O × O | O |

### Multiple Alleles

More than two alleles exist in population (though individuals have only two).

**Examples**:
- ABO blood groups (three alleles: IA, IB, i)
- Coat color in rabbits (four alleles)
- HLA genes in humans (hundreds of alleles)

### Pleiotropy

One gene affects multiple phenotypic traits.

**Example: Sickle cell allele**
- Abnormal hemoglobin shape
- Sickle-shaped red blood cells
- Reduced oxygen delivery
- Pain, organ damage, stroke risk
- Increased malaria resistance

**Example: Phenylketonuria (PKU)**
- Single enzyme deficiency
- Affects brain development, skin pigmentation, body odor

### Epistasis

One gene masks or modifies effects of another gene.

**Example: Labrador retriever coat color**
- Gene E (pigment deposition): E_ allows color, ee prevents deposition (yellow)
- Gene B (pigment color): B_ = black, bb = brown
- Genotypes:
  - E_B_ = black
  - E_bb = brown
  - ee__ = yellow (regardless of B allele)

### Polygenic Inheritance

Multiple genes contribute to one trait; produces continuous variation.

**Examples**:
- Height
- Skin color
- Intelligence
- Eye color (multiple genes, not just one as often taught)

**Characteristics**:
- Bell curve distribution in populations
- Many intermediate phenotypes
- Environmental factors also contribute

## Chromosomal Basis of Inheritance

### Chromosome Theory

Proposed by Walter Sutton and Theodor Boveri (1902-1903):
- Chromosomes carry genes
- Chromosomes segregate during meiosis (explains Mendel's laws)
- Fertilization restores chromosome number

**Evidence**:
- Parallel behavior of genes and chromosomes during inheritance
- Chromosome number constant within species
- Thomas Hunt Morgan's fruit fly experiments (1910s)

### Sex Determination

**Humans (XY system)**:
- Females: XX (homogametic)
- Males: XY (heterogametic)
- Y chromosome contains SRY gene (sex-determining region) triggering male development

**Other systems**:
- **ZW system** (birds, butterflies): Males ZZ, females ZW
- **Haplodiploidy** (bees, ants): Females diploid, males haploid
- **Temperature-dependent** (many reptiles): Incubation temperature determines sex

### Sex-Linked Inheritance

Genes located on sex chromosomes show distinctive inheritance patterns.

**X-linked Recessive**:
- More males affected (only one X chromosome)
- Affected males have carrier mothers
- No male-to-male transmission

**Examples**:
- Color blindness (red-green)
- Hemophilia A and B
- Duchenne muscular dystrophy

**Notation**: Xc = X with recessive allele, X+ = X with dominant allele

**Crosses**:

Mother (carrier) × Father (normal):
```
XcX+ × X+Y →
- Daughters: 1/2 X+X+ (normal), 1/2 XcX+ (carriers)
- Sons: 1/2 X+Y (normal), 1/2 XcY (affected)
```

**X-linked Dominant**:
- Affects both sexes, but more females
- Affected males have all affected daughters
- Example: Rett syndrome, hypophosphatemic rickets

**Y-linked**:
- Male-to-male transmission only
- All sons of affected males affected
- Rare; few genes on Y chromosome
- Example: Male infertility genes

### Autosomal vs Sex-Linked Inheritance

| Feature | Autosomal Dominant | Autosomal Recessive | X-linked Recessive |
|---------|-------------------|--------------------|--------------------|
| Males vs Females | Equal | Equal | More males |
| Affected Parent | Usually yes | Often no | Mother carrier |
| Skips Generations | Rare | Common | Common |
| Male-to-Male | Yes | Yes | Never |

## Linkage and Recombination

### Gene Linkage

Genes on same chromosome tend to be inherited together (violates independent assortment).

**Linked genes**: Located close together on same chromosome

**Unlinked genes**: On different chromosomes or far apart on same chromosome

### Recombination

During meiosis, crossing over exchanges DNA segments between homologous chromosomes, creating new allele combinations.

**Recombination Frequency**: Percentage of recombinant offspring

**Relationship to distance**:
- Genes farther apart = more recombination
- 1% recombination = 1 map unit (centimorgan)

**Example**: Genes A and B

If 10% recombinant offspring produced, genes are 10 map units apart.

### Genetic Maps

Linear diagrams showing relative positions of genes on chromosomes based on recombination frequencies.

**Creating Maps**:
1. Measure recombination frequencies between gene pairs
2. Calculate map distances
3. Order genes based on distances

**Example**:
- A-B: 10 map units
- B-C: 15 map units
- A-C: 25 map units

Gene order: A—(10)—B—(15)—C

### Complete Linkage

Genes so close that recombination essentially never occurs.

**Example**: Some genes in humans show no recombination in practical experiments.

## Pedigree Analysis

### Pedigree Symbols

- Square = male
- Circle = female
- Diamond = sex unknown
- Filled shape = affected individual
- Half-filled = carrier (heterozygote)
- Horizontal line = mating
- Vertical line = offspring
- Roman numerals = generations

### Determining Inheritance Patterns

**Autosomal Dominant**:
- Appears every generation
- Both sexes equally affected
- Affected individuals usually have affected parent

**Autosomal Recessive**:
- Skips generations
- Both sexes equally affected
- Parents of affected often unaffected (carriers)
- Consanguinity (related parents) increases risk

**X-linked Recessive**:
- More affected males
- Affected males connected through carrier females
- No male-to-male transmission
- Skips generations

**X-linked Dominant**:
- More affected females
- Affected males have all affected daughters, no affected sons
- Does not skip generations

## Real-World Examples

**Example 1: Cystic Fibrosis**
Autosomal recessive disorder caused by mutations in CFTR gene. Two carrier parents (Cc × Cc) have 25% chance of affected child (cc), 50% chance of carrier child (Cc), 25% chance of unaffected non-carrier (CC).

**Example 2: Huntington's Disease**
Autosomal dominant caused by expanded CAG repeats in huntingtin gene. Affected parent (Hh) has 50% chance of passing allele to each child. Shows anticipation (earlier onset in successive generations).

**Example 3: Hemophilia in European Royalty**
Queen Victoria carried X-linked hemophilia allele, passing it to Russian, Spanish, and German royal families. Demonstrated X-linked recessive pattern: carrier females, affected males, no male-to-male transmission.

**Example 4: ABO Incompatibility**
Mother with type O blood (ii) carrying type B baby (IBi from father) may produce anti-B antibodies causing hemolytic disease. Demonstrates codominance and multiple alleles.

**Example 5: Sickle Cell and Malaria**
Heterozygotes (HbAHbS) have some sickle cells but also malaria resistance. In malaria-endemic regions, this heterozygote advantage maintains sickle allele in population despite homozygous disadvantage.

## Key Terms

**Allele**: Alternative form of a gene

**Dominant**: Allele expressed in heterozygotes

**Recessive**: Allele masked by dominant allele in heterozygotes

**Homozygous**: Two identical alleles for a gene

**Heterozygous**: Two different alleles for a gene

**Genotype**: Genetic composition

**Phenotype**: Observable characteristics

**Incomplete Dominance**: Heterozygote has intermediate phenotype

**Codominance**: Both alleles fully expressed in heterozygote

**Epistasis**: One gene masks another gene's effects

**Sex-Linked**: Gene located on sex chromosome

**Linkage**: Genes on same chromosome inherited together

**Recombination**: Formation of new allele combinations via crossing over

**Pedigree**: Chart showing inheritance pattern in family

## Summary

Inheritance patterns explain how genetic variation passes between generations. Mendel's laws of segregation and independent assortment provide the foundation, explaining simple dominant/recessive traits. However, inheritance often involves complications: incomplete dominance, codominance, epistasis, and polygenic traits create diverse phenotypes. The chromosomal basis of inheritance explains sex determination and sex-linked traits while accounting for linkage between genes on the same chromosome. Recombination during meiosis generates genetic diversity by shuffling linked alleles. Pedigree analysis applies these principles to trace traits through families, essential for genetic counseling. Understanding inheritance patterns enables prediction of offspring traits, diagnosis of genetic disorders, and appreciation of evolution's raw material: genetic variation.

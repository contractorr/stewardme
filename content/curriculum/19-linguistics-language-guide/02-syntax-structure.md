# Syntax: The Structure of Sentences

## Overview

Syntax is the study of how words combine to form phrases and sentences. It's the combinatorial engine of language—a finite set of rules that generates an infinite number of grammatical sentences while excluding ungrammatical ones. Syntax reveals the hidden architecture underlying every utterance we produce.

## What is Syntax?

**Definition:** The principles and rules that govern sentence structure, including word order, grammatical relationships, and hierarchical organization.

**Core Insight:** Sentences have internal structure beyond linear word sequences. The sentence "The cat chased the mouse" isn't just five words in a row—it's a hierarchical structure where *the cat* forms a unit (noun phrase), *chased the mouse* forms another (verb phrase), and these combine to form a sentence.

## Constituency and Phrase Structure

### Constituent Tests

How do we know words group into phrases? Multiple tests reveal constituency:

**Replacement Test:**
- "The old dog barked" → "It barked" (*the old dog* replaces with pronoun → constituent)
- Can't say "*The old it" replacing just *dog*

**Movement Test:**
- "John will eat pizza" → "Pizza, John will eat" (*pizza* moves → constituent)
- Can't move just part: "*Piz-, John will eat za"

**Coordination Test:**
- "The cat and the dog ran" (*the cat* and *the dog* coordinate → both constituents)

**Standalone Test:**
- Q: "What did you see?" A: "The tall building" (*the tall building* can stand alone)

### Tree Diagrams

Syntax represents structure as hierarchical trees:

```
         S (Sentence)
        / \
       /   \
      NP    VP
     / \    / \
   Det  N  V  NP
    |   |  |  / \
   The cat saw Det N
              |  |
             the dog
```

**Key Principles:**
- Binary branching (nodes have two daughters) is common
- Heads (N, V) project to phrases (NP, VP)
- Specifiers and complements attach at different levels

### Phrase Types

| Phrase | Head | Example | Structure |
|--------|------|---------|-----------|
| Noun Phrase (NP) | Noun | *the big house* | Det + Adj + N |
| Verb Phrase (VP) | Verb | *ate the apple* | V + NP |
| Adjective Phrase (AP) | Adjective | *very tall* | Adv + Adj |
| Prepositional Phrase (PP) | Preposition | *in the box* | P + NP |
| Complementizer Phrase (CP) | Complementizer | *that she left* | C + S |

## Word Order and Typology

### Basic Word Order

Languages exhibit systematic variation in constituent order:

| Type | Order | Example Languages | % of Languages |
|------|-------|-------------------|----------------|
| **SOV** | Subject-Object-Verb | Japanese, Korean, Turkish, Hindi | ~45% |
| **SVO** | Subject-Verb-Object | English, Mandarin, Spanish, French | ~42% |
| **VSO** | Verb-Subject-Object | Irish, Arabic (Classical), Tagalog | ~9% |
| **VOS** | Verb-Object-Subject | Malagasy, Fijian | ~3% |
| **OVS** | Object-Verb-Subject | Hixkaryana, Urarina | <1% |
| **OSV** | Object-Subject-Verb | Warao | <1% |

**Japanese (SOV):**
- 田中さんがリンゴを食べた
- Tanaka-san ga ringo wo tabeta
- Tanaka apple ate
- "Tanaka ate an apple"

**Irish (VSO):**
- Chonaic mé an madra
- Saw I the dog
- "I saw the dog"

### Implicational Universals

Word order correlates with other properties:

| Property | SVO/VSO Languages | SOV Languages |
|----------|-------------------|---------------|
| Prepositions vs. Postpositions | Prepositions (*in the house*) | Postpositions (*house in*) |
| Noun-Adjective Order | Often N-Adj (*house big*) | Often Adj-N (*big house*) |
| Auxiliary-Verb Order | Aux-V (*has eaten*) | V-Aux (*eaten has*) |
| Relative Clauses | Often N-Rel | Often Rel-N |

**Greenberg's Universal 3:** Languages with VSO order are always prepositional (not postpositional).

## Grammatical Relations

### Subject and Object

**Subjects** typically:
- Appear before objects (in SVO/SOV)
- Trigger verb agreement
- Control reflexive pronouns
- Are nominative case (in case-marking languages)

**Objects** typically:
- Follow verbs (in SVO/VSO)
- Are accusative case
- Can become subjects in passive voice

**English Examples:**
- Active: "The cat [subject] chased the dog [object]"
- Passive: "The dog [subject] was chased by the cat"
- Agreement: "The cat runs" vs. "*The cat run"
- Reflexive: "John saw himself" (*himself* refers to subject *John*)

### Grammatical Cases

Many languages mark grammatical relations with case morphology:

**Latin:**
- *Puella* (nominative) *puerum* (accusative) *videt*
- Girl boy sees
- "The girl sees the boy"

**Russian:**
- *Студент* (nominative) читает *книгу* (accusative)
- Student reads book
- "The student reads a book"

**Case Systems:**

| Case | Function | Example (German) |
|------|----------|------------------|
| Nominative | Subject | *der Mann* (the man) |
| Accusative | Direct object | *den Mann* |
| Dative | Indirect object | *dem Mann* |
| Genitive | Possession | *des Mannes* (of the man) |

Some languages have 10+ cases (Finnish has ~15, Hungarian has ~18).

## Movement and Transformations

### Wh-Movement

Questions move wh-words to sentence-initial position:

- Statement: "You bought *what*?"
- Question: "*What* did you buy ___?" (wh-word moves, leaves gap)

**Evidence for movement:**
- Gaps in original position
- Locality constraints (can't move arbitrarily far)
- Island effects (some structures block movement)

**Complex Example:**
- "What do you think [that Mary said [that John bought ___]]?"
- *What* originated after *bought*, moved to front

### Islands

Some structures block movement ("islands"):

**Complex NP Island:**
- ✗ "*What did you meet [the person who bought ___]?"
- (Can't extract from relative clause)

**Wh-Island:**
- ✗ "*What do you wonder [who bought ___]?"
- (Can't extract across wh-question)

These constraints appear universal, suggesting innate linguistic principles.

## X-Bar Theory

A unified framework for phrase structure:

**Every phrase has:**
1. **Head (X)**: Core element (N, V, A, P)
2. **Complement**: Sister to head (required argument)
3. **Specifier**: Daughter of phrase, sister to intermediate level
4. **Adjunct**: Optional modifier

**Schema:**
```
    XP (X Phrase)
   /  \
 Spec  X'
      /  \
     X   Complement
```

**Example (VP):**
```
       VP
      /  \
   quickly V'
          / \
         V  NP
        eat the apple
```

- *eat* = head verb
- *the apple* = complement
- *quickly* = adjunct (modifier)

## Binding Theory

Governs relationships between pronouns and their antecedents:

**Principle A:** Reflexives (*himself*) must be bound locally
- "John₁ hurt himself₁" ✓
- "*John₁ said Mary hurt himself₁" ✗

**Principle B:** Pronouns (*him*) must be free locally
- "John₁ hurt him₂" ✓ (him ≠ John)
- "*John₁ hurt him₁" ✗ (in same clause)

**Principle C:** Names (*John*) must be free everywhere
- "He₁ said John₂ left" ✓
- "*He₁ said John₁ left" ✗ (if he = John)

## Recursion and Infinity

**Recursion:** Embedding phrases within phrases of the same type

**Example:**
- "The cat sat"
- "The cat [that chased the dog] sat"
- "The cat [that chased the dog [that bit the rat]] sat"
- "The cat [that chased the dog [that bit the rat [that ate the cheese]]] sat"
- ... (infinite)

**Center-Embedding:**
- "The rat the cat chased escaped"
- "The rat the cat the dog bit chased escaped" (harder)
- Processing difficulty after 2-3 embeddings (performance limitation, not competence)

**Coordination:**
- "John and Mary left" (2 NPs)
- "John and Mary and Bill and Sue left" (unlimited)

## Universal Grammar

**Chomsky's Hypothesis:** All languages share core syntactic principles (Universal Grammar), with limited variation (parameters).

### Principles (Universal)

- **Structure Dependence:** Rules refer to hierarchical structure, not linear order
  - English questions: "The man who is here *is* happy" → "*Is* the man who is here ___ happy?"
  - Not: "*Is* the man who ___ here is happy?" (moving first *is*)
  - Rule: Move auxiliary in main clause (hierarchical), not "move first auxiliary" (linear)

- **Subjacency:** Movement crosses at most one bounding node
- **C-command:** Binding relations defined by tree structure, not word order

### Parameters (Variable)

- **Pro-drop Parameter:** Can subject pronouns be omitted?
  - Spanish: "Hablo" (I speak) — yes
  - English: "*Speak" — no

- **Head Parameter:** Do heads precede or follow complements?
  - English: Verb before object (*eat apples*)
  - Japanese: Verb after object (*apples eat*)

**Language Acquisition:** Children set parameters based on input, explaining rapid acquisition.

## Real-World Applications

**NLP Parsing:**
- Syntax parsers (Stanford Parser, spaCy) build tree structures to understand sentences
- Dependency parsing for information extraction

**Machine Translation:**
- Syntactic transfer: Parse source language → map structure → generate target language
- Neural models implicitly learn syntactic patterns

**Speech Recognition:**
- Syntax constrains word sequences, improving recognition accuracy
- "Recognize speech" more likely than "wreck a nice beach" (despite identical acoustics)

**Grammar Checkers:**
- Detect subject-verb disagreement, misplaced modifiers
- Grammarly uses syntactic analysis for suggestions

**Language Learning:**
- Explicit syntax instruction for adult learners
- Contrastive analysis of L1 vs. L2 syntax

## Key Terms

- **Syntax**: Rules governing sentence structure
- **Constituent**: Group of words forming a structural unit
- **Phrase Structure**: Hierarchical organization of constituents
- **Head**: Core element of a phrase
- **Complement**: Required argument of a head
- **Subject/Object**: Grammatical relations
- **Movement**: Displacement of constituents from base position
- **Recursion**: Embedding structures within themselves
- **Universal Grammar**: Innate linguistic knowledge
- **Parameter**: Variable property across languages

## Summary

Syntax reveals language as a combinatorial system with hierarchical structure, not just linear word sequences. Tree structures represent constituency, with phrases built around heads and related through grammatical relations like subject and object.

Languages vary systematically in word order and morphological marking, but share deep principles like structure-dependence and locality constraints. Movement operations (wh-questions, passives) and binding relations demonstrate abstract syntactic knowledge.

X-bar theory unifies diverse phrase types under a single schema. Recursion enables infinite expressiveness from finite rules. Universal Grammar hypothesizes that core syntactic principles are innate, with parameters explaining cross-linguistic variation.

Syntax underpins practical applications from NLP to language teaching, providing the structural skeleton that enables computational language processing and human language acquisition.

# Semantics & Pragmatics: Meaning in Language

## Overview

Semantics studies literal meaning—how words and sentences relate to the world. Pragmatics studies meaning in context—how speakers use language to communicate beyond literal content. Together, they explain how language conveys information, from dictionary definitions to subtle implications.

**Key Distinction:**
- **Semantics**: "What does this sentence *mean*?"
- **Pragmatics**: "What does the speaker *mean* by saying this sentence?"

## Part I: Semantics

### What is Meaning?

**Core Questions:**
- What does a word like "dog" mean?
- How do we know "All dogs are animals" is true without checking every dog?
- Why is "colorless green ideas sleep furiously" grammatical but meaningless?

### Theories of Meaning

#### 1. Reference Theory

**Idea:** Meaning = what a word refers to (its referent)

**Simple Cases:**
- "Paris" → the city Paris
- "Barack Obama" → the person Barack Obama

**Problems:**
- Synonyms: "morning star" and "evening star" both refer to Venus, but have different meanings (Frege's puzzle)
- Non-existent entities: "unicorn" has meaning but no referent
- Abstract concepts: "justice," "seven," "if" have no clear referents

#### 2. Sense and Reference (Frege)

**Gottlob Frege** distinguished:
- **Reference (Bedeutung)**: What a word picks out in the world
- **Sense (Sinn)**: Mode of presentation, cognitive content

**Example:**
- "Morning star" and "evening star" have the same reference (Venus) but different senses (how we identify it)

**Implication:** "The morning star is the evening star" is informative (different senses), unlike "The morning star is the morning star" (tautology)

#### 3. Truth-Conditional Semantics

**Idea:** Meaning of a sentence = conditions under which it's true

**Example:**
- "Snow is white" is true if and only if snow is white
- Knowing meaning = knowing truth conditions, not necessarily knowing if it's true

**Advantages:**
- Compositional: Meaning of whole from meanings of parts
- Handles logical relations (entailment, contradiction)

**Logical Operators:**
| Operator | Symbol | Example | Truth Condition |
|----------|--------|---------|-----------------|
| Negation | ¬ | "Not raining" | True if "raining" is false |
| Conjunction | ∧ | "Raining and cold" | True if both parts true |
| Disjunction | ∨ | "Raining or snowing" | True if either part true |
| Implication | → | "If it rains, it pours" | False only if antecedent true, consequent false |

#### 4. Prototype Theory

**Eleanor Rosch**: Categories have central members (prototypes) and graded membership

**Example:**
- "Bird": Robin is more prototypical than penguin or ostrich
- "Red": Fire-engine red is more prototypical than brick red

**Explains:**
- Fuzzy boundaries: Is a tomato a fruit or vegetable?
- Graded judgments: "A robin is a very bird-y bird" makes sense

### Compositionality

**Principle of Compositionality (Frege):** Meaning of complex expression derived from meanings of parts + combination rules

**Examples:**
- "Black bird" = black + bird (compositional)
- "Blackbird" = specific species (non-compositional, idiomatic)

**Importance:** Enables understanding novel sentences
- First time hearing "The purple elephant danced backwards" but you understand it

### Lexical Semantics: Word Meaning

#### Sense Relations

| Relation | Definition | Example |
|----------|------------|---------|
| **Synonymy** | Same meaning | *big* / *large* |
| **Antonymy** | Opposite meaning | *hot* / *cold* |
| **Hyponymy** | Subordinate relation | *rose* is a hyponym of *flower* |
| **Meronymy** | Part-whole | *wheel* is meronym of *car* |
| **Polysemy** | Multiple related meanings | *head* (body part, leader, top) |
| **Homonymy** | Same form, unrelated meanings | *bank* (financial institution / river edge) |

#### Semantic Features

Words decompose into features:

**Example:**
- *man* = [+HUMAN, +ADULT, +MALE]
- *woman* = [+HUMAN, +ADULT, -MALE]
- *boy* = [+HUMAN, -ADULT, +MALE]

**Explains:**
- Why "The rock is asleep" is semantically odd (*rock* lacks [+ANIMATE])
- Selectional restrictions: "eat" requires [+EDIBLE] object

#### Semantic Roles (Thematic Roles)

Words play roles in events:

| Role | Definition | Example |
|------|------------|---------|
| **Agent** | Doer of action | *John* kicked the ball |
| **Patient** | Undergoes action | John kicked *the ball* |
| **Theme** | Moved or located entity | I sent *the letter* |
| **Experiencer** | Feels/perceives | *Mary* heard the sound |
| **Instrument** | Tool for action | I cut it with *a knife* |
| **Goal** | Destination | I went *to Boston* |
| **Source** | Origin | I came *from Chicago* |
| **Location** | Where action occurs | We met *in Paris* |

**Different syntax, same roles:**
- "John broke the window" (active): John = Agent, window = Patient
- "The window was broken by John" (passive): Same semantic roles, different syntax

### Entailment and Inference

**Entailment:** A entails B if B must be true whenever A is true

**Examples:**
- "John killed Mary" → "Mary is dead" (entailment)
- "John is a bachelor" → "John is unmarried" (entailment)
- "John is unmarried" ↛ "John is a bachelor" (not entailment; might be married before or child)

**Contradiction:** Cannot both be true
- "It's raining" contradicts "It's not raining"

**Presupposition:** Background assumption taken for granted
- "John stopped smoking" presupposes "John used to smoke"
- "The King of France is bald" presupposes "There is a King of France"

### Quantification

**Quantifiers** specify quantity:

| Quantifier | Symbol | Example | Truth Condition |
|------------|--------|---------|-----------------|
| Universal | ∀ | "All dogs bark" | Every dog in domain barks |
| Existential | ∃ | "Some dog barks" | At least one dog barks |

**Scope Ambiguity:**
- "Everyone loves someone"
  - Reading 1: ∀x ∃y (x loves y) — everyone loves some person (possibly different people)
  - Reading 2: ∃y ∀x (x loves y) — there's one person everyone loves

**Negation Scope:**
- "I didn't eat *two* cookies"
  - (1) Ate fewer/more than two
  - (2) Ate zero cookies

## Part II: Pragmatics

### What is Pragmatics?

**Definition:** Study of meaning in context; how speakers convey more than what they literally say

**Why Needed:**
- Same sentence, different meanings:
  - "Can you pass the salt?" (usually request, not question about ability)
  - "It's cold in here" (often request to close window/turn up heat)

### Speech Acts (Austin, Searle)

**J.L. Austin**: Speaking is *doing things with words*

#### Types of Speech Acts

**Locutionary Act:** Uttering words with meaning
- Saying "I promise to come"

**Illocutionary Act:** Social action performed
- Promising (by saying "I promise...")

**Perlocutionary Act:** Effect on hearer
- Hearer feels reassured

#### Illocutionary Force

| Type | Function | Examples |
|------|----------|----------|
| **Assertives** | Commit speaker to truth | "It's raining," "The Earth is round" |
| **Directives** | Get hearer to do something | Commands, requests: "Close the door!" |
| **Commissives** | Commit speaker to future action | Promises, threats: "I'll be there" |
| **Expressives** | Express psychological state | Apologies, thanks: "I'm sorry," "Thank you" |
| **Declarations** | Change world through utterance | "I pronounce you married," "Meeting adjourned" |

**Felicity Conditions:** For speech act to succeed, conditions must hold
- To promise: Speaker must be able to do action, hearer wants it done, speaker commits to doing it
- "I promise it will rain tomorrow" — odd, since speaker can't control weather

### Gricean Pragmatics

**Paul Grice**: Conversation governed by **Cooperative Principle**

#### Cooperative Principle
"Make your conversational contribution such as is required, at the stage at which it occurs, by the accepted purpose or direction of the talk exchange."

#### Gricean Maxims

| Maxim | Principle | Example Violation |
|-------|-----------|-------------------|
| **Quantity** | Say neither too much nor too little | "Where's the library?" — "In the city" (too little) |
| **Quality** | Be truthful, have evidence | Lying, guessing without basis |
| **Relevance** | Be relevant | "How are you?" — "Elephants have trunks" |
| **Manner** | Be clear, brief, orderly | Obscure jargon, rambling |

#### Conversational Implicature

**Implicature:** Meaning implied beyond literal content

**Example:**
- A: "Is John a good philosopher?"
- B: "He has beautiful handwriting"
- **Implicature**: John is *not* a good philosopher (violating Relevance/Quantity to convey implicit message)

**Characteristics:**
- **Cancellable**: "He has nice handwriting... and he's also brilliant" (cancels implicature)
- **Non-detachable**: Can't rephrase to avoid implicature
- **Calculable**: Derivable from maxims + context

**Scalar Implicature:**
- "Some students passed" implicates "Not all students passed"
- <all, most, many, some, few> — saying weaker term implicates stronger one doesn't hold

### Deixis

**Deixis:** Reference depends on context

| Type | Examples | Context-Dependent Meaning |
|------|----------|---------------------------|
| **Personal** | I, you, he | Who's speaking/addressed |
| **Spatial** | here, there, this, that | Location relative to speaker |
| **Temporal** | now, then, yesterday, today | Time of utterance |
| **Discourse** | this (idea), that (mentioned earlier) | Preceding/following text |
| **Social** | tu/vous (French), honorifics | Social relationship |

**Example:**
- "I'll meet you here tomorrow" — meaning changes based on who speaks, when, where

### Presupposition

**Definition:** Assumption that remains true even under negation

**Example:**
- "John stopped smoking" presupposes "John used to smoke"
- "John didn't stop smoking" — *still* presupposes he used to smoke

**Presupposition Triggers:**
- **Definite descriptions**: "The King of France" presupposes existence
- **Factive verbs**: "know," "realize," "regret" presuppose complement is true
  - "Mary knows it's raining" presupposes "It's raining"
- **Change-of-state verbs**: "stop," "begin," "continue"
- **Cleft constructions**: "It was *John* who left" presupposes "Someone left"

**Presupposition Failure:**
- "The present King of France is bald" — France has no king (presupposition fails)
- Is the sentence false or meaningless? (Philosophical debate)

### Politeness Theory (Brown & Levinson)

**Face:** Public self-image people want to maintain
- **Positive face**: Desire to be liked, approved
- **Negative face**: Desire for autonomy, freedom from imposition

**Face-Threatening Acts (FTAs):**
- Requests, orders (threaten negative face)
- Criticism, disagreement (threaten positive face)

**Politeness Strategies:**

| Strategy | Example | Use |
|----------|---------|-----|
| **Bald on-record** | "Close the door" | Urgency, close relationship |
| **Positive politeness** | "Hey buddy, could you close the door?" | Build solidarity |
| **Negative politeness** | "I'm sorry to bother you, but could you possibly close the door if you don't mind?" | Minimize imposition |
| **Off-record (indirect)** | "It's cold in here" (implying request) | Highest politeness, ambiguity |

**Cross-cultural variation:**
- Directness varies: U.S. values directness; Japan/Korea value indirectness
- Power distance affects honorifics (Korean, Japanese have elaborate systems)

### Relevance Theory (Sperber & Wilson)

**Alternative to Grice:** Replace maxims with single principle

**Relevance Principle:** Utterances create expectation of relevance
- Hearer interprets utterance to maximize relevance (cognitive effects vs. processing effort)

**Example:**
- "I'm thirsty" → hearer infers speaker wants a drink (most relevant interpretation)

## Real-World Applications

**Sentiment Analysis:**
- Detecting sarcasm: "Great, another meeting" (positive words, negative sentiment)
- Implicature matters for accurate opinion mining

**Dialogue Systems:**
- Chatbots must handle indirect requests: "Do you know the time?" expects time, not "yes"
- Pragmatic interpretation improves user experience

**Machine Translation:**
- Preserving implicature across languages
- Honorifics in Japanese/Korean → politeness markers in English

**Legal Language:**
- Presuppositions in courtroom: "When did you stop beating your wife?" (presupposes guilt)
- Precise semantics critical for contracts, laws

**Advertising:**
- "Some doctors recommend..." implicates "not all doctors" (weaker claim)
- Exploiting implicature while remaining technically truthful

**Autism Research:**
- Difficulty with pragmatics (sarcasm, indirect requests) while semantics intact
- Distinguishes semantic vs. pragmatic competence

## Key Terms

**Semantics:**
- **Reference**: What a word picks out in the world
- **Sense**: Mode of presentation of a referent
- **Truth Conditions**: Conditions under which a sentence is true
- **Compositionality**: Whole meaning from part meanings
- **Entailment**: A → B must be true if A is true
- **Presupposition**: Background assumption
- **Quantifier**: Specifies quantity (all, some, no)

**Pragmatics:**
- **Speech Act**: Action performed by utterance
- **Implicature**: Implied meaning beyond literal content
- **Deixis**: Context-dependent reference
- **Cooperative Principle**: Conversational expectations
- **Maxims**: Quantity, Quality, Relevance, Manner
- **Face**: Public self-image
- **Politeness**: Strategies to manage face

## Summary

Semantics provides the foundation of linguistic meaning through reference, truth conditions, and compositionality. Words have senses, relate through synonymy and hyponymy, and compose into sentences whose truth we can evaluate. Logical operators, quantifiers, and semantic roles capture systematic aspects of meaning.

Pragmatics extends semantics to context-dependent meaning. Speech acts show language as action. Gricean maxims explain how hearers derive implicatures beyond literal content. Deixis anchors meaning to context. Presuppositions carry background assumptions. Politeness theory explains indirectness and social face management.

Together, semantics and pragmatics explain the full range of linguistic meaning—from "bachelor means unmarried man" to "could you pass the salt?" as a polite request. This dual framework underpins applications from NLP to legal interpretation to cross-cultural communication, revealing language as both a logical system and a social tool.

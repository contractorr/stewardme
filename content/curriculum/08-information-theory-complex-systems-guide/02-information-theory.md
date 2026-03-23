# Information Theory Fundamentals

## Overview

Information theory provides the mathematical framework for quantifying, compressing, and transmitting information. Claude Shannon's 1948 paper established precise limits on what is achievable—and modern systems (WiFi, 5G, JPEG, Spotify) operate remarkably close to those limits. This chapter explores Shannon entropy, mutual information, channel capacity, compression algorithms, and Kolmogorov complexity—the foundational concepts enabling all modern digital communication and storage.

Information theory answers seemingly philosophical questions with mathematical precision: What is information? How much information does a message contain? What is the minimum size to which data can be compressed? What is the maximum rate of reliable communication through a noisy channel? These aren't just theoretical curiosities—they determine the fundamental performance limits of every digital system.

## Shannon Entropy

### Intuition

Entropy measures surprise or uncertainty. If you know the outcome before observing it, there's no information gained—zero entropy. If the outcome is maximally uncertain, observing it is maximally informative—maximum entropy. Shannon entropy quantifies this average surprise across all possible outcomes.

Consider two scenarios:
1. **Predictable**: You flip a coin that always shows heads. Before flipping, you know the outcome. Observing the result tells you nothing. Entropy = 0 bits.
2. **Unpredictable**: You flip a fair coin. Before flipping, you're uncertain. Observing the result (heads or tails) tells you 1 bit of information. Entropy = 1 bit.

The key insight: information is about *reducing uncertainty*. Messages that don't reduce uncertainty carry no information. Messages that resolve high uncertainty carry much information.

**Real-world examples:**
- Learning the outcome of a heavily favored sports game provides little information (you expected it)
- Learning the winner of a 50-50 toss-up game provides much information (genuine uncertainty resolved)
- Weather forecasts are informative when they diverge from climatology (base rates)
- Stock prices move most when unexpected news arrives—expected news is already priced in

### Definition

For a discrete random variable X with possible values {x₁, x₂, ..., xₙ} and probability mass function p(x):

```
H(X) = -Σ p(xᵢ) log₂ p(xᵢ)
```

Measured in **bits** when using log base 2, or **nats** when using natural log (ln), or **hartleys** when using log base 10. The negative sign ensures H(X) ≥ 0 since 0 ≤ p(x) ≤ 1 means log₂ p(x) ≤ 0.

By convention, we define 0 log 0 = 0 (the limit as p → 0 of p log p is 0).

### Properties

| Property | Statement | Implication |
|----------|-----------|-------------|
| Non-negativity | H(X) ≥ 0 | Information is never negative |
| Maximum | H(X) ≤ log₂(n) | Achieved when all outcomes equally likely (uniform distribution) |
| Concavity | H is concave in p | Mixing distributions increases entropy |
| Additivity | H(X,Y) = H(X) + H(Y) for independent X,Y | Independent info adds |
| Continuity | Small changes in p cause small changes in H | Entropy is well-behaved |
| Symmetry | H doesn't depend on labeling | Permuting outcomes doesn't change entropy |
| Conditioning reduces entropy | H(X|Y) ≤ H(X) | Knowing Y cannot increase uncertainty about X |

**Maximum entropy principle**: Among all distributions consistent with given constraints, the maximum entropy distribution makes fewest assumptions. For example, if you only know the mean, the maximum entropy distribution is exponential. If you know mean and variance, it's Gaussian. This principle is foundational in statistical physics, Bayesian inference, and machine learning.

### Worked Examples

**Fair coin**: p(H) = p(T) = 0.5
```
H = -0.5 log₂(0.5) - 0.5 log₂(0.5)
  = -0.5 × (-1) - 0.5 × (-1)
  = 0.5 + 0.5 = 1 bit
```
One coin flip conveys exactly one bit of information.

**Biased coin**: p(H) = 0.9, p(T) = 0.1
```
H = -0.9 log₂(0.9) - 0.1 log₂(0.1)
  = -0.9 × (-0.152) - 0.1 × (-3.322)
  = 0.137 + 0.332 = 0.469 bits
```
Less entropy because outcome is more predictable. Information gained is less than 1 bit per flip. You need about 2.13 flips of this biased coin to get 1 bit of information.

**Fair 8-sided die**: Each outcome has p = 1/8
```
H = -8 × (1/8) log₂(1/8)
  = -8 × (1/8) × (-3)
  = 3 bits
```
Makes sense: 8 equally likely outcomes require 3 bits to represent (2³ = 8).

**Unfair 8-sided die**: p = {1/2, 1/4, 1/8, 1/16, 1/32, 1/64, 1/128, 1/128}
```
H = -(1/2) log₂(1/2) - (1/4) log₂(1/4) - (1/8) log₂(1/8) - ...
  = 1/2 × 1 + 1/4 × 2 + 1/8 × 3 + 1/16 × 4 + 1/32 × 5 + 1/64 × 6 + 2 × 1/128 × 7
  = 0.5 + 0.5 + 0.375 + 0.25 + 0.156 + 0.094 + 0.109
  = 1.984 bits
```
Lower than the fair die (3 bits) because outcomes have unequal probabilities. This distribution is close to optimal Huffman coding—each outcome's code length matches its self-information.

**English text**: Empirical measurements show ~1.0-1.5 bits per character. This is far below log₂(27) ≈ 4.75 bits if all 26 letters plus space were equally likely. The gap reveals massive redundancy in English:
- Letter frequency varies enormously: 'e' appears 12.7%, 'z' only 0.07%
- Sequences aren't random: 'q' almost always followed by 'u'
- Words follow grammar: "the cat" is likely, "cat the" is rare
- Semantic constraints: "the cat sat" is likely, "the cat swam" less so
- Context: "I went to the ___" — likely completions are limited (bank, store, park, etc.)

This redundancy is why you cn stll rd ths sntnc wth mssng vwls. Compression algorithms and error correction exploit this redundancy. ZIP compression of English text typically achieves 2-3x compression, approaching the entropy limit.

### Connection to Coding Theory

Shannon's **source coding theorem** states: The expected code length L for encoding a source cannot be less than its entropy H. More precisely:
```
H(X) ≤ L < H(X) + 1
```

For optimal prefix-free codes (Huffman), the bound is tight. For arithmetic coding with long sequences, we can achieve L → H(X). You cannot compress below entropy without losing information—this is as fundamental as thermodynamic limits on heat engines.

## Information Content of Events

The **self-information** (surprisal) of a single event x:

```
I(x) = -log₂ p(x) = log₂(1/p(x))
```

This quantifies how surprising event x is. Rare events have high self-information; common events have low self-information. The relationship is logarithmic because information is additive for independent events, and probabilities are multiplicative.

| Event | Probability | Self-information | Interpretation |
|-------|------------|-----------------|----------------|
| Fair coin heads | 0.5 | 1 bit | One binary choice |
| Fair die shows 6 | 1/6 ≈ 0.167 | 2.58 bits | Between 2 and 3 binary choices |
| Drawing ace of spades | 1/52 ≈ 0.019 | 5.7 bits | ~6 binary choices |
| Royal flush in poker | 1/649,740 | 19.6 bits | Highly surprising |
| Winning Powerball (1 in 292M) | 3.4×10⁻⁹ | 28.1 bits | Extremely surprising |
| Typing specific 10-char password | 1/(62¹⁰) ≈ 8.4×10⁻¹⁸ | 59.5 bits | Security relies on this |
| DNA mutation at specific site | ~10⁻⁸ | 26.6 bits | Rare enough for genetic stability |
| Spontaneous proton decay | <10⁻³⁴ | >113 bits | Astronomically rare |

Shannon entropy is the *expected value* of self-information:
```
H(X) = E[I(X)] = Σ p(x) × I(x) = Σ p(x) × (-log₂ p(x))
```

This connects the intuitive notion of "surprise" to the mathematical notion of information.

### Connection to Coding

Self-information I(x) = -log₂ p(x) tells you the optimal code length for encoding event x. If event x has probability p(x), you should use approximately -log₂ p(x) bits to encode it. This is the foundation of **Huffman coding** and **arithmetic coding**.

For example, if 'e' appears 12.7% of the time in English, optimal code length is -log₂(0.127) ≈ 2.98 bits. If 'z' appears 0.07% of the time, optimal length is -log₂(0.0007) ≈ 10.5 bits. Assigning shorter codes to frequent symbols and longer codes to rare symbols minimizes average code length.

**Shannon-Fano-Elias coding** achieves expected length within 1 bit of entropy. **Arithmetic coding** achieves expected length arbitrarily close to entropy for long sequences.

## Conditional Entropy and Mutual Information

### Joint Entropy

Information content of two variables together:
```
H(X,Y) = -Σ Σ p(x,y) log₂ p(x,y)
```

For independent variables: H(X,Y) = H(X) + H(Y). Otherwise: H(X,Y) ≤ H(X) + H(Y). The difference (H(X) + H(Y) - H(X,Y)) is the mutual information I(X;Y)—the reduction in combined entropy due to dependence.

### Conditional Entropy

Remaining uncertainty about X given knowledge of Y:
```
H(X|Y) = H(X,Y) - H(Y) = -Σ Σ p(x,y) log₂ p(x|y) = Σ p(y) H(X|Y=y)
```

If Y completely determines X (X is a function of Y), then H(X|Y) = 0—no remaining uncertainty.
If X and Y are independent, then H(X|Y) = H(X)—knowing Y tells you nothing about X.

**Example: Weather and clothing choice**
- H(clothing) might be 2 bits (4 typical outfits: casual, formal, athletic, winter)
- H(clothing | temperature) might be 1 bit (temperature narrows choices to 2 outfits)
- Knowing temperature reduces uncertainty about clothing by 1 bit
- I(clothing; temperature) = H(clothing) - H(clothing | temperature) = 2 - 1 = 1 bit

**Example: Disease diagnosis**
- H(disease) = 1 bit if 50% of population has disease
- After a test with 90% accuracy: H(disease | test result) ≈ 0.47 bits
- Mutual information I(disease; test result) ≈ 0.53 bits
- The test reduces uncertainty about disease status by ~0.53 bits

### Mutual Information

Information shared between X and Y:
```
I(X;Y) = H(X) - H(X|Y) = H(Y) - H(Y|X) = H(X) + H(Y) - H(X,Y)
```

Mutual information measures how much knowing one variable tells you about another. Key properties:

| Property | Statement |
|----------|-----------|
| Symmetry | I(X;Y) = I(Y;X) |
| Non-negativity | I(X;Y) ≥ 0 |
| Bound | I(X;Y) ≤ min(H(X), H(Y)) |
| Independence | I(X;Y) = 0 iff X and Y are independent |
| Determinism | I(X;Y) = H(X) if Y completely determines X |
| Conditioning reduces | I(X;Y|Z) ≤ I(X;Y) in general |

**Venn diagram interpretation**: Picture H(X) and H(Y) as circles. Their overlap is I(X;Y). The parts that don't overlap are H(X|Y) and H(Y|X). The union is H(X,Y).

**Example: Gene expression and disease**
- If I(gene expression; disease) is high, the gene is informative about disease status
- If I(gene expression; disease) is near zero, the gene tells you little about disease
- This is how bioinformatics identifies disease biomarkers
- Genome-wide association studies (GWAS) search for SNPs with high I(SNP; trait)

**Example: Feature selection in machine learning**
- Select features with high I(feature; label) — most informative about class
- But also consider I(feature₁; feature₂) — avoid redundant features
- Maximize I(features; label) - λI(features₁; features₂) for some λ

### Chain Rule

```
H(X₁, X₂, ..., Xₙ) = Σ H(Xᵢ | X₁, ..., Xᵢ₋₁)
```

The entropy of a sequence equals the sum of conditional entropies. Each new variable adds its conditional entropy given all previous variables.

For a Markov chain (where each state depends only on the previous state):
```
H(X₁, X₂, ..., Xₙ) = H(X₁) + Σ H(Xᵢ | Xᵢ₋₁)
```

This simplifies because future states are conditionally independent of the past given the present. Markov chains are the mathematical foundation for many compression algorithms (like Lempel-Ziv) and language models.

### KL Divergence

The **Kullback-Leibler divergence** measures how one probability distribution P differs from another Q:

```
D(P||Q) = Σ p(x) log₂(p(x)/q(x))
```

Properties:
- Always non-negative: D(P||Q) ≥ 0
- Equals zero iff P = Q
- NOT symmetric: D(P||Q) ≠ D(Q||P) in general
- NOT a true distance metric (violates triangle inequality)

**Interpretation**: KL divergence is the extra bits needed to encode data from distribution P using a code optimized for Q. If you design your compression assuming distribution Q, but the true distribution is P, you pay D(P||Q) extra bits per symbol on average.

**Example: Language model**
- Model assigns probability q(word) to each word
- True distribution is p(word)
- KL divergence D(p||q) measures model quality
- Cross-entropy H(p,q) = H(p) + D(p||q) combines entropy and divergence

**Application in machine learning**: Cross-entropy loss minimizes D(p||q) where p is the true label distribution and q is the model's predicted distribution.

## Channel Capacity

### Communication Channel Model

```
Source → [Encoder] → Channel (noisy) → [Decoder] → Destination
```

The channel introduces errors. Shannon asked: What is the maximum rate at which information can be reliably transmitted?

Key insight: You can't eliminate errors by simply boosting signal strength—noise grows proportionally. Instead, you must encode intelligently to detect and correct errors.

**Before Shannon (pre-1948)**: Engineers believed that to communicate reliably through noise, you must reduce noise. Better materials, better amplifiers, more power.

**After Shannon**: With clever error-correcting codes, you can communicate *perfectly* through a noisy channel—as long as you stay below capacity. The problem isn't reducing noise but encoding intelligently.

### Shannon's Noisy Channel Theorem

**Channel capacity** C is the maximum mutual information between input and output:

```
C = max I(X;Y)  (maximized over input distributions p(X))
```

**Shannon's theorem (1948)**:
1. For any rate R < C, there exists a coding scheme achieving arbitrarily low error probability
2. For any rate R > C, reliable communication is impossible

This is remarkable: even through a noisy channel that randomly flips bits, you can communicate *perfectly*—as long as you don't exceed capacity and use appropriate error-correcting codes.

The theorem is **existential** (proves codes exist) but not **constructive** (doesn't show how to build them). Finding capacity-approaching codes took decades (turbo codes in 1993, LDPC codes rediscovered in 1990s, polar codes in 2000s).

### Binary Symmetric Channel (BSC)

Channel flips each bit with probability p (crossover probability):
```
C = 1 - H(p) = 1 + p log₂(p) + (1-p) log₂(1-p)
```

| Crossover probability p | Capacity C | Interpretation |
|------------------------|-----------|----------------|
| 0 (no errors) | 1 bit per transmission | Perfect channel |
| 0.01 (1% errors) | 0.919 bits | Slight degradation—91.9% efficiency |
| 0.1 (10% errors) | 0.531 bits | Significant loss—only 53% efficiency |
| 0.11 (11% errors) | 0.500 bits | Half capacity lost |
| 0.5 (random) | 0 bits | No useful communication—output independent of input |

At p = 0.5, the channel is completely random—output is independent of input. No information gets through. Counterintuitively, p > 0.5 is actually useful: just flip all received bits! This gives effective p' = 1-p < 0.5.

**Example: Hard drive storage**
Modern hard drives have bit error rate ~10⁻¹⁴. BSC capacity at this error rate is 0.999999999999952 bits per bit—essentially perfect. But without error correction, you'd lose data. Error-correcting codes (BCH, Reed-Solomon, LDPC) make hard drives reliable despite physical imperfections.

### Binary Erasure Channel (BEC)

Channel either transmits bit correctly or erases it (returns "?") with probability p:
```
C = 1 - p
```

If 20% of bits are erased, capacity is 0.8 bits per transmission. This model applies to:
- Packet loss in networks (dropped packets are "erasures")
- QR codes (damaged areas are erasures)
- Satellite communication (burst errors treated as erasures)

**Fountain codes** (like Raptor codes) are optimal for erasure channels—you can recover data from any subset of packets equal to the original data size, plus overhead.

### Gaussian Channel

For a channel with additive white Gaussian noise (AWGN), the **Shannon-Hartley theorem**:
```
C = B × log₂(1 + S/N)  bits per second
```

Where:
- B = bandwidth (Hz)
- S = signal power (watts)
- N = noise power (watts)
- S/N = signal-to-noise ratio (often expressed in dB: 10 log₁₀(S/N))

This is the theoretical foundation for ALL modern telecommunications: WiFi, 4G/5G, satellite, fiber optics, deep space communications.

**Consequences**:
- Doubling bandwidth doubles capacity
- Doubling signal power adds only log₂(3) ≈ 1.58 to C/B—diminishing returns
- At high SNR: C ≈ B log₂(S/N). At low SNR: C ≈ (S/N)B (linear in power)
- There's a fundamental tradeoff: bandwidth vs power vs rate vs reliability

**Example: WiFi channel with 20 MHz bandwidth and 30 dB SNR**
SNR in dB: 30 dB = 10^(30/10) = 1000
```
C = 20×10⁶ × log₂(1 + 1000) ≈ 20×10⁶ × 9.97 ≈ 199 Mbps
```

Modern WiFi 6 (802.11ax) achieves ~150-200 Mbps under these conditions—within 75-100% of Shannon capacity! This uses LDPC codes, OFDM modulation, MIMO, and sophisticated signal processing.

**Example: Deep space communication (Voyager 1)**
- Distance: 15 billion miles (24 billion km)
- Transmit power: 23 watts
- Receive antenna: 70-meter dish (large effective area)
- Signal strength at receiver: ~10⁻¹⁶ watts
- Noise: Cosmic background + receiver thermal noise
- SNR: Extremely low (~-180 dB)
- Data rate: 160 bits per second
- Error rate: <10⁻⁴ with concatenated Reed-Solomon + convolutional codes
- Operating within 1-2 dB of Shannon limit!

This is possible because:
1. Large antenna increases effective signal strength
2. Low data rate allows very narrow bandwidth (low noise)
3. Sophisticated error-correcting codes approach Shannon limit
4. Multiple transmissions of same data provide redundancy

### Capacity-Achieving Codes

**Turbo codes (1993)**: First practical codes to approach Shannon capacity within 0.5 dB. Use two parallel convolutional encoders with iterative decoding. Revolutionized coding theory.

**LDPC codes** (Low-Density Parity-Check): Invented by Gallager (1963), forgotten, rediscovered (1990s). Approach capacity within 0.04 dB—almost perfect! Used in 5G, WiFi 6, 10G Ethernet, deep space (Mars rovers).

**Polar codes (2009)**: Theoretically proven to achieve capacity with low encoding/decoding complexity. Used in 5G control channels.

These represent the culmination of Shannon's 1948 vision: reliable communication through noisy channels at rates approaching capacity.

## Data Compression

### Source Coding Theorem

Shannon's source coding theorem states: The average number of bits per symbol needed to encode a source cannot be less than its entropy H. Entropy sets the fundamental compression limit.

For a source with entropy H(X):
- **Lossless compression**: Average code length L ≥ H(X)
- **Optimal coding**: Achieves L → H(X) as block length → ∞

You cannot compress below entropy without losing information. Any lossless compression claiming to compress all files to smaller sizes is impossible—a counting argument proves this (there are more long files than short files, so you can't map all long files to shorter representations).

**Pigeonhole principle**: With n bits, there are 2ⁿ possible strings. A compressor mapping m-bit inputs to n-bit outputs (m > n) cannot be lossless for all inputs—some inputs must map to the same output or to longer outputs.

**Incompressibility of random data**: A truly random n-bit string has entropy n bits and cannot be compressed. Most strings are random (Kolmogorov complexity ≈ length). Therefore, most strings are incompressible. Good compressors exploit structure—which exists only in non-random data.

### Huffman Coding

Optimal prefix-free code assigning shorter codes to more frequent symbols. Developed by David Huffman (1952) as a student term paper—better than his professor's (Robert Fano's) method!

**Algorithm**:
1. List symbols with their probabilities
2. Combine two least probable symbols into a new "super-symbol" with combined probability
3. Repeat until one symbol remains
4. Trace back to assign binary codes (left=0, right=1)

**Example: English character frequencies (simplified)**

| Character | Frequency | Huffman Code | Bits |
|-----------|-----------|-------------|------|
| e | 12.7% | 100 | 3 |
| t | 9.1% | 101 | 3 |
| a | 8.2% | 000 | 3 |
| o | 7.5% | 001 | 3 |
| i | 7.0% | 1100 | 4 |
| n | 6.7% | 1101 | 4 |
| s | 6.3% | 1110 | 4 |
| h | 6.1% | 1111 | 4 |
| r | 6.0% | 01000 | 5 |
| ... | ... | ... | ... |
| z | 0.07% | 0100101011 | 10 |

Expected length: Σ p(x) × length(code(x)) ≈ 4.2 bits/char vs 8 bits for ASCII. Compression ratio ~1.9x. This approaches but doesn't quite reach the entropy limit (~1.5 bits/char for English) because Huffman codes individual characters, not sequences.

**Limitations**:
1. Huffman coding assigns integer bit lengths. If a symbol has probability 0.9, optimal code length is -log₂(0.9) ≈ 0.15 bits, but Huffman must assign at least 1 bit.
2. Huffman codes symbols independently—doesn't exploit sequential dependencies.
3. Requires knowing probability distribution in advance.

**Arithmetic coding** solves (1) and (2) by encoding entire messages as single numbers in [0,1), achieving rates arbitrarily close to entropy. **Adaptive Huffman coding** solves (3) by updating the code as data arrives.

### Lempel-Ziv (LZ) Compression

Used in ZIP, gzip, PNG, GIF. Instead of coding individual symbols, identifies repeated patterns and replaces them with references. This exploits sequential structure without requiring probability models.

**LZ77 (1977)—sliding window**:
- Maintain a window of recent data (e.g., last 32 KB)
- When encountering a sequence, search for it in the window
- If found, encode as (offset back, length); otherwise encode literal
- Example: "the cat sat on the mat" → "the cat sat on ", (11,3), " m", (11,2)
  - (11,3) refers back 11 positions and copies 3 characters: "the" → "sat"
  - (11,2) refers back 11 positions and copies 2: "at"

**LZ78 (1978)—dictionary**:
- Build a dictionary of sequences encountered
- Encode as (dictionary index, next character)
- Dictionary grows adaptively as new patterns appear
- Dictionary is implicit—decoder can reconstruct it from encoded data

**LZW (1984)**: Variant of LZ78 used in GIF, TIFF. Builds dictionary of strings, outputs indices. Patent issues (expired 2004) led to development of alternatives (PNG using DEFLATE).

**DEFLATE (ZIP/gzip)**: Combines LZ77 with Huffman coding. First, LZ77 identifies repeated sequences. Then, Huffman codes the literals and (offset, length) pairs. Achieves better compression than either alone.

**Properties of LZ algorithms**:
- No need to know symbol probabilities in advance—fully adaptive
- Universal: Achieves entropy rate for ergodic sources (as block length → ∞)
- Complexity: O(n) time and space for encoding/decoding n symbols
- Works well on text, DNA, logs, source code (repetitive structure)
- Poor on random data (can't compress incompressible data)
- Poor on already-compressed data (JPEG, MP3)—adds overhead

**Compression results**:
- Text: 2-3x compression typically
- Logs: 10-100x (highly repetitive)
- DNA sequences: 5-10x (4-letter alphabet, repetitive patterns)
- Source code: 3-5x (keywords, variable names reused)
- Already compressed data: 1.0-1.1x (slight expansion due to overhead)

### Lossy Compression

For signals where some loss is acceptable (images, audio, video), we can compress far below entropy by discarding imperceptible information. This exploits properties of human perception.

**Rate-distortion theory** (Shannon, 1959): For a given acceptable distortion D, what is the minimum rate R(D)?

```
R(D) = minimum of I(X;Y) over all p(y|x) satisfying E[d(X,Y)] ≤ D
```

This sets theoretical limits. For Gaussian source with variance σ² and mean squared error distortion:
```
R(D) = ½ log₂(σ²/D)  for D < σ²
```

Halving distortion costs 1 extra bit per sample. Perfect reconstruction (D=0) requires infinite rate.

**JPEG (images)**:
1. Transform to frequency domain (DCT—Discrete Cosine Transform)
2. Human vision is less sensitive to high frequencies (fine details)
3. Quantize high frequencies coarsely, low frequencies finely
4. Quantization is the lossy step—discards imperceptible information
5. Huffman code the quantized coefficients (lossless)
6. Typical: 10-20x compression with minimal visible quality loss

Quality levels:
- JPEG quality 95: ~4 MB (2:1 compression), imperceptible loss
- JPEG quality 75: ~400 KB (20:1 compression), slight artifacts
- JPEG quality 50: ~200 KB (40:1 compression), visible blocking

**WebP, AVIF**: Modern formats using more sophisticated transforms and entropy coding. 20-30% better than JPEG.

**MP3 (audio)**:
1. Psychoacoustic model determines which frequencies are inaudible:
   - Quiet sounds masked by loud sounds at nearby frequencies
   - Frequencies above ~20 kHz inaudible to humans (Nyquist)
   - Temporal masking: loud sounds mask quieter sounds just before/after
2. Discard inaudible frequencies
3. Quantize remaining frequencies based on audibility
4. Huffman code the quantized values
5. Typical: 10x compression (1.4 Mbps CD audio → 128-320 kbps MP3)

Bitrates:
- 320 kbps: Near-transparent quality
- 192 kbps: Transparent for most listeners/music
- 128 kbps: Good quality, some artifacts on critical listening
- 64 kbps: Noticeable quality loss
- 32 kbps: "AM radio" quality

**AAC, Opus**: Modern codecs ~20-30% more efficient than MP3. Opus optimized for speech (very efficient at low bitrates).

**H.264/AVC and H.265/HEVC (video)**:
1. Exploit temporal redundancy: Most frames similar to previous frame
2. Motion prediction: Encode only the differences (residuals)
3. Block-based coding: Divide frame into blocks
4. Intra prediction: Predict from surrounding blocks within same frame
5. Transform coding (DCT, like JPEG) for residuals
6. Entropy coding (CABAC—context-adaptive binary arithmetic coding)
7. Typical: 100-1,000x compression (raw 1080p video → streaming quality)

Bitrates for 1080p video:
- Raw: ~1.5 Gbps (1920×1080 × 24fps × 24bpp)
- H.264 high quality: ~8 Mbps (200:1 compression)
- H.264 streaming: ~3 Mbps (500:1 compression)
- H.265: ~50% better than H.264 at same quality

**AV1, VVC**: Next-generation codecs 30-40% more efficient than H.265 but computationally expensive.

Modern codecs (H.265, AV1, Opus) approach rate-distortion limits within a few bits of theoretical optimum.

## Kolmogorov Complexity

### Definition

The Kolmogorov complexity K(x) of a string x is the length of the shortest program that produces x on a universal Turing machine:

```
K(x) = min{|p| : U(p) = x}
```

Where U is a universal Turing machine and p is a program. This measures the *intrinsic* algorithmic information content of x—how concisely can we describe it?

### Intuition

Kolmogorov complexity measures the *intrinsic* information content of an individual string—its shortest possible description.

**Examples**:

**Repetitive string**: "000000000000000000" (18 zeros) has low complexity:
- Program: "print '0' 18 times" ≈ 20 bytes in most languages
- K(x) ≈ 20 << 18 (if representing in binary)
- Highly compressible

**Digits of π**: "3.1415926535897932" (first 16 digits) has low complexity:
- Program: "compute π to 16 digits" ≈ 50-100 bytes
- K(x) ≈ 50-100 << ~54 bits (16 digits × log₂(10) ≈ 3.32 bits/digit)
- Very compressible—π has infinite digits but finite description

**Random-looking string**: "r9f3k2l8p0s5m7q1" (16 random alphanumeric characters) has high complexity:
- No pattern—shortest program is essentially "print 'r9f3k2l8p0s5m7q1'"
- K(x) ≈ length of string itself (plus small constant for print statement)
- Incompressible

**Shakespeare's Hamlet**: ~130,000 characters
- Not truly random—follows English grammar, Shakespeare's style, narrative structure
- But complex enough that shortest program is probably close to the text itself
- K(Hamlet) ≈ |Hamlet| minus redundancy in English
- Some compression possible, but not dramatic

### Properties

**1. Uncomputability**: K(x) is not computable. There's no algorithm that can calculate K(x) for all inputs.

**Proof sketch** (Berry paradox variant):
Suppose we could compute K. Consider the program: "find the first string x with K(x) > 1000." This program has length ~100 bytes (in some reasonable language), so it defines a string with K(x) ≤ 100. But the program explicitly searches for K(x) > 1000—contradiction.

More formally: If K were computable, we could generate all strings in order of increasing complexity. But the halting problem (undecidable) reduces to this, so K cannot be computable.

**Implication**: This doesn't mean compression is impossible—it means there's no perfect compressor that achieves optimal compression for all inputs. Real compressors (ZIP, gzip) are heuristics that work well on structured data.

**2. Invariance**: K(x) depends on choice of universal Turing machine U, but only by an additive constant. If U₁ and U₂ are two universal machines:
```
|K_U₁(x) - K_U₂(x)| ≤ c_U₁,U₂
```
Where c is a constant independent of x (the length of an interpreter translating between U₁ and U₂). So K(x) is well-defined "up to a constant"—asymptotically, choice of machine doesn't matter.

**3. Upper bound**: You can always just list the string explicitly:
```
K(x) ≤ |x| + O(1)
```
The +O(1) accounts for the "print" command overhead.

**4. Incompressibility**: Most strings are incompressible. Among n-bit strings:
- There are 2ⁿ total strings of length n
- Programs shorter than n bits: 1 + 2 + 4 + ... + 2ⁿ⁻¹ = 2ⁿ - 1
- Therefore, at least one string has K(x) ≥ n

More strongly: fraction of n-bit strings with K(x) ≥ n - k is at least 1 - 2⁻ᵏ. So:
- At least 3/4 of strings have K(x) ≥ n - 2
- At least 7/8 of strings have K(x) ≥ n - 3
- At least 1 - ε of strings have K(x) ≥ n - log₂(1/ε)

**Most strings are random** (incompressible).

**5. Randomness definition**: A string is "random" if K(x) ≈ |x|—it's incompressible. This gives an algorithmic definition of randomness: a string is random if the shortest program producing it is about as long as the string itself.

This differs from statistical randomness (passing statistical tests). A string can pass all statistical tests yet have low Kolmogorov complexity (e.g., pseudorandom number generator output).

### Connection to Shannon Entropy

Shannon entropy characterizes average information for a *distribution*. Kolmogorov complexity characterizes information in an *individual string*.

For random sequences from a distribution with entropy H per symbol:
```
K(x₁, x₂, ..., xₙ) ≈ n × H  (asymptotically, as n → ∞)
```

So for large n, the Kolmogorov complexity per symbol approaches Shannon entropy. This connects the two frameworks:
- Shannon's probabilistic information theory
- Kolmogorov's algorithmic information theory

Both measure "information content" but from different perspectives. They converge asymptotically for typical sequences from a distribution.

**Logical depth** (Charles Bennett): The time required for a universal Turing machine to compute x from its shortest description. Distinguishes between:
- **Shallow**: Random strings (high K, but trivial to generate—just list them)
- **Deep**: Complex evolved objects (high K, and take long time to generate from short programs)

Example: A 1 MB string of random bits has K ≈ 1 MB and can be generated instantly (just output it). A 1 MB human genome has K << 1 MB (compressible) but took billions of years of evolution to generate—it's logically deep.

## Information Theory in Other Domains

### Genetics and Molecular Biology

**DNA as information storage**:
- 4 nucleotides (A, C, G, T) = 2 bits per base pair maximum
- Human genome: ~3.2 billion base pairs = 6.4 billion bits ≈ 800 MB raw
- Actual information content much lower due to:
  - Repetitive sequences: transposons (~45% of genome), tandem repeats
  - Introns: non-coding regions spliced out
  - Synonymous codons: multiple codons encode same amino acid (degeneracy)
  - "Junk DNA": Debated whether it's functional or not

**Compression estimate**: Human genome compresses to ~4-10 MB with standard algorithms (50-200x compression), suggesting effective information content is much less than 800 MB.

**Mutation as noise**:
- DNA replication error rate: ~10⁻⁸ to 10⁻¹⁰ per base per cell division
- This is a noisy channel: transmitting genetic information across generations
- Error correction mechanisms: proofreading (DNA polymerase), mismatch repair
- Without error correction, mutation rate would be ~10⁻⁶ (too high for complex life)

**Channel capacity of heredity**: Given mutation rate μ and genome size L, maximum sustainable information is ~L × H(μ) where H is binary entropy. At μ = 10⁻⁸, this is very close to 1 bit per base—nearly perfect fidelity.

**Protein folding**:
- Amino acid sequence (1D) determines 3D structure
- 20 amino acids × 300 residues (typical protein) = 20³⁰⁰ ≈ 10³⁹⁰ possible sequences
- Yet proteins fold reproducibly to specific structures
- Levinthal's paradox: exhaustive search would take longer than age of universe
- Resolution: Folding pathway is directed by energy landscape—doesn't search randomly

**Mutual information in structure prediction**:
- I(residue i; residue j) reveals which residues are in contact in 3D structure
- High mutual information → likely spatial contact (correlated evolution)
- Used in modern protein structure prediction (AlphaFold uses attention mechanisms related to mutual information)

### Thermodynamics and Statistical Mechanics

**Landauer's principle** (Rolf Landauer, 1961): Erasing one bit of information requires minimum energy:
```
E_min = kT ln 2 ≈ 2.9 × 10⁻²¹ J at room temperature (T = 300K)
```

Where k ≈ 1.38×10⁻²³ J/K is Boltzmann's constant. Information is physical—computation has thermodynamic costs.

**Implications**:
- Reversible computation could avoid this cost (theoretical; practically challenging)
- Explains why computers dissipate heat (logic operations erase bits)
- Sets lower bound on energy efficiency of computation
- At biological temperatures: ~0.018 eV per bit (18 meV)
- Neurons spend ~10⁹ ATP molecules per spike (~10⁹ × 0.5 eV ≈ 500 MeV), far above Landauer limit
- Modern transistors use ~10⁵ kT per operation—still far above limit, but improving

**Maxwell's demon paradox** (James Clerk Maxwell, 1867):
- Hypothetical being observes molecules, sorts fast/slow to create temperature difference
- Appears to decrease entropy without work, violating second law
- Resolution (Landauer, Bennett, Szilard): Demon must record observations
- Memory has finite capacity → eventually must erase
- Erasure costs kT ln 2 per bit, paying entropy debt
- Total entropy increases: second law preserved

**Information and entropy connection**:
- Boltzmann entropy: S = k log W (W = number of microstates)
- Shannon entropy: H = -Σ p log p
- Same mathematical form—deep connection between information and thermodynamics

**Szilard engine**: Thought experiment making Maxwell's demon precise:
1. Single molecule in box
2. Measure which half it's in (1 bit of information)
3. Insert partition, expand gas isothermally
4. Extract work kT ln 2
5. Remove partition
6. Erase measurement (costs kT ln 2)
Net: No entropy decrease. Second law saved.

### Economics and Finance

**Market efficiency**: The efficient market hypothesis (EMH) states that prices incorporate all available information. This is an information-theoretic claim:
- Strong form: I(any info; future price changes) = 0
- Semi-strong: I(public info; future price changes) = 0
- Weak form: I(past prices; future price changes) = 0

Evidence mixed: Markets are largely efficient (hard to beat consistently) but exhibit anomalies (momentum, value effects, January effect).

**Entropy in portfolio theory**:
- Portfolio diversity can be measured by entropy of asset allocation
- H = -Σ wᵢ log wᵢ where wᵢ is fraction in asset i
- Higher entropy = more diversified = lower concentration risk
- Maximize entropy subject to return/risk constraints

**Kelly criterion**: Optimal bet sizing to maximize long-run wealth growth uses information theory:
```
f* = (p(b+1) - 1)/b
```
where p is win probability, b is odds. Equivalently:
```
f* = (expected log growth rate)
```
Derived from maximizing E[log(wealth)] — directly related to entropy.

**Information asymmetry**: When different parties have different information (used cars, insurance), markets fail. Resolving information asymmetry is a communication problem:
- Signaling: Informed party credibly reveals information (warranties, education credentials)
- Screening: Uninformed party induces revelation (insurance deductibles sort risk types)

### Neuroscience

**Neural coding**: How do neurons represent information?
- **Rate code**: Information in average firing frequency over time window
- **Temporal code**: Information in precise spike timing
- **Population code**: Information distributed across many neurons
- Debate continues; likely all three are used depending on context

**Spike train entropy**: Given spike train (sequence of spike times), what's the entropy rate?
- H ≈ 2-4 bits per spike for visual cortex neurons
- Total information rate ~50-100 bits/sec per neuron

**Capacity**:
- Retina transmits ~10 Mbps to brain (1M ganglion cells × 10 bits/sec each)
- Auditory nerve: ~100 kbps
- Entire brain: Estimates range from 1-100 Tbps (highly uncertain)

**Efficient coding hypothesis**: Sensory systems maximize mutual information between stimuli and neural responses subject to metabolic constraints. This predicts:
- Center-surround receptive fields (decorrelate spatially redundant input)
- Temporal whitening (decorrelate temporally redundant input)
- Sparse coding (efficient for naturalistic stimuli with heavy-tailed distributions)

Evidence: V1 simple cells resemble independent components of natural images—near-optimal for efficient coding.

### Cryptography

**Perfect secrecy** (Claude Shannon, 1949): A cipher is perfectly secure iff:
1. Key length ≥ message length
2. Key is truly random (maximum entropy)
3. Key is used only once (one-time pad)

Under these conditions: I(plaintext; ciphertext) = 0. Ciphertext reveals zero information about plaintext. This is information-theoretically secure—unbreakable even with infinite computation.

**Problem**: Key distribution. If you can securely share a key as long as the message, why not just securely share the message? Quantum key distribution (QKD) potentially solves this.

**Modern cryptography**: RSA, AES, elliptic curve crypto are not information-theoretically secure—they're computationally secure. Given infinite time, they're breakable. But breaking them requires computational effort believed to be infeasible (would take millions of years with current computers).

**Entropy in passwords**:
- 8-character lowercase: 26⁸ ≈ 2×10¹¹ possibilities ≈ 37.6 bits entropy
- 8-character alphanumeric + symbols: 95⁸ ≈ 6×10¹⁵ possibilities ≈ 52.6 bits
- Four random common words (XKCD method): 2048⁴ ≈ 44 bits, much more memorable
- But: If passwords are chosen by humans (not randomly), entropy is much lower
  - "password123" has ~37.6 bits if chosen randomly from 8-char lowercase
  - But <10 bits effective entropy because it's a common choice

## Real-World Applications

| Application | Information Theory Concept | Impact |
|-------------|--------------------------|--------|
| **5G/WiFi** | Shannon-Hartley capacity, LDPC codes | MIMO, OFDM approach Shannon limits; ~95% efficiency |
| **ZIP/gzip** | Lempel-Ziv compression | Universal compression without probability models; 2-10x |
| **JPEG/MP3** | Rate-distortion theory, psychoacoustics | 10-20x compression with imperceptible loss |
| **QR codes** | Reed-Solomon error correction | Damaged codes still readable (up to 30% damage) |
| **Voyager probe** | Turbo codes, low-rate transmission, concatenated codes | Communication from 15 billion miles with <10⁻⁴ error rate |
| **DNA sequencing** | Source coding, error correction, mutual information | Genome compression, handling sequencing errors, variant calling |
| **Hard drives** | LDPC codes, constrained codes | Reliable storage despite physical imperfections (10⁻¹⁴ BER) |
| **Blockchain** | Cryptographic hash functions (SHA-256) | Collision resistance ~2²⁵⁶, irreversibility |
| **Machine learning** | Cross-entropy loss, KL divergence, mutual information | Training objective for classification, generative models |
| **MRI/CT scans** | Compressed sensing, sparse coding | Fewer measurements → faster scans, lower radiation |
| **Streaming video** | H.264/H.265 (AVC/HEVC) | 100-1000x compression enabling YouTube, Netflix |
| **Optical fiber** | Shannon capacity of fiber channels | 100+ Tbps per fiber using wavelength division multiplexing |

### Modern Error-Correcting Codes

**Turbo codes (1993)**:
- First codes to approach Shannon capacity within 0.5 dB
- Use two parallel encoders with interleaver
- Iterative decoding exchanges "soft decisions" between decoders
- Revolutionized coding theory—sparked renewed interest
- Used in 3G/4G cellular, deep space (Mars missions)

**LDPC codes** (Low-Density Parity-Check):
- Invented by Robert Gallager (1963 PhD thesis), forgotten for 30 years
- Rediscovered independently (MacKay, Neal, 1990s)
- Approach capacity within 0.04 dB—almost perfect!
- Sparse parity-check matrix enables efficient decoding
- Graph-based: Bipartite graph of variable and check nodes
- Belief propagation algorithm for decoding
- Used in 5G, WiFi 6, 10G Ethernet, DVB-S2 satellite, deep space (Mars rovers)

**Polar codes (Erdal Arıkan, 2009)**:
- First codes proven to achieve capacity with polynomial complexity
- Encoding/decoding: O(N log N) where N is block length
- Based on channel polarization: N uses of channel → some perfect, some useless
- Use only the perfect subchannels
- Used in 5G control channels (3GPP standard)

**Comparison**:

| Code Type | Gap to Capacity | Complexity | Used In |
|-----------|----------------|------------|---------|
| Reed-Solomon | ~2-3 dB | Low | QR codes, CDs, DVDs |
| Convolutional | ~2 dB | Low | Old WiFi, GSM |
| Turbo | ~0.5 dB | Medium | 3G/4G, DVB |
| LDPC | ~0.04 dB | Medium | 5G, WiFi 6, 10GbE |
| Polar | ~achieves capacity | Low | 5G control |

These represent the culmination of Shannon's 1948 vision: reliable communication through noisy channels at rates approaching capacity. We're now within 99% of theoretical limits!

## Key Terms

- **Shannon Entropy**: H(X) = -Σ p(x) log₂ p(x) — average information per symbol; measured in bits; maximum when uniform distribution

- **Self-Information**: I(x) = -log₂ p(x) — information gained from observing event x; rare events have high self-information; measured in bits

- **Mutual Information**: I(X;Y) = H(X) - H(X|Y) = H(Y) - H(Y|X) — information shared between variables; symmetric measure of dependence; zero iff independent

- **Conditional Entropy**: H(X|Y) — remaining uncertainty about X given Y; equals H(X,Y) - H(Y); never exceeds H(X)

- **Channel Capacity**: Maximum rate of reliable communication; C = max I(X;Y) over input distributions; measured in bits per transmission

- **Shannon-Hartley Theorem**: C = B log₂(1 + S/N) for Gaussian channel — capacity increases logarithmically with SNR, linearly with bandwidth

- **Huffman Coding**: Optimal prefix-free code assigning shorter codes to frequent symbols; achieves average length approaching entropy; used in JPEG, MP3, ZIP

- **Lempel-Ziv**: Universal compression algorithm identifying repeated patterns; used in ZIP, gzip, PNG; adapts without prior probability knowledge

- **Kolmogorov Complexity**: K(x) = length of shortest program producing x; algorithmic information content; uncomputable but theoretically fundamental

- **Landauer's Principle**: Erasing 1 bit costs minimum kT ln 2 energy; information is physical, not abstract; explains why computation dissipates heat

- **Rate-Distortion**: R(D) = minimum rate for distortion D; theoretical foundation for lossy compression; tradeoff between compression and quality

- **KL Divergence**: D(P||Q) = Σ p(x) log(p(x)/q(x)) — "distance" between distributions; used in machine learning as loss function; non-symmetric

- **Cross-Entropy**: H(P,Q) = -Σ p(x) log q(x) — expected code length using distribution Q when true distribution is P; equals H(P) + D(P||Q)

- **Ergodic**: Source where time averages equal ensemble averages; Lempel-Ziv achieves entropy rate for ergodic sources; stationary + mixing

- **Source Coding Theorem**: Average code length L ≥ H(X); cannot compress below entropy losslessly; fundamental limit like Carnot efficiency

- **Channel Coding Theorem**: Reliable communication possible at rates R < C, impossible at R > C; existential (codes exist) but not constructive

- **LDPC Codes**: Low-density parity-check codes; approach capacity within 0.04 dB; used in 5G, WiFi 6; sparse matrices enable efficient decoding

## Summary

Information theory provides the mathematical foundation for quantifying and transmitting information. Shannon entropy H(X) = -Σ p(x) log p(x) measures average uncertainty or information content—a fundamental quantity like energy or mass. Self-information I(x) = -log₂ p(x) measures surprise of individual events. Mutual information I(X;Y) measures shared information between variables and is central to understanding dependencies, correlations, and communication.

Shannon's channel coding theorem establishes that reliable communication is possible through noisy channels at rates below capacity C = max I(X;Y)—a result that enables all modern telecommunications. Before Shannon, engineers thought noise was an insurmountable barrier requiring better physical components. Shannon proved that with clever encoding, you can communicate perfectly through imperfect channels. The shift from "reduce noise" to "encode intelligently" was revolutionary.

Modern systems (5G, WiFi 6, deep space communications) operate within fractions of a decibel from Shannon's 1948 theoretical limits using turbo codes, LDPC codes, and polar codes. This represents one of the great engineering achievements—taking theoretical limits from paper to practice.

The source coding theorem establishes that lossless compression cannot compress below entropy—a fundamental limit like thermodynamic efficiency limits. Compression algorithms approach this limit: Huffman coding for sources with known statistics (achieves H ≤ L < H+1), Lempel-Ziv for adaptive compression without prior knowledge (achieves entropy rate asymptotically). Lossy compression (JPEG, MP3, H.264) uses rate-distortion theory to discard imperceptible information, achieving far higher compression ratios (10-1000x) by exploiting human perception.

Kolmogorov complexity extends information theory to individual strings, measuring intrinsic complexity as the shortest program length. While uncomputable, it provides a theoretical foundation for randomness (random strings have K(x) ≈ |x|) and connects algorithmic and probabilistic information theory (K approaches H×n for typical sequences of length n).

Applications span telecommunications (5G approaching Shannon capacity with LDPC codes), data compression (ZIP using Lempel-Ziv, JPEG approaching rate-distortion limits), error correction (QR codes using Reed-Solomon, hard drives using LDPC), genetics (DNA as 2 bits/base noisy channel, mutual information revealing protein contacts), thermodynamics (Landauer's principle linking information and energy at kT ln 2 per bit), economics (market efficiency as information aggregation, Kelly criterion for optimal betting), neuroscience (efficient coding hypothesis explaining receptive fields), and cryptography (Shannon's perfect secrecy theorem establishing one-time pad, entropy in password strength).

The profound insight: information is a precisely quantifiable physical quantity with fundamental limits. These limits—entropy bounds on compression, capacity bounds on communication, energy bounds on computation (Landauer)—are not engineering challenges to be overcome but mathematical laws as fundamental as thermodynamics. No amount of engineering cleverness can compress data below its entropy, transmit faster than channel capacity, or erase bits using less than kT ln 2 energy.

Understanding information theory means understanding what's possible and what's impossible in communication, computation, and inference. It's the mathematics of uncertainty, communication, and knowledge—as foundational to the information age as calculus is to physics.


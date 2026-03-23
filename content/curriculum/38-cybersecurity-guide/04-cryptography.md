# Cryptography

## Overview

Cryptography is the science of securing information through mathematical techniques that transform readable data (plaintext) into unreadable data (ciphertext) and back again. It provides confidentiality, integrity, authentication, and non-repudiation—the cornerstones of information security. From ancient Caesar ciphers to modern quantum-resistant algorithms, cryptography has evolved to protect everything from personal messages to international financial transactions.

## Fundamental Concepts

### Basic Terminology

| Term | Definition |
|------|------------|
| **Plaintext** | Original, readable message or data |
| **Ciphertext** | Encrypted, unreadable message or data |
| **Encryption** | Converting plaintext to ciphertext |
| **Decryption** | Converting ciphertext back to plaintext |
| **Cipher** | Algorithm used for encryption/decryption |
| **Key** | Secret value used with cipher to encrypt/decrypt |
| **Cryptanalysis** | Science of breaking encryption |
| **Cryptology** | Study of cryptography and cryptanalysis |

### Security Principles

**Kerckhoffs's Principle:**
- "A cryptosystem should be secure even if everything about the system, except the key, is public knowledge"
- Security relies on key secrecy, not algorithm secrecy
- Modern algorithms (AES, RSA) are public and peer-reviewed

**Perfect Secrecy (Shannon):**
- Ciphertext reveals nothing about plaintext
- Only achievable with One-Time Pad (OTP)
- Impractical for most applications

**Computational Security:**
- Breaking encryption is theoretically possible but computationally infeasible
- Modern cryptography aims for computational security
- Security depends on key length and algorithm strength

## Symmetric Encryption

### Definition

Symmetric encryption uses the same key for both encryption and decryption. Both sender and receiver must possess the shared secret key.

**Characteristics:**
- Fast and efficient
- Suitable for large data volumes
- Key distribution challenge
- Key management scales poorly (n² key problem)

### Block Ciphers

Block ciphers encrypt fixed-size blocks of data (typically 64 or 128 bits).

#### DES (Data Encryption Standard)

**History:**
- Developed by IBM, adopted as standard in 1977
- 56-bit key, 64-bit block size
- Broken by brute force in 1990s

**Status**: **Obsolete and insecure**

#### 3DES (Triple DES)

**Design**: Apply DES three times with different keys

**Configuration:**
- 3 independent keys: 168-bit effective security
- 2 keys (K1=K3): 112-bit security

**Status**: Deprecated, replaced by AES

#### AES (Advanced Encryption Standard)

**History:**
- Selected in 2001 as DES replacement
- Originally called Rijndael
- Current global standard

**Specifications:**
- Block size: 128 bits
- Key sizes: 128, 192, or 256 bits
- Rounds: 10 (128-bit), 12 (192-bit), 14 (256-bit)

**Strength:**
- No practical attacks on full AES
- AES-128 considered secure until ~2030
- AES-256 considered quantum-resistant

**Use Cases:**
- File encryption (BitLocker, FileVault)
- VPN tunnels
- TLS/SSL connections
- Database encryption

| Key Size | Security Level | Quantum Resistance | Recommended For |
|----------|----------------|-------------------|-----------------|
| **AES-128** | High | No | General use, current standard |
| **AES-192** | Very High | Partial | Government, sensitive data |
| **AES-256** | Extremely High | Better | Top secret, long-term security |

#### Blowfish and Twofish

**Blowfish:**
- Variable key length (32-448 bits)
- 64-bit block size (vulnerable to birthday attacks)
- Fast on older processors
- **Status**: Avoid for new implementations

**Twofish:**
- AES finalist
- 128-bit block, up to 256-bit keys
- Public domain
- **Status**: Secure alternative to AES

### Block Cipher Modes of Operation

Modes define how to apply block ciphers to data larger than one block.

| Mode | Name | Parallelizable | IV Required | Characteristics |
|------|------|----------------|-------------|-----------------|
| **ECB** | Electronic Codebook | Yes | No | **Insecure**: identical plaintext blocks → identical ciphertext |
| **CBC** | Cipher Block Chaining | Decrypt only | Yes | Sequential encryption, common, padding required |
| **CTR** | Counter | Yes | Yes | Converts block cipher to stream cipher, no padding |
| **GCM** | Galois/Counter Mode | Yes | Yes | **Authenticated encryption**, most recommended |
| **CCM** | Counter with CBC-MAC | No | Yes | Authenticated encryption, used in 802.11i |
| **CFB** | Cipher Feedback | Decrypt only | Yes | Stream cipher mode |
| **OFB** | Output Feedback | No | Yes | Stream cipher mode, error propagation limited |

**Best Practice**: Use **AES-GCM** for authenticated encryption (provides both confidentiality and integrity).

#### ECB Mode - Why It's Insecure

**Problem**: Identical plaintext blocks produce identical ciphertext blocks, revealing patterns.

**Visual Example**: Encrypting an image with ECB preserves visible patterns, while other modes produce random-looking output.

**Never use ECB mode in production.**

### Stream Ciphers

Stream ciphers encrypt data bit-by-bit or byte-by-byte, generating a keystream.

#### ChaCha20

**Design**: Modern stream cipher by Daniel Bernstein

**Advantages:**
- Faster than AES on devices without hardware acceleration
- Simpler to implement securely
- No timing attack vulnerabilities

**Usage:**
- TLS 1.3 (ChaCha20-Poly1305)
- VPN protocols (WireGuard)
- Mobile devices

#### RC4

**History**: Once widely used (WEP, TLS, PDF encryption)

**Status**: **Broken and deprecated**
- Multiple cryptographic weaknesses discovered
- Biases in keystream
- **Do not use**

### Symmetric Key Management

**Challenges:**
- Secure key generation (cryptographically secure random numbers)
- Secure key distribution
- Secure key storage
- Key rotation and lifecycle management
- Scale: n users need n(n-1)/2 keys for pairwise communication

**Solutions:**
- Key Derivation Functions (KDF)
- Key Encryption Keys (KEK)
- Hardware Security Modules (HSM)
- Key Management Systems (KMS)

## Asymmetric Encryption (Public Key Cryptography)

### Definition

Asymmetric encryption uses a key pair:
- **Public key**: Freely distributed, used for encryption
- **Private key**: Kept secret, used for decryption

**Key Properties:**
- Encryption with public key → decryption with private key
- Encryption with private key (signing) → verification with public key
- Computationally infeasible to derive private key from public key
- Slower than symmetric encryption

### RSA (Rivest-Shamir-Adleman)

**History**: Published in 1977, most widely used asymmetric algorithm

**Mathematical Basis**: Difficulty of factoring large prime numbers

**Key Sizes and Security:**

| Key Size | Security Level | Status | Notes |
|----------|---------------|--------|-------|
| **1024-bit** | Weak | **Deprecated** | Factorable with significant resources |
| **2048-bit** | Adequate | Current minimum | Standard for current use |
| **3072-bit** | High | Recommended | Equivalent to AES-128 |
| **4096-bit** | Very High | Long-term | Slower, diminishing returns |

**Use Cases:**
- TLS/SSL certificates
- SSH authentication
- Email encryption (PGP/GPG)
- Digital signatures
- Key exchange

**Limitations:**
- Slow for large data (typically used to encrypt symmetric keys)
- Vulnerable to quantum computing (Shor's algorithm)
- Padding schemes critical (use OAEP, not PKCS#1 v1.5)

**RSA Workflow:**
```
1. Generate key pair (public key, private key)
2. Distribute public key
3. Sender encrypts data with recipient's public key
4. Recipient decrypts with their private key
```

### ECC (Elliptic Curve Cryptography)

**Mathematical Basis**: Discrete logarithm problem on elliptic curves

**Advantages:**
- Smaller keys for equivalent security
- Faster operations
- Lower power consumption
- Better for mobile and IoT

**Security Comparison:**

| RSA Key Size | ECC Key Size | Symmetric Equivalent |
|--------------|--------------|---------------------|
| 1024-bit | 160-bit | 80-bit |
| 2048-bit | 224-bit | 112-bit |
| 3072-bit | 256-bit | 128-bit |
| 7680-bit | 384-bit | 192-bit |
| 15360-bit | 521-bit | 256-bit |

**Common Curves:**
- **NIST P-256, P-384, P-521**: NIST-standardized curves
- **Curve25519**: Modern curve by Bernstein, recommended
- **secp256k1**: Used in Bitcoin

**Concerns:**
- Some NIST curves potentially backdoored (NSA involvement)
- Prefer Curve25519 or Ed25519 for new implementations

**Use Cases:**
- TLS 1.3 (ECDHE key exchange)
- Modern VPNs
- Cryptocurrencies
- IoT device authentication
- Mobile applications

### Diffie-Hellman Key Exchange

**Purpose**: Establish shared secret over insecure channel

**Process:**
1. Alice and Bob agree on public parameters (p, g)
2. Alice generates private key (a), computes public value (A = g^a mod p)
3. Bob generates private key (b), computes public value (B = g^b mod p)
4. Exchange public values
5. Alice computes shared secret: s = B^a mod p
6. Bob computes shared secret: s = A^b mod p
7. Both arrive at same shared secret without transmitting it

**Variants:**
- **DHE**: Ephemeral Diffie-Hellman (temporary keys)
- **ECDHE**: Elliptic Curve Diffie-Hellman Ephemeral (most common in TLS 1.3)

**Security:**
- Vulnerable to Man-in-the-Middle (MitM) without authentication
- Requires authentication via digital signatures or certificates
- Provides Perfect Forward Secrecy (PFS) when ephemeral keys used

### Hybrid Cryptography

**Approach**: Combine asymmetric and symmetric encryption

**Process:**
1. Generate random symmetric key (session key)
2. Encrypt data with symmetric key (fast)
3. Encrypt symmetric key with recipient's public key (small amount of data)
4. Send encrypted data + encrypted key
5. Recipient decrypts symmetric key with private key
6. Recipient decrypts data with symmetric key

**Used in**: PGP, S/MIME, TLS/SSL

**Benefits:**
- Speed of symmetric encryption
- Key distribution of asymmetric encryption
- Best of both worlds

## Cryptographic Hash Functions

### Definition

Hash functions transform input data of any size into fixed-size output (hash/digest). Cryptographic hash functions have additional security properties.

**Properties:**

| Property | Description | Security Implication |
|----------|-------------|---------------------|
| **Deterministic** | Same input always produces same output | Consistent verification |
| **Fixed Size** | Output length constant regardless of input size | Predictable storage |
| **One-Way** | Infeasible to reverse (pre-image resistance) | Cannot recover original data |
| **Collision Resistant** | Infeasible to find two inputs with same hash | Integrity assurance |
| **Avalanche Effect** | Small input change drastically changes output | Tamper detection |

### Common Hash Functions

#### MD5 (Message Digest 5)

**Specifications:**
- Output: 128 bits (32 hex characters)
- Designed in 1991

**Status**: **Cryptographically broken**
- Collision attacks practical since 2004
- Pre-image attacks demonstrated
- **Do not use for security purposes**

**Acceptable uses**:
- Non-security checksums (file integrity verification when not adversarial)
- Database keys (not for passwords)

#### SHA-1 (Secure Hash Algorithm 1)

**Specifications:**
- Output: 160 bits (40 hex characters)
- Designed by NSA, published 1995

**Status**: **Deprecated**
- Theoretical collision attacks since 2005
- Practical collision demonstrated by Google (2017)
- Browsers reject SHA-1 certificates
- **Do not use for new applications**

#### SHA-2 Family

**Variants:**

| Algorithm | Output Size | Security | Status |
|-----------|-------------|----------|--------|
| **SHA-224** | 224 bits | Good | Less common |
| **SHA-256** | 256 bits | Strong | **Recommended standard** |
| **SHA-384** | 384 bits | Very Strong | High security needs |
| **SHA-512** | 512 bits | Very Strong | High security needs |

**Characteristics:**
- No known practical attacks
- Current industry standard
- SHA-256 most commonly used
- Performance varies by platform (SHA-512 faster on 64-bit systems)

**Use Cases:**
- Digital signatures
- Certificate signing
- Password hashing (with salting)
- Blockchain (Bitcoin uses SHA-256)
- File integrity verification

#### SHA-3 (Keccak)

**History:**
- Winner of NIST competition in 2012
- Different construction than SHA-2 (sponge construction)
- Published as standard in 2015

**Variants**: SHA3-224, SHA3-256, SHA3-384, SHA3-512

**Status**: Modern, secure alternative to SHA-2
- Not intended to replace SHA-2
- Provides diversity (different vulnerabilities)
- Used where SHA-2 concerns exist

#### BLAKE2

**Characteristics:**
- Faster than MD5, SHA-1, SHA-2
- As secure as SHA-3
- Simpler than SHA-3
- Not NIST-standardized (widely used anyway)

**Variants:**
- **BLAKE2b**: Optimized for 64-bit platforms (up to 512-bit output)
- **BLAKE2s**: Optimized for 32-bit platforms (up to 256-bit output)

**Use Cases:**
- Argon2 password hashing
- File integrity (restic, borg backup tools)
- Cryptocurrencies (Zcash, Nano)

### Password Hashing

**Problem**: Standard hash functions too fast (billions of hashes/second)
- Enables brute-force attacks
- Rainbow table attacks

**Solution**: Use specialized password hashing functions

#### Key Derivation Functions (KDFs)

**Purpose**: Derive cryptographic keys from passwords

**Requirements:**
- Deliberately slow (configurable)
- Memory-hard (resist GPU/ASIC attacks)
- Salting (unique per password)

#### bcrypt

**Design**: Based on Blowfish cipher

**Features:**
- Configurable work factor (2^n iterations)
- Automatic salting
- Maximum password length: 72 bytes

**Format:**
```
$2b$12$R9h/cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jWMUW
 │  │  │                       │
 │  │  │                       └─ Salt + Hash
 │  │  └─ Cost factor (2^12 = 4096 rounds)
 │  └─ Algorithm version
 └─ Prefix
```

**Status**: Good, widely supported, proven track record

#### scrypt

**Design**: Memory-hard function (requires large memory)

**Features:**
- Configurable CPU and memory costs
- Resists GPU/ASIC attacks better than bcrypt
- More resource-intensive

**Parameters:**
- N: CPU/memory cost factor
- r: Block size
- p: Parallelization factor

**Usage**: Litecoin, password hashing in high-security contexts

#### Argon2

**History**: Winner of Password Hashing Competition (2015)

**Variants:**
- **Argon2i**: Optimized for password hashing (resistant to side-channel attacks)
- **Argon2d**: Optimized for cryptocurrencies (faster, but vulnerable to side-channels)
- **Argon2id**: Hybrid (recommended for most uses)

**Parameters:**
- Memory cost
- Time cost (iterations)
- Parallelism degree

**Status**: **Most recommended** for new applications

**Comparison:**

| Algorithm | Speed Control | Memory-Hard | Side-Channel Resistant | Recommendation |
|-----------|---------------|-------------|----------------------|----------------|
| **MD5** | No | No | N/A | **Never use** |
| **SHA-256** | No | No | N/A | **Not for passwords** |
| **bcrypt** | Yes | Minimal | Yes | Good |
| **scrypt** | Yes | Yes | Partial | Good |
| **Argon2id** | Yes | Yes | Yes | **Best** |
| **PBKDF2** | Yes | No | Yes | Acceptable |

**Best Practice:**
```python
# Python example with Argon2
from argon2 import PasswordHasher

ph = PasswordHasher(
    time_cost=2,        # Number of iterations
    memory_cost=102400, # Memory usage in KB
    parallelism=8,      # Number of threads
    hash_len=32,        # Output length
    salt_len=16         # Salt length
)

hash = ph.hash("user_password")
# Verify
ph.verify(hash, "user_password")
```

## Digital Signatures

### Purpose

Digital signatures provide:
- **Authentication**: Verify sender's identity
- **Integrity**: Detect message tampering
- **Non-repudiation**: Sender cannot deny signing

### How Digital Signatures Work

**Signing Process:**
1. Hash the message (SHA-256)
2. Encrypt hash with sender's private key
3. Attach encrypted hash (signature) to message

**Verification Process:**
1. Decrypt signature with sender's public key (recovers hash)
2. Hash the received message
3. Compare decrypted hash with computed hash
4. If match: signature valid, message authentic and unmodified

**Algorithms:**
- **RSA**: Most common, based on factoring
- **DSA**: Digital Signature Algorithm (US standard)
- **ECDSA**: Elliptic Curve DSA (smaller keys)
- **EdDSA**: Modern, based on Curve25519 (recommended)

**Use Cases:**
- Software distribution (code signing)
- Email (S/MIME, PGP)
- Legal documents (PDF signatures)
- Blockchain transactions
- Certificate authorities

## Public Key Infrastructure (PKI)

### Definition

PKI is a framework for managing digital certificates and public-key encryption, establishing trust in digital communications.

### Components

#### 1. Certificate Authority (CA)

**Role**: Trusted third party that issues and signs digital certificates

**Responsibilities:**
- Verify identity before issuing certificates
- Sign certificates with CA's private key
- Maintain certificate revocation lists (CRL)
- Publish certificates and CRLs

**Examples**: DigiCert, Let's Encrypt, GlobalSign, Comodo

#### 2. Registration Authority (RA)

**Role**: Verifies certificate requests before CA issues certificates

**Responsibilities:**
- Authenticate certificate applicants
- Verify information accuracy
- Approve/reject certificate requests
- May be part of CA or separate entity

#### 3. Digital Certificates

**Definition**: Electronic documents binding public key to identity

**X.509 Certificate Contents:**
- Subject (owner) information
- Public key
- Issuer (CA) information
- Validity period (not before/not after dates)
- Serial number
- Signature algorithm
- CA's digital signature
- Extensions (key usage, SANs, etc.)

**Certificate Format (PEM):**
```
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAKL0UG+mRxiLMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
...
-----END CERTIFICATE-----
```

#### 4. Certificate Revocation

**Reasons for Revocation:**
- Private key compromised
- Certificate information incorrect
- CA compromise
- End of relationship

**Revocation Methods:**

| Method | How It Works | Pros | Cons |
|--------|--------------|------|------|
| **CRL** | Certificate Revocation List | Simple, supported | Large lists, infrequent updates |
| **OCSP** | Online Certificate Status Protocol | Real-time, smaller | Privacy concerns, additional request |
| **OCSP Stapling** | Server provides OCSP response | Fast, private | Requires server config |
| **CRLSets** | Browser-maintained short lists | Fast | Only critical revocations |

### Certificate Types

**By Validation Level:**

| Type | Validation | Cost | Use Case |
|------|------------|------|----------|
| **Domain Validated (DV)** | Domain control only | Low/Free | Personal sites, blogs |
| **Organization Validated (OV)** | Organization verification | Medium | Business websites |
| **Extended Validation (EV)** | Extensive vetting | High | E-commerce, banking |

**By Purpose:**
- **SSL/TLS Certificates**: Secure websites (HTTPS)
- **Code Signing**: Sign software and drivers
- **Email Certificates**: S/MIME email encryption
- **Client Certificates**: User authentication
- **Wildcard**: Secure subdomains (*.example.com)

### Certificate Chain (Trust Chain)

**Hierarchy:**
```
Root CA (Self-signed, in trust store)
  │
  └─ Intermediate CA (Signed by Root CA)
      │
      └─ End-Entity Certificate (Signed by Intermediate CA)
```

**Verification Process:**
1. Browser receives end-entity certificate
2. Browser follows chain to intermediate CA
3. Continues to root CA
4. Verifies root CA is in trusted store
5. Validates all signatures in chain
6. Checks certificate validity dates
7. Checks revocation status

**Why Intermediates?**
- Protect root CA private key (offline)
- Enable operational flexibility
- Allow root key rotation without replacing all certificates
- Limit damage if intermediate compromised

### Trust Models

#### Hierarchical Trust

**Structure**: Single root CA with subordinate CAs
**Pros**: Clear authority, easy management
**Cons**: Single point of failure, centralized control
**Example**: Traditional PKI in enterprises

#### Web of Trust

**Structure**: Peer-to-peer trust model, no central authority
**Mechanism**: Users sign each other's keys
**Pros**: Decentralized, no CA needed
**Cons**: Complex, hard to scale
**Example**: PGP/GPG

#### Hybrid Models

Combine elements of both (e.g., blockchain-based PKI)

## Real-World Example: Let's Encrypt

**Background**: Free, automated Certificate Authority launched 2016

**Impact:**
- Issued over 2 billion certificates
- Enabled HTTPS for millions of websites
- Increased global HTTPS adoption from 40% to 85%+

**How It Works:**
1. Website owner runs automated client (Certbot)
2. Client proves domain control via ACME protocol
3. Let's Encrypt issues DV certificate (valid 90 days)
4. Client automatically renews before expiration
5. Entire process automated, no human intervention

**Significance:**
- Removed cost barrier to HTTPS
- Automated certificate management
- Improved web security globally
- Demonstrated viability of free, automated PKI

**Technical Details:**
- Uses ECDSA or RSA certificates
- 90-day validity encourages automation
- Domain validation via HTTP-01, DNS-01, or TLS-ALPN-01 challenges
- Rate limits to prevent abuse

## Quantum Cryptography and Post-Quantum Cryptography

### Quantum Computing Threat

**Problem**: Quantum computers can break current public-key cryptography

**Algorithms at Risk:**
- **RSA**: Shor's algorithm factors large numbers efficiently
- **ECC**: Shor's algorithm solves discrete logarithm problem
- **Diffie-Hellman**: Vulnerable to quantum attacks

**Algorithms Safe (for now):**
- **AES**: Grover's algorithm reduces effective key size by half (AES-256 → AES-128 effective security)
- **SHA-256/SHA-3**: Largely resistant with increased output size

**Timeline:**
- Large-scale quantum computers: 10-20 years estimate
- "Harvest now, decrypt later" attacks: already possible
- Need quantum-resistant algorithms now

### Post-Quantum Cryptography (PQC)

**NIST PQC Standardization (2022 selections):**

| Algorithm | Type | Status |
|-----------|------|--------|
| **CRYSTALS-Kyber** | Key Encapsulation Mechanism | Primary standard |
| **CRYSTALS-Dilithium** | Digital Signature | Primary standard |
| **FALCON** | Digital Signature | Alternative standard |
| **SPHINCS+** | Digital Signature | Stateless hash-based |

**Mathematical Foundations:**
- Lattice-based cryptography (Kyber, Dilithium)
- Hash-based signatures (SPHINCS+)
- Code-based cryptography
- Multivariate polynomial cryptography

**Migration Strategy:**
- Hybrid approach: combine classical and PQC algorithms
- Gradual transition over next decade
- Update long-lived systems first
- Monitor NIST standardization progress

## Cryptography Best Practices

**Algorithm Selection:**
- Use AES-256-GCM for symmetric encryption
- Use RSA-3072+ or ECC (Curve25519) for asymmetric encryption
- Use SHA-256 or SHA-3 for hashing
- Use Argon2id for password hashing
- Avoid deprecated algorithms (DES, 3DES, RC4, MD5, SHA-1)

**Key Management:**
- Generate keys with cryptographically secure random number generators
- Use appropriate key lengths (AES-256, RSA-3072+, ECC-256+)
- Rotate keys regularly
- Store keys securely (HSM, key management service)
- Separate key storage from encrypted data
- Implement key destruction procedures

**Implementation:**
- Use established, audited libraries (OpenSSL, libsodium, cryptography.io)
- Never implement your own cryptography
- Enable Perfect Forward Secrecy (PFS)
- Use authenticated encryption (GCM, Poly1305)
- Implement proper error handling (avoid timing attacks)
- Keep cryptographic libraries updated

**Compliance:**
- Follow NIST guidelines (FIPS 140-2/140-3)
- Meet industry standards (PCI DSS, HIPAA)
- Document cryptographic choices
- Plan for crypto-agility (ability to swap algorithms)

## Key Terms

| Term | Definition |
|------|------------|
| **Cipher Suite** | Set of algorithms for key exchange, encryption, and MAC |
| **Initialization Vector (IV)** | Random value ensuring unique ciphertext for identical plaintexts |
| **Salt** | Random data added to passwords before hashing |
| **Nonce** | Number used once, prevents replay attacks |
| **Perfect Forward Secrecy** | Session keys not compromised if long-term keys are |
| **Key Stretching** | Increasing time to derive key from password |
| **Side-Channel Attack** | Exploiting implementation characteristics (timing, power) |
| **Homomorphic Encryption** | Computation on encrypted data without decryption |

## Summary

Cryptography is the mathematical foundation of information security, protecting data confidentiality, integrity, and authenticity. Symmetric encryption (AES) provides fast, efficient encryption for large data volumes, while asymmetric encryption (RSA, ECC) solves key distribution and enables digital signatures. Cryptographic hash functions (SHA-256, SHA-3) provide data integrity verification and are essential for digital signatures and password storage.

Modern security relies on hybrid systems combining symmetric and asymmetric cryptography for optimal performance and security. Public Key Infrastructure (PKI) establishes trust through certificates and certificate authorities, enabling secure communications across the internet. Specialized password hashing functions (Argon2, bcrypt, scrypt) protect user credentials from offline attacks.

The future of cryptography faces challenges from quantum computing, driving development of post-quantum algorithms. Organizations must balance current security needs with preparation for quantum threats through crypto-agility and hybrid approaches. Success in cryptography requires not just selecting strong algorithms, but implementing them correctly, managing keys securely, and staying informed about evolving threats and standards. Remember: cryptography is only as strong as its weakest link—typically key management or implementation, not the algorithms themselves.

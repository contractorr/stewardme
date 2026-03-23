# Threats and Attacks

## Overview

Understanding cyber threats and attack methods is fundamental to building effective defenses. This guide explores the diverse landscape of malicious software, attack techniques, and threat actors that organizations and individuals face. From sophisticated nation-state operations to opportunistic cybercriminals, the threat ecosystem is complex and constantly evolving.

## Types of Threats

### Threat Categories

| Category | Description | Motivation | Examples |
|----------|-------------|------------|----------|
| **Malware** | Malicious software designed to harm or exploit | Financial gain, espionage, disruption | Viruses, ransomware, trojans |
| **Social Engineering** | Manipulating people to divulge information | Credential theft, access | Phishing, pretexting, baiting |
| **Network Attacks** | Exploiting network vulnerabilities | Data theft, DoS, MitM | Packet sniffing, session hijacking |
| **Web Application Attacks** | Targeting web app vulnerabilities | Data breach, defacement | SQL injection, XSS, CSRF |
| **Physical Threats** | Direct physical access to systems | Theft, sabotage, espionage | Device theft, shoulder surfing |
| **Insider Threats** | Threats from within organization | Revenge, financial gain, negligence | Data exfiltration, sabotage |

## Malware Types

### 1. Viruses

**Definition**: Self-replicating code that attaches to clean files and spreads throughout a system.

**Characteristics:**
- Requires host file to propagate
- Activated when infected file is executed
- Can corrupt, delete, or modify data
- Spreads through file sharing and email attachments

**Types:**
- **File Infector**: Attaches to executable files (.exe, .com)
- **Boot Sector**: Infects master boot record
- **Macro Virus**: Embedded in document macros (Word, Excel)
- **Polymorphic**: Changes code to evade detection

**Example**: The ILOVEYOU virus (2000) spread via email, overwriting files and causing $10 billion in damages globally.

### 2. Worms

**Definition**: Self-replicating malware that spreads independently without host files.

**Characteristics:**
- Spreads automatically across networks
- Consumes bandwidth and system resources
- Exploits security vulnerabilities
- Can carry payloads for additional damage

**Notable Examples:**
- **Morris Worm (1988)**: First major internet worm, affected 10% of internet
- **SQL Slammer (2003)**: Spread globally in 10 minutes
- **Conficker (2008)**: Infected millions of Windows computers

### 3. Trojans

**Definition**: Malware disguised as legitimate software to trick users into installation.

**Characteristics:**
- Appears useful or harmless
- Creates backdoors for attacker access
- Does not self-replicate
- Often downloaded voluntarily by victim

**Types:**
- **Backdoor Trojans**: Provide remote access
- **Banking Trojans**: Steal financial information
- **Downloader Trojans**: Download additional malware
- **Remote Access Trojans (RATs)**: Full remote control

**Example**: Emotet began as banking trojan, evolved into malware distribution platform affecting thousands of organizations.

### 4. Ransomware

**Definition**: Malware that encrypts victim's data and demands payment for decryption key.

**Evolution:**

| Generation | Characteristics | Examples |
|------------|-----------------|----------|
| **1.0: Lock Screen** | Simple screen locks, easily removed | Police-themed ransomware |
| **2.0: Crypto** | File encryption, professional operations | CryptoLocker, Locky |
| **3.0: Double Extortion** | Encryption + data theft threat | Maze, REvil, Conti |
| **4.0: Triple Extortion** | Add DDoS threats, contact customers | Various current groups |

**Modern Tactics:**
- Ransomware-as-a-Service (RaaS) business model
- Targeting backups to prevent recovery
- Demanding millions in cryptocurrency
- Public data leak sites to pressure victims

**Notable Attacks:**
- **WannaCry (2017)**: 200,000+ computers in 150 countries, exploited EternalBlue
- **NotPetya (2017)**: Disguised as ransomware, actually destructive wiper
- **Colonial Pipeline (2021)**: $4.4M ransom, fuel supply disruption

### 5. Spyware and Adware

**Spyware:**
- Monitors user activity without consent
- Collects personal information, browsing habits
- Logs keystrokes (keyloggers)
- Captures screenshots and webcam images

**Adware:**
- Displays unwanted advertisements
- Tracks browsing for ad targeting
- Slows system performance
- May bundle with legitimate software

**Example**: The Pegasus spyware (NSO Group) exploits zero-day vulnerabilities to compromise smartphones, targeting journalists and activists.

### 6. Rootkits

**Definition**: Software that provides privileged access while hiding its presence.

**Characteristics:**
- Operates at kernel or firmware level
- Extremely difficult to detect and remove
- Can hide other malware
- Persists across reboots

**Types:**
- **User-Mode**: Easier to detect, limited privileges
- **Kernel-Mode**: Deep system access, harder to detect
- **Firmware/BIOS**: Survives OS reinstallation

### 7. Botnets

**Definition**: Network of infected computers controlled remotely for coordinated attacks.

**Uses:**
- Distributed Denial of Service (DDoS) attacks
- Spam email distribution
- Cryptocurrency mining
- Credential stuffing attacks

**Example**: Mirai botnet (2016) infected IoT devices (cameras, routers) and launched massive DDoS attacks, peaking at 1.2 Tbps.

## Social Engineering

### Definition and Psychology

Social engineering exploits human psychology rather than technical vulnerabilities. It relies on:
- **Authority**: Posing as authority figures
- **Urgency**: Creating pressure to act quickly
- **Trust**: Exploiting established relationships
- **Fear**: Threatening consequences
- **Curiosity**: Enticing with interesting content

### Attack Types

#### 1. Phishing

**Email-based attacks** impersonating legitimate organizations to steal credentials or distribute malware.

**Indicators:**
- Generic greetings ("Dear Customer")
- Urgent or threatening language
- Suspicious sender addresses
- Spelling and grammar errors
- Requests for sensitive information
- Suspicious links or attachments

**Variants:**

| Type | Target | Method |
|------|--------|--------|
| **Spear Phishing** | Specific individuals | Personalized messages with research |
| **Whaling** | Executives (C-suite) | High-value targets, sophisticated |
| **Smishing** | Mobile users | SMS/text messages |
| **Vishing** | Phone recipients | Voice calls |
| **Clone Phishing** | Previous email recipients | Legitimate email resent with malicious link |

**Example**: Business Email Compromise (BEC) scams impersonate executives requesting wire transfers, causing $43 billion in losses (2016-2021).

#### 2. Pretexting

Creating fabricated scenarios to obtain information.

**Common Scenarios:**
- IT support requesting password "verification"
- HR conducting "employee survey"
- Bank "security department" verifying account
- Vendor requesting payment information update

**Example**: Attacker poses as IT helpdesk, convinces employee to install "security update" that's actually malware.

#### 3. Baiting

Offering something enticing to lure victims.

**Methods:**
- Infected USB drives left in parking lot
- Free software downloads with malware
- "Free" movie or music downloads
- Fake job offers requiring information

**Example**: Attackers drop USB drives labeled "Executive Salary Information" outside company, hoping curious employees will plug them in.

#### 4. Tailgating/Piggybacking

Following authorized persons into restricted areas.

**Techniques:**
- Carrying boxes, appearing to need help
- Posing as delivery person or contractor
- Timing entry with legitimate employees
- Exploiting politeness and social norms

#### 5. Quid Pro Quo

Offering service in exchange for information or access.

**Examples:**
- Fake tech support offering to fix problems
- "Security audit" requesting credentials
- "Survey" in exchange for gift card
- IT calling about "virus infection"

## Attack Vectors and Methods

### Network-Based Attacks

#### 1. Man-in-the-Middle (MitM)

**Description**: Intercepting communications between two parties.

**Methods:**
- **ARP Spoofing**: Redirecting network traffic
- **DNS Spoofing**: Redirecting domain requests
- **Session Hijacking**: Stealing session tokens
- **SSL Stripping**: Downgrading HTTPS to HTTP

**Prevention:**
- Use VPNs on public networks
- Verify SSL certificates
- Implement certificate pinning
- Use encrypted protocols (HTTPS, SSH)

#### 2. Denial of Service (DoS/DDoS)

**Description**: Overwhelming systems to make them unavailable.

**Types:**

| Attack Type | Method | Impact |
|-------------|--------|--------|
| **Volumetric** | Flood bandwidth with traffic | Network saturation |
| **Protocol** | Exploit protocol weaknesses | Server resource exhaustion |
| **Application Layer** | Target specific applications | Service unavailability |
| **Amplification** | Use third parties to multiply traffic | Massive traffic volume |

**Notable DDoS Attacks:**
- GitHub (2018): 1.35 Tbps via memcached amplification
- AWS (2020): 2.3 Tbps, largest recorded
- Google (2017): 2.54 Tbps via multiple amplification vectors

#### 3. Packet Sniffing

**Description**: Capturing network traffic to analyze data.

**Tools**: Wireshark, tcpdump, Ettercap

**Risks:**
- Unencrypted credentials captured
- Sensitive data exposure
- Network reconnaissance

**Protection**: Encryption (SSL/TLS, VPN)

#### 4. Port Scanning

**Description**: Probing systems to identify open ports and services.

**Tools**: Nmap, Masscan, Angry IP Scanner

**Purpose**: Reconnaissance for attack planning

### Application-Level Attacks

#### 1. Password Attacks

**Brute Force**: Trying all possible combinations
- Time-consuming but eventually successful
- Defeated by account lockouts and rate limiting

**Dictionary Attack**: Using common passwords
- More efficient than brute force
- Exploits poor password choices

**Credential Stuffing**: Using leaked credentials
- Exploits password reuse across sites
- Automated using botnets

**Password Spraying**: Trying common passwords against many accounts
- Avoids account lockouts
- Targets weak password policies

**Rainbow Tables**: Pre-computed hash values
- Fast lookup of password hashes
- Defeated by salting

#### 2. Session Hijacking

**Description**: Stealing or predicting session tokens to impersonate users.

**Methods:**
- Session fixation
- Cross-site scripting (XSS)
- Network sniffing
- Session sidejacking

**Prevention:**
- Secure session management
- HTTPS enforcement
- HTTPOnly and Secure cookie flags
- Session timeout and regeneration

#### 3. Drive-by Downloads

**Description**: Automatic malware download from compromised websites.

**Attack Flow:**
1. Attacker compromises legitimate website
2. Injects malicious code exploiting browser vulnerabilities
3. Visitor's browser automatically downloads malware
4. Malware executes without user interaction

**Prevention:**
- Keep browsers and plugins updated
- Disable automatic file downloads
- Use script blockers (NoScript)
- Employ endpoint protection

### Advanced Persistent Threats (APTs)

**Definition**: Long-term, targeted attacks by sophisticated actors (often nation-states).

**Characteristics:**
- Specific high-value targets
- Multi-stage, stealthy operations
- Custom malware and tools
- Patient, persistent approach
- Well-resourced operations

**Attack Phases:**

| Phase | Activities | Duration |
|-------|------------|----------|
| **Reconnaissance** | Target research, vulnerability identification | Weeks to months |
| **Initial Compromise** | Spear phishing, zero-day exploits | Hours to days |
| **Establish Foothold** | Install backdoors, create accounts | Days to weeks |
| **Escalate Privileges** | Gain administrative access | Days to weeks |
| **Lateral Movement** | Spread to other systems | Weeks to months |
| **Data Exfiltration** | Steal target information | Months to years |
| **Maintain Presence** | Persist undetected | Months to years |

**Notable APT Groups:**
- **APT28/Fancy Bear**: Russian military intelligence (GRU)
- **APT29/Cozy Bear**: Russian foreign intelligence (SVR)
- **APT1**: Chinese PLA Unit 61398
- **Lazarus Group**: North Korean state-sponsored

**Example**: SolarWinds attack (2020) by APT29 compromised software updates, affecting 18,000+ organizations including US government agencies.

## Threat Actors

### Classification

| Actor Type | Motivation | Sophistication | Examples |
|------------|------------|----------------|----------|
| **Script Kiddies** | Notoriety, curiosity | Low | Using pre-built tools without understanding |
| **Hacktivists** | Political/social causes | Medium | Anonymous, LulzSec |
| **Cybercriminals** | Financial gain | Medium-High | Ransomware groups, financial fraud |
| **Nation-States** | Espionage, sabotage | Very High | APT groups, intelligence agencies |
| **Insider Threats** | Revenge, gain, negligence | Varies | Disgruntled employees, careless staff |
| **Terrorists** | Fear, disruption | Medium-High | Targeting critical infrastructure |

### Real-World Examples

**Edward Snowden (Insider Threat, 2013):**
- NSA contractor leaked classified documents
- Motivation: Whistleblowing
- Impact: Revealed global surveillance programs
- Lesson: Insider access controls and monitoring

**NotPetya (Nation-State Attack, 2017):**
- Russian attack disguised as ransomware
- Targeted Ukraine, spread globally
- $10 billion in damages
- Lesson: Geopolitical cyber conflicts have global impact

## Attack Kill Chain

The Lockheed Martin Cyber Kill Chain models attack stages:

1. **Reconnaissance**: Research, identify targets
2. **Weaponization**: Couple exploit with payload
3. **Delivery**: Transmit weapon to target
4. **Exploitation**: Trigger vulnerability
5. **Installation**: Install backdoor/malware
6. **Command & Control**: Establish remote control
7. **Actions on Objectives**: Achieve goal (data theft, etc.)

**Defense Strategy**: Break the chain at any point to prevent attack success.

## Indicators of Compromise (IoCs)

**Network Indicators:**
- Unusual outbound traffic
- Connections to suspicious IPs
- DNS requests to uncommon domains
- Unexpected open ports

**System Indicators:**
- Unknown processes or services
- Registry modifications
- New scheduled tasks
- Unusual file changes

**User Indicators:**
- Failed login attempts
- Account access from unusual locations
- Privilege escalation attempts
- Off-hours access

## Key Terms

| Term | Definition |
|------|------------|
| **Zero-Day** | Previously unknown vulnerability with no patch |
| **Exploit Kit** | Pre-packaged tools for exploiting vulnerabilities |
| **C2/C&C** | Command and Control server for malware communication |
| **Payload** | Malicious code delivered by exploit |
| **Threat Intelligence** | Information about threats and threat actors |
| **Attack Surface** | All possible entry points for attacks |
| **Lateral Movement** | Spreading within compromised network |
| **Persistence** | Maintaining access after reboot or detection attempts |

## Summary

The cyber threat landscape is diverse and constantly evolving, ranging from simple malware to sophisticated nation-state operations. Malware types include viruses, worms, trojans, ransomware, spyware, rootkits, and botnets, each with unique characteristics and impacts. Social engineering exploits human psychology through phishing, pretexting, baiting, and other manipulation techniques—often proving more effective than technical attacks.

Attack vectors span network-based methods (MitM, DDoS, sniffing), application-level attacks (password attacks, session hijacking), and Advanced Persistent Threats (APTs) that combine multiple techniques for long-term infiltration. Threat actors range from unskilled script kiddies to highly sophisticated nation-state groups, each with different motivations and capabilities.

Understanding these threats is the first step in building effective defenses. The Cyber Kill Chain provides a framework for understanding attack progression and identifying intervention points. Combining technical controls with user awareness training creates defense-in-depth that addresses both technical and human vulnerabilities. Remember: security is about managing risk, not eliminating it entirely—staying informed about evolving threats enables better-informed defensive decisions.

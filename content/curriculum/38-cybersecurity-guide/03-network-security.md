# Network Security

## Overview

Network security protects the integrity, confidentiality, and availability of data as it transmits across or is stored on networks. It involves implementing policies, practices, and technologies to prevent unauthorized access, misuse, malfunction, modification, destruction, or improper disclosure of network resources. This guide explores fundamental network security concepts, technologies, and best practices.

## Network Fundamentals

### OSI Model and Security

The OSI (Open Systems Interconnection) model provides a framework for understanding network security at each layer:

| Layer | Name | Security Concerns | Security Controls |
|-------|------|-------------------|-------------------|
| **7** | Application | Malware, phishing, application vulnerabilities | WAF, application firewalls, input validation |
| **6** | Presentation | Data encryption, encoding attacks | TLS/SSL, data encryption |
| **5** | Session | Session hijacking, authentication | Session management, tokens, timeouts |
| **4** | Transport | Port scanning, DoS | Firewalls, rate limiting, TCP wrappers |
| **3** | Network | IP spoofing, routing attacks, packet sniffing | IPSec, routers, VPNs, network segmentation |
| **2** | Data Link | MAC spoofing, ARP poisoning, VLAN hopping | Port security, 802.1X, VLAN isolation |
| **1** | Physical | Physical access, wire tapping | Physical security, cable encryption |

### TCP/IP Protocol Suite Security

**Key Protocols and Vulnerabilities:**

| Protocol | Purpose | Vulnerabilities | Security Measures |
|----------|---------|-----------------|-------------------|
| **IP** | Addressing and routing | Spoofing, fragmentation attacks | IPSec, ingress/egress filtering |
| **TCP** | Reliable data transmission | SYN flooding, session hijacking | SYN cookies, sequence randomization |
| **UDP** | Fast, connectionless transmission | Amplification attacks, spoofing | Rate limiting, filtering |
| **ICMP** | Error messages, diagnostics | DoS, reconnaissance | ICMP filtering, rate limiting |
| **DNS** | Domain name resolution | Cache poisoning, tunneling | DNSSEC, monitoring |
| **HTTP/HTTPS** | Web traffic | MitM, injection attacks | TLS/SSL, HSTS, certificate validation |

## Firewalls

### Definition and Purpose

Firewalls are network security devices that monitor and control incoming and outgoing network traffic based on predetermined security rules. They establish a barrier between trusted internal networks and untrusted external networks.

### Types of Firewalls

#### 1. Packet-Filtering Firewalls

**Operation:**
- Examines packet headers (source/destination IP, port, protocol)
- Makes allow/deny decisions based on rules
- Operates at Network Layer (Layer 3)

**Advantages:**
- Fast and efficient
- Low cost
- Minimal impact on performance

**Disadvantages:**
- No application awareness
- Vulnerable to IP spoofing
- Cannot inspect packet contents
- No state awareness (early versions)

**Example Rule:**
```
Allow TCP from 192.168.1.0/24 to any port 443
Deny TCP from any to 10.0.0.0/8 port 22
```

#### 2. Stateful Inspection Firewalls

**Operation:**
- Tracks connection states (NEW, ESTABLISHED, RELATED)
- Maintains state table of active connections
- Makes decisions based on context, not just individual packets

**Advantages:**
- More secure than packet filtering
- Understands connection lifecycle
- Detects out-of-state packets
- Better performance than proxy firewalls

**State Table Example:**
```
Source IP    | Dest IP      | Source Port | Dest Port | State
192.168.1.10 | 8.8.8.8      | 54321       | 443       | ESTABLISHED
192.168.1.15 | 93.184.216.34| 49152       | 80        | NEW
```

#### 3. Proxy Firewalls (Application-Level Gateways)

**Operation:**
- Acts as intermediary between clients and servers
- Terminates connections on both sides
- Inspects application-layer data
- Operates at Application Layer (Layer 7)

**Types:**
- **Forward Proxy**: Client-side proxy for outbound connections
- **Reverse Proxy**: Server-side proxy for inbound connections

**Advantages:**
- Deep packet inspection
- Application-aware filtering
- Can block specific content types
- Hides internal network structure

**Disadvantages:**
- Performance impact
- Higher latency
- More complex configuration
- Resource intensive

#### 4. Next-Generation Firewalls (NGFW)

**Features:**
- Traditional firewall capabilities
- Deep packet inspection (DPI)
- Intrusion prevention system (IPS)
- Application awareness and control
- SSL/TLS inspection
- Threat intelligence integration
- User/identity awareness

**Vendors**: Palo Alto Networks, Cisco Firepower, Fortinet FortiGate, Check Point

**Capabilities Table:**

| Feature | Traditional Firewall | NGFW |
|---------|---------------------|------|
| Packet filtering | Yes | Yes |
| Stateful inspection | Yes | Yes |
| Application control | No | Yes |
| IPS/IDS | No | Yes |
| DPI | No | Yes |
| User identity | No | Yes |
| Threat intelligence | No | Yes |

#### 5. Web Application Firewalls (WAF)

**Purpose**: Protect web applications from HTTP/HTTPS attacks

**Protections:**
- SQL injection
- Cross-site scripting (XSS)
- Cross-site request forgery (CSRF)
- File inclusion
- Protocol violations

**Deployment:**
- Network-based (hardware appliance)
- Host-based (server module)
- Cloud-based (SaaS)

**Popular WAFs**: ModSecurity, AWS WAF, Cloudflare WAF, Imperva

### Firewall Architectures

#### 1. Screened Subnet (DMZ)

**Design:**
```
Internet <--> External Firewall <--> DMZ (Public Servers) <--> Internal Firewall <--> Internal Network
```

**Benefits:**
- Public services isolated from internal network
- Two layers of protection
- Compromised DMZ doesn't expose internal network

**Use Cases:**
- Web servers
- Email servers
- DNS servers
- FTP servers

#### 2. Dual-Homed Host

**Design:**
- Single firewall with two network interfaces
- One interface to internet, one to internal network
- All traffic passes through firewall

**Considerations:**
- Single point of failure
- Must be hardened and monitored
- Less resilient than screened subnet

#### 3. Multi-Layer Defense

**Design:**
- Multiple firewalls at different network segments
- Each layer enforces different policies
- Defense in depth approach

**Example:**
```
Internet <--> Perimeter Firewall <--> Public DMZ <--> Distribution Firewall <--> Internal Segments <--> Data Center Firewall <--> Sensitive Data
```

### Firewall Best Practices

**Configuration:**
- Default deny (whitelist approach)
- Least privilege principle
- Regular rule review and cleanup
- Document all rules and changes
- Use groups and objects for clarity

**Management:**
- Change control procedures
- Regular backups of configurations
- Logging and monitoring
- Periodic security audits
- Keep firmware updated

**Common Mistakes:**
- "Any-any-any" rules
- Overly permissive rules
- Unmanaged rule sprawl
- Insufficient logging
- No regular reviews

## Intrusion Detection and Prevention Systems

### Intrusion Detection Systems (IDS)

**Definition**: Monitors network traffic for suspicious activity and alerts administrators.

**Modes:**
- **Passive**: Monitors traffic copy (span port, tap)
- **Detection only**: Cannot block attacks
- **Generates alerts**: For human review

**Types:**

#### 1. Network-Based IDS (NIDS)

**Placement**: Strategic network points (border, DMZ, critical segments)

**Monitors:**
- Network packets
- Protocol anomalies
- Known attack signatures
- Traffic patterns

**Advantages:**
- Sees all network traffic
- Difficult for attackers to detect
- Minimal impact on network devices

**Disadvantages:**
- Cannot see encrypted traffic (without decryption)
- High traffic volumes challenging
- Cannot detect host-based attacks

**Popular Tools**: Snort, Suricata, Zeek (Bro)

#### 2. Host-Based IDS (HIDS)

**Placement**: Individual hosts (servers, workstations)

**Monitors:**
- System calls
- File integrity
- Log files
- Application activity
- Registry changes (Windows)

**Advantages:**
- Sees encrypted traffic (after decryption)
- Detects local attacks
- Specific to host context

**Disadvantages:**
- Resource consumption on host
- Attacker may disable if host compromised
- Must be installed on each host

**Popular Tools**: OSSEC, Tripwire, Samhain

### Intrusion Prevention Systems (IPS)

**Definition**: Actively blocks detected threats in real-time.

**Modes:**
- **Inline**: Traffic passes through IPS
- **Active response**: Can block malicious traffic
- **Prevention**: Stops attacks before reaching target

**Deployment:**

| IDS | IPS |
|-----|-----|
| Out-of-band (passive) | Inline (active) |
| Alerts only | Blocks attacks |
| No traffic impact | Can affect traffic flow |
| Lower risk | Higher risk (false positives) |

**Prevention Actions:**
- Drop malicious packets
- Reset connections
- Block source IP (temporary or permanent)
- Alert administrator
- Log incident

### Detection Methods

#### 1. Signature-Based Detection

**Method**: Matches traffic against known attack patterns (signatures).

**Advantages:**
- Low false positive rate
- Fast detection
- Well-understood attacks

**Disadvantages:**
- Cannot detect zero-day attacks
- Requires signature updates
- Evasion techniques bypass signatures

**Example Signature (Snort):**
```
alert tcp any any -> any 80 (msg:"SQL Injection Attempt"; content:"union select"; nocase; sid:100001;)
```

#### 2. Anomaly-Based Detection

**Method**: Establishes baseline of normal behavior, alerts on deviations.

**Advantages:**
- Can detect zero-day attacks
- Identifies unknown threats
- Adapts to environment

**Disadvantages:**
- Higher false positive rate
- Requires training period
- Normal changes trigger alerts

**Techniques:**
- Statistical analysis
- Protocol analysis
- Traffic pattern analysis
- Machine learning

#### 3. Hybrid Approach

**Method**: Combines signature and anomaly detection.

**Benefits:**
- Broader detection coverage
- Reduced false positives (vs. anomaly alone)
- Detects both known and unknown threats

### IDS/IPS Best Practices

**Deployment:**
- Place NIDS at critical network points
- Deploy IPS inline at perimeter
- Use HIDS on critical servers
- Encrypt management traffic

**Configuration:**
- Tune signatures for environment
- Establish accurate baselines
- Regular signature updates
- Balance detection vs. false positives

**Operations:**
- Monitor alerts continuously (SOC)
- Investigate all high-priority alerts
- Regularly review and tune rules
- Correlate with other security tools
- Document incidents and responses

**Testing:**
- Test IPS in IDS mode first
- Validate signatures before deployment
- Regular testing with attack tools
- Verify prevention actions work

## Virtual Private Networks (VPNs)

### Definition and Purpose

VPNs create secure, encrypted tunnels over public networks, enabling secure remote access and site-to-site connectivity.

### VPN Types

#### 1. Remote Access VPN

**Purpose**: Connect remote users to corporate network.

**Use Cases:**
- Remote workers
- Traveling employees
- Contractors
- BYOD access

**Components:**
- VPN client software
- VPN gateway (concentrator)
- Authentication server
- Access control policies

**Connection Flow:**
1. User initiates VPN connection
2. Authentication (username/password, certificate, MFA)
3. Tunnel established and encrypted
4. User accesses internal resources
5. Traffic encrypted through tunnel

#### 2. Site-to-Site VPN

**Purpose**: Connect entire networks across locations.

**Use Cases:**
- Branch offices to headquarters
- Partner network connections
- Cloud to on-premises connectivity
- Disaster recovery sites

**Advantages:**
- Always-on connectivity
- No client software needed
- Entire subnet access
- Transparent to users

**Disadvantages:**
- Complex configuration
- Higher bandwidth requirements
- Single point of failure

### VPN Protocols

| Protocol | Layer | Encryption | Ports | Pros | Cons |
|----------|-------|------------|-------|------|------|
| **IPSec** | Layer 3 | Strong | UDP 500, 4500 | Industry standard, strong security | Complex configuration |
| **SSL/TLS VPN** | Layer 4-7 | Strong | TCP 443 | Easy deployment, web-based | May be slower |
| **OpenVPN** | Layer 2/3 | Strong (SSL/TLS) | Configurable | Open source, flexible, cross-platform | Requires client software |
| **WireGuard** | Layer 3 | Modern | UDP (configurable) | Fast, simple, modern crypto | Relatively new |
| **L2TP/IPSec** | Layer 2 | IPSec | UDP 500, 1701, 4500 | Wide support | Slower, complex |
| **PPTP** | Layer 2 | Weak (MPPE) | TCP 1723 | Easy setup, legacy support | **Insecure, deprecated** |

### IPSec Deep Dive

**Components:**

1. **Authentication Header (AH)**
   - Provides authentication and integrity
   - No encryption
   - Rarely used alone

2. **Encapsulating Security Payload (ESP)**
   - Provides encryption and authentication
   - Most commonly used
   - Protects payload confidentiality

**Modes:**

| Mode | Description | Use Case |
|------|-------------|----------|
| **Transport** | Encrypts only payload, original IP header visible | Host-to-host, end-to-end |
| **Tunnel** | Encrypts entire packet, adds new IP header | Site-to-site, gateway-to-gateway |

**Key Exchange:**
- **IKE (Internet Key Exchange)**: Negotiates security associations
- **IKEv1**: Original version, two phases
- **IKEv2**: Modern version, fewer round trips, better performance

**Configuration Parameters:**
- Encryption algorithms (AES-128/256, 3DES)
- Authentication algorithms (SHA-256, SHA-512)
- Diffie-Hellman groups (DH14, DH19, DH20)
- Lifetime/rekey timers
- Perfect Forward Secrecy (PFS)

### SSL/TLS VPN

**Advantages:**
- Uses standard HTTPS port (443)
- Works through most firewalls
- No client installation (portal-based)
- Granular access control

**Deployment Modes:**
- **Clientless (Portal)**: Web-based access to specific applications
- **Thin Client**: Browser plugin for enhanced capabilities
- **Full Client**: Installed software for complete network access

**Authentication Methods:**
- Username/password
- Digital certificates
- Multi-factor authentication (MFA)
- Smart cards
- SAML/SSO integration

### VPN Security Considerations

**Split Tunneling:**
- **Full Tunnel**: All traffic through VPN (more secure)
- **Split Tunnel**: Only corporate traffic through VPN (better performance)
- **Risk**: Split tunnel allows bypass of corporate security controls

**Best Practices:**
- Require MFA for VPN access
- Use strong encryption (AES-256, modern ciphers)
- Implement idle timeout policies
- Monitor VPN connections and traffic
- Regular security updates
- Disable split tunneling if policy requires
- Use device posture checking
- Implement least privilege access

## Network Segmentation

### Definition and Benefits

Network segmentation divides networks into smaller isolated segments, limiting lateral movement and containing breaches.

**Benefits:**
- **Reduced Attack Surface**: Limits accessible systems
- **Contain Breaches**: Prevents lateral movement
- **Performance**: Reduces broadcast domains
- **Compliance**: Isolates regulated data
- **Access Control**: Granular security policies

### Segmentation Techniques

#### 1. VLANs (Virtual LANs)

**Definition**: Logical network divisions on physical switches.

**Configuration:**
```
VLAN 10: Finance Department (10.10.10.0/24)
VLAN 20: Engineering (10.10.20.0/24)
VLAN 30: Guest Network (10.10.30.0/24)
VLAN 99: Management (10.10.99.0/24)
```

**Security:**
- Inter-VLAN routing controlled by firewall
- Prevents broadcast storms
- Logical isolation without physical separation

**Limitations:**
- VLAN hopping attacks possible
- Requires proper trunk configuration
- All VLANs share physical infrastructure

#### 2. Subnetting

**Purpose**: Divide IP address space into smaller networks.

**Example:**
```
Corporate Network: 10.0.0.0/8

Data Center: 10.1.0.0/16
  - Web Servers: 10.1.1.0/24
  - App Servers: 10.1.2.0/24
  - Database: 10.1.3.0/24

Offices: 10.2.0.0/16
  - Building A: 10.2.1.0/24
  - Building B: 10.2.2.0/24

Remote Access: 10.3.0.0/16
```

#### 3. Microsegmentation

**Definition**: Granular, workload-level segmentation.

**Implementation:**
- Software-defined networking (SDN)
- Host-based firewalls
- Network access control
- Zero trust architecture

**Benefits:**
- East-west traffic control
- Application-aware policies
- Dynamic policy enforcement
- Cloud-native security

### Segmentation Models

#### 1. Three-Tier Architecture

**Tiers:**
- **Presentation (Web)**: Public-facing web servers
- **Application (Logic)**: Business logic servers
- **Data**: Database servers

**Security:**
- Each tier in separate network segment
- Firewalls between tiers
- Strict access control rules

#### 2. Zero Trust Model

**Principles:**
- Never trust, always verify
- Assume breach
- Verify explicitly
- Least privilege access
- Microsegmentation

**Implementation:**
- Identity-based access control
- Continuous verification
- Encrypt all traffic
- Monitor and log everything
- Automated threat response

## Secure Network Protocols

### Protocol Comparison

| Protocol | Purpose | Security | Port | Status |
|----------|---------|----------|------|--------|
| **HTTP** | Web traffic | None (plaintext) | 80 | Deprecated for sensitive data |
| **HTTPS** | Secure web traffic | TLS/SSL | 443 | Standard |
| **Telnet** | Remote access | None (plaintext) | 23 | **Insecure, deprecated** |
| **SSH** | Secure remote access | Encrypted | 22 | Standard |
| **FTP** | File transfer | None (plaintext) | 20, 21 | **Insecure, deprecated** |
| **SFTP** | Secure file transfer | SSH encryption | 22 | Standard |
| **FTPS** | FTP over SSL/TLS | TLS/SSL | 989, 990 | Secure alternative |
| **SNMP v1/v2** | Network management | None/weak | 161, 162 | **Insecure** |
| **SNMP v3** | Secure management | Encrypted | 161, 162 | Standard |
| **DNS** | Name resolution | None | 53 | Insecure without DNSSEC |
| **DNSSEC** | Secure DNS | Cryptographic signatures | 53 | Recommended |

### SSH (Secure Shell) Best Practices

**Configuration:**
- Disable password authentication (use keys only)
- Disable root login
- Use strong ciphers and MACs
- Change default port (optional)
- Implement idle timeout
- Restrict access by IP/subnet

**Example `/etc/ssh/sshd_config`:**
```
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
Protocol 2
Port 2222
ClientAliveInterval 300
ClientAliveCountMax 2
AllowUsers admin sysadmin
```

### TLS/SSL Best Practices

**Configuration:**
- Use TLS 1.3 or TLS 1.2 minimum
- Disable TLS 1.0, TLS 1.1, SSLv3
- Use strong cipher suites
- Enable Perfect Forward Secrecy (PFS)
- Implement HSTS (HTTP Strict Transport Security)
- Use valid certificates from trusted CAs
- Implement certificate pinning (for apps)

**Strong Cipher Suite Example:**
```
TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
```

## Real-World Example: Network Segmentation Preventing Breach Spread

**Scenario**: Financial institution with segmented network.

**Network Design:**
```
Internet
  |
Perimeter Firewall
  |
DMZ (Web Servers, Email Gateway)
  |
Internal Firewall
  |
Corporate Network
  |-- Employee VLAN (802.1X authentication)
  |-- Finance VLAN (accounting systems)
  |-- Trading VLAN (trading platforms)
  |-- Database VLAN (customer data)
```

**Incident:**
1. Phishing email compromises employee workstation
2. Attacker gains access to Employee VLAN
3. Attempts to move to Finance VLAN
4. Firewall blocks unauthorized inter-VLAN traffic
5. IPS detects reconnaissance attempts
6. Security team alerted and isolates compromised host

**Outcome:**
- Breach contained to single VLAN segment
- No access to sensitive financial or customer data
- Quick incident response and remediation
- Minimal business impact

**Lessons:**
- Network segmentation limited blast radius
- Defense in depth prevented complete compromise
- IDS/IPS provided early warning
- Proper firewall rules enforced separation

## Key Terms

| Term | Definition |
|------|------------|
| **DMZ** | Demilitarized Zone; network segment for public-facing services |
| **ACL** | Access Control List; rules defining allowed/denied traffic |
| **NAT** | Network Address Translation; remapping IP addresses |
| **Port Forwarding** | Redirecting traffic from one port to another |
| **Egress Filtering** | Controlling outbound traffic from network |
| **Ingress Filtering** | Controlling inbound traffic to network |
| **East-West Traffic** | Traffic between servers within data center |
| **North-South Traffic** | Traffic between data center and external networks |
| **Span Port** | Switch port that mirrors traffic for monitoring |
| **Network Tap** | Physical device that copies network traffic |

## Summary

Network security forms the foundation of organizational cybersecurity, protecting data in transit and controlling access to resources. Firewalls—from basic packet filters to sophisticated next-generation firewalls—provide the first line of defense by controlling traffic flow based on security policies. Intrusion detection and prevention systems add another layer, monitoring for malicious activity and blocking threats in real-time.

Virtual Private Networks enable secure remote access and site-to-site connectivity through encrypted tunnels, with protocols like IPSec and SSL/TLS providing strong security. Network segmentation divides networks into isolated zones, limiting lateral movement and containing breaches when they occur. Modern approaches like zero trust and microsegmentation extend these principles to individual workloads.

Effective network security requires understanding protocols, deploying appropriate technologies, and following best practices. Using secure protocols (SSH vs. Telnet, HTTPS vs. HTTP, SFTP vs. FTP) protects data confidentiality. Regular monitoring, proper configuration, and defense-in-depth architecture create resilient networks capable of withstanding sophisticated attacks. Remember: network security isn't a one-time implementation but an ongoing process of monitoring, updating, and improving defenses as threats evolve.

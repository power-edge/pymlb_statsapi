# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of PyMLB StatsAPI seriously. If you discover a security vulnerability, please follow these steps:

### How to Report

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

1. **GitHub Security Advisory** (Preferred):
   - Go to the [Security Advisory page](https://github.com/power-edge/pymlb_statsapi/security/advisories/new)
   - Click "New draft security advisory"
   - Provide details about the vulnerability

2. **Email**:
   - Send an email to the project maintainers
   - Include "SECURITY" in the subject line
   - Provide details about the vulnerability

3. **Private Issue**:
   - Contact a maintainer directly through GitHub
   - Request a private channel to discuss the issue

### What to Include

When reporting a vulnerability, please include:

- **Type of issue** (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- **Full paths of source file(s)** related to the manifestation of the issue
- **Location of the affected source code** (tag/branch/commit or direct URL)
- **Step-by-step instructions to reproduce** the issue
- **Proof-of-concept or exploit code** (if possible)
- **Impact of the issue**, including how an attacker might exploit it

### What to Expect

After you submit a vulnerability report:

1. **Acknowledgment**: We will acknowledge receipt of your report within 48 hours
2. **Assessment**: We will investigate and assess the severity within 7 days
3. **Updates**: We will keep you informed of our progress
4. **Fix**: We will work on a fix and coordinate disclosure
5. **Credit**: We will credit you for the discovery (unless you prefer to remain anonymous)

## Security Update Process

When a security vulnerability is confirmed:

1. **Private Fix**: We develop a fix in a private repository
2. **Testing**: The fix is thoroughly tested
3. **Advisory**: A security advisory is prepared
4. **Release**: A new version is released with the fix
5. **Disclosure**: The vulnerability is publicly disclosed with appropriate details

## Security Best Practices for Users

When using PyMLB StatsAPI:

### 1. Keep Dependencies Updated

```bash
# Regularly update to the latest version
pip install --upgrade pymlb-statsapi

# Check for security vulnerabilities
pip-audit
```

### 2. Environment Variables

- Never commit API keys or tokens to version control
- Use environment variables or secure configuration management
- Rotate credentials regularly

### 3. Input Validation

While PyMLB StatsAPI validates parameters against schemas, always validate user input in your application:

```python
from pymlb_statsapi import api

# Bad: Direct user input without validation
user_input = request.get('game_pk')
response = api.Game.boxscore(game_pk=user_input)

# Good: Validate user input first
user_input = request.get('game_pk')
if user_input.isdigit() and len(user_input) <= 10:
    response = api.Game.boxscore(game_pk=user_input)
else:
    raise ValueError("Invalid game_pk")
```

### 4. Error Handling

Don't expose sensitive information in error messages:

```python
try:
    response = api.Schedule.schedule(sportId=1, date="2024-10-27")
except Exception as e:
    # Bad: Exposing full error to user
    return str(e)

    # Good: Log the error, show generic message to user
    logger.error(f"API error: {e}")
    return "An error occurred while fetching data"
```

### 5. Rate Limiting

Implement rate limiting to prevent abuse:

```python
from time import sleep

# Implement rate limiting
for game_pk in game_pks:
    response = api.Game.boxscore(game_pk=game_pk)
    sleep(0.1)  # 100ms delay between requests
```

## Known Security Considerations

### 1. File Storage

When using the file storage feature:

- Files are saved with metadata including URLs and parameters
- Default storage location is `./.var/local/mlb_statsapi`
- Ensure appropriate file permissions if storing in shared locations

### 2. Network Requests

- All API requests go to `statsapi.mlb.com` over HTTPS
- Certificate verification is enabled by default
- Requests library handles SSL/TLS

### 3. Data Privacy

- PyMLB StatsAPI does not collect or transmit any user data
- All API calls go directly to MLB Stats API
- No telemetry or analytics

## Security Tools

We use the following tools to maintain security:

- **Bandit**: Python security linting
- **Safety/pip-audit**: Dependency vulnerability scanning
- **GitHub Dependabot**: Automated dependency updates
- **CodeQL**: Static code analysis
- **Pre-commit hooks**: Automated security checks

## Disclosure Policy

- **90-day disclosure timeline**: We aim to fix vulnerabilities within 90 days
- **Coordinated disclosure**: We coordinate with reporters before public disclosure
- **CVE assignment**: We request CVE IDs for significant vulnerabilities
- **Security advisories**: Published via GitHub Security Advisories

## Security Hall of Fame

We recognize and thank security researchers who responsibly disclose vulnerabilities:

<!-- Hall of Fame list will be maintained here -->

## Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

## Contact

For security concerns, please contact:

- **GitHub Security Advisory**: [Create advisory](https://github.com/power-edge/pymlb_statsapi/security/advisories/new)
- **Project Maintainers**: Via GitHub profile

## Updates to This Policy

This security policy may be updated from time to time. Please check back regularly for updates.

**Last Updated**: 2025-01-15

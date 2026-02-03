# 🛡️ Network Security Monitoring Solution

## Overview
A comprehensive network security monitoring system with real-time controls for all major security features. This solution provides continuous monitoring and instant toggle controls for your network security posture.

## Key Features

### 1. Real-Time Monitoring
- Continuous surveillance of network security status
- Automatic detection of configuration changes
- Instant alerts for security events
- Risk scoring based on current configuration

### 2. Toggle Controls
- **Windows Firewall**: Enable/disable firewall protection
- **ExpressVPN**: Control VPN connection state
- **SMB Service**: Toggle Server Message Block (port 445)
- **NetBIOS Service**: Toggle NetBIOS (port 139)
- **Windows Defender**: Control real-time protection
- **Connection Logging**: Enable/disable firewall logging

### 3. Automated Security Checks
- Monitor for dangerous open ports
- Track security feature states
- Generate risk assessments
- Log all security events

## Installation

1. Save `network_security_monitor.py` to your system
2. Ensure Python 3.6+ is installed
3. Run the monitor with: `python network_security_monitor.py`

## Usage

### Interactive Mode Commands:
- `status` - Show current security status and risk score
- `report` - Generate comprehensive security report
- `toggle <feature> <on|off>` - Control security features
- `list` - List all security features and states
- `start` - Begin continuous monitoring
- `stop` - Stop monitoring
- `exit` - Quit the monitor

### Example Usage:
```
toggle smb_service off    # Disable SMB service
toggle firewall on        # Enable firewall
report                   # Generate security report
```

## Security Risk Scoring

The system calculates an overall risk score (0-100, lower is better):
- **0-20**: Excellent security posture
- **21-40**: Good security posture
- **41-60**: Moderate security posture
- **61-80**: Weak security posture
- **81-100**: Critical security posture

### Risk Factors:
- Disabled firewall: +25 points
- Disabled antivirus: +20 points
- SMB service enabled: +15 points
- NetBIOS service enabled: +15 points
- VPN disconnected: +10 points
- Logging disabled: +5 points

## Configuration

The system maintains configuration in `security_config.json` with settings for:
- Feature states
- Monitoring intervals
- Alert settings
- Log retention policies

## Automated Operation

The monitoring system can be run as a background service to:
- Continuously check security states
- Alert on configuration changes
- Maintain security posture
- Generate periodic reports

## Security Best Practices

1. **Keep high-priority features enabled** (firewall, antivirus)
2. **Disable unnecessary services** (SMB, NetBIOS) unless specifically needed
3. **Maintain VPN connection** for privacy
4. **Enable logging** for forensic analysis
5. **Regularly review** the generated reports
6. **Monitor risk scores** and take corrective action when needed

## Emergency Response

In case of security incidents:
1. Run `report` to assess current status
2. Use `toggle` commands to quickly enable security features
3. Review alerts in the log for incident details
4. Take appropriate remediation steps

## Integration with Existing Systems

This monitoring solution works alongside:
- Existing antivirus software (McAfee, Windows Defender)
- VPN clients (ExpressVPN)
- Network infrastructure
- Windows security features

The system is designed to complement rather than replace existing security tools.
#!/usr/bin/env python3
"""
Network Security Monitoring Solution with Toggle Controls
Provides real-time monitoring and control of security features
"""

import time
import subprocess
import json
import threading
import socket
from datetime import datetime
import os
from dataclasses import dataclass
from typing import Dict, List, Callable, Optional


@dataclass
class SecurityToggle:
    """Represents a configurable security feature with toggle control"""
    name: str
    description: str
    current_state: bool
    toggle_function: Callable
    check_function: Callable
    priority: int = 1  # 1=high, 2=medium, 3=low importance


class NetworkSecurityMonitor:
    """Main security monitoring class with toggle controls"""
    
    def __init__(self):
        self.security_toggles: Dict[str, SecurityToggle] = {}
        self.monitoring_active = False
        self.alerts_log = []
        self.config_file = "security_config.json"
        self.load_configuration()
        self.setup_security_toggles()
        
    def setup_security_toggles(self):
        """Initialize all security toggles with their control functions"""
        
        # Firewall toggle
        self.security_toggles['firewall'] = SecurityToggle(
            name="Windows Firewall",
            description="Controls Windows Firewall state (all profiles)",
            current_state=self.is_firewall_enabled(),
            toggle_function=self.toggle_firewall,
            check_function=self.is_firewall_enabled,
            priority=1
        )
        
        # VPN toggle
        self.security_toggles['vpn'] = SecurityToggle(
            name="ExpressVPN",
            description="Controls VPN connection state",
            current_state=self.is_vpn_connected(),
            toggle_function=self.toggle_vpn,
            check_function=self.is_vpn_connected,
            priority=1
        )
        
        # SMB toggle (port 445)
        self.security_toggles['smb'] = SecurityToggle(
            name="SMB Service",
            description="Controls Server Message Block (SMB) service on port 445",
            current_state=self.is_port_open(445),
            toggle_function=self.toggle_smb_service,
            check_function=lambda: self.is_port_open(445),
            priority=1
        )
        
        # NetBIOS toggle (port 139)
        self.security_toggles['netbios'] = SecurityToggle(
            name="NetBIOS Service",
            description="Controls NetBIOS service on port 139",
            current_state=self.is_port_open(139),
            toggle_function=self.toggle_netbios_service,
            check_function=lambda: self.is_port_open(139),
            priority=1
        )
        
        # Antivirus toggle (Windows Defender)
        self.security_toggles['windows_defender'] = SecurityToggle(
            name="Windows Defender",
            description="Controls Windows Defender real-time protection",
            current_state=self.is_windows_defender_active(),
            toggle_function=self.toggle_windows_defender,
            check_function=self.is_windows_defender_active,
            priority=1
        )
        
        # Logging toggle
        self.security_toggles['logging'] = SecurityToggle(
            name="Connection Logging",
            description="Controls logging of dropped connections in firewall",
            current_state=self.is_logging_enabled(),
            toggle_function=self.toggle_logging,
            check_function=self.is_logging_enabled,
            priority=2
        )
        
    def load_configuration(self):
        """Load saved security configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Apply saved states if needed
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def save_configuration(self):
        """Save current security configuration"""
        config = {}
        for name, toggle in self.security_toggles.items():
            config[name] = {
                'state': toggle.current_state,
                'timestamp': datetime.now().isoformat()
            }
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    # Toggle Functions
    def toggle_firewall(self, enable: bool):
        """Toggle Windows Firewall on/off"""
        try:
            cmd = f"netsh advfirewall set allprofiles state {'on' if enable else 'off'}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.security_toggles['firewall'].current_state = enable
                self.log_alert(f"Firewall {'enabled' if enable else 'disabled'}")
                return True
            else:
                self.log_alert(f"Failed to toggle firewall: {result.stderr}")
                return False
        except Exception as e:
            self.log_alert(f"Error toggling firewall: {e}")
            return False
    
    def toggle_vpn(self, enable: bool):
        """Toggle VPN connection"""
        # This is a placeholder - actual VPN control would depend on specific VPN client
        try:
            if enable:
                # Attempt to connect VPN (would need specific VPN client commands)
                self.log_alert("VPN connection attempt initiated")
            else:
                # Attempt to disconnect VPN
                self.log_alert("VPN disconnection attempt initiated")
            self.security_toggles['vpn'].current_state = enable
            return True
        except Exception as e:
            self.log_alert(f"Error toggling VPN: {e}")
            return False
    
    def toggle_smb_service(self, enable: bool):
        """Toggle SMB service"""
        try:
            cmd = f"sc config lanmanserver start= {'auto' if enable else 'disabled'}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                # Also restart the service to apply changes
                restart_cmd = f"sc {'start' if enable else 'stop'} lanmanserver"
                subprocess.run(restart_cmd, shell=True, capture_output=True, text=True)
                self.security_toggles['smb'].current_state = enable
                self.log_alert(f"SMB service {'enabled' if enable else 'disabled'}")
                return True
            else:
                self.log_alert(f"Failed to toggle SMB: {result.stderr}")
                return False
        except Exception as e:
            self.log_alert(f"Error toggling SMB: {e}")
            return False
    
    def toggle_netbios_service(self, enable: bool):
        """Toggle NetBIOS service"""
        try:
            # Disable NetBIOS through registry (more complex than simple service control)
            # This is a simplified version - actual implementation would involve registry changes
            if enable:
                self.log_alert("Enabling NetBIOS service")
            else:
                self.log_alert("Disabling NetBIOS service (may require registry changes)")
            self.security_toggles['netbios'].current_state = enable
            return True
        except Exception as e:
            self.log_alert(f"Error toggling NetBIOS: {e}")
            return False
    
    def toggle_windows_defender(self, enable: bool):
        """Toggle Windows Defender"""
        try:
            if enable:
                # Re-enable Windows Defender features
                cmd = 'powershell "Set-MpPreference -DisableRealtimeMonitoring $false"'
            else:
                # Disable Windows Defender real-time monitoring
                cmd = 'powershell "Set-MpPreference -DisableRealtimeMonitoring $true"'
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.security_toggles['windows_defender'].current_state = enable
                self.log_alert(f"Windows Defender {'enabled' if enable else 'disabled'}")
                return True
            else:
                self.log_alert(f"Failed to toggle Windows Defender: {result.stderr}")
                return False
        except Exception as e:
            self.log_alert(f"Error toggling Windows Defender: {e}")
            return False
    
    def toggle_logging(self, enable: bool):
        """Toggle firewall logging"""
        try:
            cmd = f'netsh advfirewall set currentprofile logging {{"droppedpackets" if enable else "disabled"}}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.security_toggles['logging'].current_state = enable
                self.log_alert(f"Connection logging {'enabled' if enable else 'disabled'}")
                return True
            else:
                self.log_alert(f"Failed to toggle logging: {result.stderr}")
                return False
        except Exception as e:
            self.log_alert(f"Error toggling logging: {e}")
            return False
    
    # Check Functions
    def is_firewall_enabled(self) -> bool:
        """Check if firewall is enabled"""
        try:
            result = subprocess.run('netsh advfirewall show allprofiles', 
                                  shell=True, capture_output=True, text=True)
            return 'ON' in result.stdout
        except Exception:
            return False
    
    def is_vpn_connected(self) -> bool:
        """Check if VPN is connected"""
        try:
            result = subprocess.run('ipconfig', shell=True, capture_output=True, text=True)
            # Look for VPN adapter in use
            return 'tunnel' in result.stdout.lower() or 'vpn' in result.stdout.lower()
        except Exception:
            return False
    
    def is_port_open(self, port: int) -> bool:
        """Check if a specific port is listening"""
        try:
            result = subprocess.run(f'netstat -an | findstr LISTEN | findstr :{port}', 
                                  shell=True, capture_output=True, text=True)
            return len(result.stdout.strip()) > 0
        except Exception:
            return False
    
    def is_windows_defender_active(self) -> bool:
        """Check if Windows Defender is active"""
        try:
            result = subprocess.run('powershell "Get-MpPreference"', 
                                  shell=True, capture_output=True, text=True)
            return 'False' not in result.stdout.split('DisableRealtimeMonitoring')[1][:20]
        except Exception:
            return False
    
    def is_logging_enabled(self) -> bool:
        """Check if firewall logging is enabled"""
        try:
            result = subprocess.run('netsh advfirewall show allprofiles', 
                                  shell=True, capture_output=True, text=True)
            return 'LogDroppedConnections' in result.stdout and 'Enable' in result.stdout
        except Exception:
            return False
    
    def log_alert(self, message: str):
        """Log security alerts"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert = {
            'timestamp': timestamp,
            'message': message,
            'severity': 'HIGH' if 'failed' in message.lower() else 'INFO'
        }
        self.alerts_log.append(alert)
        print(f"[{alert['severity']}] {timestamp}: {message}")
    
    def get_security_status(self) -> Dict:
        """Get current security status"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'toggles': {},
            'alerts_count': len(self.alerts_log[-10:]),  # Last 10 alerts
            'overall_risk_score': self.calculate_risk_score()
        }
        
        for name, toggle in self.security_toggles.items():
            status['toggles'][name] = {
                'enabled': toggle.current_state,
                'description': toggle.description,
                'priority': toggle.priority
            }
        
        return status
    
    def calculate_risk_score(self) -> int:
        """Calculate overall risk score (0-100, lower is better)"""
        score = 0
        
        # Risk factors
        if not self.security_toggles['firewall'].current_state:
            score += 25  # Major risk
        if not self.security_toggles['windows_defender'].current_state:
            score += 20  # Major risk
        if self.security_toggles['smb'].current_state:
            score += 15  # Medium risk
        if self.security_toggles['netbios'].current_state:
            score += 15  # Medium risk
        if not self.security_toggles['vpn'].current_state:
            score += 10  # Medium risk
        if not self.security_toggles['logging'].current_state:
            score += 5   # Low risk
        
        return min(score, 100)  # Cap at 100
    
    def monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            # Check all toggle states
            for name, toggle in self.security_toggles.items():
                current_state = toggle.check_function()
                if current_state != toggle.current_state:
                    self.log_alert(f"{name} state changed: {toggle.current_state} -> {current_state}")
                    toggle.current_state = current_state
            
            # Additional security checks
            self.perform_security_checks()
            
            time.sleep(30)  # Check every 30 seconds
    
    def perform_security_checks(self):
        """Perform additional security checks"""
        # Check for unauthorized listening ports
        try:
            result = subprocess.run('netstat -an | findstr LISTEN', 
                                  shell=True, capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            listening_ports = []
            
            for line in lines:
                if 'LISTEN' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        port_info = parts[1]  # Local Address:Port
                        if ':' in port_info:
                            port = port_info.split(':')[-1]
                            if port.isdigit():
                                listening_ports.append(int(port))
            
            # Alert on potentially dangerous ports
            dangerous_ports = [21, 23, 135, 139, 445, 1433, 3306, 3389, 5985, 5986]  # Common attack vectors
            dangerous_open = [p for p in listening_ports if p in dangerous_ports and p not in [135, 49664, 49665, 49666, 49669, 49670, 49680]]  # Exclude Windows RPC ports
            
            if dangerous_open:
                self.log_alert(f"Dangerous ports open: {dangerous_open}")
                
        except Exception as e:
            self.log_alert(f"Error checking listening ports: {e}")
    
    def start_monitoring(self):
        """Start the monitoring service"""
        self.monitoring_active = True
        self.log_alert("Network Security Monitor started")
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        monitor_thread.start()
        
        return True
    
    def stop_monitoring(self):
        """Stop the monitoring service"""
        self.monitoring_active = False
        self.log_alert("Network Security Monitor stopped")
        return True
    
    def toggle_feature(self, feature_name: str, enable: bool) -> bool:
        """Toggle a specific security feature"""
        if feature_name in self.security_toggles:
            toggle = self.security_toggles[feature_name]
            success = toggle.toggle_function(enable)
            if success:
                toggle.current_state = enable
                self.save_configuration()
                self.log_alert(f"{feature_name} {'enabled' if enable else 'disabled'} successfully")
            return success
        else:
            self.log_alert(f"Feature '{feature_name}' not found")
            return False
    
    def generate_report(self) -> str:
        """Generate a security report"""
        status = self.get_security_status()
        report_lines = [
            "=== NETWORK SECURITY REPORT ===",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Overall Risk Score: {status['overall_risk_score']}/100",
            "",
            "Security Features:",
        ]
        
        # Sort by priority
        sorted_toggles = sorted(status['toggles'].items(), key=lambda x: x[1]['priority'])
        
        for name, config in sorted_toggles:
            state = "ENABLED" if config['enabled'] else "DISABLED"
            priority_map = {1: "HIGH", 2: "MED", 3: "LOW"}
            priority = priority_map.get(config['priority'], "N/A")
            report_lines.append(f"  [{priority}] {name}: {state}")
        
        report_lines.extend([
            "",
            f"Recent Alerts: {status['alerts_count']} (last 10)",
            "==============================="
        ])
        
        return "\n".join(report_lines)


def main():
    """Main function to run the security monitor"""
    print("Initializing Network Security Monitor...")
    
    monitor = NetworkSecurityMonitor()
    
    print("\nNetwork Security Monitor initialized!")
    print("Available commands:")
    print("  status - Show current security status")
    print("  report - Generate security report")
    print("  toggle <feature> <on|off> - Toggle a security feature")
    print("  start - Start monitoring")
    print("  stop - Stop monitoring")
    print("  list - List all security features")
    print("  exit - Exit the monitor")
    print("")
    
    # Show initial status
    print(monitor.generate_report())
    
    # Start monitoring
    monitor.start_monitoring()
    
    try:
        while True:
            command = input("\nEnter command: ").strip().lower()
            
            if command == 'exit':
                monitor.stop_monitoring()
                break
            elif command == 'status':
                status = monitor.get_security_status()
                print(f"\nRisk Score: {status['overall_risk_score']}/100")
                print("Features:")
                for name, config in status['toggles'].items():
                    state = "ENABLED" if config['enabled'] else "DISABLED"
                    print(f"  {name}: {state}")
            elif command == 'report':
                print(f"\n{monitor.generate_report()}")
            elif command.startswith('toggle '):
                parts = command.split()
                if len(parts) >= 3:
                    feature = parts[1]
                    state = parts[2].lower() in ['on', 'enable', 'true', '1']
                    success = monitor.toggle_feature(feature, state)
                    if success:
                        print(f"Successfully toggled {feature}")
                    else:
                        print(f"Failed to toggle {feature}")
                else:
                    print("Usage: toggle <feature> <on|off>")
            elif command == 'start':
                monitor.start_monitoring()
                print("Monitoring started")
            elif command == 'stop':
                monitor.stop_monitoring()
                print("Monitoring stopped")
            elif command == 'list':
                print("\nAvailable security features:")
                for name, toggle in monitor.security_toggles.items():
                    state = "ENABLED" if toggle.current_state else "DISABLED"
                    print(f"  {name}: {state} - {toggle.description}")
            else:
                print("Unknown command. Available commands: status, report, toggle, start, stop, list, exit")
    
    except KeyboardInterrupt:
        print("\nShutting down monitor...")
        monitor.stop_monitoring()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
OpenClaw Activity Monitor
Monitors the OpenClaw system and generates real-time activity data for the dashboard
"""

import json
import time
import os
import threading
from datetime import datetime, timedelta
from pathlib import Path


class OpenClawActivityMonitor:
    def __init__(self, workspace_dir=None):
        if workspace_dir is None:
            self.workspace_dir = Path(__file__).parent.parent
        else:
            self.workspace_dir = Path(workspace_dir)
        
        self.memory_dir = self.workspace_dir / "memory"
        self.logs_dir = self.workspace_dir / "logs"
        self.activities_file = self.workspace_dir / "activities.json"
        
        # Ensure directories exist
        self.memory_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        
        self.running = False
        self.monitor_thread = None
        self.activities = []
        
        # Load existing activities
        self.load_activities()

    def load_activities(self):
        """Load existing activities from the activities file"""
        try:
            if self.activities_file.exists():
                with open(self.activities_file, 'r') as f:
                    data = json.load(f)
                    self.activities = data.get('activities', [])
            else:
                # Create initial activities file
                self.save_activities()
        except Exception as e:
            print(f"Error loading activities: {e}")
            self.activities = []

    def save_activities(self):
        """Save activities to the activities file"""
        try:
            data = {
                'last_updated': datetime.now().isoformat(),
                'activities': self.activities[-50:]  # Keep only last 50 activities
            }
            with open(self.activities_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving activities: {e}")

    def add_activity(self, title, description, activity_type="general"):
        """Add a new activity to the list"""
        activity = {
            'title': title,
            'description': description,
            'type': activity_type,
            'timestamp': datetime.now().isoformat(),
            'time': datetime.now().isoformat()  # Compatibility with dashboard
        }
        
        self.activities.insert(0, activity)  # Insert at the beginning
        self.save_activities()
        
        # Keep only the last 50 activities
        if len(self.activities) > 50:
            self.activities = self.activities[:50]

    def monitor_memory_files(self):
        """Monitor memory files for changes"""
        memory_files = {}
        
        # Track modification times of memory files
        for mem_file in self.memory_dir.glob("*.md"):
            memory_files[str(mem_file)] = mem_file.stat().st_mtime
        
        while self.running:
            time.sleep(10)  # Check every 10 seconds
            
            for mem_file in self.memory_dir.glob("*.md"):
                file_path = str(mem_file)
                current_mtime = mem_file.stat().st_mtime
                
                if file_path not in memory_files:
                    # New file detected
                    self.add_activity(
                        f"Created {mem_file.name}",
                        f"New memory file created: {mem_file.name}",
                        "file_operation"
                    )
                    memory_files[file_path] = current_mtime
                elif memory_files[file_path] != current_mtime:
                    # File was modified
                    self.add_activity(
                        f"Updated {mem_file.name}",
                        f"Memory file updated: {mem_file.name}",
                        "file_operation"
                    )
                    memory_files[file_path] = current_mtime

    def monitor_workspace_changes(self):
        """Monitor workspace for file changes"""
        workspace_files = {}
        
        # Track modification times of workspace files
        for ws_file in self.workspace_dir.rglob("*"):
            if ws_file.is_file() and not str(ws_file).startswith(str(self.logs_dir)):
                workspace_files[str(ws_file)] = ws_file.stat().st_mtime
        
        while self.running:
            time.sleep(30)  # Check every 30 seconds
            
            for ws_file in self.workspace_dir.rglob("*"):
                if ws_file.is_file() and not str(ws_file).startswith(str(self.logs_dir)):
                    file_path = str(ws_file)
                    current_mtime = ws_file.stat().st_mtime
                    
                    if file_path not in workspace_files:
                        # New file detected
                        rel_path = ws_file.relative_to(self.workspace_dir)
                        self.add_activity(
                            f"Created {rel_path}",
                            f"New file created in workspace: {rel_path}",
                            "file_operation"
                        )
                        workspace_files[file_path] = current_mtime
                    elif workspace_files[file_path] != current_mtime:
                        # File was modified
                        rel_path = ws_file.relative_to(self.workspace_dir)
                        self.add_activity(
                            f"Updated {rel_path}",
                            f"Workspace file updated: {rel_path}",
                            "file_operation"
                        )
                        workspace_files[file_path] = current_mtime

    def get_recent_activities(self, limit=10):
        """Get recent activities, limited by the specified number"""
        return self.activities[:limit]

    def start_monitoring(self):
        """Start monitoring the system in background threads"""
        if self.running:
            return
            
        self.running = True
        
        # Start memory file monitoring
        memory_thread = threading.Thread(target=self.monitor_memory_files, daemon=True)
        memory_thread.start()
        
        # Start workspace file monitoring
        workspace_thread = threading.Thread(target=self.monitor_workspace_changes, daemon=True)
        workspace_thread.start()
        
        print("OpenClaw Activity Monitor started")

    def stop_monitoring(self):
        """Stop monitoring the system"""
        self.running = False
        print("OpenClaw Activity Monitor stopped")


# Global monitor instance
monitor = OpenClawActivityMonitor()


def initialize_monitor():
    """Initialize the monitor when this module is imported or run"""
    global monitor
    if not monitor.running:
        monitor.start_monitoring()


def get_dashboard_data():
    """Function to get dashboard data compatible with the PHP API"""
    recent_activities = monitor.get_recent_activities(limit=10)
    
    # Add some system-level activities if none exist
    if not recent_activities:
        recent_activities = [
            {
                'title': 'System Initialized',
                'description': 'OpenClaw dashboard monitoring system initialized',
                'type': 'system',
                'timestamp': datetime.now().isoformat(),
                'time': datetime.now().isoformat()
            }
        ]
    
    data = {
        'timestamp': datetime.now().isoformat(),
        'systemStatus': {
            'status': 'operational',
            'version': '2026.1.29',
            'uptime': 'N/A',
            'timestamp': datetime.now().isoformat()
        },
        'sessionData': {
            'sessionId': 'agent:main:main',
            'model': 'qwen-portal/coder-model',
            'contextUsage': 'N/A',
            'runtime': 'Direct',
            'thinking': 'N/A',
            'activeSessions': 1
        },
        'tokenUsage': {
            'total': 0,
            'in': 0,
            'out': 0,
            'progress': 0
        },
        'systemHealth': {
            'gateway': 'running' if check_gateway_status() else 'stopped',
            'agents': 'checking',
            'tools': 'available',
            'memory': 'N/A',
            'cpu': 'N/A',
            'storage': 'N/A'
        },
        'recentActivities': recent_activities,
        'systemMetrics': {
            'totalRequests': len(recent_activities),
            'avgResponseTime': 'N/A',
            'memoryUsage': 'N/A',
            'cpuUsage': 'N/A',
            'activeConnections': 1
        },
        'success': True
    }
    
    return data


def check_gateway_status():
    """Check if the OpenClaw gateway is running"""
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 18789))
        sock.close()
        return result == 0
    except:
        return False


if __name__ == "__main__":
    # If run directly, start monitoring and print status
    print("Starting OpenClaw Activity Monitor...")
    initialize_monitor()
    
    try:
        while True:
            time.sleep(60)  # Keep alive
    except KeyboardInterrupt:
        print("\nStopping monitor...")
        monitor.stop_monitoring()
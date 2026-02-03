#!/usr/bin/env python3
"""
System Monitor for OpenClaw
Provides system monitoring capabilities with appropriate security measures
"""

import psutil
import platform
from datetime import datetime, timedelta
from typing import Dict, Any, List
import time

def get_system_info() -> Dict[str, Any]:
    """
    Gets general system information
    """
    info = {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "hostname": platform.node(),
        "processor": platform.processor(),
        "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
    }
    return info

def get_cpu_info() -> Dict[str, Any]:
    """
    Gets CPU-related information
    """
    cpu_freq = psutil.cpu_freq()
    
    info = {
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "max_frequency_ghz": round(cpu_freq.max / 1000, 2) if cpu_freq else 0,
        "min_frequency_ghz": round(cpu_freq.min / 1000, 2) if cpu_freq else 0,
        "current_frequency_ghz": round(cpu_freq.current / 1000, 2) if cpu_freq else 0,
        "cpu_usage_percent": psutil.cpu_percent(interval=1),
        "per_core_usage": psutil.cpu_percent(interval=1, percpu=True)
    }
    return info

def get_memory_info() -> Dict[str, Any]:
    """
    Gets memory-related information
    """
    virtual_memory = psutil.virtual_memory()
    swap_memory = psutil.swap_memory()
    
    info = {
        "virtual_memory": {
            "total_gb": round(virtual_memory.total / (1024**3), 2),
            "available_gb": round(virtual_memory.available / (1024**3), 2),
            "used_gb": round(virtual_memory.used / (1024**3), 2),
            "percentage_used": virtual_memory.percent
        },
        "swap_memory": {
            "total_gb": round(swap_memory.total / (1024**3), 2),
            "free_gb": round(swap_memory.free / (1024**3), 2),
            "used_gb": round(swap_memory.used / (1024**3), 2),
            "percentage_used": swap_memory.percent
        }
    }
    return info

def get_disk_info() -> List[Dict[str, Any]]:
    """
    Gets disk partition information
    """
    partitions = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            partition_info = {
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "file_system_type": partition.fstype,
                "total_gb": round(usage.total / (1024**3), 2),
                "used_gb": round(usage.used / (1024**3), 2),
                "free_gb": round(usage.free / (1024**3), 2),
                "percentage_used": round((usage.used / usage.total) * 100, 2)
            }
            partitions.append(partition_info)
        except PermissionError:
            # This can happen on Windows for certain drives
            continue
    
    return partitions

def get_network_info() -> Dict[str, Any]:
    """
    Gets network-related information
    """
    net_io = psutil.net_io_counters()
    
    info = {
        "bytes_sent": net_io.bytes_sent,
        "bytes_recv": net_io.bytes_recv,
        "packets_sent": net_io.packets_sent,
        "packets_recv": net_io.packets_recv,
        "errin": net_io.errin,
        "errout": net_io.errout,
        "dropin": net_io.dropin,
        "dropout": net_io.dropout
    }
    return info

def get_running_processes(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Gets information about running processes (limited for security)
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent']):
        try:
            # Get process info, but limit sensitive data
            process_info = proc.info
            process_info['status'] = proc.status()
            
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Skip processes we can't access
            continue
    
    # Sort by memory usage and return top N
    processes.sort(key=lambda x: x.get('memory_percent', 0) or 0, reverse=True)
    return processes[:limit]

def get_system_health_summary() -> Dict[str, Any]:
    """
    Gets a summary of system health metrics
    """
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/').percent if '/' in [p.mountpoint for p in psutil.disk_partitions()] else psutil.disk_usage('C:\\').percent
    
    # Determine health status based on thresholds
    health_status = "OK"
    if cpu_percent > 90 or memory.percent > 90 or disk_usage > 90:
        health_status = "WARNING"
    if cpu_percent > 95 or memory.percent > 95 or disk_usage > 95:
        health_status = "CRITICAL"
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "disk_percent": disk_usage,
        "health_status": health_status,
        "active_processes": len(psutil.pids())
    }
    
    return summary

def monitor_system(duration: int = 60, interval: int = 5) -> List[Dict[str, Any]]:
    """
    Monitors system metrics over time
    """
    measurements = []
    end_time = time.time() + duration
    
    while time.time() < end_time:
        measurement = {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent if '/' in [p.mountpoint for p in psutil.disk_partitions()] else psutil.disk_usage('C:\\').percent
        }
        measurements.append(measurement)
        time.sleep(interval)
    
    return measurements

def get_battery_info() -> Dict[str, Any]:
    """
    Gets battery information if available
    """
    try:
        battery = psutil.sensors_battery()
        if battery:
            return {
                "percent": battery.percent,
                "power_plugged": battery.power_plugged,
                "secs_left": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited",
                "hours_left": round(battery.secsleft / 3600, 2) if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited"
            }
        else:
            return {"status": "No battery detected (desktop?)", "percent": None}
    except AttributeError:
        # Some systems might not have battery sensors
        return {"status": "Battery info not available on this system", "percent": None}

def main():
    """
    Example usage of the system monitor
    """
    print("System Monitor for OpenClaw")
    print("Provides system monitoring capabilities with security considerations\n")
    
    try:
        print("=== System Information ===")
        sys_info = get_system_info()
        for key, value in sys_info.items():
            print(f"{key}: {value}")
        
        print("\n=== CPU Information ===")
        cpu_info = get_cpu_info()
        for key, value in cpu_info.items():
            print(f"{key}: {value}")
        
        print("\n=== Memory Information ===")
        mem_info = get_memory_info()
        for key, value in mem_info.items():
            if isinstance(value, dict):
                print(f"{key}:")
                for k, v in value.items():
                    print(f"  {k}: {v}")
            else:
                print(f"{key}: {value}")
        
        print("\n=== Disk Information ===")
        disk_info = get_disk_info()
        for disk in disk_info:
            print(f"Device: {disk['device']}")
            print(f"  Mountpoint: {disk['mountpoint']}")
            print(f"  File System: {disk['file_system_type']}")
            print(f"  Total: {disk['total_gb']} GB")
            print(f"  Used: {disk['used_gb']} GB ({disk['percentage_used']}%)")
            print(f"  Free: {disk['free_gb']} GB\n")
        
        print("=== System Health Summary ===")
        health = get_system_health_summary()
        for key, value in health.items():
            print(f"{key}: {value}")
        
        print("\n=== Battery Information ===")
        battery_info = get_battery_info()
        for key, value in battery_info.items():
            print(f"{key}: {value}")
        
    except Exception as e:
        print(f"Error retrieving system information: {str(e)}")

if __name__ == "__main__":
    main()
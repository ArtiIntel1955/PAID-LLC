<?php
/**
 * Enhanced OpenClaw Dashboard API Endpoint
 * Provides real-time data for the enhanced dashboard with actual system monitoring
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header('Access-Control-Allow-Headers: Content-Type');

// Function to get actual OpenClaw gateway status
function getOpenClawGatewayStatus() {
    $gateway_port = $_ENV['OPENCLAW_GATEWAY_PORT'] ?? 18789;
    $gateway_host = '127.0.0.1';
    
    // Try to connect to the OpenClaw gateway
    $socket = @fsockopen($gateway_host, $gateway_port, $errno, $errstr, 1);
    if ($socket) {
        fclose($socket);
        return [
            'status' => 'running',
            'port' => $gateway_port,
            'host' => $gateway_host,
            'response_time' => getGatewayResponseTime($gateway_host, $gateway_port)
        ];
    } else {
        return [
            'status' => 'stopped',
            'port' => $gateway_port,
            'host' => $gateway_host,
            'response_time' => null
        ];
    }
}

// Function to measure gateway response time
function getGatewayResponseTime($host, $port) {
    $start = microtime(true);
    $socket = @fsockopen($host, $port, $errno, $errstr, 1);
    if ($socket) {
        fclose($socket);
        return round((microtime(true) - $start) * 1000, 2); // Return milliseconds
    }
    return null;
}

// Function to get recent activities from OpenClaw logs and workspace
function getRecentActivitiesFromSystem() {
    $activities = [];
    
    // 1. Try to get activities from the Python monitor file
    $activities_file = __DIR__ . '/../../activities.json';
    if (file_exists($activities_file)) {
        $json_data = file_get_contents($activities_file);
        $data = json_decode($json_data, true);
        
        if ($data && isset($data['activities'])) {
            return array_slice($data['activities'], 0, 10);
        }
    }
    
    // 2. Check for recent memory files in the workspace
    $memoryDir = __DIR__ . '/../../memory/';
    $today = date('Y-m-d');
    $yesterday = date('Y-m-d', strtotime('-1 day'));
    
    // Check today's and yesterday's memory files
    foreach ([$today, $yesterday] as $date) {
        $memoryFile = $memoryDir . $date . '.md';
        if (file_exists($memoryFile)) {
            $content = file_get_contents($memoryFile);
            
            // Extract recent activities based on common patterns
            $lines = explode("\n", $content);
            foreach ($lines as $line) {
                $line = trim($line);
                if (!empty($line) && strlen($line) > 20) { // Only meaningful entries
                    
                    // Skip if it's just a heading or very general text
                    if (preg_match('/^(#|\*|-|[0-9]+\.)\s*/', $line)) {
                        continue;
                    }
                    
                    // Add to activities if it looks like a real activity
                    if (strpos($line, 'system:') === false && 
                        strpos($line, 'user:') === false && 
                        strpos($line, 'assistant:') === false) {
                        
                        $activities[] = [
                            'title' => substr($line, 0, 60) . (strlen($line) > 60 ? '...' : ''),
                            'time' => date('c', time() - (count($activities) * 300)), // Stagger times
                            'description' => $line,
                            'type' => 'memory_update'
                        ];
                    }
                }
            }
        }
    }
    
    // 3. Check for recently modified files in workspace
    $workspaceDir = __DIR__ . '/../../';
    $files = glob($workspaceDir . '*');
    
    foreach ($files as $file) {
        if (is_file($file)) {
            $mtime = filemtime($file);
            if ($mtime > strtotime('-2 hours')) { // Modified in last 2 hours
                $basename = basename($file);
                $activities[] = [
                    'title' => "Updated $basename",
                    'time' => date('c', $mtime),
                    'description' => "File modified: $basename",
                    'type' => 'file_operation'
                ];
            }
        }
    }
    
    // Sort by time (most recent first) and limit to 10
    usort($activities, function($a, $b) {
        return strtotime($b['time']) - strtotime($a['time']);
    });
    
    return array_slice($activities, 0, 10);
}

// Function to get actual system status from OpenClaw
function getSystemStatus() {
    $gateway_status = getOpenClawGatewayStatus();
    
    return [
        'status' => $gateway_status['status'],
        'version' => '2026.1.29',
        'uptime' => 'N/A', // Would require more complex logic to determine
        'gateway_info' => $gateway_status,
        'timestamp' => date('c')
    ];
}

function getSessionData() {
    // In a real implementation, this would fetch from OpenClaw's session system
    return [
        'sessionId' => 'agent:main:main',
        'model' => 'qwen-portal/coder-model',
        'contextUsage' => 'N/A', // Would require OpenClaw API access
        'runtime' => 'Direct',
        'thinking' => 'N/A', // Would require OpenClaw API access
        'activeSessions' => 1 // Assuming at least main session is active
    ];
}

function getTokenUsage() {
    // Placeholder - would connect to OpenClaw's token tracking system in a full implementation
    return [
        'total' => 0, // Would be retrieved from actual token usage
        'in' => 0,
        'out' => 0,
        'progress' => 0
    ];
}

function getSystemHealth() {
    $gateway_status = getOpenClawGatewayStatus();
    
    // Basic system health check
    $memory_usage = round((memory_get_usage(true) / 1024 / 1024), 2) . 'MB';
    $disk_free = round(disk_free_space('/') / (1024 * 1024 * 1024), 2) . 'GB';
    
    return [
        'gateway' => $gateway_status['status'],
        'agents' => 'checking', // Would require OpenClaw API access
        'tools' => 'available',
        'memory' => $memory_usage,
        'cpu' => 'N/A', // Would require system command execution
        'storage' => $disk_free . ' free',
        'response_time_ms' => $gateway_status['response_time']
    ];
}

function getSystemMetrics() {
    // Placeholder for system metrics
    return [
        'totalRequests' => 0, // Would track actual requests
        'avgResponseTime' => 'N/A',
        'memoryUsage' => round((memory_get_usage(true) / memory_get_peak_usage(true)) * 100, 2) . '%',
        'cpuUsage' => 'N/A',
        'activeConnections' => 1, // At least the dashboard connection
        'timestamp' => date('c')
    ];
}

// Main API response
try {
    $response = [
        'timestamp' => date('c'),
        'systemStatus' => getSystemStatus(),
        'sessionData' => getSessionData(),
        'tokenUsage' => getTokenUsage(),
        'systemHealth' => getSystemHealth(),
        'recentActivities' => getRecentActivitiesFromSystem(),
        'systemMetrics' => getSystemMetrics(),
        'success' => true
    ];
} catch (Exception $e) {
    $response = [
        'timestamp' => date('c'),
        'error' => $e->getMessage(),
        'success' => false
    ];
}

echo json_encode($response, JSON_PRETTY_PRINT);
?>
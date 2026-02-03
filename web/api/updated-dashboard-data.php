<?php
/**
 * OpenClaw Dashboard API Endpoint
 * Provides real-time data for the enhanced dashboard
 * Updated to pull actual data from OpenClaw system
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header('Access-Control-Allow-Headers: Content-Type');

// Function to get recent activities from OpenClaw logs
function getRecentActivitiesFromLogs() {
    $activities = [];
    
    // Look for recent memory files in the workspace
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
                            'description' => $line
                        ];
                    }
                }
            }
        }
    }
    
    // Add some recent system events if workspace files were modified recently
    $workspaceDir = __DIR__ . '/../../';
    $recentFiles = glob($workspaceDir . '*.{php,py,js,md,json}', GLOB_BRACE);
    
    foreach ($recentFiles as $file) {
        $mtime = filemtime($file);
        if ($mtime > strtotime('-24 hours')) { // Modified in last 24 hours
            $basename = basename($file);
            $activities[] = [
                'title' => "Updated $basename",
                'time' => date('c', $mtime),
                'description' => "Modified file: $basename in workspace"
            ];
        }
    }
    
    // Sort by time (most recent first) and limit to 10
    usort($activities, function($a, $b) {
        return strtotime($b['time']) - strtotime($a['time']);
    });
    
    return array_slice($activities, 0, 10);
}

// Function to get system status from OpenClaw
function getSystemStatus() {
    // Check if OpenClaw gateway is running by attempting to connect
    $status = 'operational'; // Default assumption
    $version = '2026.1.29'; // Default version
    
    // Try to determine actual status by checking if gateway is responding
    $gateway_port = $_ENV['OPENCLAW_GATEWAY_PORT'] ?? 18789;
    $gateway_host = '127.0.0.1';
    
    // Attempt to connect to gateway to verify status
    $fp = @fsockopen($gateway_host, $gateway_port, $errno, $errstr, 2);
    if (!$fp) {
        $status = 'unreachable';
    } else {
        fclose($fp);
    }
    
    return [
        'status' => $status,
        'version' => $version,
        'uptime' => 'N/A', // Would require more complex logic to determine
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
    // Basic system health check
    $memory_usage = round((memory_get_usage(true) / 1024 / 1024), 2) . 'MB';
    $disk_free = round(disk_free_space('/') / (1024 * 1024 * 1024), 2) . 'GB';
    
    return [
        'gateway' => isGatewayRunning() ? 'running' : 'stopped',
        'agents' => 'checking', // Would require OpenClaw API access
        'tools' => 'available',
        'memory' => $memory_usage,
        'cpu' => 'N/A', // Would require system command execution
        'storage' => $disk_free . ' free'
    ];
}

function isGatewayRunning() {
    $gateway_port = $_ENV['OPENCLAW_GATEWAY_PORT'] ?? 18789;
    $gateway_host = '127.0.0.1';
    
    $fp = @fsockopen($gateway_host, $gateway_port, $errno, $errstr, 2);
    if ($fp) {
        fclose($fp);
        return true;
    }
    return false;
}

function getSystemMetrics() {
    // Placeholder for system metrics
    return [
        'totalRequests' => 0, // Would track actual requests
        'avgResponseTime' => 'N/A',
        'memoryUsage' => round((memory_get_usage(true) / memory_get_peak_usage(true)) * 100, 2) . '%',
        'cpuUsage' => 'N/A',
        'activeConnections' => 0
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
        'recentActivities' => getRecentActivitiesFromLogs(),
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
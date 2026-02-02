# PowerShell script to run the companion monitor and send it via OpenClaw's webhook or API

# Run the Python script and capture its output
$output = & "C:\Users\MyAIE\AppData\Local\Python\pythoncore-3.14-64\python.exe" "C:\Users\MyAIE\.openclaw\workspace\openclaw_companion_monitor_final.py"

# Parse the output to find the message
$lines = $output -split "`n"

if ($lines -contains "STATUS_UPDATE_READY") {
    $statusIndex = [array]::IndexOf($lines, "STATUS_UPDATE_READY")
    if ($statusIndex + 1 -lt $lines.Length) {
        $message = $lines[$statusIndex + 1]
        
        # Write the message to a temporary file that can be processed by OpenClaw
        $message | Out-File -FilePath "C:\Users\MyAIE\.openclaw\workspace\pending_telegram_message.txt" -Encoding UTF8
        
        # Also write a flag file to indicate that a message needs to be sent
        "STATUS" | Out-File -FilePath "C:\Users\MyAIE\.openclaw\workspace\message_type.txt" -Encoding UTF8
        
        Write-Host "Status update message saved to pending_telegram_message.txt"
    } else {
        Write-Host "No status message found after STATUS_UPDATE_READY marker"
    }
} else {
    Write-Host "STATUS_UPDATE_READY marker not found in output"
}

# Clean up variables
Remove-Variable output, lines, statusIndex, message -ErrorAction SilentlyContinue
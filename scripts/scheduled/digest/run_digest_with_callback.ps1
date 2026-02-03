# PowerShell script to run the digest and send it via OpenClaw's webhook or API

# Run the Python script and capture its output
$output = & "C:\Users\MyAIE\AppData\Local\Python\pythoncore-3.14-64\python.exe" "C:\Users\MyAIE\.openclaw\workspace\daily_news_digest_final.py"

# Parse the output to find the message
$lines = $output -split "`n"

if ($lines -contains "DIGEST_READY") {
    $digestIndex = [array]::IndexOf($lines, "DIGEST_READY")
    if ($digestIndex + 1 -lt $lines.Length) {
        $message = $lines[$digestIndex + 1]
        
        # Write the message to a temporary file that can be processed by OpenClaw
        $message | Out-File -FilePath "C:\Users\MyAIE\.openclaw\workspace\pending_telegram_message.txt" -Encoding UTF8
        
        # Also write a flag file to indicate that a message needs to be sent
        "DIGEST" | Out-File -FilePath "C:\Users\MyAIE\.openclaw\workspace\message_type.txt" -Encoding UTF8
        
        Write-Host "Digest message saved to pending_telegram_message.txt"
    } else {
        Write-Host "No digest message found after DIGEST_READY marker"
    }
} else {
    Write-Host "DIGEST_READY marker not found in output"
}

# Clean up variables
Remove-Variable output, lines, digestIndex, message -ErrorAction SilentlyContinue
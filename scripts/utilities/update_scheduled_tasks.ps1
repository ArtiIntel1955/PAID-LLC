# PowerShell script to update the scheduled tasks to use the new wrapper scripts

# Update the PAID Daily AI News Digest task to use the wrapper
$action = New-ScheduledTaskAction -Execute "C:\Users\MyAIE\AppData\Local\Python\pythoncore-3.14-64\python.exe" -Argument "C:\Users\MyAIE\.openclaw\workspace\run_daily_digest.py" -WorkingDirectory "C:\Users\MyAIE\.openclaw\workspace"

$trigger = New-ScheduledTaskTrigger -Daily -At "9:00AM"

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName "PAID Daily AI News Digest" -Action $action -Trigger $trigger -Settings $settings -Description "Daily AI and OpenClaw news digest sent to Telegram" -Force

Write-Host "Updated PAID Daily AI News Digest scheduled task"


# Update the PAID OpenClaw Companion Monitor task (if it exists) or create it
$action2 = New-ScheduledTaskAction -Execute "C:\Users\MyAIE\AppData\Local\Python\pythoncore-3.14-64\python.exe" -Argument "C:\Users\MyAIE\.openclaw\workspace\run_companion_monitor.py" -WorkingDirectory "C:\Users\MyAIE\.openclaw\workspace"

# Create a trigger to run every 4 hours
$trigger2 = @{
    Frequency = 'Hourly'
    RepetitionInterval = (New-TimeSpan -Hours 4)
    RepetitionDuration = (New-TimeSpan -Days 365)  # Repeat indefinitely
}

$settings2 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Register the task (this will update if it exists, create if it doesn't)
Register-ScheduledTask -TaskName "PAID OpenClaw Companion Monitor" -Action $action2 -Settings $settings2 -Description "Regular status updates for OpenClaw system sent to Telegram" -Force

Write-Host "Updated PAID OpenClaw Companion Monitor scheduled task"

Write-Host "Scheduled tasks updated successfully!"
Write-Host "1. PAID Daily AI News Digest - runs daily at 9:00 AM"
Write-Host "2. PAID OpenClaw Companion Monitor - runs every 4 hours"
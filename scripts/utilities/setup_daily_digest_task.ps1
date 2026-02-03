# PowerShell script to create the Daily AI & OpenClaw News Digest Task

# Define task properties
$TaskName = "PAID Daily AI News Digest"
$TaskDescription = "Daily digest of AI news and OpenClaw updates for PAID LLC"
$ActionExecutable = "C:\Users\MyAIE\AppData\Local\Microsoft\WindowsApps\python.exe"
$ActionArguments = "C:\Users\MyAIE\.openclaw\workspace\daily_news_digest.py"
$ActionWorkingDirectory = "C:\Users\MyAIE\.openclaw\workspace"
$TriggerTime = "09:00"  # 9:00 AM daily

# Check if the script exists
if (-not (Test-Path $ActionArguments)) {
    Write-Host "Script not found at: $ActionArguments" -ForegroundColor Red
    exit 1
}

# Create the scheduled task action
$Action = New-ScheduledTaskAction -Execute $ActionExecutable -Argument $ActionArguments -WorkingDirectory $ActionWorkingDirectory

# Create the scheduled task trigger (daily at 9:00 AM)
$Trigger = New-ScheduledTaskTrigger -Daily -At $TriggerTime

# Create the scheduled task principal (run whether user is logged on or not)
$Principal = New-ScheduledTaskPrincipal -UserId ([Security.Principal.WindowsIdentity]::GetCurrent().Name) -LogonType Interactive

# Create the scheduled task settings
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Create the scheduled task
$ScheduledTaskParams = @{
    TaskName    = $TaskName
    Action      = $Action
    Trigger     = $Trigger
    Principal   = $Principal
    Settings    = $Settings
    Description = $TaskDescription
}

# Check if task already exists and update if needed
$ExistingTask = Get-ScheduledTask | Where-Object {$_.TaskName -eq $TaskName}

if ($ExistingTask) {
    Write-Host "Updating existing task: $TaskName" -ForegroundColor Yellow
    Set-ScheduledTask @ScheduledTaskParams
    Write-Host "Task updated successfully!" -ForegroundColor Green
} else {
    Write-Host "Creating new task: $TaskName" -ForegroundColor Yellow
    Register-ScheduledTask @ScheduledTaskParams
    Write-Host "Task created successfully!" -ForegroundColor Green
}

# Display task information
Write-Host "`nTask Information:" -ForegroundColor Cyan
Get-ScheduledTask -TaskName $TaskName | Select-Object TaskName, State, Description

Write-Host "`nNext scheduled run:" -ForegroundColor Cyan
$TaskInfo = Get-ScheduledTask -TaskName $TaskName | Get-ScheduledTaskInfo
$TaskInfo.NextRunTime
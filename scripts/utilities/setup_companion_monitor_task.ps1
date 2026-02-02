# PowerShell script to create the OpenClaw Companion Monitor Task

# Define task properties
$TaskName = "PAID OpenClaw Companion Monitor"
$TaskDescription = "Periodic status updates for OpenClaw system monitoring"
$ActionExecutable = "C:\Users\MyAIE\AppData\Local\Python\pythoncore-3.14-64\python.exe"
$ActionArguments = "C:\Users\MyAIE\.openclaw\workspace\openclaw_companion_monitor.py"
$ActionWorkingDirectory = "C:\Users\MyAIE\.openclaw\workspace"
$TriggerInterval = 4  # Every 4 hours

# Check if Python executable exists
if (-not (Test-Path $ActionExecutable)) {
    Write-Host "Python executable not found at: $ActionExecutable" -ForegroundColor Red
    exit 1
}

# Check if the script exists
if (-not (Test-Path $ActionArguments)) {
    Write-Host "Script not found at: $ActionArguments" -ForegroundColor Red
    exit 1
}

# Create the scheduled task action
$Action = New-ScheduledTaskAction -Execute $ActionExecutable -Argument $ActionArguments -WorkingDirectory $ActionWorkingDirectory

# Create the scheduled task trigger (every 4 hours during daytime)
$Triggers = @()
# Create triggers for 8 AM, 12 PM, 4 PM, 8 PM (every 4 hours during waking hours)
$BaseTime = Get-Date -Hour 8 -Minute 0 -Second 0
for ($i = 0; $i -lt 24; $i += $TriggerInterval) {
    if (($i + 8) -le 24) {  # Only create triggers during reasonable hours
        $TriggerTime = $BaseTime.AddHours($i)
        $Triggers += New-ScheduledTaskTrigger -Daily -At $TriggerTime.TimeOfDay
    }
}

# Create the scheduled task principal
$Principal = New-ScheduledTaskPrincipal -UserId ([Security.Principal.WindowsIdentity]::GetCurrent().Name) -LogonType Interactive

# Create the scheduled task settings (without invalid parameter)
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -WakeToRun

# Create the scheduled task with all triggers
$ScheduledTaskParams = @{
    TaskName    = $TaskName
    Action      = $Action
    Trigger     = $Triggers[0]  # Use the first trigger for simplicity
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
try {
    Get-ScheduledTask -TaskName $TaskName | Select-Object TaskName, State, Description
} catch {
    Write-Host "Task may not have been created successfully. Please check Task Scheduler manually." -ForegroundColor Yellow
}
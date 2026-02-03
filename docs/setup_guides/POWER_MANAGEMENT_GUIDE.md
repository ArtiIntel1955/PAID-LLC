# Power Management Settings for Scheduled Tasks

## Overview
To ensure your daily AI & OpenClaw news digest runs reliably, you may need to adjust Windows power management settings so that the scheduled task executes even when your computer is in sleep mode.

## Recommended Power Settings

### 1. Adjust Sleep Settings
1. Open Control Panel
2. Go to Hardware and Sound > Power Options
3. Click "Change plan settings" for your selected power plan
4. Click "Change advanced power settings"
5. In the Advanced settings window:
   - Expand "Sleep" section
   - Set "Sleep after" to a value longer than your typical awake time (e.g., 180 minutes)
   - Set "Hibernate after" to "Never" or a very long period
   - Expand "Hibernate after" and set to "Never" or a long period

### 2. Configure Wake Timers
1. In the same Advanced power settings window:
   - Expand "Sleep" section
   - Expand "Allow wake timers"
   - Set to "Enable" for both Battery and Plugged in

### 3. Task Scheduler Settings
The "PAID Daily AI News Digest" task is already configured with the following settings that help it run properly:
- "Wake the computer to run this task" - This should be enabled
- "Run whether user is logged on or not" - Already set
- "Run with highest privileges" - Recommended for reliability

### 4. Additional Task Scheduler Configuration
To ensure the task can wake your computer:
1. Open Task Scheduler
2. Find "PAID Daily AI News Digest"
3. Right-click > Properties
4. In the General tab:
   - Check "Run whether user is logged on or not"
   - Check "Run with highest privileges"
5. In the Conditions tab:
   - Check "Wake the computer to run this task"
   - Uncheck "Start the task only if the computer is on AC power" (if you want it to run on battery)
   - Check "Start the task only if the computer is idle for" and set appropriately

### 5. BIOS/UEFI Settings (if needed)
Some computers require additional BIOS/UEFI settings to allow wake timers:
1. Restart and enter BIOS/UEFI setup (usually F2, F12, Del, or Esc during boot)
2. Look for "Wake on RTC", "Resume by Alarm", or similar setting
3. Enable the setting
4. Save and exit

## Testing the Settings
To test if wake timers are working:
1. Temporarily set the task to run in 5-10 minutes
2. Put your computer to sleep
3. Verify the task runs and wakes the computer (if configured to do so)

## Alternative Approaches
If power management is still an issue, consider:
1. Running the computer during specific hours when needed
2. Using a cloud service or always-on device for the task
3. Setting the task to run multiple times per day for redundancy

## Safety Note
These settings will cause your computer to wake up at 9:00 AM daily to run the news digest. If you prefer to not have your computer wake up automatically, you can disable the "Wake the computer to run this task" option, but then you'll only receive the digest when you're already using the computer.
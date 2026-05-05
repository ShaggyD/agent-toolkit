---
name: macos-task-scheduler
description: Schedule recurring tasks on macOS using launchd plists
version: 1.0.0
author: Dustin Chadwick (@ShaggyD)
tags: [macos, automation, launchd, scheduling]
---

# macos-task-scheduler

Create and manage macOS launchd plist files for scheduled tasks. Handles the launchd configuration, scheduling syntax, and task lifecycle (load/unload/start).

## When to use me

- Schedule scripts to run daily/weekly/hourly
- Set up recurring system tasks
- Automate background jobs on Mac

## Quick Reference

### Create a plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.yourname.taskname</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-l</string>
        <string>-c</string>
        <string>YOUR COMMAND HERE</string>
    </array>
    <key>StartCalendarInterval</key>
    <array>
        <dict>
            <key>Minute</key><integer>0</integer>
            <key>Hour</key><integer>9</integer>
        </dict>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/project</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin</string>
    </dict>
    <key>StandardOutPath</key>
    <string>/path/to/project/taskname.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/project/taskname.error.log</string>
</dict>
</plist>
```

### Key launchd fixes

1. **Environment Variables**: launchd doesn't inherit user PATH - set explicitly
2. **Bash Login Shell**: Use `/bin/bash -l -c` wrapper
3. **Full Paths**: Everything needs absolute paths

### Commands

| Command | Description |
|---------|-------------|
| `launchctl load path/to/plist` | Register task |
| `launchctl unload path/to/plist` | Remove task |
| `launchctl start com.name.task` | Run immediately |
| `launchctl list \| grep taskname` | Check status |

### Schedule Examples

```xml
<!-- Daily at 9:30 AM -->
<dict>
    <key>Minute</key><integer>30</integer>
    <key>Hour</key><integer>9</integer>
</dict>

<!-- Every hour -->
<dict>
    <key>Minute</key><integer>0</integer>
</dict>

<!-- Weekly on Sundays at 10 AM -->
<dict>
    <key>Minute</key><integer>0</integer>
    <key>Hour</key><integer>10</integer>
    <key>Weekday</key><integer>0</integer>
</dict>

<!-- First day of month at midnight -->
<dict>
    <key>Minute</key><integer>0</integer>
    <key>Hour</key><integer>0</integer>
    <key>Day</key><integer>1</integer>
</dict>
```

### List tasks

```bash
ls -la ~/Library/LaunchAgents/
launchctl list | grep -E "com\.yourname\."
```

### Remove a task

```bash
launchctl unload ~/Library/LaunchAgents/com.yourname.taskname.plist
rm ~/Library/LaunchAgents/com.yourname.taskname.plist
```

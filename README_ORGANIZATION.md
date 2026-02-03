# OpenClaw Workspace Organization

Welcome to the organized OpenClaw workspace! This structure is designed to keep all files organized and easily accessible.

## Folder Structure

### agents/
Contains all agent-related files and configurations
- main/: Main agent files
- sub_agents/: Sub-agent configurations

### config/
Configuration files for various systems
- openclaw/: OpenClaw specific configurations
- channels/: Channel-specific configurations (Telegram, etc.)
- tools/: Tool configurations

### docs/
Documentation files organized by category
- projects/: Project documentation
- processes/: Process documentation
- reference/: Reference materials and guides

### logs/
Log files separated by function
- system/: System logs
- agents/: Agent activity logs
- channels/: Channel interaction logs

### memory/
Memory and history files
- daily/: Daily memory files
- weekly/: Weekly summaries
- archived/: Archived memory

### scripts/
Executable scripts organized by function
- ai_tools/: AI-related tools and utilities
- automation/: General automation scripts
- monitoring/: System and process monitoring scripts
- utilities/: General utility scripts
- scheduled/: Scheduled task scripts (like the daily AI news)

### tools/
Reusable tools and modules
- data_analysis/: Data analysis tools
- nlp/: Natural language processing tools
- web/: Web interaction tools
- media/: Media processing tools

### web/
Web interface files
- dashboard/: Dashboard components
- api/: API endpoints
- static/: Static assets (CSS, JS, images)

### projects/
Project-specific files
- current/: Active projects
- completed/: Completed projects
- archived/: Archived projects

### archives/
Archive files for backup and historical purposes
- backups/: Backup files
- old_logs/: Old log files
- deprecated/: Deprecated files

### temp/
Temporary files that are cleared regularly

## Migration Status

The workspace reorganization is complete. All existing files have been moved to their appropriate locations according to their function. The daily AI news system remains operational, located at `scripts/scheduled/daily_ai_news.py`.

## Best Practices

1. New scripts should be placed in the appropriate `scripts/` subdirectory
2. Documentation should go in the `docs/` directory
3. Tools and utilities should be placed in the `tools/` directory
4. Log files are automatically managed in the `logs/` directory
5. Memory files are handled in the `memory/` directory

This structure ensures that the workspace remains organized and manageable as it continues to grow.
# Workspace Organization Structure

This document describes the new organizational structure for the OpenClaw workspace to improve manageability and maintainability.

## Folder Structure

```
workspace/
├── docs/                    # Documentation files
│   ├── business_plans/      # Business plans and strategies
│   ├── setup_guides/        # Setup and configuration guides
│   ├── website/            # Website-related documentation
│   └── (other docs)        # Other documentation
├── scripts/                # Python and executable scripts
│   ├── monitoring/         # Monitoring and status scripts
│   ├── digest/            # News digest and reporting scripts
│   └── utilities/         # Utility and helper scripts
├── config/                 # Configuration files
│   ├── telegram/          # Telegram-specific configs
│   ├── digest/            # Digest system configs
│   └── (other configs)    # Other configuration files
├── web/                    # HTML and web files
├── memory/                 # Memory and log files (existing)
├── logs/                   # Log files (new)
├── archives/               # Archived files (new)
└── (root files)            # Essential root-level files
```

## File Categories

### Documentation (docs/)
- Business plans and launch documents
- Setup and configuration guides
- System documentation
- Integration documentation

### Scripts (scripts/)
- Monitoring and status scripts
- Digest and reporting scripts
- Utility scripts
- Automation scripts

### Configuration (config/)
- System configuration files
- Service-specific configurations
- API keys and settings (securely managed)

### Web Assets (web/)
- HTML templates
- Static web files
- Website assets

## Migration Notes

All existing files have been categorized and moved according to their function:
- Business-related documents → `docs/business_plans/`
- Setup guides → `docs/setup_guides/`
- Monitoring scripts → `scripts/monitoring/`
- Digest scripts → `scripts/digest/`
- Utility scripts → `scripts/utilities/`
- Configuration files → `config/`
- Web files → `web/`

## Best Practices

When adding new files:
1. Place documentation in the appropriate `docs/` subdirectory
2. Place scripts in the relevant `scripts/` subdirectory
3. Place configuration files in the `config/` directory
4. Place web assets in the `web/` directory
5. Keep only essential files in the root directory

This structure improves maintainability, makes it easier to locate files, and provides clear separation of concerns across different functional areas of the system.
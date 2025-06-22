# Dictionary mapping technical metrics to user-friendly KPI names and thresholds
KPI_TRANSLATION_MAP = {
    "PreTaxCost": {
        "label": "Cloud Spend",
        "warn_threshold": 5000
    },
    "CPUUtilization": {
        "label": "CPU Utilization (%)",
        "warn_threshold": 80
    },
    "MemoryUtilization": {
        "label": "Memory Utilization (%)",
        "warn_threshold": 75
    },
    "DiskReadOps": {
        "label": "Disk Read Operations",
        "warn_threshold": 10000
    },
    "DiskWriteOps": {
        "label": "Disk Write Operations",
        "warn_threshold": 10000
    },
    "NetworkIn": {
        "label": "Network In (MB)",
        "warn_threshold": 1000
    },
    "NetworkOut": {
        "label": "Network Out (MB)",
        "warn_threshold": 1000
    },
    # Add more mappings as needed
}

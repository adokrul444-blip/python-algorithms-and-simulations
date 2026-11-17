# Marathon Race Data Analytics

Python analytical toolkit for parsing, filtering, and evaluating 42.195 km marathon split times and runner telemetry.

## Features
- **CSV Telemetry Parser**: Parses runner bibs, categories, intermediate split checkpoints (5K to 41K), gun times, and net times.
- **Pace & Consistency Modeling**: Calculates split-by-split pace deviations to identify the most consistent runners and computes target pacing required for specific placements.
- **Category Rankings & Export**: Ranks runners at arbitrary checkpoints and exports filtered leaderboard CSV reports.

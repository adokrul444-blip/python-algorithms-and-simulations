# Aircraft Boarding Monte Carlo Simulation

Discrete-step grid simulation comparing passenger boarding algorithms and seat-interference bottlenecks on commercial aircraft.

## Implemented Boarding Strategies
- **Front-to-Back (`BoardingFTB`)** & **Back-to-Front (`BoardingBTF`)**
- **Window-to-Aisle / WilMA (`BoardingWTA`)** & **Aisle-to-Window (`BoardingATW`)**
- **Steffen Method (`BoardingSteffen`)** & **Random Boarding (`BoardingRandom`)**

## Key Mechanics
- Models aisle congestion, overhead bin luggage stowage delays, and row seat-interference resolution (`Plane.move_row` / `Plane.return_row`).
- Executes Monte Carlo batch runs (`test_boarding_method`) to benchmark average boarding steps across strategies.

## Run
    bash
python main.py

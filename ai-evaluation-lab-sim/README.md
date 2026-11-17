# AI Evaluation Research Lab Simulation

Object-oriented discrete-time simulation modeling multi-expert evaluation workflows for AI systems.

## Architecture & Design Patterns
- **Inheritance & Polymorphism (`expert.py`)**: Abstract `Expert` hierarchy specialized into `LinguistExpert`, `MLResearcher`, and `Statistician` with seniority-based duration estimation and domain reliability weighting.
- **Strategy Pattern (`lab.py`)**: Interchangeable scheduling policies (`ChronologicalStrategy`, `ComplexProtocolStrategy`, `EfficientStrategy`) optimizing resource allocation across concurrent evaluation protocols.
- **Stochastic Dialogue & Variance Modeling (`ai_system.py`, `experiment.py`)**: Simulates multi-trial NLP/dialogue quality metrics, variance reduction, and weighted statistical score aggregation.

## Run
```bash
python main.py

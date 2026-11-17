import random

from ai_system import AISystem
from evaluation import EvaluationProtocol
from expert import *
from lab import *
from lab import ChronologicalStrategy, ComplexProtocolStrategy, EfficientStrategy


AI_SYSTEMS = 6
REQUESTS = 12


def generate_ai_systems(n=AI_SYSTEMS):
    specializations = ["NLP", "medicine", "law", "education"]
    frameworks = ["PyTorch", "TensorFlow", "JAX"]

    systems = []
    for i in range(n):
        name = f"AI_{i}"
        specialization = random.choice(specializations)
        framework = random.choice(frameworks)
        quality = round(random.uniform(0.4, 0.95), 2)

        systems.append(
            AISystem(name, specialization, framework, quality)
        )

    return systems


def generate_experts():
    experts = [
        LinguistExpert("Ling1", "NLP", "assistant", 0.55),
        LinguistExpert("Ling2", "law", "associate", 0.65),

        MLResearcher("ML1", "NLP", "associate", 0.7, ["PyTorch", "TensorFlow"]),
        MLResearcher("ML2", "medicine", "professor", 0.85, ["TensorFlow"]),

        Statistician("Stat1", "NLP", "associate", 0.7),
        Statistician("Stat2", "medicine", "professor", 0.9)
    ]

    return experts


def generate_protocols():
    protocols = []

    for i in range(REQUESTS):
        prot = EvaluationProtocol(f"Protocol_{i}")

        prot.add_step({
            "desc": "linguistic evaluation",
            "duration": random.randint(2, 6) * 5,
            "requirements": [LinguistExpert]
        })

        prot.add_step({
            "desc": "model stability testing",
            "duration": random.randint(3, 8) * 5,
            "requirements": [MLResearcher]
        })

        prot.add_step({
            "desc": "statistical aggregation",
            "duration": random.randint(1, 3) * 5,
            "requirements": [Statistician]
        })

        protocols.append(prot)

    return protocols


def generate_requests():
    systems = generate_ai_systems()
    protocols = generate_protocols()

    reqs = []

    for _ in range(REQUESTS):
        sys = random.choice(systems)
        prot = random.choice(protocols)

        reqs.append((sys, prot))

    return reqs


def run_simulation():
    experts = generate_experts()
    requests = generate_requests()

    lab = ResearchLab(experts, requests)

    # choose one
    strategy = ChronologicalStrategy()
    # strategy = ChronologicalStrategy()
    # strategy = ComplexProtocolStrategy()
    # strategy = EfficientStrategy()
    strategy.assign_to_lab(lab)

    lab.set_strategy(strategy)

    days = lab.run_simulation()

    print("Simulation finished in", days, "days")
    print("Completed experiments:", len(lab.completed_experiments))


if __name__ == "__main__":
    run_simulation()

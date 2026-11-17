import random

class AISystem:
    def __init__(self, name, specialization, framework, quality):
        self.name = name
        self.specialization = specialization
        self.framework = framework
        self.quality = quality

    def simulate_dialogue(self):
        coherence = random.normalvariate(self.quality, 0.1)
        consistency = random.normalvariate(self.quality, 0.07)
        grammar_errors = random.normalvariate(10 * (1 - self.quality), 1)
        vocabulary_richness = random.normalvariate(0.5 + 0.5 * self.quality, 0.1)

        grammar_errors = max(0, int(round(grammar_errors)))

        return {
            "coherence": max(0, min(1, coherence)),
            "consistency": max(0, min(1, consistency)),
            "grammar_errors": grammar_errors,
            "vocabulary_richness": max(0, min(1, vocabulary_richness))
        }

    def get_dialogue_metrics(self, n_dialogues=100):
        c, s, g, v = [], [], [], []

        for _ in range(n_dialogues):
            d = self.simulate_dialogue()
            c.append(d["coherence"])
            s.append(d["consistency"])
            g.append(d["grammar_errors"])
            v.append(d["vocabulary_richness"])

        return {
            "coherence": sum(c) / len(c),
            "consistency": sum(s) / len(s),
            "grammar_errors": int(round(sum(g) / len(g))),
            "vocabulary_richness": sum(v) / len(v)
        }
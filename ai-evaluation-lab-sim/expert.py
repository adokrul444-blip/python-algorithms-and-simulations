import math
import statistics

class Expert:
    def __init__(self, name, specialization, seniority, reliability):
        self.name = name
        self.specialization = specialization
        self.seniority = seniority
        self.reliability = reliability

        if seniority not in ["assistant", "associate", "professor"]:
            raise ValueError(f"Unknown seniority level: {seniority}")

        if not isinstance(reliability, float):
            raise TypeError(f"Reliability must be float, not {type(reliability).__name__}")

        if not (0 <= reliability <= 1):
            raise ValueError(f"Reliability must be between 0 and 1. Got {reliability}")

        if seniority == "assistant" and reliability > 0.6:
            raise ValueError("An assistant's reliability cannot be bigger than 0.6")

        if seniority == "associate":
            if reliability < 0.5:
                raise ValueError("An associate's reliability cannot be smaller than 0.5")
            if reliability > 0.8:
                raise ValueError("An associate's reliability cannot be bigger than 0.8")

        if seniority == "professor" and reliability < 0.7:
            raise ValueError("A professor's reliability cannot be smaller than 0.7")

    def estimate_step_duration(self, base_hours):
        if self.seniority == "assistant":
            return math.ceil(base_hours * 1.2)
        if self.seniority == "associate":
            return math.ceil(base_hours)
        return math.ceil(base_hours * 0.8)

    def compute_reliability_weight(self, system_specialization):
        w = self.reliability
        if self.specialization == system_specialization:
            w *= 1.1
        return min(1.0, w)


class LinguistExpert(Expert):
    def evaluate_dialogue(self, m):
        if not all(k in m for k in ["coherence", "vocabulary_richness", "grammar_errors"]):
            raise KeyError("Did not find missing_key in metrics")

        g = 1 / (1 + m["grammar_errors"])

        if self.seniority == "assistant":
            return 0.7*m["coherence"] + 0.2*m["vocabulary_richness"] + 0.1*g
        if self.seniority == "associate":
            return 0.6*m["coherence"] + 0.3*m["vocabulary_richness"] + 0.1*g
        return 0.5*m["coherence"] + 0.3*m["vocabulary_richness"] + 0.2*g


class MLResearcher(Expert):
    def __init__(self, name, specialization, seniority, reliability, frameworks):
        super().__init__(name, specialization, seniority, reliability)
        self.known_frameworks = frameworks

    def knows_framework(self, f):
        return f in self.known_frameworks

    def validate_model(self, ai_system, hours):
        n = max(1, hours * 2)

        c, s = [], []

        for _ in range(n):
            d = ai_system.simulate_dialogue()
            c.append(d["coherence"])
            s.append(d["consistency"])

        var_c = statistics.pvariance(c)
        var_s = statistics.pvariance(s)

        if self.knows_framework(ai_system.framework):
            var_c *= 0.8
            var_s *= 0.8

        return {
            "coherences": c,
            "consistencies": s,
            "variability": (var_c + var_s) / 2
        }


class Statistician(Expert):
    def aggregate_scores(self, d):
        ai, q = d["quality"]
        linguist, lscore = d["linguist"]
        ml, mlres = d["MLexpert"]

        mc = sum(mlres["coherences"]) / len(mlres["coherences"])
        ms = sum(mlres["consistencies"]) / len(mlres["consistencies"])

        robustness = ((mc + ms) / 2) * (1 / (1 + mlres["variability"]))

        w_ml = ml.compute_reliability_weight(ai.specialization)
        w_l = linguist.compute_reliability_weight(ai.specialization)

        expert = (w_ml * robustness + w_l * lscore) / (w_ml + w_l)

        w_s = self.compute_reliability_weight(ai.specialization)

        return w_s * (0.6*q + 0.4*expert)
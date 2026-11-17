class Experiment:
    def __init__(self, lab, protocol, ai_system, experts):
        self.lab = lab
        self.protocol = protocol
        self.ai_system = ai_system
        self.experts = experts
        self.remaining_hours_per_step = {}

        for step in protocol.steps:
            expert = None

            for e in experts:
                if step.can_contribute(type(e)):
                    expert = e
                    break

            if expert:
                hours = expert.estimate_step_duration(step.duration)
            else:
                hours = step.duration

            self.remaining_hours_per_step[step] = hours

    def simulate_day(self):
        for step in self.remaining_hours_per_step:
            if self.remaining_hours_per_step[step] > 0:
                self.remaining_hours_per_step[step] = max(
                    0,
                    self.remaining_hours_per_step[step] - 6
                )

    def is_finished(self):
        return all(v <= 0 for v in self.remaining_hours_per_step.values())

    def employs(self, expert):
        return expert in self.experts

    def tests(self, ai_system, protocol):
        return self.ai_system == ai_system and self.protocol == protocol

    def compute_results(self):
        linguist = None
        ml = None
        stat = None

        for e in self.experts:
            if e.__class__.__name__ == "LinguistExpert":
                linguist = e
            elif e.__class__.__name__ == "MLResearcher":
                ml = e
            elif e.__class__.__name__ == "Statistician":
                stat = e

        if linguist is None or ml is None or stat is None:
            return {}

        # 1. linguist
        dialogue = self.ai_system.get_dialogue_metrics()
        linguist_score = linguist.evaluate_dialogue(dialogue)

        # 2. ML hours (iba relevantné kroky)
        ml_hours = 0
        for step in self.protocol.steps:
            if step.can_contribute(type(ml)):
                ml_hours += self.remaining_hours_per_step.get(step, 0)

        ml_results = ml.validate_model(self.ai_system, ml_hours)

        # 3. quality
        quality_score = self.ai_system.quality

        # 4. presný formát pre statistika
        metric_dict = {
            "quality": (self.ai_system, quality_score),
            "linguist": (linguist, linguist_score),
            "MLexpert": (ml, ml_results)
        }

        final_score = stat.aggregate_scores(metric_dict)

        return {
            "quality": (self.ai_system, quality_score),
            "linguist": (linguist, linguist_score),
            "MLexpert": (
                ml,
                ml_results["coherences"],
                ml_results["consistencies"],
                ml_results["variability"]
            ),
            "Statistician": (stat, final_score)
        }
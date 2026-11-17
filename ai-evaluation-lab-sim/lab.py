from experiment import Experiment

class ExperimentStrategy:
    def __init__(self):
        self.lab = None

    def assign_to_lab(self, lab):
        self.lab = lab

    def _build(self, lab, ai_system, protocol):
        experts = []

        for req in protocol.get_all_experts():
            cand = lab.get_available_experts(req)
            if not cand:
                return None
            experts.append(cand[0])

        return Experiment(lab, protocol, ai_system, experts)

    def create_experiment(self, requests):
        if not self.lab:
            return None

        for a, p in requests:
            e = self._build(self.lab, a, p)
            if e:
                return e

        return None


class ChronologicalStrategy(ExperimentStrategy):
    pass


class ComplexProtocolStrategy(ExperimentStrategy):
    def create_experiment(self, requests):
        if not self.lab:
            return None

        reqs = sorted(requests, key=lambda r: r[1].get_total_duration(), reverse=True)

        for a, p in reqs:
            e = self._build(self.lab, a, p)
            if e:
                return e
        return None


class EfficientStrategy(ExperimentStrategy):
    def _build(self, lab, ai_system, protocol):
        experts = []

        for req in protocol.get_all_experts():
            cand = lab.get_available_experts(req)
            if not cand:
                return None

            best = max(cand, key=lambda e: {
                "assistant": 1,
                "associate": 2,
                "professor": 3
            }.get(e.seniority, 0))

            experts.append(best)

        return Experiment(lab, protocol, ai_system, experts)


class ResearchLab:
    def __init__(self, members, requests):
        self.members = members
        self.requests = requests
        self.active_experiments = []
        self.completed_experiments = []
        self.selection_strategy = None

    def set_strategy(self, s):
        self.selection_strategy = s
        s.assign_to_lab(self)

    def get_available_experts(self, expert_type=None):
        out = []

        for m in self.members:
            busy = any(m in e.experts for e in self.active_experiments)
            if busy:
                continue

            if expert_type is None or isinstance(m, expert_type):
                out.append(m)

        return out

    def get_unsolved_requests(self):
        solved = {(e.ai_system, e.protocol)
                  for e in (self.active_experiments + self.completed_experiments)}

        return [r for r in self.requests if r not in solved]

    def can_run_protocol(self, protocol):
        avail = self.get_available_experts()

        for req in protocol.get_all_experts():
            if not any(isinstance(e, req) for e in avail):
                return False
        return True

    def run_simulation(self):
        if not self.selection_strategy:
            raise RuntimeError("No selection strategy was set")

        days = 0

        while self.requests or self.active_experiments:
            exp = self.selection_strategy.create_experiment(self.requests)

            if exp:
                self.active_experiments.append(exp)
                self.requests = [
                    r for r in self.requests
                    if not (r[0] == exp.ai_system and r[1] == exp.protocol)
                ]

            for e in self.active_experiments:
                e.simulate_day()

            finished = [e for e in self.active_experiments if e.is_finished()]

            for f in finished:
                self.active_experiments.remove(f)
                self.completed_experiments.append(f)

            days += 1

        return days
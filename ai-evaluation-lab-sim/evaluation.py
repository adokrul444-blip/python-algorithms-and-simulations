class Step:
    def __init__(self, step_desc, duration, experts):
        self.step_desc = step_desc
        self.duration = duration
        self.experts = experts

    def can_contribute(self, expert_type):
        return expert_type in self.experts


class EvaluationProtocol:
    def __init__(self, protocol_name):
        self.protocol_name = protocol_name
        self.steps = []
        self.required_experts = {}

    def add_step(self, step_info):
        if not isinstance(step_info["duration"], int) or step_info["duration"] < 1:
            raise ValueError("Step duration must be an integer and at least 1")

        step = Step(
            step_info["desc"],
            step_info["duration"],
            step_info["requirements"]
        )

        self.steps.append(step)
        self.required_experts[step] = step_info["requirements"]

    def get_all_experts(self):
        out = set()
        for reqs in self.required_experts.values():
            for r in reqs:
                out.add(r)
        return list(out)

    def get_total_duration(self):
        return sum(s.duration for s in self.steps)

    def get_hours_for_expert(self, expert):
        total = 0
        for s in self.steps:
            if s.can_contribute(type(expert)):
                total += s.duration
        return total
    
    def get_steps(self):
        return self.steps
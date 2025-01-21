from typing import List
from .evaluation import Evaluation

class Scenario:
    def __init__(self, *, name: str, prompt: str, evaluations: List[Evaluation] = []):
        """Initialize a Scenario.
        
        Args:
            name (str): The name of the scenario
            prompt (str): The system prompt for the scenario
            evaluations (List[Evaluation], optional): List of evaluations for this scenario
        """
        self.name = name
        self.prompt = prompt
        self.evaluations = evaluations

    def to_dict(self):
        return {
            "name": self.name,
            "prompt": self.prompt,
            "evaluations": [e.to_dict() for e in self.evaluations]
        }

    def __repr__(self):
        return f"Scenario(name='{self.name}', prompt='{self.prompt}', evaluations={self.evaluations})"

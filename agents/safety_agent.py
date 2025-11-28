import yaml
import re

class SafetyAgent:
    def __init__(self, policy_path="config/safety_policy.yaml"):
        with open(policy_path, "r") as f:
            self.policy = yaml.safe_load(f)

    def check_message(self, text: str):
        violations = []

        # Check prohibited content
        for rule in self.policy["prohibited_content"]:
            for pattern in rule["patterns"]:
                if re.search(pattern, text):
                    violations.append(rule["name"])

        # Check tone violations
        for bad_tone in self.policy["brand_guidelines"]["tone"]["disallowed"]:
            if bad_tone.lower() in text.lower():
                violations.append(f"Disallowed tone: {bad_tone}")

        # Check forbidden phrases
        for phrase in self.policy["brand_guidelines"]["forbidden_phrases"]:
            if phrase.lower() in text.lower():
                violations.append(f"Forbidden phrase: {phrase}")

        # Require product citation
        if self.policy["citation_requirements"]["require_product_citations"]:
            if "[source:" not in text:
                violations.append("Missing product citation")

        return violations

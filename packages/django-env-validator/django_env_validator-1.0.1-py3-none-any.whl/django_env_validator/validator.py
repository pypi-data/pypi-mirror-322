import os

from dataclasses import dataclass
from typing import Dict, Any, List, Callable, Optional

from django.core.exceptions import ImproperlyConfigured


@dataclass
class ValidationRule:
    check: Callable[[str, Any], Optional[str]]
    type_validator: Callable[[Any], bool]
    type_name: str


class EnvValidator:
    RULES = {
        "required": ValidationRule(
            check=lambda name, _: (
                f"Environment variable '{name}' is required but not set"
                if os.getenv(name) is None
                else None
            ),
            type_validator=lambda x: isinstance(x, bool),
            type_name="boolean",
        ),
        "min_length": ValidationRule(
            check=lambda name, min_len: (
                f"Environment variable '{name}' must be at least {min_len} characters long"
                if os.getenv(name) and len(os.getenv(name)) < min_len
                else None
            ),
            type_validator=lambda x: isinstance(x, int),
            type_name="integer",
        ),
        "max_length": ValidationRule(
            check=lambda name, max_len: (
                f"Environment variable '{name}' must be at most {max_len} characters long"
                if os.getenv(name) and len(os.getenv(name)) > max_len
                else None
            ),
            type_validator=lambda x: isinstance(x, int),
            type_name="integer",
        ),
        "choices": ValidationRule(
            check=lambda name, choices: (
                f"Environment variable '{name}' must be one of: {', '.join(choices)}"
                if os.getenv(name) and os.getenv(name) not in choices
                else None
            ),
            type_validator=lambda x: isinstance(x, (list, tuple, set)),
            type_name="list, tuple, or set",
        ),
    }

    def __init__(self, rules: Dict[str, Dict[str, Any]]):
        self.rules = rules
        self._validate_rule_structure()

    def _validate_rule_structure(self) -> None:
        """Validate the structure of the rules dictionary."""
        for var_name, var_rules in self.rules.items():
            for rule_name, rule_value in var_rules.items():
                if rule_name not in self.RULES:
                    raise ImproperlyConfigured(
                        f"Unknown rule '{rule_name}' for environment variable '{var_name}'"
                    )

                validation_rule = self.RULES[rule_name]
                if not validation_rule.type_validator(rule_value):
                    raise ImproperlyConfigured(
                        f"{rule_name} for '{var_name}' must be a {validation_rule.type_name}"
                    )

    def validate(self) -> None:
        """Validate all environment variables according to the rules."""
        errors: List[str] = []

        for var_name, var_rules in self.rules.items():
            # Skip further validation if required check fails
            if var_rules.get("required", False):
                required_error = self.RULES["required"].check(var_name, True)
                if required_error:
                    errors.append(required_error)
                    continue

            # Only validate other rules if the variable has a value
            if os.getenv(var_name) is not None:
                for rule_name, rule_value in var_rules.items():
                    if rule_name == "required":
                        continue

                    error = self.RULES[rule_name].check(var_name, rule_value)
                    if error:
                        errors.append(error)

        if errors:
            raise ImproperlyConfigured("\n".join(errors))


def validate_env_variables(rules: Dict[str, Dict[str, Any]]) -> None:
    """Convenience function to validate environment variables."""
    validator = EnvValidator(rules)
    validator.validate()

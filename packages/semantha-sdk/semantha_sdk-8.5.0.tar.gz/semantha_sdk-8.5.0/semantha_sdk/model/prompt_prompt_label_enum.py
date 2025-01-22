from enum import Enum

class PromptPrompt_labelEnum(str, Enum):
    COMPARE = "COMPARE",
    REQUIREMENTS = "REQUIREMENTS",
    SEARCH = "SEARCH",
    LIBRARY = "LIBRARY",
    
    def __str__(self) -> str:
        return self.value

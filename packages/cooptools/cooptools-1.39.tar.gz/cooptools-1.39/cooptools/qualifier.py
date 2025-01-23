from dataclasses import dataclass
import re
from typing import Iterable, Protocol, Dict, Callable
from cooptools import typeProviders as tp

class QualifierProtocol(Protocol):
    def qualify(self, values: Iterable[str]) -> Dict[str, bool]:
        pass

@dataclass(frozen=True, slots=True)
class PatternMatchQualifier(QualifierProtocol):
    regex: Iterable[str] = None
    regex_all: Iterable[str] = None
    regex_any: Iterable[str] = None
    values: Iterable[str] = None

    def __post_init__(self):
        if self.regex is not None and self.regex_all is None:
            object.__setattr__(self, 'regex_all', [self.regex])
        elif self.regex is not None and self.regex_all is not None:
            object.__setattr__(self, 'regex_all', list(self.regex_all) + [self.regex])

        if (self.regex_all is None
                and self.regex_any is None
                and self.values is None):
            raise ValueError(f"At least one of regex_all, regex_any or id must be filled")

    def qualify(self, values: Iterable[str]) -> Dict[str, bool]:
        ret = {}
        for value in values:
            ret[value] = True

            if self.regex_all is not None and not all(re.match(x, value) for x in self.regex_all):
                ret[value] = False

            if self.regex_any is not None and not any(re.match(x, value) for x in self.regex_any):
                ret[value] = False

            if self.values is not None and value not in self.values:
                ret[value] = False

        return ret


QualifierProvider = Iterable[QualifierProtocol] | Callable[[], Iterable[QualifierProtocol]]

def resolve_qualifier_provider(qp: QualifierProvider):
    return tp.resolve(qp)
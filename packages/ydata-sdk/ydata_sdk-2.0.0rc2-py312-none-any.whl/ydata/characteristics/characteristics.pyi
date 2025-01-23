from _typeshed import Incomplete
from ydata.metadata import Metadata
from ydata.metadata.multimetadata import MultiMetadata

CHARAC_TO_ANONYM: Incomplete
CHARAC_GROUPS: Incomplete

def suggest_anonymizer_config(metadata: Metadata | MultiMetadata) -> dict[str, list[str] | dict[str, list[str]]]: ...
def deduce_anonymizer_config_for_STR(metadata: Metadata) -> dict[str, str]: ...
def deduce_anonymizer_config_for_PII(metadata: Metadata) -> dict[str, str]: ...

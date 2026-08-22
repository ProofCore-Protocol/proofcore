from .client import ProofCoreClient, seal, get_proof

__version__ = "0.1.0"
__all__ = ["ProofCoreClient", "seal", "get_proof"]

# Ленивый импорт интеграций, если установлены соответствующие библиотеки
try:
    from .langchain import ProofCoreSealerTool
    __all__.append("ProofCoreSealerTool")
except ImportError:
    pass

try:
    from .crewai import ProofCoreCrewTool
    __all__.append("ProofCoreCrewTool")
except ImportError:
    pass
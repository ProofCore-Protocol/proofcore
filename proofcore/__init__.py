from .client import ProofCoreClient, seal, get_proof, verify, get_pubkey

__version__ = "0.1.7"
__all__ = ["ProofCoreClient", "seal", "get_proof", "verify", "get_pubkey"]

# Ленивый импорт интеграций
try:
    from .langchain import ProofCoreSealerTool
    __all__.append("ProofCoreSealerTool")
except ImportError: pass

try:
    from .crewai import ProofCoreCrewTool
    __all__.append("ProofCoreCrewTool")
except ImportError: pass

try:
    from .gradio_ui import NotarizedOutput
    __all__.append("NotarizedOutput")
except ImportError: pass
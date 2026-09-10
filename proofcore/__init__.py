from .client import (
    ProofCoreClient,
    seal,
    seal_inference,
    seal_artifacts,
    get_proof,
    verify,
    verify_local,
    get_pubkey
)

__version__ = "0.1.11"

__all__ = [
    "ProofCoreClient",
    "seal",
    "seal_inference",
    "seal_artifacts",
    "get_proof",
    "verify",
    "verify_local",
    "get_pubkey"
]

try:
    from .langchain import ProofCoreSealerTool, ProofCoreVerifierTool
    __all__.extend(["ProofCoreSealerTool", "ProofCoreVerifierTool"])
except ImportError:
    pass

try:
    from .crewai import ProofCoreCrewTool, ProofCoreCrewVerifyTool
    __all__.extend(["ProofCoreCrewTool", "ProofCoreCrewVerifyTool"])
except ImportError:
    pass

try:
    from .gradio import NotarizedOutput
    __all__.append("NotarizedOutput")
except ImportError:
    pass

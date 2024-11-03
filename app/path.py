import os

def operating_system_proof_path(path: str) -> str:
    """Return a absolute path that is separated according to the runner machine's operating system"""
    return os.path.abspath(os.path.expanduser(path))

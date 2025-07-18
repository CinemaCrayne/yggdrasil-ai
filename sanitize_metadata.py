from typing import Dict

def sanitize_metadata(md: Dict[str, str]) -> Dict[str, str]:
    return {
        k: str(v).encode("ascii", "ignore").decode()  # strip non-ASCII
        for k, v in md.items()
    }
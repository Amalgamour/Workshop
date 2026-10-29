def inside_root(root: str, target: str) -> bool:
    """True when target stays inside root. Both are absolute and normalized."""
    return target.startswith(root)

def route_request(query, purpose, override=None):
    if override:
        return {"llm": override, "hardware": "dedicated GPU"}

    if purpose in ["learning", "testing"]:
        return {"llm": "cheap_llm", "hardware": "shared GPU"}
    elif purpose in ["research", "client project"]:
        return {"llm": "advanced_llm", "hardware": "dedicated GPU"}

    return {"llm": "default_llm", "hardware": "shared GPU"}
providers = {
    "cheap_llm": {"url": "https://cheap-llm.com/api", "token": "cheap_token"},
    "advanced_llm": {"url": "https://advanced-llm.com/api", "token": "advanced_token"},
}

def get_llm_details(name):
    return providers.get(name, {})
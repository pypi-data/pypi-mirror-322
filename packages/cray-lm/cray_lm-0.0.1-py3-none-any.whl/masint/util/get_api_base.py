import masint


def get_api_base():
    if masint.api_url is None:
        return "https://meta-llama--llama-3-2-3b-instruct.cray-lm.com"

    return masint.api_url

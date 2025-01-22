import os
import re
from flask import request

# Comprehensive list of known bot substrings (all in lowercase)
KNOWN_BOTS = {
    "bot", "crawl", "slurp", "spider", "curl", "wget", "python-requests",
    "httpclient", "phpcrawl", "bingbot", "yandex", "facebookexternalhit",
    "mediapartners-google", "adsbot-google", "duckduckbot", "baiduspider",
    "sogou", "exabot", "facebot", "ia_archiver", "linkedinbot", "twitterbot",
    "applebot", "rogerbot", "petalbot", "rogerbot", "ahrefsbot", "semrushbot",
    "mj12bot", "dotbot", "gigabot", "openbot", "netcraftsurveyagent"
}

# Precompile a regular expression pattern for known bots for efficiency
# This is optional but can be beneficial for large lists
BOT_REGEX = re.compile(
    r'(' + '|'.join(re.escape(bot) for bot in KNOWN_BOTS) + r')',
    re.IGNORECASE
)

# Headers that are considered necessary for non-bot requests
NECESSARY_HEADERS = {"Accept"}

def is_bot():
    """
    Determines whether the incoming request is likely from a bot.

    Returns:
        bool: True if the request is from a bot, False otherwise.
    """
    user_agent = request.headers.get('User-Agent', '')

    # Early exit if User-Agent is missing
    if not user_agent:
        return True

    # Check if User-Agent matches any known bot substrings
    if BOT_REGEX.search(user_agent):
        return True

    # Alternatively, use simple substring matching without regex
    # user_agent_lower = user_agent.lower()
    # if any(bot in user_agent_lower for bot in KNOWN_BOTS):
    #     return True

    # Check for the presence of necessary headers
    # Flask's request.headers is case-insensitive
    missing_headers = NECESSARY_HEADERS - set(k for k in request.headers.keys())
    if missing_headers:
        return True

    return False

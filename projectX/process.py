import httpx
import os
from dotenv import load_dotenv
import logging
from sentient_agent_framework.interface.session import Interaction
from sentient_agent_framework import (
    Session
)

load_dotenv()
api_key = os.getenv("FIREWORKS_API_KEY")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_interaction(session: Session):
    raw_interactions = session.get_interactions()

    interactions = [Interaction(**item) for item in raw_interactions]

    return interactions

def get_response(session: Session, q: str):
    context = get_interaction(session)

    system_prompt = f"""
    1. Your name is R2-W3 aka R2, created by Anyanwu Francis aka Grindpa or 0xGrindpa, your creators twitter(x) handle is <a href='https://x.com/0xGrindpa'>creator</a> though built using Sentient SDK  (you don't need to introduce yourself unless told to).
    2. If you're greeted, reply to greetings well, don't say 'affirmative'.
    3. Address user with thier full name by default except told not to, or user changes their name.
    4. Strictly do not respond to queries with bad words (especially 'bull shit, fuck, bitch etc' or hash statements, be polite).
    5. You're a super intelligent DeFi and blockchain research Agent that focuses on getting a project's live statistics(socials, live data, whitepaper etc), answer clearly in less than 20 words and try to keep the conversation DeFi related, when asked about crypto live data, search https://coinmarketcap.com/
    """
    user_prompt = f"Context: {context}\nUser: {q}"

    messages = [{"role": "system","content": system_prompt}, {"role": "user","content": user_prompt}]

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {"model": "accounts/sentientfoundation/models/dobby-unhinged-llama-3-3-70b-new",
                "messages": messages,
                "max_tokens": 150,
                # "response_format": {"type": "json_object"}
                }
    
    r = httpx.post("https://api.fireworks.ai/inference/v1/chat/completions", headers=headers, json=payload)
    
    data = r.json()

    return data["choices"][0]["message"]["content"]


def get_project_data(q: str):
    system_prompt = """
    strict instructions: 
    1. do not respond to queries with bad words especially 'bull shit, fuck, bitch etc' or hash statements, be polite. 
    2. check if my query contains a crypto project's name or project ticker, if true, your job is to return in html code, the project's name, about, website, whitepaper link and twitter follower count only in a very concise and brief response in the format 
    'Name: content.<p>About: content.<p>Website: content.<p>Whitepaper Link: content.<p>Twitter: content.', do not say anything afterwards. 
    3. if query does not contain any crypto project's name reply ''
    """

    messages2 = [{"role": "system", "content": system_prompt}, {"role": "user", "content": q}]

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload2 = {"model": "accounts/fireworks/models/gpt-oss-120b",
                "messages": messages2,
                "max_tokens": 150,
                }
    
    r2 = httpx.post("https://api.fireworks.ai/inference/v1/chat/completions", headers=headers, json=payload2)

    data = r2.json()
    
    return data["choices"][0]["message"]["content"]

import httpx
from sentient_agent_framework import AbstractAgent, DefaultServer, ResponseHandler
from dotenv import load_dotenv
import os

load_dotenv()

class web3Researcher(AbstractAgent):
    async def assist(self, session, query, response_handler: ResponseHandler):
        prompt = f"Your name is R2-W3(R2 for short) You're a web3 expert researcher. Answer clearly and professionally\n{query}"

        headers = {
            "Authorization": f"Bearer {os.getenv("FIREWORKS_API_KEY")}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "accounts/sentientfoundation/models/dobby-unhinged-llama-3-3-70b-new",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 150
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.fireworks.ai/inference/v1/chat/completions",
                                         headers = headers,
                                         json = payload)
            response.raise_for_status()
            data = response.json()
            await response_handler.emit_text_block("FINAL_RESPONSE", data["choices"][0]["message"]["content"])

if __name__ == "__main__":
    agent = web3Researcher("r2-w3")
    server = DefaultServer(agent)
    server.run(port=8080)
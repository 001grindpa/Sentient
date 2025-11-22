from sentient_agent_framework import (
    ResponseHandler,
    DefaultServer,
    AbstractAgent,
    Query,
    Session
)
from process import get_response

class DeFiAgent(AbstractAgent):
    def __init__(self, name: str="R2-W3"):
        super().__init__(name)

    async def assist(self, session: Session, query: Query, response_handler: ResponseHandler):
        await response_handler.emit_text_block("Analyze", "R2 is analyzing your prompt...")

        result = await get_response(session, query.prompt)
        
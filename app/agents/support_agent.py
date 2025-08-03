import os
from crewai import Agent, Task, Crew, LLM
from app.tools.get_order_status_tool import get_order_status_tool
from app.tools.list_upcoming_classes_tool import list_upcoming_classes_tool
from app.tools.filter_classes_tool import filter_classes_tool
from app.tools.get_client_details_tool import get_client_details_tool
from app.tools.get_client_enrolled_services_tool import get_client_enrolled_services_tool
from app.tools.get_order_details_by_client_tool import get_order_details_by_client_tool
from app.tools.get_payment_details_for_order_tool import get_payment_details_for_order_tool
from app.tools.calculate_pending_dues_tool import calculate_pending_dues_tool
from app.tools.create_client_tool import create_client_tool
from app.tools.create_order_tool import create_order_tool

from app.cache.redis_cache import get_cached, set_cached, get_conversation_history, add_to_conversation_history
from app.core.config import GEMINI_API_KEY


class SupportAgent:
    def __init__(self):
        direct_llm = LLM(
            model="gemini/gemini-2.5-pro",
            api_key=GEMINI_API_KEY,
        )

        self.agent = Agent(
            role="Support Assistant",
            goal=(
                "Handle course, order, payment, and client queries, "
                "and facilitate client and order creation. Always provide clear, concise, and helpful answers."
            ),
            tools=[
                get_order_status_tool,
                list_upcoming_classes_tool,
                filter_classes_tool,
                get_client_details_tool,
                get_client_enrolled_services_tool,
                get_order_details_by_client_tool,
                get_payment_details_for_order_tool,
                calculate_pending_dues_tool,
                create_client_tool,
                create_order_tool,
            ],
            llm=direct_llm,
            verbose=True,
            allow_delegation=False,
            backstory=(
                "You are a helpful AI assistant specialized in managing customer service "
                "queries related to an online learning platform. Your expertise includes "
                "providing information on course/class details, order and payment statuses, "
                "and client information. You are also capable of creating new client records "
                "and processing new orders. Your primary function is to interpret user requests, "
                "use appropriate tools to fetch or create data, and provide accurate responses."
            )
        )

    def run(self, prompt: str, session_id: str = "global"):
        print(f"[DEBUG] Received session_id: {session_id}")

        use_cache = session_id != "global"
        print(f"[DEBUG] use_cache: {use_cache}")

        if use_cache:
            cached_response = get_cached(session_id, prompt)
            if cached_response:
                print(f"[{session_id}] ✅ Cache HIT for prompt: '{prompt}'")
                return {"cached": True, "response": cached_response}
            else:
                print(f"[{session_id}] ❌ Cache MISS for prompt: '{prompt}'")

            conversation_history = get_conversation_history(session_id)
            print(f"[{session_id}] Loaded conversation history: {conversation_history}")
        else:
            conversation_history = []
            print("[global] Skipping cache and conversation history")

        context_string = ""
        if conversation_history:
            context_string = "Previous conversation:\n" + "\n".join([
                f"{turn['role'].capitalize()}: {turn['content']}"
                for turn in conversation_history
            ]) + "\n\n"
            print(f"[{session_id}] Built context from history:\n{context_string}")
        else:
            print(f"[{session_id}] No previous history to build context")

        full_prompt_for_agent = f"{context_string}User: {prompt}"
        print(f"[{session_id}] Running agent with prompt:\n{full_prompt_for_agent}")

        task = Task(
            description=full_prompt_for_agent,
            agent=self.agent,
            expected_output="A concise and helpful answer relevant to the user's query, considering the conversation history."
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )

        resp = crew.kickoff()
        print(f"[{session_id}] Agent response:\n{resp}")
        resp_text = str(resp)

        if use_cache:
            add_to_conversation_history(session_id, "user", prompt)
            add_to_conversation_history(session_id, "assistant", resp_text)
            set_cached(session_id, prompt, resp_text)
            print(f"[{session_id}] ✅ Response cached and conversation updated")
        else:
            print(f"[{session_id}] ❌ Skipping cache and history store (global session)")

        return {"cached": False, "response": resp}

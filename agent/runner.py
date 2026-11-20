from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from tools import tools
from agent.prompts import SYSTEM_PROMPT


TOOL_MAP = {tool.name: tool for tool in tools}


def run_travel_agent(user_request: str, llm, max_iterations: int = 8) -> str:
    """
    Run a simple tool-calling agent loop.

    Pass in the already configured ChatGoogleGenerativeAI model.
    The function returns the model's final text response.
    """
    if not isinstance(user_request, str) or not user_request.strip():
        raise ValueError("Please enter a travel-planning request.")

    if max_iterations < 1:
        raise ValueError("max_iterations must be at least 1.")

    model_with_tools = llm.bind_tools(tools)
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_request.strip()),
    ]

    for _ in range(max_iterations):
        ai_message = model_with_tools.invoke(messages)
        messages.append(ai_message)

        tool_calls = getattr(ai_message, "tool_calls", None) or []

        # No tool calls means the model has produced its final answer.
        if not tool_calls:
            content = ai_message.content
            if isinstance(content, str):
                return content
            return str(content)

        for call in tool_calls:
            tool_name = call.get("name")
            tool_args = call.get("args", {})
            tool_call_id = call.get("id")

            selected_tool = TOOL_MAP.get(tool_name)
            if selected_tool is None:
                tool_result = {"error": f"Unknown tool requested: {tool_name}"}
            else:
                try:
                    tool_result = selected_tool.invoke(tool_args)
                except Exception as exc:
                    tool_result = {"error": f"Tool execution failed: {exc}"}

            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call_id,
                )
            )

    raise RuntimeError(
        "The agent reached its tool-call limit without producing a final answer. "
        "Try a simpler request or increase max_iterations."
    )

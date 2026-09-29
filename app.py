import llm
from tools import save_note, search_notes
from schemas import SaveNoteArgs, SearchNotesArgs
import logging

logger = logging.getLogger(__name__)


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages = [
        {
            "role": "user",
            "content": user_input
        }
    ]

    response = llm.llm_call(
        model="qwen3:8b",
        messages=messages,
        tools=[save_note, search_notes]
    )
    

    if response.message.tool_calls:

        # Add Qwen's tool-call message to the conversation
        messages.append(response.message)

        for tool_call in response.message.tool_calls:

            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            logger.info(
                "Tool call | tool=%s | arguments=%s",
                tool_name,
                arguments
            )

            if tool_name == "search_notes":
                validated_args = SearchNotesArgs(**arguments)
                result = search_notes(**validated_args.model_dump())

            elif tool_name == "save_note":
                validated_args = SaveNoteArgs(**arguments)
                result = save_note(**validated_args.model_dump())

            else:
                result = f"Unknown tool: {tool_name}"

            # Give the tool result back to Qwen
            messages.append(
                {
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": str(result)
                }
            )

        # Ask Qwen to produce the final answer
        final_response = llm.llm_call(
            model="qwen3:8b",
            messages=messages
        )

        print(final_response.message.content)

    else:
        print(response.message.content)


print(f"Input tokens: {llm.total_input_tokens}")
print(f"Output tokens: {llm.total_output_tokens}")
print(
    f"Total tokens: "
    f"{llm.total_input_tokens + llm.total_output_tokens}"
)
print(f"Estimated cost: ${llm.total_cost:.6f}")
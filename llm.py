from tenacity import retry, stop_after_attempt, wait_exponential
from ollama import chat
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

total_input_tokens = 0
total_output_tokens = 0
total_cost = 0
INPUT_COST_PER_1K = 0.0
OUTPUT_COST_PER_1K = 0.0

def log_retry(retry_state):
    logger.warning(
        "LLM call failed | attempt=%s | retrying...",
        retry_state.attempt_number
    )
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    before_sleep=log_retry
)

def llm_call(model, messages, output_schema=None, tools=None):
    logger.info(
        "LLM call | model=%s | messages=%d | tools=%s",
        model,
        len(messages),
        bool(tools)
    )
    response = chat(
        model=model,
        messages=messages,
        format=output_schema,
        tools=tools
    )
    global total_input_tokens, total_output_tokens , total_cost

    total_input_tokens += response.prompt_eval_count
    total_output_tokens += response.eval_count

    input_cost = (response.prompt_eval_count / 1000) * INPUT_COST_PER_1K
    output_cost = (response.eval_count / 1000) * OUTPUT_COST_PER_1K

    total_cost += input_cost + output_cost

    return response
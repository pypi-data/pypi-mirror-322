from typing import Optional
from langchain.chat_models import init_chat_model
from langmem.prompts.prompt import INSTRUCTION_REFLECTION_PROMPT, GeneralResponse
from langmem.prompts.utils import get_trajectory_clean
from langsmith import traceable


class PromptMemory:
    def __init__(self, model: Optional = None):
        if model is not None:
            self.model = model.with_structured_output(
                GeneralResponse, method="json_schema"
            )
        else:
            self.model = init_chat_model(
                "claude-3-5-sonnet-latest", model_provider="anthropic", temperature=0
            ).with_structured_output(GeneralResponse, method="json_schema")

    @traceable
    def reflect(self, messages, current_prompt: str, feedback: str, instructions: str):
        trajectory = get_trajectory_clean(messages)
        prompt = INSTRUCTION_REFLECTION_PROMPT.format(
            current_prompt=current_prompt,
            trajectory=trajectory,
            feedback=feedback,
            instructions=instructions,
        )
        _output = self.model.invoke(prompt)
        return _output

    @traceable
    def areflect(self, messages, current_prompt: str, feedback: str, instructions: str):
        trajectory = get_trajectory_clean(messages)
        prompt = INSTRUCTION_REFLECTION_PROMPT.format(
            current_prompt=current_prompt,
            trajectory=trajectory,
            feedback=feedback,
            instructions=instructions,
        )
        _output = await self.model.ainvoke(prompt)
        return _output

import asyncio
import re
import typing
from typing_extensions import TypedDict
import uuid

import langsmith as ls
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.messages.utils import merge_message_runs
from langchain_core.tools import tool
from langchain_core.messages import AnyMessage
from langgraph.utils.config import get_config, get_store
from pydantic import BaseModel, Field, model_validator
from trustcall import create_extractor

## LangGraph Tools


def create_manage_memory_tool(
    instructions: str = """Proactively call this tool when you:
1. Identify a new USER preference.
2. Receive an explicit USER request to remember something or otherwise alter your behavior.
3. Are working and want to record important context.
4. Identify that an existing MEMORY is incorrect or outdated.""",
    namespace_prefix: tuple[str, ...] = ("memories", "{user_id}"),
):
    namespacer = _NamespaceTemplate(namespace_prefix)

    @tool
    async def manage_memory(
        action: typing.Literal["create", "update", "delete"],
        content: typing.Optional[str] = None,
        *,
        id: typing.Optional[uuid.UUID] = None,
    ):
        """Create, update, or delete persistent MEMORIES that will be carried over to future conversations.
        {instructions}"""
        store = get_store()

        if action == "create" and id is not None:
            raise ValueError(
                "You cannot provide a MEMORY ID when creating a MEMORY. Please try again, omitting the id argument."
            )

        if action in ("delete", "update") and not id:
            raise ValueError(
                "You must provide a MEMORY ID when deleting or updating a MEMORY."
            )
        if action == "delete":
            await store.adelete(namespace_prefix, key=str(id))
            return f"Deleted memory {id}"
        namespace = namespacer()
        id = id or uuid.uuid4()
        await store.aput(
            namespace,
            key=str(id),
            value={"content": content},
        )
        return f"{action}d memory {id}"

    manage_memory.__doc__.format(instructions=instructions)

    return manage_memory


_MEMORY_SEARCH_INSTRUCTIONS = (
    """Call this tool to search your long term memory for information."""
)


def create_search_memory_tool(
    instructions: str = _MEMORY_SEARCH_INSTRUCTIONS,
    namespace_prefix: tuple[str, ...] = ("memories", "{user_id}"),
):
    namespacer = _NamespaceTemplate(namespace_prefix)

    @tool
    async def search_memory(
        query: str,
        *,
        limit: int = 10,
        offset: int = 0,
        filter: typing.Optional[dict] = None,
    ):
        """Search for MEMORIES stored in the graph.
        {instructions}"""
        store = get_store()
        namespace = namespacer()
        memories = await store.asearch(
            namespace,
            query=query,
            filter=filter,
            limit=limit,
            offset=offset,
        )
        return [m.dict() for m in memories]

    search_memory.__doc__.format(instructions=instructions)  # type: ignore

    return search_memory


def create_thread_extractor(
    model: str,
    schema: typing.Union[None, BaseModel, type] = None,
    instructions: str = "You are tasked with summarizing the following conversation.",
):
    class SummarizeThread(BaseModel):
        """Summarize the thread."""

        title: str
        summary: str

    schema_ = schema or SummarizeThread
    extractor = create_extractor(model, tools=[schema_], tool_choice="any")

    async def summarize_conversation(messages: list[AnyMessage]):
        id_ = str(uuid.uuid4())
        messages = [
            {"role": "system", "content": instructions},
            {
                "role": "user",
                "content": f"Summarize the conversation below:\n\n"
                f"<conversation_{id_}>\n{_get_conversation}\n</conversation_{id_}>",
            },
        ]
        response = await extractor.ainvoke(messages)
        result = response["responses"][0]
        if isinstance(result, schema_):
            return result
        return result.model_dump(mode="json")

    return summarize_conversation


_MEMORY_INSTRUCTIONS = """You are tasked with extracting or upserting memories for all entities, concepts, etc.

Extract all important facts or entities. If an existing MEMORY is incorrect or outdated, update it based on the new information."""


@typing.overload
def create_memory_enricher(
    model: str,
    *,
    instructions: str = _MEMORY_INSTRUCTIONS,
    enable_inserts: bool = True,
) -> typing.Callable[
    [list[AnyMessage], typing.Optional[list[str]]], typing.Awaitable[list[str]]
]: ...


@typing.overload
def create_memory_enricher(
    model: str,
    *,
    schemas: list,
    instructions: str = _MEMORY_INSTRUCTIONS,
    enable_inserts: bool = True,
) -> typing.Callable[
    [
        list[AnyMessage],
        typing.Optional[
            typing.Union[
                list[tuple[str, BaseModel]],
                list[tuple[str, str, dict]],
            ]
        ],
    ],
    typing.Awaitable[tuple[str, BaseModel]],
]: ...


def create_memory_enricher(
    model: str | BaseChatModel,
    *,
    schemas: list | None = None,
    instructions: str = _MEMORY_INSTRUCTIONS,
    enable_inserts: bool = True,
):
    model = model if isinstance(model, BaseChatModel) else init_chat_model(model)
    str_type = False
    if schemas is None:

        class Memory(BaseModel):
            """Call this tool to extract memories for things like preferences, instructions, important context, events, and anything else you want to remember about for future conversations."""

            content: str

        schemas = [Memory]
        str_type = True
    extractor = create_extractor(
        model, tools=schemas, tool_choice="any", enable_inserts=enable_inserts
    )

    async def extract(
        messages: list[AnyMessage],
        existing: typing.Optional[
            typing.Union[
                list[str],
                list[tuple[str, BaseModel]],
                list[tuple[str, str, dict]],
            ]
        ] = None,
    ):
        id_ = str(uuid.uuid4())
        coerced = [
            {"role": "system", "content": instructions},
            {
                "role": "user",
                "content": f"Extract all important facts or entities. "
                "If an existing MEMORY is incorrect or outdated, update it based"
                " on the new information."
                f"<conversation_{id_}>\n{_get_conversation(messages)}\n</conversation_{id_}>",
            },
        ]
        if str_type and existing and all(isinstance(ex, str) for ex in existing):
            existing = [(str(uuid.uuid4()), Memory(content=ex)) for ex in existing]
        response = await extractor.ainvoke({"messages": coerced, "existing": existing})
        result = [
            (rmeta.get("json_doc_id", str(uuid.uuid4())), r)
            for r, rmeta in zip(response["responses"], response["response_metadata"])
        ]
        if str_type:
            return [r[1].content for r in result]
        return result

    return extract


def create_memory_store_enricher(
    model: str | BaseChatModel,
    *,
    schemas: list,
    instructions: str = _MEMORY_INSTRUCTIONS,
    enable_inserts: bool = True,
    namespace_prefix: tuple[str, ...] = ("memories", "{user_id}"),
):
    model = model if isinstance(model, BaseChatModel) else init_chat_model(model)
    evolver = create_memory_enricher(
        model, schemas=schemas, instructions=instructions, enable_inserts=enable_inserts
    )
    search_tool = create_search_memory_tool(namespace_prefix=namespace_prefix)
    query_gen = model.bind_tools(
        [search_tool],
        tool_choice="search_memory",
    )

    namespacer = _NamespaceTemplate(namespace_prefix)

    async def manage_memories(messages: list[AnyMessage]):
        store = get_store()
        namespace = namespacer()
        convo = _get_conversation(messages)
        msg = await query_gen.ainvoke(
            f"""Generate a search query to retrieve memories based on the conversation: \n\n<convo>\n{convo}\n</convo>."""
        )
        all_search_results = await asyncio.gather(
            *(store.asearch(namespace, **tc["args"]) for tc in msg.tool_calls)
        )
        memories = [
            (r.key, r.value["kind"], r.value["content"])
            for search_results in all_search_results
            for r in search_results
        ]
        new_memories = await evolver(messages, existing=memories)
        put_kwargs = [
            {
                "namespace": namespace,
                "key": key,
                "value": {
                    "kind": content.__repr_name__(),
                    "content": content.model_dump(mode="json"),
                },
            }
            for key, content in new_memories
        ]
        await asyncio.gather(
            *(
                store.aput(
                    **kwargs,
                )
                for kwargs in put_kwargs
            )
        )

        return [kwargs for kwargs in put_kwargs]

    return manage_memories


_DEFAULT_RECOMMENDATION_PROMPT = """You are reviewing the performance of an AI assistant in a given interaction. 

## Instructions

The current prompt that was used for the session is provided below.

<current_prompt>
{prompt}
</current_prompt>

The developer provided the following instructions around when and how to update the prompt:

<update_instructions>
{update_instructions}
</update_instructions>

## Session data

Analyze the following sessions (and any associated user feedback) (either conversations with a user or other work that was performed by the assistant):

<sessions>
{sessions}
</sessions>

## Feedback

The following feedback is provided for this session:

<feedback>
{feedback}
</feedback>

## Task

Analyze the conversation, including the user’s request and the assistant’s response, and evaluate:
1. How effectively the assistant fulfilled the user’s intent.
2. Where the assistant might have deviated from user expectations or the desired outcome.
3. Specific areas (correctness, completeness, style, tone, alignment, etc.) that need improvement.

Then, provide clear and specific recommendations for how to improve the prompt so that future responses better satisfy user needs. 
Focus on actionable changes and be concrete.

1. Summarize the key successes and failures in the assistant’s response. 
2. Identify which failure mode(s) best describe the issues (examples: style mismatch, unclear or incomplete instructions, flawed logic or reasoning, hallucination, etc.).
3. Based on these failure modes, recommend the most suitable edit strategy. For example, consider::
   - Use synthetic few-shot examples for style or clarifying decision boundaries.
   - Use explicit instruction updates for conditionals, rules, or logic fixes.
   - Insert references or constraints to reduce hallucinations.
   - Provide step-by-step reasoning guidelines for multi-step logic problems.

4. Provide detailed, concrete suggestions for how to update the prompt accordingly.


First think through the conversation and critique the current behavior.
If you believe the prompt needs to further adapt to the target context, provide precise recommendations.
Otherwise, mark `warrants_adjustment` as False and respond with 'No recommendations.'"""


DEFAULT_METAPROMPT = """You are optimizing a prompt to handle its target task more effectively.

<current_prompt>
{current_prompt}
</current_prompt>

We hypothesize the current prompt underperforms for these reasons:

<hypotheses>
{hypotheses}
</hypotheses>

Based on these hypotheses, we recommend the following adjustments:

<recommendations>
{recommendations}
</recommendations>

Respond with the updated prompt:"""


def create_prompt_optimizer(
    model: str | BaseChatModel, metaprompt: str = DEFAULT_METAPROMPT
):
    @ls.traceable
    async def react_agent(model: str | BaseChatModel, inputs: str, n=5):
        messages = [
            {"role": "user", "content": inputs},
        ]
        just_think = create_extractor(
            model,
            tools=[think, critique],
            tool_choice="any",
        )
        any_chain = create_extractor(
            model,
            tools=[think, critique, recommend],
            tool_choice="any",
        )
        final_chain = create_extractor(
            model,
            tools=[recommend],
            tool_choice="recommend",
        )
        for ix in range(n):
            if ix == n - 1:
                chain = final_chain
            elif ix == 0:
                chain = just_think
            else:
                chain = any_chain
            response = await chain.ainvoke(messages)
            final_response = next(
                (r for r in response["responses"] if r.__repr_name__() == "recommend"),
                None,
            )
            if final_response:
                return final_response
            msg: AIMessage = response["messages"][-1]
            messages.append(msg)
            ids = [tc["id"] for tc in (msg.tool_calls or [])]
            for id_ in ids:
                messages.append({"role": "tool", "content": "", "tool_call_id": id_})

        raise ValueError(f"Failed to generate response after {n} attempts")

    def think(thought: str):
        """First call this to reason over complicated domains, uncover hidden input/output patterns, theorize why previous hypotheses failed, and creatively conduct error analyses (e.g., deep diagnostics/recursively analyzing "why" something failed). List characteristics of the data generating process you failed to notice before. Hypothesize fixes, prioritize, critique, and repeat calling this tool until you are confident in your next solution."""
        return "Take as much time as you need! If you're stuck, take a step back and try something new."

    def critique(criticism: str):
        """Then, critique your thoughts and hypotheses. Identify flaws in your previous hypotheses and current thinking. Forecast why the hypotheses won't work. Get to the bottom of what is really driving the problem. This tool returns no new information but gives you more time to plan."""
        return "Take as much time as you need. It's important to think through different strategies."

    def recommend(
        warrants_adjustment: bool,
        hypotheses: str | None = None,
        full_recommendations: str | None = None,
    ):
        """Once you've finished thinking, decide whether the session indicates the prompt should be adjusted.
        If so, hypothesize why the prompt is inadequate and provide a clear and specific recommendation for how to improve the prompt.
        If not, respond with 'No recommendations.'"""

    @ls.traceable
    async def update_prompt(
        hypotheses: str,
        recommendations: str,
        current_prompt: str,
        update_instructions: str,
    ):
        schema = _prompt_schema(current_prompt)

        extractor = create_extractor(
            model,
            tools=[schema],
            tool_choice="OptimizedPromptOutput",
        )
        result = await extractor.ainvoke(
            metaprompt.format(
                current_prompt=current_prompt,
                recommendations=recommendations,
                hypotheses=hypotheses,
            )
        )
        return result["responses"][0].improved_prompt

    @ls.traceable
    async def process_session(
        sessions: (
            list[list[AnyMessage]]
            | list[AnyMessage]
            | list[tuple[list[AnyMessage], str]]
            | tuple[list[AnyMessage], str]
            | str
        ),
        prompt: str,
        feedback: str = "",
        update_instructions: str = "",
    ):
        if not sessions:
            return prompt
        elif isinstance(sessions, str):
            sessions = sessions
        else:
            sessions = format_sessions(sessions)

        inputs = _DEFAULT_RECOMMENDATION_PROMPT.format(
            sessions=sessions,
            feedback=feedback,
            prompt=prompt,
            update_instructions=update_instructions,
        )
        result = await react_agent(model, inputs)
        if result.warrants_adjustment:
            return await update_prompt(
                result.hypotheses,
                result.full_recommendations,
                prompt,
                update_instructions,
            )
        return prompt

    return process_session


class Prompt(TypedDict):
    name: str
    prompt: str
    update_instructions: str
    when_to_update: str | None


def create_multi_prompt_optimizer(model: str | BaseChatModel):
    _optimizer = create_prompt_optimizer(model)

    @ls.traceable
    async def process_multi_prompt_sessions(
        sessions: (
            list[list[AnyMessage]]
            | list[AnyMessage]
            | list[tuple[list[AnyMessage], str]]
            | tuple[list[AnyMessage], str]
            | str
        ),
        prompts: list[Prompt],
    ):
        choices = [p["name"] for p in prompts]
        sessions = format_sessions(sessions)

        class Classify(BaseModel):
            """Classify which prompts merit updating for this conversation."""

            reasoning: str = Field(
                description="Reasoning for classifying which prompts merit updating. Cite any relevant evidence."
            )

            which: list[str] = Field(
                description=f"List of prompt names that should be updated. Must be one or more of: {choices}"
            )

            @model_validator(mode="after")
            def validate_choices(self) -> "Classify":
                invalid = set(self.which) - set(choices)
                if invalid:
                    raise ValueError(
                        f"Invalid choices: {invalid}. Must be one of: {choices}"
                    )
                return self

        classifier = create_extractor(model, tools=[Classify], tool_choice="Classify")
        prompts_str = "\n\n".join(f"{p['name']}: {p}" for p in prompts)
        result = await classifier.ainvoke(
            f"""Analyze the following sessions and decide which prompts ought to be updated to improve the performance on future sessions:
{sessions}

Below are the prompts being optimized:
{prompts_str}
Consider any instructions on when_to_update when making a decision.
"""
        )
        to_update = result["responses"][0].which
        which_to_update = [p for p in prompts if p["name"] in to_update]
        results = await asyncio.gather(
            *(
                _optimizer(
                    sessions,
                    prompt=p["prompt"],
                    update_instructions=p.get("update_instructions", ""),
                )
                for p in which_to_update
            )
        )
        updated = {p["name"]: r for p, r in zip(which_to_update, results)}
        # Return the final prompts
        final = []
        for p in prompts:
            if p["name"] in updated:
                final.append({**p, "prompt": updated[p["name"]]})
            else:
                final.append(p)
        return final

    return process_multi_prompt_sessions


class _NamespaceTemplate:
    __slots__ = ("template", "vars")

    def __init__(self, template: tuple[str, ...]):
        self.template = template
        self.vars = {
            ix: _get_key(ns)
            for ix, ns in enumerate(template)
            if _get_key(ns) is not None
        }

    def __call__(self, config: RunnableConfig | None = None):
        config = config or get_config()
        if self.vars:
            configurable = config["configurable"] if "configurable" in config else {}
            return tuple(
                configurable.get(self.vars[ix], ns) if ix in self.vars else ns
                for ix, ns in enumerate(self.template)
            )
        else:
            return self.template


def _get_key(ns: str):
    return ns.strip(r"{}") if isinstance(ns, str) and ns.startswith("{") else None


def _get_conversation(messages: list):
    merged = merge_message_runs(messages)
    return "\n\n".join(m.pretty_repr() for m in merged)


def format_sessions(
    sessions: (
        list[list[AnyMessage]]
        | list[AnyMessage]
        | list[tuple[list[AnyMessage], str]]
        | tuple[list[AnyMessage], str]
    )
):
    # Get into list[tuple[list[AnyMessage], str]]
    if not sessions:
        return ""
    # TODO: Handle others
    if isinstance(sessions, str):
        sessions = [(sessions, "")]
    elif isinstance(sessions, list) and isinstance(sessions[0], list):
        sessions = [(session, "") for session in sessions]
    elif isinstance(sessions, tuple) and isinstance(sessions[0], list):
        sessions = [sessions]
    acc = []
    ids_ = [uuid.uuid4().hex for _ in sessions]
    for id_, (session, feedback) in zip(ids_, sessions):
        if feedback:
            feedback = (
                f"\n\nFeedback for session {id_}:\n<FEEDBACK>\n{feedback}\n</FEEDBACK>"
            )
        acc.append(
            f"<session_{id_}>\n{_get_conversation(session)}{feedback}\n</session_{id_}>"
        )
    return "\n\n".join(acc)


def _get_var_healer(vars: set[str], all_required: bool = False):
    var_to_uuid = {f"{{{v}}}": uuid.uuid4().hex for v in vars}
    uuid_to_var = {v: k for k, v in var_to_uuid.items()}

    def escape(input_string: str) -> str:
        result = re.sub(r"(?<!\{)\{(?!\{)", "{{", input_string)
        result = re.sub(r"(?<!\})\}(?!\})", "}}", result)
        return result

    if not vars:
        return escape

    mask_pattern = re.compile("|".join(map(re.escape, var_to_uuid.keys())))
    unmask_pattern = re.compile("|".join(map(re.escape, var_to_uuid.values())))

    strip_to_optimize_pattern = re.compile(
        r"<TO_OPTIMIZE.*?>|</TO_OPTIMIZE>", re.MULTILINE | re.DOTALL
    )

    def assert_all_required(input_string: str) -> str:
        if not all_required:
            return input_string

        missing = [var for var in vars if f"{{{var}}}" not in input_string]
        if missing:
            raise ValueError(f"Missing required variable: {', '.join(missing)}")

        return input_string

    def mask(input_string: str) -> str:
        return mask_pattern.sub(lambda m: var_to_uuid[m.group(0)], input_string)

    def unmask(input_string: str) -> str:
        return unmask_pattern.sub(lambda m: uuid_to_var[m.group(0)], input_string)

    def pipe(input_string: str) -> str:
        return unmask(
            strip_to_optimize_pattern.sub(
                "", escape(mask(assert_all_required(input_string)))
            )
        )

    return pipe


def _prompt_schema(
    original_prompt: str,
):
    required_variables = set(re.findall(r"\{(.+?)\}", original_prompt, re.MULTILINE))
    if required_variables:
        variables_str = ", ".join(f"{{{var}}}" for var in required_variables)
        prompt_description = (
            f" The prompt section being optimized contains the following f-string variables to be templated in: {variables_str}."
            " You must retain all of these variables in your improved prompt. No other input variables are allowed."
        )
    else:
        prompt_description = (
            " The prompt section being optimized contains no input f-string variables."
            " Any brackets {{ foo }} you emit will be escaped and not used."
        )

    pipeline = _get_var_healer(set(required_variables), all_required=True)

    class OptimizedPromptOutput(BaseModel):
        """Schema for the optimized prompt output."""

        analysis: str = Field(
            description="First, analyze the current results and plan improvements to reconcile them."
        )
        improved_prompt: typing.Optional[str] = Field(
            description="Finally, generate the full updated prompt to address the identified issues. "
            f" <TO_OPTIMIZE> and </TO_OPTIMIZE> tags, in f-string format. Do not include <TO_OPTIMIZE> in your response. {prompt_description}"
        )

        @model_validator(mode="before")
        @classmethod
        def validate_input_variables(cls, data: typing.Any) -> typing.Any:
            assert "improved_prompt" in data
            data["improved_prompt"] = pipeline(data["improved_prompt"])
            return data

    return OptimizedPromptOutput

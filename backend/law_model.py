import uuid
from typing import Sequence, List, Any, Dict, Tuple, Optional

from llama_index.core.agent import CustomSimpleAgentWorker
from llama_index.core.base.llms.types import CompletionResponse
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.tools import ToolOutput
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.bridge.pydantic import Field
from llama_index.core.agent.types import Task, TaskStep
from llama_index.core.chat_engine.types import AgentChatResponse
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.llms.text_generation_inference import TextGenerationInference

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)


class SimpleLLMAgentWorker(CustomSimpleAgentWorker):
    """A simple agent worker that uses a LLM for chat"""

    prefix_message: List[ChatMessage] = Field(default_factory=list,
                                              description="Prefix messages")

    def get_all_messages(self, task: Task) -> List[ChatMessage]:

        return (self.prefix_message + task.memory.get(input=task.input) +
                task.extra_state["new_memory"].get_all())

    def _initialize_state(self, task: Task, **kwargs: Any) -> Dict[str, Any]:
        pass

    def initialize_step(self, task: Task, **kwargs: Any) -> TaskStep:

        sources: List[ToolOutput] = []
        # temporary memory for new messages
        new_memory = ChatMemoryBuffer.from_defaults()
        # initialize task state
        task_state = {
            "sources": sources,
            "n_function_calls": 0,
            "new_memory": new_memory,
        }
        task.extra_state.update(task_state)

        return TaskStep(
            task_id=task.task_id,
            step_id=str(uuid.uuid4()),
            input=task.input,
        )

    def _run_step(self,
                  state: Dict[str, Any],
                  task: Task,
                  input: str | None = None) -> Tuple[AgentChatResponse, bool]:

        if input is not None:
            user_message = ChatMessage(content=input, role=MessageRole.USER)
            task.extra_state["new_memory"].put(user_message)
            if self.verbose:
                print(f"Added user message to memory: {input}")

        response = self.llm.chat(self.get_all_messages(task))
        # TODO: whether enable function call

        if self.verbose and response.message.content:
            print("=== LLM Response ===")
            print(str(response.message.content))

        task.extra_state["new_memory"].put(response.message)

        agent_response = AgentChatResponse(
            response=str(response.message.content),
            sources=task.extra_state["sources"],
        )

        return agent_response, True

    def _finalize_task(self, state: Dict[str, Any], **kwargs: Any) -> None:
        pass

    def finalize_task(self, task: Task, **kwargs: Any) -> None:
        # add new messages to memory
        task.memory.set(task.memory.get_all() +
                        task.extra_state["new_memory"].get_all())
        # reset new memory
        task.extra_state["new_memory"].reset()


class HuggingFaceLLMModified(HuggingFaceLLM):
    """A modified HuggingFace LLM for complete"""

    def complete(self,
                 prompt: str,
                 formatted: bool = False,
                 **kwargs: Any) -> CompletionResponse:

        if '[INST]' not in prompt:
            prompt = self.messages_to_prompt(
                [ChatMessage(content=prompt, role=MessageRole.USER)])
        return super().complete(prompt, formatted, **kwargs)


def prepare_law_llm(
        model_name: str = "Equall/Saul-7B-Instruct-v1"
) -> HuggingFaceLLMModified:
    """Prepare a law LLM with the given model name

    :params model_name: the model name
    :return: a law LLM
    """

    # load the model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map='auto',
        trust_remote_code=True,
        use_safetensors=True,
        quantization_config=BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype="bfloat16",
            bnb_4bit_use_double_quant=False,
            bnb_4bit_quant_type='nf4',
            llm_int8_skip_modules=['lm_head'],
        ),
    )

    # connect to llama-index
    def messages_to_prompt(messages: Sequence[ChatMessage]):

        messages = [{
            'role': msg.role.value,
            'content': msg.content.strip()
        } for msg in messages]

        prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        return prompt

    law_llm = HuggingFaceLLMModified(
        model_name=model_name,
        model=model,
        tokenizer=tokenizer,
        messages_to_prompt=messages_to_prompt,
    )

    return law_llm


def prepare_law_agent(
    model_name: str,
    model_url: Optional[str] = None,
    verbose: bool = False,
    **kwargs,
):
    """Prepare a law agent with the given model name

    :params model_name: the model name
    :params model_url: the model url; if passed, use TGI, else load locally
    :params verbose: verbose mode
    :params kwargs: additional arguments for `as_agent`
    :return: a law agent
    """

    if model_url:
        law_llm = TextGenerationInference(model_url=model_url, token=False)
    else:
        law_llm = prepare_law_llm(model_name)

    # create agent
    law_agent_worker = SimpleLLMAgentWorker(
        tools=[],
        llm=law_llm,
        verbose=verbose,
    )
    law_agent = law_agent_worker.as_agent(**kwargs)

    return law_agent

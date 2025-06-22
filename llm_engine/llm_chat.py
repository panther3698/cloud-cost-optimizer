from langchain_community.llms import AzureOpenAI, OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from llm_engine.prompt_templates import prompt_templates

def chat_with_llm(question_type: str, cost_data: str, persona: str = "FinOps", use_azure: bool = True, **llm_kwargs) -> str:
    """
    Uses LangChain to answer a question about cost data using the appropriate prompt and LLM.

    Args:
        question_type (str): One of the keys in prompt_templates (e.g., 'explain_cost_spikes')
        cost_data (str): Stringified cost data or summary
        persona (str): Persona for prompt (e.g., 'FinOps', 'CIO')
        use_azure (bool): If True, use Azure OpenAI; else use local Mistral/OpenAI
        **llm_kwargs: Additional kwargs for LLM initialization

    Returns:
        str: Human-readable insights from the LLM
    """
    # Select prompt template
    if question_type not in prompt_templates:
        raise ValueError(f"Unknown question_type: {question_type}")
    prompt_str = prompt_templates[question_type]["template"]
    prompt = PromptTemplate.from_template(prompt_str + "\n\nCost Data:\n{cost_data}")

    # Choose LLM
    if use_azure:
        llm = AzureOpenAI(**llm_kwargs)
    else:
        llm = OpenAI(**llm_kwargs)  # Replace with Mistral integration if available

    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(persona=persona, cost_data=cost_data)
    return response
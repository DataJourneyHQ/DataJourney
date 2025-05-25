import os
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI

# NOTE: Using GitHub models here (add your preferred token attribute)

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

llm = OpenAI(
    base_url=endpoint,
    api_key=token,
    model=model_name,
    temperature=0.7
)

# Step 2: Define a Prompt Template
prompt = PromptTemplate(
    input_variables=["question"],
    template="You are a helpful assistant. Answer the following question in a clear and concise way: {question}"
)


# Step 3: Create a Function to Get AI Responses
def get_answer(question):
    # Format the prompt with the input question
    formatted_prompt = prompt.format(question=question)

    # Use the LLM to generate a response
    response = llm(formatted_prompt)
    return response


# Example Usage
if __name__ == "__main__":
    question = "What is LangChain and why is it useful?"
    answer = get_answer(question)
    print("AI Speaks:\n", answer)

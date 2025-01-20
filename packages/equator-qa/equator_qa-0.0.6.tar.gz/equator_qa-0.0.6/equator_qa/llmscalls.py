import os
import json
from loguru import logger
import requests
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv
from prompts import get_student_prompt


load_dotenv()


def call_groq_evaluator_api(evaluator_model, student_answer, evaluator_system_prompt):
    """
    Evaluates a student's answer using the Groq Evaluator API.

    This function sends the student's answer along with a system prompt to the Groq Evaluator API
    and retrieves the evaluation response.

    Args:
        evaluator_model (str):
            The identifier of the evaluator model to use.
        
        student_answer (str):
            The student's answer to be evaluated.
        
        evaluator_system_prompt (List[Dict[str, str]]):
            A list of messages defining the system prompt for the evaluator.

    Returns:
        Optional[Tuple[str, str]]:
            A tuple containing the `student_answer` and the evaluator's feedback if successful.
            Returns `None` if the evaluation fails.
    
    Example:
        ```python
        evaluator_model = "groq-eval-model-v1"
        student_answer = "The capital of France is Paris."
        evaluator_system_prompt = [
            {"role": "system", "content": "You are an evaluator for geography questions."},
            {"role": "user", "content": "Evaluate the following student answer for correctness and completeness."}
        ]

        result = call_groq_evaluator_api(evaluator_model, student_answer, evaluator_system_prompt)
        if result:
            answer, feedback = result
            print(f"Answer: {answer}\nFeedback: {feedback}")
        else:
            print("Evaluation failed.")
        ```
    
    Notes:
        - Ensure that the `GROQ_API_KEY` environment variable is set.
        - The `Groq` client library must be installed and imported.
        - Handle sensitive data securely.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    gorq_api = Groq(api_key=api_key)
    completion_eval = gorq_api.chat.completions.create(
        temperature=0,
        model=evaluator_model,
        messages=evaluator_system_prompt,
    )
    response_eval = completion_eval.choices[0].message.content

    if response_eval:
        logger.info(f"call_groq_evaluator_api: {response_eval}")
        return student_answer, response_eval
    else:
        logger.error("Failed to get evaluator response.")
        return None




def call_ollama_evaluator_api(evaluator_model, student_answer, evaluator_system_prompt):
    """
    Evaluates a student's answer using the Ollama Evaluator API.

    Sends the student's answer and a system prompt to the Ollama API and retrieves the evaluation response.

    Args:
        evaluator_model (str):
            The evaluator model to use.
        
        student_answer (str):
            The student's answer to be evaluated.
        
        evaluator_system_prompt (List[Dict[str, str]]):
            A list of messages defining the system prompt for the evaluator.

    Returns:
        Tuple[str, str]:
            A tuple containing the `student_answer` and the evaluator's feedback.

    Example:
        ```python
        evaluator_model = "ollama-model-v1"
        student_answer = "The capital of France is Paris."
        evaluator_system_prompt = [
            {"role": "system", "content": "You are an evaluator for geography questions."},
            {"role": "user", "content": "Evaluate the following student answer for correctness and completeness."}
        ]

        result = call_ollama_evaluator_api(evaluator_model, student_answer, evaluator_system_prompt)
        if result:
            answer, feedback = result
            print(f"Answer: {answer}\nFeedback: {feedback}")
        else:
            print("Evaluation failed.")
        ```

    Notes:
        - Ensure the Ollama API is running and accessible at the specified URL.
        - Handle sensitive data securely.
    """
    url = "http://localhost:11434/api/chat"
    payload = {"model": evaluator_model, "messages": evaluator_system_prompt}
    # Make a single POST request
    response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        stream=True,
    )

    complete_message = ""

    # Read the streamed response line by line
    for line in response.iter_lines():
        if line:
            chunk = json.loads(line.decode("utf-8"))
            # Safely retrieve content if present
            if "message" in chunk and "content" in chunk["message"]:
                complete_message += chunk["message"]["content"]

            # If the API signals completion
            if chunk.get("done"):
                break

    logger.info(f"Complete message: {complete_message}")
    return student_answer, complete_message




def call_openrouter_student_api(full_prompt_student, model_path):
    """
    Sends a student's prompt to the OpenRouter API and retrieves the response.

    Args:
        full_prompt_student (str):
            The complete prompt from the student that needs to be processed.
        
        model_path (str):
            The path or identifier of the model to be used for generating the response.

    Returns:
        str:
            The response generated by the OpenRouter API based on the provided prompts.

    Example:
        ```python
        full_prompt_student = "Explain the theory of relativity."
        model_path = "gpt-4"

        response = call_openrouter_student_api(full_prompt_student, model_path)
        print(response)
        ```
    
    Notes:
        - Ensure the `OPENROUTER_KEY` environment variable is set with a valid API key.
        - The `OpenAI` client should be properly installed and imported.
        - The function assumes that `get_student_prompt` is defined and returns the appropriate message format.
    """
    api_key = os.environ.get("OPENROUTER_KEY")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    model_path = str(model_path)

    # Make the API call
    completion = client.chat.completions.create(
        model=model_path,
        messages=get_student_prompt(full_prompt_student),
    )
    # last_api_call_time = time.time()  # Update the time of the last API call
    response = completion.choices[0].message.content
    logger.info(f"call_openrouter_student_api: {response}")
    return response



def call_ollama_student_api(full_prompt_student, student_model):
    """
    Sends a student's prompt to the Ollama API and retrieves the response.

    Args:
        full_prompt_student (str):
            The student's prompt to be processed.
        
        student_model (str):
            The model to use for generating the response.

    Returns:
        str:
            The response from the Ollama API.

    Example:
        ```python
        response = call_ollama_student_api("Explain photosynthesis.", "ollama-model-v1")
        print(response)
        ```
    
    Notes:
        - Ensure the Ollama API is running and accessible at the specified URL.
        - The `get_student_prompt` function should be defined to format the messages correctly.
    """
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": student_model,
        "messages": get_student_prompt(full_prompt_student),
    }

    response = requests.post(
        url=url,
        json=payload,
        headers={"Content-Type": "application/json"},
        stream=True,
    )
    complete_message = ""
    for line in response.iter_lines():
        if line:
            chunk = json.loads(line.decode("utf-8"))
            complete_message += chunk["message"]["content"]
            if chunk.get("done"):
                break
    logger.info(f"ollama student student api = {complete_message}")
    if complete_message:
        return complete_message

    
def call_ollama_student_docker(full_prompt_student, student_model):
    """
    Sends a student's prompt to the Ollama Docker API and retrieves the response.

    Args:
        full_prompt_student (str): The student's prompt to be processed.
        student_model (str): The model to use for generating the response.

    Returns:
        Optional[str]:
            The response from the Ollama API if successful, otherwise `None`.

    Example:
        ```python
        response = call_ollama_student_docker("Explain photosynthesis.", "ollama-model-v1")
        if response:
            print(response)
        else:
            print("Evaluation failed.")
        ```
    
    Notes:
        - Ensure the Ollama API is running and accessible at the specified URL.
        - The `get_student_prompt` function should be defined to format the messages correctly.
    """
    url = "http://localhost:11435/api/chat"
    payload = {
        "model": student_model,
        "messages": get_student_prompt(full_prompt_student),
    }

    response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        stream=True,
    )
    complete_message = ""
    for line in response.iter_lines():
        if line:
            chunk = json.loads(line.decode("utf-8"))
            complete_message += chunk["message"]["content"]
            if chunk.get("done"):
                break
    if complete_message:
        logger.info(f"Student answer = {complete_message}")
        return complete_message
    return None

    

def call_groq_student_api(full_prompt_student, groq_student_model):
    """
    Sends a student's prompt to the Groq API and retrieves the response.

    Args:
        full_prompt_student (str):
            The student's prompt to be processed.
        groq_student_model (str):
            The model identifier to use for generating the response.

    Returns:
        Optional[str]:
            The response from the Groq API if successful, otherwise `None`.

    Example:
        ```python
        response = call_groq_student_api("Explain photosynthesis.", "groq-model-v1")
        if response:
            print(response)
        else:
            print("Evaluation failed.")
        ```
    
    Notes:
        - Ensure the `GROQ_API_KEY` environment variable is set with a valid API key.
        - The `Groq` client library must be installed and imported.
        - The `get_student_prompt` function should be defined to format the messages correctly.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    gorq_api = Groq(api_key=api_key)
    completion_eval = gorq_api.chat.completions.create(
        temperature=0,
        model=groq_student_model,
        messages=get_student_prompt(full_prompt_student),
    )
    response = completion_eval.choices[0].message.content

    if response:
        logger.info(f"call_groq_student_api: {response}")
        return response
    else:
        logger.error("Failed to get evaluator response.")
        return None

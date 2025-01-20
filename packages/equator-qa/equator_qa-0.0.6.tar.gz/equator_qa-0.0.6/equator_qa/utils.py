import os
import shutil
import uuid
import json as jn
from loguru import logger
import re
from prompts import get_evaluator_system_prompt
from equator_qa.llmscalls import (
    call_ollama_evaluator_api,
    call_groq_evaluator_api,
    call_openrouter_student_api,
    call_ollama_student_api,
    call_groq_student_api,
    call_ollama_student_docker,
)

import sqlite3

# Configure the logger
logger.add(
    "equator.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    level="DEBUG",          # Include all messages for detailed debugging
    rotation="50 MB",       # Rotate log file after it reaches 50 MB
    retention="30 days",    # Keep logs for 30 days
)

def begin_benchmark(
    execution_steps,
    student_ollama_models,
    student_groq_models,
    student_openrouter_models,
    OLLAMA_EVALUATOR_MODEL,
    GROQ_EVALUATOR_MODEL,
    vectordb_instance,
    benchmark_name,
    date_now,
    answer_rounds,
):
    """
    Initiates and manages the benchmarking process based on specified execution steps.

    Depending on the `execution_steps`, this function evaluates student models against evaluator models
    using the EQUATOR_Client. It supports various evaluation workflows, including:
    - Ollama to GROQ
    - GROQ to Ollama
    - Ollama to OpenRouter
    - Ollama to Ollama
    - GROQ to OpenRouter

    Args:
        execution_steps (str):
            Specifies the benchmarking workflow to execute (e.g., "ollama_to_groq_evaluate").
        
        student_ollama_models (List[str]):
            List of student models using the Ollama platform.
        
        student_groq_models (List[str]):
            List of student models using the GROQ platform.
        
        student_openrouter_models (List[str]):
            List of student models using the OpenRouter platform.
        
        OLLAMA_EVALUATOR_MODEL (str):
            The evaluator model identifier for Ollama evaluations.
        
        GROQ_EVALUATOR_MODEL (str):
            The evaluator model identifier for GROQ evaluations.
        
        vectordb_instance:
            Instance of the vector database used for storing and retrieving embeddings.
        
        benchmark_name (str):
            Name of the benchmark being executed.
        
        date_now (str):
            Current date in a suitable string format for folder naming.
        
        answer_rounds (int):
            Number of evaluation rounds to perform.

    Returns:
        None

    Example:
        ```python
        begin_benchmark(
            execution_steps="ollama_to_groq_evaluate",
            student_ollama_models=["ollama-model-1", "ollama-model-2"],
            student_groq_models=["groq-model-1"],
            student_openrouter_models=["openrouter-model-1"],
            OLLAMA_EVALUATOR_MODEL="ollama-eval-model",
            GROQ_EVALUATOR_MODEL="groq-eval-model",
            vectordb_instance=vector_db,
            benchmark_name="midterm_benchmark",
            date_now="2025-01-19",
            answer_rounds=5,
        )
        ```

    Notes:
        - Ensure that the `EQUATOR_Client` is correctly implemented and imported.
        - The `extract_model_parts` function should be defined to parse model identifiers.
        - Logging should be properly configured to capture informational and debug messages.
        - Directory paths for saving outputs should have the necessary write permissions.
    """
    logger.info(f"Starting benchmark execution steps -> {execution_steps}")
    
    if "ollama_to_groq_evaluate" in execution_steps:
        logger.info(f"ollama_to_groq_evaluate == execution_steps = {execution_steps}")
        for model in student_groq_models:
            student_model = model
            evaluator_model = OLLAMA_EVALUATOR_MODEL
            client = EQUATOR_Client(
                execution_steps,
                student_model,
                evaluator_model,
                vectordb_instance,
            )
            lab = "eval"  # TODO: think about a more generic way of doing this
            if student_model:
                logger.info(f"Extracted Lab name: {lab}")
                logger.info(f"student model name: {student_model}")
            else:
                logger.debug("Model name not found.")

            student_models = [student_model]
            print("1. GETTING EQUATOR Evaluator ANSWERS -> Local Student")
            logger.info("1. GETTING EQUATOR Evaluator ANSWERS -> GROQ Student")
            model_path = ""
            folder_name = f"{date_now}-{benchmark_name}"
            # answers_save_path = f"./{folder_name}/llm_outputs"
            auto_eval_save_path = f"./{folder_name}/auto_eval_outputs"
            # stats_save_path = f"./{folder_name}/tables_and_charts"
            for n in range(answer_rounds):
                print(f"\n----- Round: {n+1} of {answer_rounds} -----")
                logger.info(f"\n----- Round: {n+1} of {answer_rounds} -----")

                answer_save_path_round = f"{auto_eval_save_path}"
                client.EQUATOR_Controller(
                    model_path,
                    lab,
                    student_models,
                    answer_save_path_round=answer_save_path_round,
                    count=n,
                    prefix_replace="equator-",
                )

    elif "groq_to_ollama_evaluate" in execution_steps:
        logger.info(f"groq_to_ollama_evaluate == execution_steps = {execution_steps}")
        for model in student_ollama_models:
            evaluator_model = GROQ_EVALUATOR_MODEL
            student_model = model
            client = EQUATOR_Client(
                execution_steps,
                student_model,
                evaluator_model,
                vectordb_instance,
            )
            lab = "eval"
            if student_model:
                logger.info(f"Extracted Lab name: {lab}")
                logger.info(f"student model name: {student_model}")
            else:
                logger.debug("Model name not found.")
            student_models = [student_model]
            print("1. GETTING EQUATOR Evaluator ANSWERS -> Local Student")
            logger.info(f"1. GETTING EQUATOR Evaluator ANSWERS -> {student_model} Ollama Student")
            model_path = ""
            folder_name = f"{date_now}-{benchmark_name}"
            # answers_save_path = f"./{folder_name}/llm_outputs"
            auto_eval_save_path = f"./{folder_name}/auto_eval_outputs"
            # stats_save_path = f"./{folder_name}/tables_and_charts"
            for n in range(answer_rounds):
                print(f"\n----- Round: {n+1} of {answer_rounds} -----")
                logger.info(f"\n----- Round: {n+1} of {answer_rounds} -----")
                answer_save_path_round = f"{auto_eval_save_path}"
                client.EQUATOR_Controller(
                    model_path,
                    lab,
                    student_models,
                    answer_save_path_round=answer_save_path_round,
                    count=n,
                    prefix_replace="equator-",
                )

    elif "ollama_to_openrouter_evaluate" in execution_steps:
        logger.info(f"ollama_to_openrouter_evaluate <- execution_steps = {execution_steps}")
        for model in student_openrouter_models:
            model_path = model
            evaluator_model = OLLAMA_EVALUATOR_MODEL
            lab, student_model = extract_model_parts(model)
            lab = "eval-"
            if student_model:
                logger.info(f"Extracted Lab name: {lab}")
                logger.info(f"student model name: {student_model}")
            else:
                logger.debug("Model name not found.")
            evaluator_model = OLLAMA_EVALUATOR_MODEL
            student_models = [student_model]
            client = EQUATOR_Client(
                execution_steps,
                student_model,
                evaluator_model,
                vectordb_instance,
            )
            folder_name = f"{date_now}-{benchmark_name}"
            # answers_save_path = f"./{folder_name}/llm_outputs"
            auto_eval_save_path = f"./{folder_name}/auto_eval_outputs"
            # stats_save_path = f"./{folder_name}/tables_and_charts"
            print("1. GETTING EQUATOR LLM Evaluator ANSWERS")
            logger.info(f"1. GETTING EQUATOR Evaluator ANSWERS -> from {student_model} openrouter Student")
            for n in range(answer_rounds):
                print(f"\n----- Round: {n+1} of {answer_rounds} -----")
                logger.info(f"\n----- Round: {n+1} of {answer_rounds} -----")
                answer_save_path_round = f"{auto_eval_save_path}"
                client.EQUATOR_Controller(
                    model_path,
                    lab,
                    student_models,
                    answer_save_path_round=answer_save_path_round,
                    count=n,
                    prefix_replace="equator-",
                )

    elif "ollama_to_ollama_evaluate" in execution_steps:
        logger.info(f"groq_to_ollama_evaluate <- execution_steps {execution_steps}" )
        for model in student_ollama_models:
            evaluator_model = OLLAMA_EVALUATOR_MODEL
            student_model = model
            client = EQUATOR_Client(
                execution_steps,
                student_model,
                evaluator_model,
                vectordb_instance,
            )
            lab = "eval"
            if student_model:
                logger.info(f"Lab name: {lab}")
                logger.info(f"student model name: {student_model}")
            else:
                logger.debug("Model name not found.")
            student_models = [student_model]
            print("1. GETTING EQUATOR Evaluator ANSWERS -> Ollama Student")
            logger.info(f"1. GETTING EQUATOR Evaluator ANSWERS -> from {student_model} Ollama Student")
            model_path = ""
            folder_name = f"{date_now}-{benchmark_name}"
            # answers_save_path = f"./{folder_name}/llm_outputs"
            auto_eval_save_path = f"./{folder_name}/auto_eval_outputs"
            # stats_save_path = f"./{folder_name}/tables_and_charts"
            for n in range(answer_rounds):
                print(f"\n----- Round: {n+1} of {answer_rounds} -----")
                logger.info(f"\n----- Round: {n+1} of {answer_rounds} -----")
                answer_save_path_round = f"{auto_eval_save_path}"
                client.EQUATOR_Controller(
                    model_path,
                    lab,
                    student_models,
                    answer_save_path_round=answer_save_path_round,
                    count=n,
                    prefix_replace="equator-",
                )

    elif "groq_to_openrouter_evaluate" in execution_steps:
        logger.info(f"groq_to_openrouter_evaluate <- execution_steps {execution_steps}" )
        for model in student_openrouter_models:
            model_path = model
            _, student_model = extract_model_parts(model)
            lab = "eval"
            if student_model:
                logger.info(f"Extracted Lab name: {lab}")
                logger.info(f"student model name: {student_model}")
            else:
                logger.debug("Model name not found.")
            student_model = student_model.replace("/", "-")

            student_models = [student_model]

            evaluator_model = GROQ_EVALUATOR_MODEL
            client = EQUATOR_Client(
                execution_steps,
                student_model,
                evaluator_model,
                vectordb_instance,
            )
            folder_name = f"{date_now}-{benchmark_name}"
            # answers_save_path = f"./{folder_name}/llm_outputs"
            auto_eval_save_path = f"./{folder_name}/auto_eval_outputs"
            # stats_save_path = f"./{folder_name}/tables_and_charts"
            print("1. GETTING BERNARD LLM Evaluator ANSWERS")
            logger.info(f"1. GETTING EQUATOR Evaluator ANSWERS -> from {student_model} openrouter Student")
            for n in range(answer_rounds):
                print(f"\n----- Round: {n+1} of {answer_rounds} -----")
                answer_save_path_round = f"{auto_eval_save_path}"
                logger.info(f"\n----- Round: {n+1} of {answer_rounds} -----")
                client.EQUATOR_Controller(
                    model_path,
                    lab,
                    student_models,
                    answer_save_path_round=answer_save_path_round,
                    count=n,
                    prefix_replace="equator-",
                )

class EQUATOR_Client(object):
    """
    EQUATOR_Client handles the benchmarking process by evaluating student models against evaluator models
    using a vector database for storing and retrieving embeddings.

    Attributes:
        student_model (str): The identifier of the student model.
        evaluator_model (str): The identifier of the evaluator model.
        execution_steps (str): The workflow steps to execute.
        vectordb2: Instance of the vector database for embeddings management.
    """

    def __init__(
        self,
        execution_steps,
        student_model,
        evaluator_model,
        vectordb_instance,
    ):
        """
        Initializes the EQUATOR_Client with the necessary parameters.

        Args:
            execution_steps (str):
                Specifies the benchmarking workflow to execute (e.g., "ollama_to_groq_evaluate").
            
            student_model (str):
                The identifier of the student model to be evaluated.
            
            evaluator_model (str):
                The identifier of the evaluator model to assess the student model's performance.
            
            vectordb_instance:
                Instance of the vector database used for storing and retrieving embeddings.
        """
        self.student_model = student_model
        self.evaluator_model = evaluator_model
        self.execution_steps = execution_steps
        self.vectordb2 = vectordb_instance

    def EQUATOR_Controller(
        self,
        model_path,
        lab,
        student_models,
        answer_save_path_round,
        count,
        prefix_replace,
    ):
        """
        Controls the evaluation process by iterating through questions in the vector database,
        obtaining evaluator responses, and saving the results.

        Args:
            model_path (str):
                The path or identifier of the model to be used for generating responses.
            
            lab (str):
                The label or identifier for the current evaluation context.
            
            student_models (List[str]):
                A list of student model identifiers to be evaluated.
            
            answer_save_path_round (str):
                The directory path where the evaluation results for the current round will be saved.
            
            count (int):
                The current round count of the evaluation process.
            
            prefix_replace (str):
                A prefix string to replace or append in the output filenames for organization.
        
        Returns:
            None

        Example:
            ```python
            client = EQUATOR_Client(
                execution_steps="ollama_to_groq_evaluate",
                student_model="groq-model-1",
                evaluator_model="ollama-eval-model",
                vectordb_instance=vector_db,
            )
            client.EQUATOR_Controller(
                model_path="",
                lab="eval",
                student_models=["groq-model-1"],
                answer_save_path_round="./2025-01-19-midterm_benchmark/auto_eval_outputs",
                count=0,
                prefix_replace="equator-",
            )
            ```
        
        Notes:
            - Ensure that the `get_student_prompt`, `extract_score_from_string`, and `create_template_json` functions are defined and imported.
            - The `EQUATOR_Controller` method interacts with a SQLite database named `chroma.sqlite3`. Ensure that this database exists and is accessible.
            - Logging is used extensively for tracking the evaluation process. Ensure that the logging configuration captures the desired log levels.
            - The method currently stops processing if a question with ID "1" is encountered. Modify the stop condition as needed.
        """
        print("prefix ==", prefix_replace)

        # Path to your chroma.sqlite3 file
        db_path = "chroma.sqlite3"
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        batch_size = 100  # Define your batch size
        offset = 0  # Start offset
        stop_processing = False  # Flag to stop the outer loop
        while True:
            # Fetch a batch of results
            query = f"""
            SELECT 
                json_extract(string_value, '$.id'), 
                json_extract(string_value, '$.category'), 
                json_extract(string_value, '$.question'), 
                json_extract(string_value, '$.response') 
            FROM embedding_fulltext_search
            LIMIT {batch_size} OFFSET {offset}
            """
            logger.info(
                f"sqlite executing query with OFFSET={offset}, LIMIT={batch_size}"
            )
            cursor.execute(query)
            results = cursor.fetchall()

            # Break the loop if no more records are fetched
            if not results:
                logger.info("No more records found. Exiting.")
                break

            for row in results:
                question_id, category, question_text, response = row
                logger.info(f"Processing Question ID: {question_id}, Category: {category}, Question: {question_text}, Answer: {response}")

                # Simulate stripping and processing text
                question = question_text.strip() if question_text else ""
                human_answer = response.strip() if response else ""

                for student_model in student_models:
                    output_path = f"{answer_save_path_round}/round_{count + 1}/{prefix_replace}{self.evaluator_model+'-'}{'stu-'}{student_model}.json"
                    if model_path:
                        logger.info(f"Model Path  = {model_path}")
                    logger.info(f"student_model = {student_model}")

                    # Call your evaluator function
                    evaluator_result = self.call_evaluator(
                        model_path=model_path,
                        prompt=question,
                    )
                    if evaluator_result is None:
                        logger.error("Evaluator failed to return a result.")
                        continue

                    student_answer, evaluator_response = evaluator_result

                    score = extract_score_from_string(evaluator_response)
                    logger.info(f"score = {score}")
                    create_template_json(
                        student_model,
                        output_path,
                        question_id,
                        category,
                        human_answer,
                        question,
                        student_answer,
                        evaluator_response,
                        score,
                    )
                # Stop processing if a condition is met
                if question_id == "1":  # Replace "1" with the desired stop condition
                    logger.debug("Stop condition met. Exiting.")
                    stop_processing = True  # Set the flag to stop outer loop
                    break
            # Increment offset to fetch the next batch
            if stop_processing:
                logger.debug("Breaking the outer loop.")
                break
            offset += batch_size  # Move to the next batch

        # Close the database connection after processing
        conn.close()
        logger.info("Database connection closed.")

    # Generate student answer
    def student(self, model_path, full_prompt_student):
        """
        Retrieves a student's answer by invoking the appropriate evaluator API based on execution steps.

        Args:
            model_path (str):
                The path or identifier of the student model to be used.
            full_prompt_student (str):
                The student's prompt that needs to be processed and evaluated.

        Returns:
            Optional[str]:
                The student's answer returned by the evaluator API if successful, otherwise `None`.

        Example:
            ```python
            response = client.student("ollama-model-v1", "Explain photosynthesis.")
            if response:
                print(f"Student Answer: {response}")
            else:
                print("Failed to retrieve student answer.")
            ```
        
        Notes:
            - Ensure that the `get_student_prompt` function is defined and properly formats the messages.
            - The evaluator functions (`call_openrouter_student_api`, `call_ollama_student_api`, etc.) must be imported and accessible.
            - Logging is used to track the execution flow and responses.
        """
        model_path = str(model_path)
        if model_path:
            logger.info(f"Model Path = {model_path}")
        logger.info(f"Execution steps = {self.execution_steps}")
        
        if "ollama_to_openrouter_evaluate" in self.execution_steps:
            logger.info(f"call_openrouter_student_api <-  {self.execution_steps}")
            response = call_openrouter_student_api(
                full_prompt_student,  model_path
            )
            return response

        elif "groq_to_ollama_evaluate" in self.execution_steps:
            logger.info(f"call_ollama_student_api  <- {self.execution_steps}")
            response = call_ollama_student_api(
                full_prompt_student, self.student_model
            )
            logger.info(f"call_ollama_student_api -> response {response}")            
            return response

        elif "ollama_to_ollama_evaluate" in self.execution_steps:
            logger.info(f"call_ollama_student_docker <- {self.execution_steps}")
        
            response = call_ollama_student_docker(
                full_prompt_student, self.student_model
            )

            logger.info(f"call_ollama_student_docker -> response {response}")
            return response

        elif "ollama_to_groq_evaluate" in self.execution_steps:
            logger.info(f"call_groq_student_api <- {self.execution_steps}")           

            response = call_groq_student_api(
                full_prompt_student, self.student_model
            )
            logger.info(f"call_groq_student_api -> response {response}")            
            return response

        elif "groq_to_openrouter_evaluate" in self.execution_steps:
            logger.info(f"call_openrouter_student_api <- {self.execution_steps}")

            response = call_openrouter_student_api(
                full_prompt_student, model_path
            )
            logger.info(f"call_openrouter_student_api -> response {response}")
            return response

        return None

    def call_evaluator(self, model_path, prompt):
        """
        Calls the appropriate evaluator API based on the execution steps and retrieves the evaluation response.

        Args:
            model_path (str):
                The path or identifier of the evaluator model to be used.
            prompt (str):
                The prompt/question to be evaluated.

        Returns:
            Optional[Tuple[str, str]]:
                A tuple containing the student's answer and the evaluator's response if successful, otherwise `None`.
        """
        results = self.vectordb2.retrieve_embedding(prompt)
        if results is None:
            logger.error("Failed to retrieve similar documents.")
            return None
        context = ""
        if "documents" in results and results["documents"]:
            metadatas = results.get("metadatas", [])[0]
            for metadata in metadatas:
                context += f"Question: {metadata.get('question', '')}\n"
                context += f"Answer: {metadata.get('response', '')}\n\n"
            # logger.info(context)
            logger.info(f"Similar documents found. -> {context}")
        else:
            logger.warning("No similar documents found.")

        student_answer = self.student(model_path, prompt)
        if not student_answer:
            logger.error("Failed to get Student Answer.")
            return None

        logger.info(f"Student Answer: {student_answer}")

        evaluator_system_prompt = get_evaluator_system_prompt(context, student_answer)

        if "ollama_to_groq_evaluate" in self.execution_steps:
            logger.info(f"call_ollama_evaluator_api <- {self.execution_steps}")          
            student_answer, eval_response = call_ollama_evaluator_api(
                self.evaluator_model, student_answer, evaluator_system_prompt
            )
            return student_answer, eval_response

        elif (
            "ollama_to_ollama_evaluate" in self.execution_steps
            or "ollama_to_openrouter_evaluate" in self.execution_steps
        ):
            logger.info(f"call_ollama_evaluator_api <- {self.execution_steps}")

            student_answer, eval_response = call_ollama_evaluator_api(
                self.evaluator_model, student_answer, evaluator_system_prompt
            )
            return student_answer, eval_response

        elif (
            "groq_to_ollama_evaluate" in self.execution_steps
            or "groq_to_openrouter_evaluate" in self.execution_steps
        ):
            logger.info(f"call_groq_evaluator_api <- {self.execution_steps}")
             
            student_answer, eval_response = call_groq_evaluator_api(
                self.evaluator_model, student_answer, evaluator_system_prompt
            )
            return student_answer, eval_response

        elif "groq_to_openrouter_evaluate" in self.execution_steps:
            logger.info(f"call_openrouter_student_api <- {self.execution_steps}")
         
            student_answer, eval_response = call_openrouter_student_api(
                self.evaluator_model, student_answer, evaluator_system_prompt
            )
            return student_answer, eval_response

        return None

def extract_model_parts(model_string):
    """
    Splits a model string into its constituent parts based on a predefined pattern.
    
    This function uses a regular expression to extract two parts from the `model_string`,
    separated by a forward slash (`/`). If the string matches the pattern, it returns a tuple
    containing both parts. Otherwise, it returns `(None, None)`.
    
    Args:
        model_string (str):
            The model identifier string to be split. Expected format is "part1/part2",
            where neither part contains a forward slash (`/`) or colon (`:`).
    
    Returns:
        Tuple[Optional[str], Optional[str]]:
            A tuple containing the two extracted parts of the model string. Returns `(None, None)`
            if the input does not match the expected pattern.
    
    Example:
        ```python
        part1, part2 = extract_model_parts("category/model")
        print(part1)  # Output: "category"
        print(part2)  # Output: "model"
        
        part1, part2 = extract_model_parts("invalidmodelstring")
        print(part1)  # Output: None
        print(part2)  # Output: None
        ```
    
    Notes:
        - Ensure that the `model_string` follows the "part1/part2" format to successfully extract both parts.
        - This function does not handle cases where there are multiple slashes or colons in the `model_string`.
    """
    # Define the regex pattern to extract both parts
    pattern = r"^([^/]+)/([^/:]+)"
    # Use re.match to find the model parts
    match = re.match(pattern, model_string)
    if match:
        return match.group(1), match.group(2)
    return None, None

def sanitize_string(value):
    """
    Escapes curly braces in strings to prevent issues with format specifiers in logging.
    """
    if isinstance(value, str):
        return value.replace("{", "{{").replace("}", "}}")
    return value

def create_template_json(
    student_model,
    output_path,
    question_id,
    category,
    human_answer,
    question,
    student_answer,
    evaluator_response,
    score,
):
    """
    Creates or updates a JSON file with evaluation results for a student's answer.

    This function ensures the output directory exists, loads existing data if available,
    updates the JSON structure with the new evaluation data, and saves it back to the file.

    Args:
        student_model (str):
            The identifier of the student model that generated the answer.
        output_path (str):
            The file path where the JSON data will be saved or updated.
        question_id (str):
            The unique identifier for the question being evaluated.
        category (str):
            The category or topic of the question.
        human_answer (str):
            The correct or reference answer provided by a human.
        question (str):
            The text of the question being evaluated.
        student_answer (str):
            The answer generated by the student model.
        evaluator_response (str):
            The feedback or evaluation provided by the evaluator.
        score (float):
            The numerical score assigned based on the evaluation.

    Returns:
        None

    Example:
        ```python
        create_template_json(
            student_model="gpt-4",
            output_path="./results/evaluation.json",
            question_id="Q123",
            category="Biology",
            human_answer="Photosynthesis is the process by which green plants...",
            question="Explain photosynthesis.",
            student_answer="Photosynthesis allows plants to convert sunlight into energy.",
            evaluator_response="The answer is correct but lacks detail on the chemical process.",
            score=85.0,
        )
        ```
    
    Notes:
        - Ensure that the `jn` module is correctly imported as `json`.
        - The function will overwrite existing entries with the same `question_id`.
        - Handle sensitive data appropriately when writing to JSON files.
    """
    # Ensure the directory for the output path exists
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    logger.info(f"student_model = {student_model} ")
    # Load existing data if the file exists
    if os.path.exists(output_path):
        try:
            with open(output_path, "r", encoding="utf-8") as infile:
                template_data = jn.load(infile)
        except (jn.JSONDecodeError, FileNotFoundError):
            template_data = {}  # Start fresh if file is empty or corrupted
    else:
        template_data = {}

    # Define or update the structure of the template JSON
    template_data[question_id] = {
        "category": category,
        "question": question,
        "human_answer": human_answer,
        "model_answer": student_answer,
        "eval_response": evaluator_response,
        "score": score,
    }

    # Write the updated data back to the file
    with open(output_path, "w", encoding="utf-8") as json_file:
        jn.dump(template_data, json_file, indent=4, ensure_ascii=False)

    logger.info(f"Template JSON created/updated: {output_path}")

def extract_score_from_string(response_string):
    """
    Extracts a numerical score from a response string using predefined patterns.
    
    This function searches the input `response_string` for various patterns that indicate a score.
    It uses regular expressions to match different formats and returns the first found score as an integer.
    If no score pattern is matched, it returns `None`.
    
    Args:
        response_string (str):
            The string containing the evaluator's response from which to extract the score.
    
    Returns:
        Optional[int]:
            The extracted score as an integer if a pattern is matched; otherwise, `None`.
    
    Example:
        ```python
        response = "The score assigned is 85%."
        score = extract_score_from_string(response)
        print(score)  # Output: 85
        ```
    
    Notes:
        - The function is case-insensitive and handles multiple score formats.
        - Ensure that the response strings follow one of the predefined patterns for accurate extraction.
    """
    # Regular expressions to match different patterns that indicate a score
    patterns = [
        r"\"score\"\s*:\s*(\d+)",  # JSON-like: "score": 0 or "score":0
        r"'score':\s*(\d+)",       # Python dict-like: {'score': 0}
        r"'grade':\s*(\d+)",       # Python dict-like: {'grade': 0}
        r"Grade:\s*(\d+)",          # Grade without ratio, e.g., Grade: 0
        r"Grade:\s*{'score':\s*(\d+)}",  # Grade followed by Python dict, e.g., Grade: {'score': 0}
        r"Score:\s*{'score':\s*(\d+)}",  # Score followed by Python dict, e.g., Score: {'score': 0}
        r"\*\*Score:\*\*\s*{'score':\s*(\d+)}",  # Markdown Score followed by Python dict, e.g., **Score:** {'score': 20}
        r"\*\*Grade:\*\*\s*{'score':\s*(\d+)}",  # Markdown Grade followed by Python dict, e.g., **Grade:** {'score': 0}
        r"score\s*is\s*(\d+)%",               # Plain text: score is 0%
        r"score\s*of\s*\*\*(\d+)%\*\*",       # Markdown: score of **0%**
        r"the\s*score\s*assigned\s*is\s*(\d+)%",  # Assigned score: the score assigned is 0%
        r"Grade:\s*A\s*\(\s*(\d+)%\)",        # Grade with percentage, e.g., Grade: A (100%)
        r"Grade:\s*[F]\s*\(\s*(\d+)/\d+\)",   # Grade F with ratio, e.g., Grade: F (0/10)
        r"Grade:\s*(\d+)/\d+",                # Ratio format, e.g., Grade: 0/10
        r"\*\*Grade:\*\*\s*(\d+)/\d+",        # Markdown style: **Grade:** 0/10
        r"\*\*Grade:\*\*\s*F\s*\(\s*(\d+)/\d+\)",  # Markdown style with grade F: **Grade:** F (0/100)
        r"Grade:\s*\*\*(\d+)/\d+\*\*",        # Markdown format, e.g., **Grade:** 0/10
        r"Grade:\s*F\s*\(\s*(\d+)\s*out\s*of\s*\d+\)",  # Grade F with "out of", e.g., Grade: F (0 out of 10)
        r"You\s*received\s*a\s*score\s*of\s*(\d+)\s*out\s*of\s*\d+",  # Plain text: You received a score of 0 out of 10
        r"\*\*(\d+)/100\s*score\*\*",        # Markdown style, e.g., **100/100 score**
        r"would\s*earn\s*a\s*score\s*of\s*(\d+)",  # Plain text: would earn a score of 100
        r"return\s*a\s*score\s*of\s*(\d+)",       # Plain text: return a score of 0
    ]

    # Iterate over each pattern to find a match
    for pattern in patterns:
        match = re.search(pattern, response_string, re.IGNORECASE)
        if match:
            return int(match.group(1))

    # If no matching score pattern is found, return None
    return None

def is_valid_uuid4(uuid_string):
    """
    Validate that a string is a valid UUID4.

    Args:
        uuid_string (str): The string to validate.

    Returns:
        bool: True if valid UUID4, False otherwise.
    """
    try:
        val = uuid.UUID(uuid_string, version=4)
    except ValueError:
        return False
    return str(val) == uuid_string

def cleanup_chromadb(db_filename="chroma.sqlite3", root_dir="."):
    """
    Clean up the ChromaDB by removing the specified SQLite file and any directories
    in the root directory that have names matching UUIDv4.

    Args:
        db_filename (str): The name of the SQLite database file to remove.
        root_dir (str): The root directory to search for UUIDv4-named directories.
    """
    # Construct the full path for the database file
    db_path = os.path.join(root_dir, db_filename)

    # 1. Remove chromadb.sqlite3 file if it exists
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            logger.info(f"Removed database file: {db_path}")
        except Exception as e:
            logger.error(f"Failed to remove database file '{db_path}': {e}")
    else:
        logger.warning(f"Database file '{db_path}' does not exist.")

    # 2. Remove directories in the root directory that look like UUIDv4
    try:
        for item in os.listdir(root_dir):
            item_path = os.path.join(root_dir, item)
            if os.path.isdir(item_path) and is_valid_uuid4(item):
                try:
                    shutil.rmtree(item_path)
                    logger.info(f"Removed UUID-like directory: {item_path}")
                except Exception as e:
                    logger.error(f"Failed to remove directory '{item_path}': {e}")
    except Exception as e:
        logger.error(f"Failed to list directories in '{root_dir}': {e}")

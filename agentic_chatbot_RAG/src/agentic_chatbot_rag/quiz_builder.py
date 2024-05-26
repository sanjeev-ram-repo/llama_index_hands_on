import pandas as pd
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.program.evaporate.df import DFRowsProgram
from settings import INDEX_STORAGE, QUIZ_FILE, QUIZ_SIZE

QUIZ_PROMPT: str = """
Create {QUIZ_SIZE} different quiz question to test knowledge about {TOPIC}.
Each question will have 4 answer options. 
Questions must be general topic-related, not specific to the provided text. 
For each question, provide also the correct answer and the answer rationale.
The rationale must not make any reference to the provided context or any exams or topic. 
Only one answer option should be correct.
"""


def build_quiz(topic: str) -> pd.DataFrame:
    """Given a topic generate a dataframe of 'n' questions

    Args:
        topic (str): Topic name

    Returns:
        pd.DataFrame: Questions and answers as a dataframe
    """
    try:
        df = pd.DataFrame(
            {
                "Question_No": pd.Series(dtype="int"),
                "Question_text": pd.Series(dtype="str"),
                "Option1": pd.Series(dtype="str"),
                "Option2": pd.Series(dtype="str"),
                "Option3": pd.Series(dtype="str"),
                "Option4": pd.Series(dtype="str"),
                "Correct_answer": pd.Series(dtype="str"),
                "Rationale": pd.Series(dtype="str"),
            }
        )
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORAGE)
        vector_index = load_index_from_storage(storage_context, index_id="vector")
        df_rows_program = DFRowsProgram.from_defaults(
            pydantic_program_cls=LLMTextCompletionProgram, df=df
        )
        query_engine = vector_index.as_query_engine()
        response = query_engine.query(
            QUIZ_PROMPT.format(QUIZ_SIZE=QUIZ_SIZE, TOPIC=topic)
        )
        result_obj = df_rows_program(input_str=response)
        quiz_df = result_obj.to_df(existing_df=df)
        quiz_df.to_csv(QUIZ_FILE, index=False)
        return quiz_df
    except Exception as e:
        raise Exception(f"Unable to create quiz: {str(e)}")

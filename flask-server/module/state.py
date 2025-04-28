
from flask import Blueprint, request, jsonify
import json
from typing import List, Dict, Any, TypedDict
from typing_extensions import Annotated
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from module.systemFunction import log_message
from module.tools import Tool
from langchain_groq import ChatGroq
from langchain import hub
from langsmith import Client
from dotenv import load_dotenv
import ast
import os

data_source_bp=Blueprint('state', __name__)

class State:

    _instance=None

    def __init__(self):
        self._db: object = None
        self._llm: object = None
        self._schema: List[str] = []
        self._prompt: object = None
        self._question: str = ""
        self._query: str = ""
        self._result: str = ""
        self._data: dict = {}
        self._tools: list = []
        self._analysis: str = ""
        self._visualization: object = None

    def getInstance():
        '''
        Returns State class' instance.
        '''
        if State._instance is None:
            State._instance=State() # Create State object

        return State._instance
    
    # DB property
    @property
    def db(self) -> object:
        return self._db

    @db.setter
    def db(self, value: object):
        self._db = value  # No type restriction
    
    # LLM property
    @property
    def llm(self) -> object:
        return self._llm

    @llm.setter
    def llm(self, value: object):
        self._llm = value  # No type restriction

    # prompt property
    @property
    def prompt(self) -> object:
        return self._prompt

    @prompt.setter
    def prompt(self, value: object):
        self._prompt = value  # No type restriction
    
    @property
    def schema(self) -> List[str]:
        return self._schema

    @schema.setter
    def schema(self, value: List[str]):
        if not isinstance(value, list):
            raise ValueError("Schema must be a list of strings.")
        self._schema = value

    @property
    def question(self) -> str:
        return self._question

    @question.setter
    def question(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Question must be a string.")
        self._question = value

    @property
    def query(self) -> str:
        return self._query

    @query.setter
    def query(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Query must be a string.")
        self._query = value

    @property
    def result(self) -> str:
        return self._result

    @result.setter
    def result(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Result must be a string.")
        self._result = value

    # Data property
    @property
    def data(self) -> dict:
        return self._data

    @data.setter
    def data(self, value: str):
        if not isinstance(value, dict):
            raise ValueError("Data must be a dictionary.")
        self._data = value

    @property
    def tools(self) -> list:
        return self._tools

    @tools.setter
    def tools(self, value: list):
        if not isinstance(value, list):
            raise ValueError("Tools must be a list.")
        self._tools = value

    # Analysis property
    @property
    def analysis(self) -> str:
        return self._analysis

    @analysis.setter
    def analysis(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Analysis must be a string.")
        self._analysis = value

    # Visualization property
    @property
    def visualization(self) -> object:
        return self._visualization

    @visualization.setter
    def visualization(self, value: object):
        self._visualization = value  # No type restriction

    def writeQuery(self):
        """Generate SQL query to fetch information."""
        prompt = self.prompt.invoke(
            {
                "dialect": "mysql",
                "top_k": 10,
                "table_info": self.schema,
                "input": self.question,
            }
        )
        structured_llm = self.llm.with_structured_output(QueryOutput)
        result = structured_llm.invoke(prompt)
        self.query=result["query"]
        return self.query
    
    def executeQuery(self):
            """Execute SQL query."""
            execute_query_tool=QuerySQLDatabaseTool(db=self.db)
            self.result=execute_query_tool.invoke(self.query)
            # print(f"{type(data)}")
            return self.result
    
    def generateDF(self):
        """Generate dictionary based on the data provided and user prompt."""
        prompt = f"""
            Given the following user question and data, generate a dictionary containing the name of the column and the corresponding data.
            Your response will be converted directly into a dataframe, hence your response should only be in form of dictionary only.

            f'Question: {self.question}\n'
            f'SQL Result: {self.result}'
            
            """
        
        response = self.llm.invoke(prompt)
        data={"df": response.content}
        dict_data = ast.literal_eval(data['df'])  # Convert to dictionary
        # print(f"{type(dict_data)}")
        self.data=dict_data

        return self.data
    
    def chooseVisualization(self):

            prompt=f"""
            
            You are given several tools that correspond to different types of data visualization graphs and charts.
            Given the following user questions, the result from the database, the data, and the tools, choose the best tool to represent the data.

            Question: {self.question}
            Result: {self.result}
            Data: {self.data}
            Tools: {self.tools}

            """

            llm_with_tools=self.llm.bind_tools(self.tools)
            # chain = llm_with_tools | human_approval
            
            try:

                # Step 1: Invoke LLM to get the function call
                response = llm_with_tools.invoke(prompt)

                # Step 2: Extract tool calls from AIMessage
                tool_calls = response.additional_kwargs.get("tool_calls", [])
                if not tool_calls:
                    raise ValueError("No tool call returned by the LLM.")

                function_call = tool_calls[0]  # Assuming a single function call
                function_name = function_call["function"]["name"]
                function_args = json.loads(function_call["function"]["arguments"])  # Convert string to dict

                # Step 3: Execute tool dynamically using LangChain's `.invoke()`
                tool_mapping = {tool.name: tool for tool in self.tools}  # Map tool names

                if function_name in tool_mapping:
                    print(function_name)
                    print(function_args)
                    visualization_result = tool_mapping[function_name].invoke(input=function_args)
                    self.visualization = visualization_result

                    # Get the parent directory (folder containing `State.py`'s folder)
                    parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

                    # Ensure the folder exists (optional)
                    visualization_folder = os.path.join(parent_folder, "prompt")
                    os.makedirs(visualization_folder, exist_ok=True)

                    # Save HTML file inside the parent folder (or "visualizations" inside it)
                    html_file = os.path.join(visualization_folder, "visual.html")

                    # Save the visualization
                    fig = self.visualization
                    fig.write_html(html_file)

                    html_file = os.path.join(visualization_folder, "visual.html")
                    fig = self.visualization
                    fig.write_html(html_file)

                    return self.visualization
                else:
                    raise ValueError(f"Unknown function: {function_name}")

            except Exception as e:
                print(e)

    def generateAnalysis(self):
        """Answer question using retrieved information as context."""
        prompt = (
            "Given the following user question, corresponding SQL query, "
            "and SQL result, answer the user question. Make sure to go into detail and summarize the trends and main outcome. \n\n"
            f'Question: {self.question}\n'
            f'SQL Query: {self.query}\n'
            f'SQL Result: {self.result}'
        )
        self.analysis = self.llm.invoke(prompt).content
        return self.analysis
    

    def setDBToState(self, db):
        try:
            self.db=db
            log_message(f"Setting Data Source Connection to state successful")
            print(f"state.db set! {state.db}")
        except Exception as e:
            log_message(f"Error setting Data Source Connection to state: {e}")


    def setSchemaToState(self):
        try:
            self.schema = []
            
            for table in self.db.get_usable_table_names():
                schema = self.db.run(f"SHOW CREATE TABLE {table};")
                self.schema.append(schema)

            log_message(f"Schema retrieval successful")
            print(f"\nstate.schema set! {state.schema}")


        except Exception as e:
            log_message(f"Error getting database schema: {e}")

    def setModelToState(self):
        load_dotenv()

        try:
            api_key=os.getenv('GROQ_API_KEY')
            langsmith_key=os.getenv('LANGSMITH_API_KEY')
            model_name=os.getenv('MODEL')
            log_message("LLM api key and model name retrieval successful")

        except Exception as e:
            log_message(f"Error retrieving LLM api key and model name: {e}")

        try:
            llm=ChatGroq(model=model_name)
            log_message("LLM instantiation successful")

        except Exception as e:
            log_message(f"Error instantiating LLM: {e}")

        try:
            self.llm=llm
            log_message(f"Setting LLM to state successful")
            print(f"\nstate.llm set! {self.llm}")
        except Exception as e:
            log_message(f"Error setting LLM to state: {e}")

        try:

            # #query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
            loc="langchain-ai/sql-query-system-prompt"
            query_prompt_template = hub.pull(loc)

            assert len(query_prompt_template.messages) == 2
            # for message in query_prompt_template.messages:
            #     message.pretty_print()

            self.prompt=query_prompt_template.messages

            log_message("Prompt template retrieval successful")
            print(f"\nstate.prompt set! {self.prompt}")

            # query_prompt_template.messages[0].pretty_print()

            # langsmith_key=os.getenv('LANGSMITH_API_KEY')
            # print(langsmith_key)
            # client = Client(api_key=langsmith_key)
            # prompt = client.pull_prompt("langchain-ai/sql-query-system-prompt", include_model=True)
            # prompt[0].pretty_print()

        except Exception as e:
            log_message(f"Error: {e} retrieving prompt template from {loc}")

    def setToolsToState(self):
        try:
            tools=Tool()
            self.tools=tools.tools
            log_message("Tools definition successful")
            print(f"\nstate.tools set! {self.tools}")

        except Exception as e:
            log_message(f"Error defining tools: {e}")
    
class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]

state=State.getInstance()
print(f"\nState created: {state}")

state.setModelToState()
state.setToolsToState()


    



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
from IPython.display import Image, display
from langgraph.graph import START, StateGraph, END 
from dotenv import load_dotenv

import ast
import os

data_source_bp=Blueprint('state', __name__)

class State(TypedDict):

    db: object = None
    llm: object = None
    schema: List[str] = []
    prompt: object = None
    question: str = ""
    query: str = ""
    result: str = ""
    retry: int=0
    SQLValidity: str=""
    SQLImprovement: str=""
    data: dict = {}
    tools: list = []
    analysis: str = ""
    visualization: object = None

    # _instance=None

    # def __init__(self):
    #     self._db: object = None
    #     self._llm: object = None
    #     self._schema: List[str] = []
    #     self._prompt: object = None
    #     self._question: str = ""
    #     self._query: str = ""
    #     self._result: str = ""
    #     self._retry: int=0
    #     self._SQLValidity: str=""
    #     self._SQLImprovement: str=""
    #     self._data: dict = {}
    #     self._tools: list = []
    #     self._analysis: str = ""
    #     self._visualization: object = None
    #     self._graph: object= None

    # def getInstance():
    #     '''
    #     Returns State class' instance.
    #     '''
    #     if State._instance is None:
    #         State._instance=State() # Create State object

    #     return State._instance
    
    # # DB property
    # @property
    # def db(self) -> object:
    #     return self._db

    # @db.setter
    # def db(self, value: object):
    #     self._db = value  # No type restriction
    
    # # LLM property
    # @property
    # def llm(self) -> object:
    #     return self._llm

    # @llm.setter
    # def llm(self, value: object):
    #     self._llm = value  # No type restriction

    # # prompt property
    # @property
    # def prompt(self) -> object:
    #     return self._prompt

    # @prompt.setter
    # def prompt(self, value: object):
    #     self._prompt = value  # No type restriction
    
    # @property
    # def schema(self) -> List[str]:
    #     return self._schema

    # @schema.setter
    # def schema(self, value: List[str]):
    #     if not isinstance(value, list):
    #         raise ValueError("Schema must be a list of strings.")
    #     self._schema = value

    # @property
    # def question(self) -> str:
    #     return self._question

    # @question.setter
    # def question(self, value: str):
    #     if not isinstance(value, str):
    #         raise ValueError("Question must be a string.")
    #     self._question = value

    # @property
    # def query(self) -> str:
    #     return self._query

    # @query.setter
    # def query(self, value: str):
    #     if not isinstance(value, str):
    #         raise ValueError("Query must be a string.")
    #     self._query = value

    # @property
    # def result(self) -> str:
    #     return self._result

    # @result.setter
    # def result(self, value: str):
    #     if not isinstance(value, str):
    #         raise ValueError("Result must be a string.")
    #     self._result = value

    # @property
    # def retry(self) -> str:
    #     return self._retry

    # @retry.setter
    # def retry(self, value: str):
    #     if not isinstance(value, int):
    #         raise ValueError("Result must be an integer.")
    #     self._retry = value
    
    # @property
    # def SQLValidity(self) -> str:
    #     return self._SQLValidity

    # @SQLValidity.setter
    # def SQLValidity(self, value: str):
    #     if not isinstance(value, str):
    #         raise ValueError("Result must be a string.")
    #     self._SQLValidity = value

    # @property
    # def SQLImprovement(self) -> str:
    #     return self._SQLImprovement

    # @SQLImprovement.setter
    # def SQLImprovement(self, value: str):
    #     if not isinstance(value, str):
    #         raise ValueError("Result must be a string.")
    #     self._SQLImprovement = value

    # # Data property
    # @property
    # def data(self) -> dict:
    #     return self._data

    # @data.setter
    # def data(self, value: str):
    #     if not isinstance(value, dict):
    #         raise ValueError("Data must be a dictionary.")
    #     self._data = value

    # @property
    # def tools(self) -> list:
    #     return self._tools

    # @tools.setter
    # def tools(self, value: list):
    #     if not isinstance(value, list):
    #         raise ValueError("Tools must be a list.")
    #     self._tools = value

    # # Analysis property
    # @property
    # def analysis(self) -> str:
    #     return self._analysis

    # @analysis.setter
    # def analysis(self, value: str):
    #     if not isinstance(value, str):
    #         raise ValueError("Analysis must be a string.")
    #     self._analysis = value

    # # Visualization property
    # @property
    # def visualization(self) -> object:
    #     return self._visualization

    # @visualization.setter
    # def visualization(self, value: object):
    #     self._visualization = value  # No type restriction

    # @property
    # def graph(self) -> object:
    #     return self._graph

    # @graph.setter
    # def graph(self, value: object):
    #     self._graph = value  # No type restriction

class StateMethods:

    def writeQuery(state: State, question=None):
        """Generate SQL query to fetch information."""

        print("\nStarting Node writeQuery()\n")

        columns = ', '.join([col for col in state["schema"] if isinstance(col, str)])
        prompt = state["prompt"].invoke(
            {
                "dialect": "mysql",
                "top_k": 10,
                "table_info": state["schema"],
                "input": f"""
                    {state["question"]}\n\nImportant: Available columns include: {columns}.
                    When answering, use the most human-readable field available.  
                    If a field is a foreign key, join the referenced table and show its descriptive column.
                    If the field is an ID, but there also exists a descriptive and human readable field of it within the same table, use the descriptive column.

                    If the SQL fails, you are required to generate a new one while considering this improvement: {state["SQLImprovement"]}
                """
            }
        )
        try:
            print("Writing Query")
            print(type(state["prompt"]))
            print(type(prompt))
            structured_llm = state["llm"].with_structured_output(QueryOutput)
            result = structured_llm.invoke(prompt)
            state["query"]=result["query"]
            print(type(state["query"]))

            return state
        except Exception as e:
            print(e)
            return
    
    def executeQuery(state: State):
        """Execute SQL query and verify the query generated."""

        print("\nStarting Node executeQuery()\n")

        try: 
            print("Executing Query")
            execute_query_tool=QuerySQLDatabaseTool(db=state["db"])
            state["result"]=execute_query_tool.invoke(state["query"])
            print(type(state["result"]))
        except Exception as e:
            print(f"ERROR! {e}")
        
        prompt = f"""
        You are required to verify the SQL query generated whether it is executable or not. 

        f'SQL Schema: {state["schema"]}'
        f'SQL Question: {state["question"]}'
        f'SQL Query: {state["query"]}'
        f'SQL Result: {state["result"]}'

        You are required to response with only one (1) string:
        If it is executable and valid, response with: valid
        If it is not executable, returns error, or the question does not relate to the database schema at all, response with: invalid          
        """

        try:
            print("Evaluating Query")
            response = state["llm"].invoke(prompt)
            state["SQLValidity"]=response.content
            print(f"{state['SQLValidity']} {type(state['SQLValidity'])}")
            return state
        except Exception as e:
            print(f"ERROR! {e}")

        return state
                     
    def improveQuery(state: State):
        print("\nStarting Node improveQuery()\n")

        print(f"try number {state['retry']}")
        if state["retry"]<=3:
            state["retry"]+=1
        
            """Verify the query generated ."""
            prompt = f"""
                You are required to provide fix for the SQL query based on the SQL query and the error message. 
                The SQL should be sytatically correct, adhere to the schema provided, and following MySQL dialect.

                f'Schema: {state["schema"]}'
                f'SQL Query: {state["query"]}'
                f'SQL Result: {state["result"]}'
                """
            try:
                print("Improving Query")
                
                response = state["llm"].invoke(prompt)
                state["SQLImprovement"]=response.content
                print(state["SQLImprovement"])
                return state
            except Exception as e:
                print(f"error: {e}")
                return
        else:
            print("max retry reached")
            return
          
    def generateDF(state: State):
        """Generate dictionary based on the data provided and user prompt."""

        print("\nStarting Node generateDF()\n")


        prompt = f"""
            Given the following user question, SQL query, and result from the SQL query, generate a dictionary containing the name of the column and the corresponding data.
            Your response will be converted directly into a dataframe, hence your response should only be in form of dictionary only.
            Do not generate a nested dictionary. Each column should be converted into a single key in the dictionary.

            f'Question: {state["question"]}\n'
            f'SQL Query: {state["query"]}
            f'SQL Result: {state["result"]}'
            
            """
        
        response = state["llm"].invoke(prompt)

        try:
            data={"df": response.content}
            dict_data = ast.literal_eval(data['df'])  # Convert to dictionary
            # print(f"{type(dict_data)}")
            state["data"]=dict_data
            print(type(state["data"]))


            return state
        except Exception as e:
            return f"error {e}"
    
    def chooseVisualization(state: State):
            
            print("\nStarting Node chooseVisualization()\n")


            prompt=f"""
            
            You are given several tools that correspond to different types of data visualization graphs and charts.
            Given the following user questions, the data, and the tools, choose the best tool to represent the data.
            

            Question: {state["question"]}
            Data: {state["data"]}
            Tools: {state["tools"]}

            """

            llm_with_tools=state["llm"].bind_tools(state["tools"])
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
                tool_mapping = {tool.name: tool for tool in state["tools"]}  # Map tool names

                if function_name in tool_mapping:
                    print(function_name)
                    print(function_args)
                    visualization_result = tool_mapping[function_name].invoke(input=function_args)
                    # self.visualization = visualization_result
                    # print(type(self.visualization))

                    #fig = self.visualization
                    # fig.write_html("visual.html")
                    state["visualization"] = visualization_result.to_html(full_html=False, include_plotlyjs='cdn')
                    print(type(state["visualization"]))

                    return state
                else:
                    raise ValueError(f"Unknown function: {function_name}")

            except Exception as e:
                print(e)
                return

    def generateAnalysis(state: State):
        """Answer question using retrieved information as context."""

        print("\nStarting Node generateAnalysis()\n")

        prompt = (
            "Given the following user question, corresponding SQL query, "
            "and SQL result, answer the user question. Make sure to go into detail and summarize the trends and main outcome. \n\n"
            f'Question:     {state["question"]}\n'
            f'SQL Query:    {state["query"]}\n'
            f'SQL Result:   {state["result"]}'
        )
        try:
            print("Generating Analysis")
            state["analysis"] = state["llm"].invoke(prompt).content
            print(type(state["analysis"]))

            return state
        except Exception as e:
            print(f"error {e}")
            return

    def agentOutputValidator(state: State):
        '''
        Verify the output of agents routing them to the necessary agent to reproduce the output
        '''

        prompt="""

        You are the validator and router agent. 
        Given the output of a certain agent, you must decide whether the output is acceptable to continue to the next agent, or the output should be done again by the agent most likely responsible for it.
        Here are the agents and its expeccted input and output:



        """

    # def setDBToState(state: State, db):
    #     try:
    #         state["db"]=db
    #         log_message(f"Setting Data Source Connection to state successful")
    #         print(f"state['db'] set! {state["db"]}")
    #     except Exception as e:
    #         log_message(f"Error setting Data Source Connection to state: {e}")
    #         return

    # def setSchemaToState(state: State):
    #     print(f"\nsetting state.schema!")

    #     # if(schema):

    #     #     state["schema"] = schema if schema is not None else state["question"]
    #     #     print(f"\ncustom state['schema'] set! {state.schema}")
    #     #     return
        
    #     # print(f"\skipping custom state['schema']!")

        
    #     try:
    #         state["schema"] = []
            
    #         for table in state["db"].get_usable_table_names():
    #             schema = state["db"].run(f"SHOW CREATE TABLE {table};")
    #             state["schema"].append(schema)

    #         log_message(f"Schema retrieval successful")
    #         print(f"\nstate['schema'] set! {state.schema}")


    #     except Exception as e:
    #         log_message(f"Error getting database schema: {e}")
    #         return

    def getModel():
        load_dotenv()

        try:
            api_key=os.getenv('GROQ_API_KEY')
            langsmith_key=os.getenv('LANGSMITH_API_KEY')
            model_name=os.getenv('MODEL')
            log_message("LLM api key and model name retrieval successful")

        except Exception as e:
            log_message(f"Error retrieving LLM api key and model name: {e}")
            return

        try:
            llm=ChatGroq(model=model_name)
            log_message("LLM instantiation successful")

        except Exception as e:
            log_message(f"Error instantiating LLM: {e}")
            return

        try:
            # log_message(f"Setting LLM to state successful")
            # print(f"\nstate['llm'] set! {state["llm"]}")
            return llm
        except Exception as e:
            log_message(f"Error setting LLM to state: {e}")
            return
        
    def getPrompt():

        try:

            loc="langchain-ai/sql-query-system-prompt"
            query_prompt_template = hub.pull(loc)

            assert len(query_prompt_template.messages) == 2
            # for message in query_prompt_template.messages:
            #     message.pretty_print()

            # state["prompt"]=query_prompt_template

            # log_message("Prompt template retrieval successful")
            # print(f"\nstate['prompt'] set! {state["prompt"]}")

            return query_prompt_template

        except Exception as e:
            log_message(f"Error: {e} retrieving prompt template from {loc}")
            return

    def getTools():
        try:
            tools=Tool()
            tools_list=tools.tools
            # log_message("Tools definition successful")
            # print(f"\nstate['tools'] set! {state["tools"]}")
            return tools_list

        except Exception as e:
            log_message(f"Error defining tools: {e}")
            return 

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]

state: State={
    "db": None,
    "llm": None,
    "schema": [],
    "prompt": None,
    "question": "",
    "query": "",
    "result": "",
    "retry": 0,
    "SQLValidity": "",
    "SQLImprovement": "",
    "data": {},
    "tools": [],
    "analysis": "",
    "visualization": None,
}

print(f"\nState created: {type(state)}")

state["llm"]=StateMethods.getModel()
state["prompt"]=StateMethods.getPrompt()
state["tools"]=StateMethods.getTools()

print(f"""\nState initialized with:\n
      llm: {type(state["llm"])}\n
      prompt: {type(state["prompt"])}\n
      tools: {type(state["tools"])} {len(state["tools"])}\n
""")

try:

    graph_builder = StateGraph(State)

    graph_builder.add_node("writeQuery", StateMethods.writeQuery)
    graph_builder.add_node("executeQuery", StateMethods.executeQuery)
    graph_builder.add_node("improveQuery", StateMethods.improveQuery)
    graph_builder.add_node("generateDF", StateMethods.generateDF)
    graph_builder.add_node("chooseVisualization", StateMethods.chooseVisualization)
    graph_builder.add_node("generateAnalysis", StateMethods.generateAnalysis)

    graph_builder.add_edge(START, "writeQuery")
    graph_builder.add_edge("writeQuery", "executeQuery")

    graph_builder.add_conditional_edges("executeQuery", lambda state: state['SQLValidity'], {
        "valid": "generateDF",
        "invalid": "improveQuery"
    })
    graph_builder.add_conditional_edges(
        "improveQuery", 
            lambda state: "retry" if state["retry"] < 3 else "max attempt",
        {
        "retry": "writeQuery",
        "max attempt": END
    })

    graph_builder.add_edge("generateDF", "chooseVisualization")
    graph_builder.add_edge("chooseVisualization", "generateAnalysis")
    graph_builder.add_edge("generateAnalysis", END)

    graph = graph_builder.compile()
    graphVisual = graph.get_graph().draw_mermaid_png()

    print(f"graph initialized: {type(graph)}")
    print(f"graph visual initialized: {type(graphVisual)}")

except Exception as e:
    print(f"error {e}")


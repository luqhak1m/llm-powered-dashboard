
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
    model: str=""
    schema: List[str] = []
    prompt: object = None
    question: str = ""
    query: str = ""
    result: str = ""
    retry: int=0
    SQLValidity: str=""
    data: dict = {}
    tools: list = []
    analysis: str = ""
    visualization: object = None
    nextNode: str=""
    routerCount: int=0
    improvement: str=""


class StateMethods:

    def writeQuery(state: State):
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

                    If the SQL fails, you are required to generate a new one while considering this improvement: {state["improvement"]}
                    If the improvement is empty, ignore the improvement
                """
            }
        )
        try:
            print("Writing Query")
            # print(f"state[prompt]: {state['prompt']}")
            # print(f"type state[prompt]: {type(state['prompt'])}")
            # print(f"type prompt{type(prompt)}")
            structured_llm = state["llm"].with_structured_output(QueryOutput)
            result = structured_llm.invoke(prompt)
            state["query"]=result["query"]
            print(f"state[query]: {(state['query'])}")
            print(type(state["query"]))

            return state
        except Exception as e:
            print(e)
            return
    
    def validateQuery(state: State):
        """Execute SQL query and verify the query generated."""

        print("\nStarting Node executeQuery()\n")

        try: 
            print("Executing Query")
            execute_query_tool=QuerySQLDatabaseTool(db=state["db"])
            state["result"]=execute_query_tool.invoke(state["query"])
            print(f"state[result]: {(state['result'])}")
            print(type(state["result"]))
        except Exception as e:
            print(f"ERROR! {e}")
        
        prompt = f"""
        <|begin_of_text|>

        <|start_header_id|>system<|end_header_id|>

        You are a SQL query validator.
        You are required to verify the SQL query generated whether it is executable or not. 

        You are required to response with only one (1) string:
        If it is executable, valid, correct, and doesn't require any fixes, response with: valid
        If it is empty, not executable, error, response with: invalid   
        If the question does not relate to the database schema at all, response with: end
        
        SQL Schema: {state["schema"]}
        Question: {state["question"]}
        SQL Query: {state["query"]}
        SQL Result: {state["result"]}

        <|eot_id|>

        <|start_header_id|>assistant<|end_header_id|>
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
        state["improvement"]=""

        print(f"try number {state['retry']}")
        if state["retry"]<=3:
            state["retry"]+=1
        
            """Verify the query generated ."""
            prompt = f"""
                <|begin_of_text|>

                <|start_header_id|>system<|end_header_id|>
                You are a SQL query validator.
                You are required to provide fix for the SQL query based on the SQL query and the error message. 
                The SQL should be sytatically correct, adhere to the schema provided, and following MySQL dialect.

                f'Schema: {state["schema"]}'
                f'SQL Query: {state["query"]}'
                f'SQL Result: {state["result"]}'
                f'SQL Improvement: {state["improvement"]}'

                <|eot_id|>

                <|start_header_id|>assistant<|end_header_id|>                
                """
            try:
                print("Improving Query")
                
                response = state["llm"].invoke(prompt)
                state["improvement"]=response.content
                print(state["improvement"])
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
            <|begin_of_text|>
            <|start_header_id|>system<|end_header_id|>
            You are a SQL query result parser.
            Given the following user question, SQL query, and result from the SQL query, generate a dictionary containing the name of the column and the corresponding data.
            Your response will be converted directly into a dataframe, hence your response should only be in form of dictionary only.
            Do not generate a nested dictionary. Each column should be converted into a single key in the dictionary.

            f'Question: {state["question"]}\n'
            f'SQL Query: {state["query"]}
            f'SQL Result: {state["result"]}'

            Take into account the existing dictionary and the required improvement. Ignore if empty.

            f'Existing Dictionary: {state["data"]}
            f'Required Improvement: {state["improvement"]}'
            <|eot_id|>

            <|start_header_id|>assistant<|end_header_id|>
            """
        
        response = state["llm"].invoke(prompt)

        try:
            print(f"generateDF response: {response.content}")

            data={"df": response.content}
            print(f"converting to dict")

            dict_data = ast.literal_eval(data['df'])  # Convert to dictionary

            print(f"dict_data: {dict_data}")
            # print(f"{type(dict_data)}")
            state["data"]=dict_data
            print(type(state["data"]))


            return state
        except Exception as e:
            print(f"error: {e}")
            return f"error {e}"
    
    def chooseVisualization(state: State):
            
            print("\nStarting Node chooseVisualization()\n")


            prompt=f"""

            <|begin_of_text|>
            <|start_header_id|>system<|end_header_id|>
            Environment: ipython
            You are a data visualization expert.
            You are given several tools that correspond to different types of data visualization graphs and charts.
            Given the following user questions, the data, and the tools, choose the best tool to represent the data.

            Question: {state["question"]}
            Data: {state["data"]}
            Tools: {state["tools"]}

            Take into account the existing visualization and the required improvement. Ignore if empty:
            
            Existing Visualization: {state["visualization"]}
            Required Improvement: {state["improvement"]}
            <|eot_id|>

            <|start_header_id|>assistant<|end_header_id|>
            
            """

            llm_with_tools=state["llm"].bind_tools(state["tools"])
            # chain = llm_with_tools | human_approval
            print("tools " + str(state["tools"]))
            
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
                    print(type(visualization_result))
                    print(f"chart function: {visualization_result}")

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

        prompt = (f"""
            <|begin_of_text|>
            <|start_header_id|>system<|end_header_id|>
            You are a data analyst.      
            Given the following user question and the data, answer the user question using the data. 
            Make sure to go into detail and summarize the trends and main outcome.
            You must response in normal string format.
            Do not include the raw SQL data inside your response.
                  
            Format it like this example:
                  
            Data Preview
                  
            <text of data preview>
                  
            Trend
                  
            <text of trend>
                  
            Main Outcome
                  
            <text of main outcome>
                  
            Question:     {state["question"]}
            SQL Result:   {state["result"]}

            Take into account the existing analysis and the required improvement. Ignore if empty:
            
            Existing Analysis: {state['analysis']}
            Required Improvement: {state['improvement']}
            <|eot_id|>

            <|start_header_id|>assistant<|end_header_id|>
            """
        )
        try:
            print("Generating Analysis")
            state["analysis"] = state["llm"].invoke(prompt).content
            print(type(state["analysis"]))

            return state
        except Exception as e:
            print(f"error {e}")
            return

    def dfValidator(state: State):
        '''
        Verify the output of agents routing them to the necessary agent to reproduce the output
        '''

        print("\nStarting Node agentOutputValidator()\n")

        prompt=f"""

        <|begin_of_text|>
        <|start_header_id|>system<|end_header_id|>

        you are an agent output validator.
        you must verify the string and make sure the output of an agent must be in form of a dictionary. 
        verify whether the output is in the form of a dictionary, if yes, move to the next agent, chooseVisualization. if the output is not in the form of dictionary, or if the output contains anything other than a dictionary, go back to the same agent with an improvement message.
        your output must be in format of dictionary with the agent name and the improvement message. there are only 2 agents:

        generateDF
        chooseVisualization

        you must output in the format of dictionary:
        
        {{ 

            "agentName": "<agentName>",
            "improvementMessage": "<improvementMessage>"

        }}

        verify this agent output: {state["data"]}

        <|eot_id|>

        <|start_header_id|>assistant<|end_header_id|>

        """
        
        print(f"count {state['routerCount']}")

        if state["routerCount"]==5:
            print("max router attempt")
            return

        try:     
            state["routerCount"]+=1
            response = state["llm"].invoke(prompt)
            response_string=response.content
            print(response_string)
            print(type(response_string))

            formatted_response = json.loads(response_string)
            print(f"agent name: {formatted_response['agentName']}")
            print(f"improvement message: {formatted_response['improvementMessage']}")
            print(type(formatted_response))

            state["nextNode"]=formatted_response['agentName']
            state["improvement"]=formatted_response['improvementMessage']
            print(f"state['nextNode']: {state['nextNode']}")
            print(f"state['improvement']: {state['improvement']}")
            
            return state
        except Exception as e:
            print(f"error: {e}")
            return

    def getModel():
        load_dotenv()

        try:
            api_key=os.getenv('GROQ_API_KEY')
            print(api_key)
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

    def getCleanState():
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
            "improvement": "",
            "data": {},
            "tools": [],
            "analysis": "",
            "visualization": None,
            "nextNode": "",
            "routerCount": 0,
        }

        print(f"\nState created: {type(state)}")
        return state

    def setupInitialState(state: State):

        try:
            state["llm"]=StateMethods.getModel()
            state["prompt"]=StateMethods.getPrompt()
            # state["tools"]=StateMethods.getTools()

            # print(f"type: {type(llm)}")
            # print(f"model_name: {(llm.model_name)}")
            # print(f"type(model_name): {type(llm.model_name)}")
            state["model"]=state["llm"].model_name

            print(f"""\nState initialized with:\n
                llm: {type(state["llm"])}\n
                model: {(state["model"])}\n
                prompt: {type(state["prompt"])}\n
                tools: {type(state["tools"])} {len(state["tools"])}\n
            """)
            return state
        
        except Exception as e:
            print(f"error {e}")

    def setupGraph(state: State):
        try:
            graph_builder = StateGraph(State)

            graph_builder.add_node("writeQuery", StateMethods.writeQuery)
            graph_builder.add_node("executeQuery", StateMethods.validateQuery)
            graph_builder.add_node("improveQuery", StateMethods.improveQuery)
            graph_builder.add_node("generateDF", StateMethods.generateDF)
            graph_builder.add_node("chooseVisualization", StateMethods.chooseVisualization)
            graph_builder.add_node("generateAnalysis", StateMethods.generateAnalysis)
            graph_builder.add_node("dfValidator", StateMethods.dfValidator)

            graph_builder.add_edge(START, "writeQuery")
            graph_builder.add_edge("writeQuery", "executeQuery")

            graph_builder.add_conditional_edges("executeQuery", lambda state: state['SQLValidity'], {
                "valid": "generateDF",
                "invalid": "improveQuery",
                "end": END
            })
            graph_builder.add_conditional_edges(
                "improveQuery", 
                    lambda state: "retry" if state["retry"] < 3 else "max attempt",
                {
                "retry": "writeQuery",
                "max attempt": END
            })

            graph_builder.add_edge("generateDF", "dfValidator")
            

            graph_builder.add_conditional_edges(
            "dfValidator",
            lambda state: 
                "generateDF" if state["nextNode"] == "generateDF"
                else "chooseVisualization",
                {
                "generateDF": "generateDF",
                "chooseVisualization": "chooseVisualization",
                }
            )

            graph_builder.add_edge("chooseVisualization", "generateAnalysis")
            graph_builder.add_edge("generateAnalysis", END)

            graph = graph_builder.compile()
            print(f"graph initialized: {type(graph)}")
            return graph
        except Exception as e:
            print(f"error {e}")
            return e
        
    def visualizeGraph(graph):
        try:
            graphVisual = graph.get_graph().draw_mermaid_png()
            print(f"graph visual initialized: {type(graphVisual)}")
            return graphVisual
        except Exception as e:
            print(f"error {e}")
            return e

    def clearState(state: State):
        state["question"]= ""
        state["query"]= ""
        state["result"]= ""
        state["retry"]= 0
        state["SQLValidity"]= ""
        state["improvement"]= ""
        state["data"]= {}
        state["analysis"]= ""
        state["visualization"]= None
        state["nextNode"]= ""
        state["routerCount"]= 0

        print("\nState cleared")

        return state

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]

init_state=StateMethods.getCleanState()
state=StateMethods.setupInitialState(init_state)
graph=StateMethods.setupGraph(state)
graphVisual=StateMethods.visualizeGraph(graph)

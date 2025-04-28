from typing_extensions import Annotated
from langchain_core.tools import tool
import plotly.express as px
import pandas as pd
import inspect
from langchain_core.messages import HumanMessage, AIMessage
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Tool:

    def __init__(self):
        self.tools = [
            self.scatterPlot, 
            self.barChart
        ]
    
    @tool
    def scatterPlot(
        data: Annotated[dict, "the dictionary containing the value to be plotted"], 
        x: Annotated[str, "the name of the x axis"], 
        y: Annotated[str, "the name of the y axis"],
        title: Annotated[str, "the title of the graph"],
    ):
        """ Generate a scatterplot"""
        df=pd.DataFrame(data)
        return px.scatter(
            data_frame=df, x=x, y=y, 
            color="size", color_continuous_scale="plasma", render_mode="webgl", title=title
        )

    @tool
    def barChart(
        data: Annotated[dict, "the dictionary containing the value to be plotted"], 
        x: Annotated[str, "the name of the x axis"], 
        y: Annotated[str, "the name of the y axis"],
    ):
        """ Generate a bar chart"""
        df=pd.DataFrame(data)
        return px.bar(
            data_frame=df, x=x, y=y 
        )

    
    
        
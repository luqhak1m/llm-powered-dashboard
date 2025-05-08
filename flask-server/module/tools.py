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
            self.barChart,
            self.choropleth,
            self.pieChart
        ]
    
    @tool
    def scatterPlot(
        data: Annotated[dict, "the dictionary containing the value to be plotted"], 
        x: Annotated[str, "the name of the x axis"], 
        y: Annotated[str, "the name of the y axis"],
        color: Annotated[str, "the key from the dictionary which contains the numeric value. the key capitalization must match exactly from the dictionary."],
        title: Annotated[str, "the title of the graph"],
    ):
        """ Generate a scatterplot"""
        df=pd.DataFrame(data)
        return px.scatter(
            data_frame=df, x=x, y=y, color=color, 
            color_continuous_scale="plasma", render_mode="webgl", title=title
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

    @tool
    def choropleth(
        data: Annotated[dict, "the dictionary containing the value to be plotted"], 
        locations: Annotated[str, "the name of the column from the data that contains the locations"],
        locationmode: Annotated[str, "the set of locations used to match entries in locations. acceptable parameter are either 'ISO-3', 'USA-states', or 'country names'"],
        color: Annotated[str, "the key from the dictionary which contains the numeric value. the key capitalization must match exactly from the dictionary."],
        # color_continuous_scale: Annotated[str, "the continuous colour scale"],
        title: Annotated[str, "the title of the chart"],
    ):
        """ Generate a choropleth (map)"""
        try:
            print("converting to df...")
            df=pd.DataFrame(data)
            # print(f'''

            # df data:
                  
            #     {df.info()}        # Shows column names, non-null counts, and data types
            #     {df.head()}        # Shows the first 5 rows
            #     {df.columns}       # Lists all column names
            #     {df.dtypes}        # Shows data type of each column
            #     {df.shape}         # Tuple of (rows, columns)
            #     {df.describe()}    # Summary stats for numeric columns

            # ''')
        except Exception as e:
            print(f"converting to df failed: {e}")
        return px.choropleth(
            data_frame=df,
            locations=locations,
            locationmode=locationmode,
            color=color,
            color_continuous_scale='Viridis',
            title=title
        )
        
    @tool
    def pieChart(
        data: Annotated[dict, "the dictionary containing the value to be plotted"], 
        names: Annotated[str, "the name of the column from the data that contains the names"],
        values: Annotated[str, "the name of the column from the data that contains the values"],
        title: Annotated[str, "the title of the chart"],
    ):
        """ Generate a pie chart"""
        df=pd.DataFrame(data)
        return px.pie(
            data_frame=df,
            names=names,
            values=values,
            title=title
        )
        
    def get_tool_names(self):
        return [tool.name for tool in self.tools]
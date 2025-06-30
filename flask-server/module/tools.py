from typing_extensions import Annotated
from langchain_core.tools import tool
import plotly.express as px
import plotly.graph_objects as go
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
            self.pieChart,
            # self.heatMap,
            self.table,
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
        try:
            print("converting to df...")
            df=pd.DataFrame(data)
            return px.scatter(
                data_frame=df, x=x, y=y, color=color, 
                color_continuous_scale="plasma", render_mode="webgl", title=title
            )
        
        except Exception as e:
            print(f"converting to df failed: {e}")
            return e

    @tool
    def barChart(
        data: Annotated[dict, "the dictionary containing the value to be plotted"], 
        x: Annotated[str, "the name of the x axis"], 
        y: Annotated[str, "the name of the y axis"],
    ):
        """ Generate a bar chart"""

        try:
            print("converting to df...")
            df=pd.DataFrame(data)
            return px.bar(
                data_frame=df, x=x, y=y
            )
        except Exception as e:
            print(f"converting to df failed: {e}")
            return e

    @tool
    def choropleth(
        data: Annotated[dict, "the dictionary containing the value to be plotted"], 
        locations: Annotated[str, "the name of the column from the data that contains the locations"],
        locationmode: Annotated[str, "the set of locations used to match entries in locations. acceptable parameter is either 'ISO-3', 'USA-states', or 'country names'"],
        color: Annotated[str, "the key from the dictionary which contains the numeric value. the key capitalization must match exactly from the dictionary."],
        # color_continuous_scale: Annotated[str, "the continuous colour scale"],
        title: Annotated[str, "the title of the chart"],
    ):
        """ Generate a choropleth (map)"""
        try:
            print("converting to df...")
            df=pd.DataFrame(data)
            return px.choropleth(
                data_frame=df,
                locations=locations,
                locationmode=locationmode,
                color=color,
                color_continuous_scale='Viridis',
                title=title
        )
        except Exception as e:
            print(f"converting to df failed: {e}")
            return e
        
    @tool
    def pieChart(
        data: Annotated[dict, "the dictionary containing the value to be plotted"], 
        names: Annotated[str, "the name of the column from the data that contains the names"],
        values: Annotated[str, "the name of the column from the data that contains the values"],
        title: Annotated[str, "the title of the chart"],
    ):
        """ Generate a pie chart"""
        try:
            print("converting to df...")
            df=pd.DataFrame(data)
            return px.pie(
                data_frame=df,
                names=names,
                values=values,
                title=title
            )
        except Exception as e:
            print(f"converting to df failed: {e}")
            return e
    
    # @tool
    # def heatMap(
    #     data: Annotated[dict, "the dictionary containing the value to be plotted"], 
    #     x: Annotated[str, "the name of the x axis"], 
    #     y: Annotated[str, "the name of the y axis"],
    #     color: Annotated[str, "the key from the dictionary which contains the numeric value. the key capitalization must match exactly from the dictionary."],
    #     title: Annotated[str, "the title of the graph"],
    # ):
    #     """ Generate a heatmap """
    #     try:
    #         print("converting to df...")
    #         df = pd.DataFrame(data)

    #         heatmap_data = df.pivot(index=y, columns=x, values=color)

    #         fig = px.imshow(
    #             heatmap_data,
    #             color_continuous_scale="plasma",
    #             text_auto=True,
    #             title=title
    #         )
    #         return fig

    #     except Exception as e:
    #         print(f"heatmap failed: {e}")
    #         return e
        
    @tool
    def table(
        data: Annotated[dict, "the dictionary containing the value to be plotted"], 
        title: Annotated[str, "the title of the graph"],
    ):
        """Generate a table"""
        try:
            print("converting to df...")
            df = pd.DataFrame(data)

            fig = go.Figure(data=[go.Table(
                header=dict(values=list(df.columns), fill_color='paleturquoise', align='left'),
                cells=dict(values=[df[col] for col in df.columns], fill_color='lavender', align='left')
            )])
            fig.update_layout(title=title)
            return fig

        except Exception as e:
            print(f"converting to df failed: {e}")
            return e
    
    def get_tool_names(self):
        return [tool.name for tool in self.tools]



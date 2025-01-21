from intake.source import base
import httpx
from .utilities import get_drought_area_type_dropdown, get_drought_index
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DroughtDataTimeSeries(base.DataSource):
    container = "python"
    version = "0.0.4"
    name = "drought_api_timeseries_data"
    visualization_args = {
        "area_type": get_drought_area_type_dropdown(),
        "data_index": get_drought_index()    
    }
    visualization_group = "Drought_Monitor"
    visualization_label = "U.S. Drought Monitor Data Time Series"
    visualization_type = "plotly"

    def __init__(self, area_type,data_index,metadata=None):

        self.api_base_url = "https://droughtmonitor.unl.edu/DmData/TimeSeries.aspx/ReturnBasicDmTimeSeries"
        self.area_type = area_type.split('-')[0]
        self.area = area_type.split('-')[1]
        self.data_index = data_index
        self.statistic_type = 1
        super(DroughtDataTimeSeries, self).__init__(metadata=metadata)

    def read(self):
        data = self._get_data_time_series()
        traces = self.create_usdm_traces(data) if self.data_index == 'usdm' else self.create_dsci_traces(data)
        layout = self.create_layout()
        return {"data": traces, "layout": layout}

    
    def _get_data_time_series(self):
        try:
            client = httpx.Client(verify=False)
            params = {
                'area': f'"{self.area}"', 
                'type':f'"{self.area_type}"' , 
                'statstype': self.statistic_type
            }
            response = client.get(
                url=f"{self.api_base_url}",
                timeout=None,
                params=params,
                headers={"Content-Type": "application/json"}
            )
            data = response.json()
            unparsed_timeseries = data.get('d', [])
            if len(unparsed_timeseries) < 1:
                return []
            else:
                return unparsed_timeseries
        except httpx.HTTPError as exc:
            logger.error(f"Error while requesting {exc.request.url!r}: {exc}")
            return []
    

    @staticmethod
    def create_usdm_traces(data):
        """
        Create traces for plotly.js based on the input data.

        Parameters:
        data (list of dict): The input data containing dates and drought levels.

        Returns:
        list of dict: A list of trace dictionaries suitable for plotly.js.
        """
        if len(data) < 1:
            return []
        # Extract dates
        dates = [item['Date'] for item in data]

        # Define drought levels, colors, and labels
        drought_levels = ['D0', 'D1', 'D2', 'D3', 'D4']
        colors = {
            'D0': '#ffff00',
            'D1': '#fcd37f',
            'D2': '#ffaa00',
            'D3': '#e60000',
            'D4': '#730000'
        }
        labels = {
            'D0': 'D0-D4',
            'D1': 'D1-D4',
            'D2': 'D2-D4',
            'D3': 'D3-D4',
            'D4': 'D4'
        }

        # Create traces
        traces = []
        for level in drought_levels:
            y_values = [item.get(level, 0) for item in data]
            trace = {
                'x': dates,
                'y': y_values,
                'type': 'scatter',
                'mode': 'lines',
                'name': labels[level],
                'line': {
                    'color': colors[level]
                },
                'hoverinfo': 'x+y+name'
            }
            traces.append(trace)

        return traces


    @staticmethod
    def create_dsci_traces(data):
        if len(data) < 1:
            return []
        # Extract dates
        dates = [item['Date'] for item in data]
        # Create traces
        traces = []
        y_values = [item.get('DSCI', 0) for item in data]
        trace = {
            'x': dates,
            'y': y_values,
            'type': 'scatter',
            'mode': 'lines',
            'name': 'DSCI',
            'line': {
                'color': '#8E0090'
            },
            'hoverinfo': 'x+y+name'
        }
        traces.append(trace)

        return traces
        
    @staticmethod
    def create_layout():
        """
        Create layout for plotly.js plot.

        Returns:
        dict: A layout dictionary suitable for plotly.js.
        """
        layout = {
            'title': 'Drought Levels Over Time',
            'xaxis': {
                'title': 'Date',
                'tickformat': '%Y-%m-%d',
                'type': 'date'
            },
            'yaxis': {
                'title': 'Percentage Area',
                'ticksuffix': '%'
            },
            'legend': {
                'title': {
                    'text': 'Drought Level'
                }
            },
            'hovermode': 'x',
            'margin': {
                'l': 60,
                'r': 50,
                't': 80,
                'b': 60
            }
        }

        return layout
from intake.source import base
import logging
import httpx
from .utilities import get_geojson, get_drought_dates,get_base_map_layers_dropdown,rgb_to_hex
from .sourceUrls import json_urls,esri_urls
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DroughtMapViewer(base.DataSource):
    container = "python"
    version = "0.0.4"
    name = "drought_map_viewer"
    visualization_args = {
        "date": get_drought_dates(), 
        "base_map_layer": get_base_map_layers_dropdown(),
    }
    visualization_group = "Drought_Monitor"
    visualization_label = "Drought Monitor Map Viewer"
    visualization_type = "custom"

    def __init__(self,date,base_map_layer,metadata=None):
        self.date = date
        # self.mfe_unpkg_url = "http://localhost:4000/remoteEntry.js"
        self.mfe_unpkg_url = "https://unpkg.com/mfe_drought_map@0.0.1/dist/remoteEntry.js"
        self.mfe_scope = "mfe_drought_map"
        self.mfe_module = "./MapComponent"
        self.view = self.get_view_config()
        self.map_config = self.get_map_config()
        self.base_map_layer = self.get_esri_base_layer_dict(base_map_layer)
        super(DroughtMapViewer, self).__init__(metadata=metadata)

    def read(self):
        logger.info("Reading map data configuration")
        return {
            "url": self.mfe_unpkg_url,
            "scope": self.mfe_scope,
            "module": self.mfe_module,
            "props": {
                "extraLayers": self.get_extra_layers(),
                "layers": self.get_layers(),
                "viewConfig": self.view,
                "mapConfig": self.map_config,
                "legend": self.make_legend(),
            },
        }

    def get_extra_layers(self):
        layers = [self.get_usdm_layer()]
        return layers
    
    def get_layers(self):
        drought_outlook_layer = self.get_drought_outlook_layer()
        layers = [self.base_map_layer,drought_outlook_layer]
        return layers
    

    def get_drought_outlook_layer(self):
        service_url = esri_urls['cpc_drought_outlk_url_esri'];
        layer_dict = {
            "type": "ImageLayer",
            "props": {
                "source": {
                    "type": "ImageArcGISRest",
                    "props": {
                        "url": service_url,
                        "params": {
                            "LAYERS": "show:0",
                        },
                    },
                },
                "name": 'Monthly Drought Outlook',
                "visible": False,
            },
        }
        logger.info(f"Service layer dictionary created for Monthly Drought Outlook")
        return layer_dict
    
    def get_usdm_layer(self):
        url = f'{json_urls['usdm']}_{self.date}.json'
        try:
            usdm_layer = get_geojson(url)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
        return usdm_layer


    @staticmethod
    def get_map_config():
        map_config = {
            "className": "ol-map",
            "style": {"width": "100%", "height": "100%", "position": "relative"},
        }
        logger.info("Map configuration created")
        return map_config
    
    @staticmethod
    def get_view_config():

        view_config = {
          "center": [-11807318, 4983337],
          "zoom": 4,
          "maxZoom": 11,
          "minZoom": 3,
        }
        logger.info("View configuration created")
        return view_config


    @staticmethod
    def get_esri_base_layer_dict(base_map_layer):
        layer_dict = {
            "type": "WebGLTile",
            "props": {
                "source": {
                    "type": "ImageTile",
                    "props": {
                        "url": f"{base_map_layer}/tile/" + "{z}/{y}/{x}",
                        "attributions": f'Tiles © <a href="{base_map_layer}">ArcGIS</a>',
                    },
                },
                "name": f'{base_map_layer.split("/")[-2].replace("_"," ").title()}',
            },
        }
        logger.info("Base layer dictionary created")
        return layer_dict
    
    @staticmethod
    def get_USDM_legend():
        legend = {
            'title': 'USDM Archive',
            'items':[
                {
                    "color": rgb_to_hex([255, 255, 0, 1]),
                    "label": "Abnormally Dry",
                },
                {
                    "color": rgb_to_hex([252, 211, 127, 1]),
                    "label": "Moderate Drought",
                },
                {
                    "color": rgb_to_hex([255, 170, 0, 1]),
                    "label": "Severe Drought",
                },
                {
                    "color": rgb_to_hex([230, 0, 0, 1]),
                    "label": "Extreme Drought",
                },
                {
                    "color": rgb_to_hex([115, 0, 0, 1]),
                    "label": "Exceptional Drought",
                },
                {
                    "color": rgb_to_hex([128, 128, 128, 1]),
                    "label": "No Data",
                },
                {
                    "color": rgb_to_hex([255, 255, 255, 1]),
                    "label": "None",
                },
            ]


        }
        return legend

    @staticmethod
    def get_drought_outlook_legend():
        legend = {
            'title': 'Monthly Drought Outlook',
            'items':[
                {
                    "color": '#9b634a',
                    "label": " Drought Persists",
                },
                {
                    "color": '#ded2bc',
                    "label": " Drought Remains but Improves",
                },
                {
                    "color": '#b2ad69',
                    "label": "Drought Removal Likely",
                },
                {
                    "color": '#ffde63',
                    "label": "Drought Development Likely",
                }
            ]


        }
        return legend

    
    def make_legend(self):
        """Create a list of dicts with color in hex and label."""

        logger.info("Creating legend for the map")
        legend = [self.get_USDM_legend(), self.get_drought_outlook_legend()]


        logger.info("Legend created successfully")
        return legend
    


import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_base_map_layers_dropdown():
    return [
        {
            "label": "ArcGIS Map Service Base Maps",
            "options": [
                {
                    "label": "World Light Gray Base",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Light_Gray_Base/MapServer",
                },
                {
                    "label": "World Dark Gray Base",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Dark_Gray_Base/MapServer",
                },
                {
                    "label": "World Topo Map",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/World_Topo_Map/MapServer",
                },
                {
                    "label": "World Imagery",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer",
                },
                {
                    "label": "World Terrain Base",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/World_Terrain_Base/MapServer",
                },
                {
                    "label": "World Street Map",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer",
                },
                {
                    "label": "World Physical Map",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/World_Physical_Map/MapServer",
                },
                {
                    "label": "World Shaded Relief",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/World_Shaded_Relief/MapServer",
                },
                {
                    "label": "World Terrain Reference",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/World_Terrain_Reference/MapServer",
                },
                {
                    "label": "World Hillshade Dark",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade_Dark/MapServer",
                },
                {
                    "label": "World Hillshade",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade/MapServer",
                },
                {
                    "label": "World Boundaries and Places Alternate",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Reference/World_Boundaries_and_Places_Alternate/MapServer",
                },
                {
                    "label": "World Boundaries and Places",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Reference/World_Boundaries_and_Places/MapServer",
                },
                {
                    "label": "World Reference Overlay",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Reference/World_Reference_Overlay/MapServer",
                },
                {
                    "label": "World Transportation",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Reference/World_Transportation/MapServer",
                },
                {
                    "label": "World Ocean Base ",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Ocean/World_Ocean_Base/MapServer",
                },
                {
                    "label": "World Ocean Reference",
                    "value": "https://server.arcgisonline.com/arcgis/rest/services/Ocean/World_Ocean_Reference/MapServer",
                },
            ],
        }
    ]

def rgb_to_hex(rgb_color):
    """Convert RGB color to hex color code."""
    if rgb_color and len(rgb_color) >= 3:
        return "#{:02x}{:02x}{:02x}".format(*rgb_color[:3])
    return "#000000"
# Drought
def get_drought_statistic_type():
        return [
            {
                "label": "Drought Statistic Type",
                "options": [
                    {
                        "label": "Cumulative Percent Area",
                        "value": 1,
                    },
                    {
                        "label": "Categorical Percent Area",
                        "value": 2,
                    },
                    {
                        "label": "Cumulative Area",
                        "value": 3,
                    },
                    {
                        "label": "Categorical Area",
                        "value": 4,
                    },
                ]
            }
        ]

def get_drought_area_type_dropdown():
    api_endpoint = 'https://droughtmonitor.unl.edu/DmData/DataTables.aspx/ReturnAOI'
    area_types_dict = {
        "national": "National",
        "state": "State",
        "climdiv": "Climate Division",
        "dregion": "Geographic Regions",
        "county": "County",
        "fema": "FEMA Region",
        "huc2": "HUC (2 digit)",
        "huc4": "HUC (4 digit)",
        "huc6": "HUC (6 digit)",
        "huc8": "HUC (8 digit)",
        "nws": "NWS Region",
        "wfo": "NWS Weather Forecast Offices",
        "rfc": "River Forecast Centers",
        "tribal": "Tribal Areas",
        "usaceds": "USACE District",
        "usacedv": "USACE Division",
        "chubs": "USDA Climate Hubs",
        "rdews": "Regional Drought Early Warning System",
        "rcc": "Regional Climate Centers",
        "oregion": "Other Regions",
    }
    dropdown_items = []
    client = httpx.Client(verify=False)
    for key, value in area_types_dict.items():
        dropdown_item ={
            "label": value,
            "options":[]
        }
        try:
            response = client.get(f'{api_endpoint}?aoi="{key}"', headers={"Content-Type": "application/json"})
            data = response.json()
            for item in data.get('d', []):
                dropdown_item['options'].append({
                    "value": f'{key}-{item.get("Value")}',
                    "label": item.get("Text")
                })
            dropdown_items.append(dropdown_item)
        except httpx.HTTPError as exc:
            logger.error(f"Error while requesting {exc.request.url!r}: {str(exc.__class__.__name__)}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
    return dropdown_items

def get_drought_data_type():
    return [
        {
            "label": "Drought Data Types",
            "options": [
                {
                    "label": "USDM",
                    "value": "0",
                },
                {
                    "label": "7-day Change",
                    "value": "1",
                }
            ]
        }
    ]


def get_drought_index():

    return [
        {
            "label": "Drought Data Index",
            "options": [
                {
                    "label": "USDM",
                    "value": "usdm",
                },
                {
                    "label": "DSCI",
                    "value": "DSCI",
                }
            ]
        }
    ]


def get_drought_dates():
    api_endpoint = 'https://droughtmonitor.unl.edu/Maps/CompareTwoWeeks.aspx/ReturnDates'
    client = httpx.Client(verify=False)
    response = client.get(f'{api_endpoint}', headers={"Content-Type": "application/json"})
    data = response.json()
    dropdown_items = []
    dropdown_item ={
        "label": "Drought Dates",
        "options":[]
    }
    for item in data.get('d', []):
        dropdown_item['options'].append({
            "value": f'{item.get("Value")}',
            "label": item.get("Text")
        })
    dropdown_items.append(dropdown_item)
    return dropdown_items


def get_geojson(url):
    try:
        with httpx.Client(verify=False) as client:
            r = client.get(
                url=url,
                timeout=None,
            )
            if r.status_code != 200:
                logger.error(f"Error: {r.status_code}")
                logger.error(r.text)
                return None
            else:
                return r.json()
    except httpx.HTTPError as exc:
        logger.error(f"Error while requesting {exc.request.url!r}: {exc}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
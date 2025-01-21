from intake.source import base
import httpx
from .utilities import get_drought_area_type_dropdown,get_drought_statistic_type,get_drought_data_type
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DroughtDataTable(base.DataSource):
    container = "python"
    version = "0.0.4"
    name = "drought_api_table_data"
    visualization_args = {
        "area_type": get_drought_area_type_dropdown(),
        "statistic_type": get_drought_statistic_type(),
        "data_type": get_drought_data_type()
    }
    visualization_group = "Drought_Monitor"
    visualization_label = "U.S. Drought Monitor Data Table"
    visualization_type = "custom"

    def __init__(self, area_type,statistic_type,data_type,metadata=None):
        # self.mfe_unpkg_url = "http://localhost:3000/remoteEntry.js"
        self.mfe_unpkg_url = "https://unpkg.com/mfe_drought_table@0.0.1/dist/remoteEntry.js"
        self.mfe_scope = "mfe_drought_table"
        self.mfe_module = "./TableComponent"
        self.api_base_url = "https://droughtmonitor.unl.edu/DmData/DataTables.aspx/ReturnTabularDMAreaPercent"
        self.area_type = area_type.split('-')[0]
        self.area = area_type.split('-')[1]
        self.statistic_type = statistic_type,
        self.data_type = data_type
        super(DroughtDataTable, self).__init__(metadata=metadata)

    def read(self):
        table_data = self.get_data_table()
        return {
            "url": self.mfe_unpkg_url,
            "scope": self.mfe_scope,
            "module": self.mfe_module,
            "props": {
                "data": table_data,
            },
        }

    def get_data_table(self):
        try:
            client = httpx.Client(verify=False)
            params = {'area': f"'{self.area}'", 'statstype':f"'{self.statistic_type[0]}'" , 'diff': f"'{self.data_type}'"}
            r = client.get(
                url=f"{self.api_base_url}_{self.area_type}",
                timeout=None,
                params=params,
                headers={"Content-Type": "application/json"}
            )
            data = r.json()
            return data.get('d', [])
        except httpx.HTTPError as exc:
            logger.error(f"Error while requesting {exc.request.url!r}: {exc}")
            return []
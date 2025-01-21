# WMS URLs
wms_urls = {
    "atlas_base_url": "http://ndmc-001.unl.edu:8080/cgi-bin/mapserv.exe?map=/ms4w/apps/BaseLayers/service/base_layers_dra_3857.map",
    "usdm_wms_base_url": "http://ndmc-001.unl.edu:8080/cgi-bin/mapserv.exe?map=/ms4w/apps/usdm/service/",
    "vegdri_wms_url": "https://dmsdata.cr.usgs.gov/geoserver/quickdri_vegdri_conus_week_data/vegdri_conus_week_data/wms",
    "quickdri_wms_url": "https://dmsdata.cr.usgs.gov/geoserver/quickdri_quickdri_conus_week_data/quickdri_conus_week_data/wms",
    "waterwatch_wms_url": "https://edcintl.cr.usgs.gov/geoserver/quickdri_water_watch_today/wms",
    "precipdays_7_wms_url": "https://edcintl.cr.usgs.gov/geoserver/quickdri_precipcdd7_conus_1_day_data/wms",
    "precipdays_30_wms_url": "https://edcintl.cr.usgs.gov/geoserver/quickdri_preciprd30_conus_1_day_data/wms",
    "totprecip_7_wms_url": "https://edcintl.cr.usgs.gov/geoserver/quickdri_preciptp7_conus_1_day_data/wms",
    "totprecip_30_wms_url": "https://edcintl.cr.usgs.gov/geoserver/quickdri_preciptp30_conus_1_day_data/wms",
    "drydays_7_wms_url": "https://edcintl.cr.usgs.gov/geoserver/quickdri_precipcdd7_conus_1_day_data/wms",
    "drydays_30_wms_url": "https://edcintl.cr.usgs.gov/geoserver/quickdri_precipcdd30_conus_1_day_data/wms",
    "last_precip_wms_url": "https://edcintl.cr.usgs.gov/geoserver/quickdri_precipdsr_conus_1_day_data/wms",
    "usdm_curr_wms_url": "https://edcintl.cr.usgs.gov/geoserver/quickdri_drought/wms",
    "nat_land_cover_2019_url": "https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2019_Land_Cover_L48/wms",
    "radar_wms_url": "https://gis.ncdc.noaa.gov/arcgis/rest/services/geo/radar_coverage/MapServer/WMSServer",
    "usdm_wms_url": "https://edcintl.cr.usgs.gov/geoserver/quickdri_drought/wms",
    "drought_out_url_esri_wms": "https://idpgis.ncep.noaa.gov/arcgis/services/NWS_Climate_Outlooks/cpc_drought_outlk/MapServer/WMSServer",
    "precip_out_url_esri_wms": "https://idpgis.ncep.noaa.gov/arcgis/services/NWS_Climate_Outlooks/cpc_6_10_day_outlk/WMSServer",
    "temp_out_url_esri_wms": "https://idpgis.ncep.noaa.gov/arcgis/rest/services/NWS_Climate_Outlooks/cpc_6_10_day_outlk/WMSServer"
}

# WFS URLs
wfs_urls = {
    "waterwatch_wfs_url": "https://edcintl.cr.usgs.gov/geoserver/quickdri_water_watch_today/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=quickdri_water_watch_today%3Awater_watch_today&outputFormat=application%2Fjson",
    "usdm_current_wfs_url": "https://dservices5.arcgis.com/0OTVzJS4K09zlixn/arcgis/services/USDM_current/WFSServer?service=wfs&request=GetFeature&typeName=USDM_current&outputFormat=GEOJSON"
}

# ESRI URLs
esri_urls = {
    "county_url_esri": "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/Counties/FeatureServer/",
    "climdiv_url_esri": "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/Climate_Divisions/FeatureServer/",
    "climhub_url_esri": "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/Climate_Hubs/FeatureServer/",
    "fema_rgn_url_esri": "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/FEMA_Regions/FeatureServer/",
    "huc2_url_esri": "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/HUC_2_digit/FeatureServer/",
    "nws_rgn_url_esri": "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/NWS_Regions/FeatureServer/",
    "nws_wfo_url_esri": "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/NWS_WFO/FeatureServer/",
    "rcc_url_esri": "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/Regional_Climate_Centers/FeatureServer/",
    "rfc_url_esri": "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/River_Forecast_Centers/FeatureServer/",
    "us_states_url_esri": "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/States/FeatureServer/",
    "urban_area_url_esri": "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/Urban_Areas/FeatureServer/",
    "rma_url_esri" : "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/RMA_Regions/FeatureServer/",
    "cocorahs_url_esri" : "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/CoCoRaHS_Reports_NDMC/FeatureServer/0",
    "cmor_url_esri" : "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/CMOR_Master/FeatureServer/0",
    "cmor_current_url_esri" : "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/CMOR_2022_Public/FeatureServer/",
    "cmor_unified_url_esri" : "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/CMOR_Unified_view/FeatureServer/",
    "cmor_mt_url_esri" : "https://services.arcgis.com/qnjIrwR8z5Izc0ij/ArcGIS/rest/services/service_dfbd68fe8806409f978c1d73761bc31d/FeatureServer/0",
    "drought_out_vector_url_esri" : "https://idpgis.ncep.noaa.gov/arcgis/rest/services/NWS_Climate_Outlooks/cpc_drought_outlk/FeatureServer/0",
    "drought_out_url_esri" : "https://idpgis.ncep.noaa.gov/arcgis/rest/services/NWS_Climate_Outlooks/cpc_drought_outlk/MapServer",
    "precip_out_url_esri" : "https://idpgis.ncep.noaa.gov/arcgis/rest/services/NWS_Climate_Outlooks/cpc_6_10_day_outlk/MapServer",
    "temp_out_url_esri" : "https://idpgis.ncep.noaa.gov/arcgis/rest/services/NWS_Climate_Outlooks/cpc_6_10_day_outlk/MapServer",
    "usdm_url_esri" : "https://services5.arcgis.com/0OTVzJS4K09zlixn/ArcGIS/rest/services/USDM_archive/MapServer",
    "usdm_vector_url_esri" : "https://services5.arcgis.com/0OTVzJS4K09zlixn/ArcGIS/rest/services/USDM_current/FeatureServer/",
    "usdm_arch_url_esri" : "https://services5.arcgis.com/0OTVzJS4K09zlixn/ArcGIS/rest/services/USDM_archive/FeatureServer/",
    "vegdri_url_esri" : "https://tiles.arcgis.com/tiles/0OTVzJS4K09zlixn/arcgis/rest/services/VegDRI_Example/MapServer",
    "ahps_url_esri" : "https://mapservices.weather.noaa.gov/raster/rest/services/obs/rfc_qpe/MapServer",
    "dra_stn_clim_url_esri" : "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/Drought_Risk_Atlas_Climate_Stations_(2017)/FeatureServer/",
    "dra_stn_hydro_url_esri" : "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/Drought_Risk_Atlas_Hydro_Stations_(2017)/FeatureServer/",
    "vda_archive_url_esri" : "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/VDA_USDM_ArchivedPhotos_Public/FeatureServer/",
    "vda_current_url_esri" : "https://services5.arcgis.com/0OTVzJS4K09zlixn/arcgis/rest/services/CMOR_USDM_Combined_Photos_Public/FeatureServer/",
    "ndam_current_url_esri" : "https://services5.arcgis.com/0OTVzJS4K09zlixn/ArcGIS/rest/services/NADM_Current/FeatureServer/",
    "land_cover_url_esri" : "https://tiles.arcgis.com/tiles/0OTVzJS4K09zlixn/arcgis/rest/services/Land_Cover_2020/MapServer/",
    "land_use_url_esri" : "https://tiles.arcgis.com/tiles/0OTVzJS4K09zlixn/arcgis/rest/services/Land_Use_2020/MapServer/",
    "biomass_example_url_esri" : "https://tiles.arcgis.com/tiles/0OTVzJS4K09zlixn/arcgis/rest/services/Biomass_2018_masked_tif/MapServer/",
    "land_owner_url_esri" : "https://gis1.usgs.gov/arcgis/rest/services/padus2_1/FeeManagers/MapServer/",
    "huc4_tile_url_esri" : "https://tiles.arcgis.com/tiles/0OTVzJS4K09zlixn/arcgis/rest/services/HUC4_Simplified/MapServer/",
    "county_tile_url_esri" : "https://tiles.arcgis.com/tiles/0OTVzJS4K09zlixn/arcgis/rest/services/Counties_Simplified/MapServer/",
    "nws_radar_tile_url_esri" : "https://tiles.arcgis.com/tiles/0OTVzJS4K09zlixn/arcgis/rest/services/NWS_Radar_10k/MapServer",
    "indemnity_tile_url_esri" : "https://tiles.arcgis.com/tiles/0OTVzJS4K09zlixn/arcgis/rest/services/Median_RMA_Payments/MapServer/",
    "cpc_6_10_day_outlk_url_esri" : "https://mapservices.weather.noaa.gov/vector/rest/services/outlooks/cpc_6_10_day_outlk/MapServer/",
    "cpc_8_14_day_outlk_url_esri" : "https://mapservices.weather.noaa.gov/vector/rest/services/outlooks/cpc_8_14_day_outlk/MapServer/",
    "cpc_mthly_temp_outlk_url_esri" : "https://mapservices.weather.noaa.gov/vector/rest/services/outlooks/cpc_mthly_temp_outlk/MapServer/",
    "cpc_mthly_precip_outlk_url_esri" : "https://mapservices.weather.noaa.gov/vector/rest/services/outlooks/cpc_mthly_precip_outlk/MapServer/",
    "cpc_sea_temp_outlk_url_esri" : "https://mapservices.weather.noaa.gov/vector/rest/services/outlooks/cpc_sea_temp_outlk/MapServer/",
    "cpc_sea_precip_outlk_url_esri" : "https://mapservices.weather.noaa.gov/vector/rest/services/outlooks/cpc_sea_precip_outlk/MapServer/",
    "cpc_drought_outlk_url_esri" : "https://mapservices.weather.noaa.gov/vector/rest/services/outlooks/cpc_drought_outlk/MapServer/",    
}

json_urls = {
    "usdm": "https://droughtmonitor.unl.edu/data/json/usdm"
}
# KML URLs
kml_urls = {
    "usgs_strm_real_url_kml": "https://waterwatch.usgs.gov/index.php?m=real&w=kml&r=us&regions=all2"
}

# NIDIS URLs
nidis_urls = {
    "nidis_base_url": "https://storage.googleapis.com/noaa-nidis-drought-gov-data/current-conditions/tile/v1/",
}

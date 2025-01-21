from datetime import datetime
from typing import Any

import fiona.errors
import geopandas as gpd
from pystac import Item
from pystac.extensions.projection import ProjectionExtension
from shapely.geometry import Polygon, mapping, shape

HYDRO_DOMAIN_DESCRIPTION = "hydro_domain:description"
HYDRO_DOMAIN_TYPE = "hydro_domain:type"
DATETIME_INFO = "datetime_info"
PROJ_EPSG = "proj:epsg"


class HydroDomain(Item):
    """
    Options include watershed, transposition_region, valid_transposition_region
    """

    def __init__(
        self,
        id: str,
        geometry: str | Polygon,
        hydro_domain_type: str,
        relevant_datetime: str | datetime = None,
        relevant_datetime_description: str = None,
        **kwargs: Any,
    ):

        self.id = id
        self.geometry = self.load_geometry(geometry)
        if hydro_domain_type not in ["watershed", "transposition_region", "valid_transposition_region"]:
            raise ValueError(
                f"hydro_domain_type must be one of: watershed, transposition_region, valid_transposition_region, not {hydro_domain_type}"
            )

        self.hydro_domain_type = hydro_domain_type

        if isinstance(relevant_datetime, str):
            self.relevant_datetime = datetime.fromisoformat(relevant_datetime)
        elif isinstance(relevant_datetime, datetime):
            self.relevant_datetime = relevant_datetime
        else:
            self.relevant_datetime = datetime.now()

        if not relevant_datetime_description:
            self.relevant_datetime_description = "Creation date of the item"

        self.stac_extensions = kwargs.get("stac_extensions", None)
        self.href = kwargs.get("href", None)
        self.properties = kwargs.get("properties", {})
        self.start_datetime = kwargs.get("start_datetime", None)
        self.end_datetime = kwargs.get("end_datetime", None)
        self.collection = kwargs.get("collection", None)
        self.extra_fields = kwargs.get("extra_fields", None)
        self.assets = kwargs.get("assets", None)
        self.description = kwargs.get("description", None)
        self.title = kwargs.get("title", None)

        if self.title:
            self.properties["title"] = self.title
        if self.description:
            self.properties["description"] = self.description

        super().__init__(
            id=self.id,
            geometry=mapping(self.geometry),
            bbox=self.geometry.bounds,
            datetime=self.relevant_datetime,
            properties=self.properties,
            stac_extensions=self.stac_extensions,
            href=self.href,
            collection=self.collection,
            extra_fields=self.extra_fields,
            assets=self.assets,
        )

        self._register_extensions()
        self.properties[HYDRO_DOMAIN_TYPE] = self.hydro_domain_type
        self.properties[DATETIME_INFO] = self.relevant_datetime_description
        self.properties[PROJ_EPSG] = 4326

    @classmethod
    def from_item(cls, item: Item) -> "HydroDomain":
        return cls(
            id=item.id,
            geometry=shape(item.geometry),
            hydro_domain_type=item.properties.get(HYDRO_DOMAIN_TYPE),
            relevant_datetime=item.properties.get("datetime"),
            relevant_datetime_description=item.properties.get("datetime_description"),
        )

    def _register_extensions(self) -> None:
        ProjectionExtension.add_to(self)
        # StorageExtension.add_to(self)

    def _ensure_datetime(self, dt):
        if isinstance(dt, str):
            return datetime.datetime.fromisoformat(dt)
        return dt or datetime.datetime.now()

    def load_geometry(self, geometry_source) -> Polygon:
        if isinstance(geometry_source, str):
            try:
                gdf = gpd.read_file(geometry_source)
            except (fiona.errors.FionaValueError, fiona.errors.DriverError) as e:
                raise ValueError(f"Error reading the geometry file: {e}")
        elif isinstance(geometry_source, Polygon):
            gdf = gpd.GeoDataFrame(geometry=[geometry_source], crs="EPSG:4326")
        else:
            raise ValueError("geometry_source must be a file path or a Polygon object")

        if len(gdf) != 1 or not isinstance(gdf.geometry.iloc[0], Polygon):
            raise ValueError("The geometry must contain a single polygon")

        try:
            if gdf.crs != "EPSG:4326":
                gdf = gdf.to_crs("EPSG:4326")
        except ValueError as e:
            raise ValueError(f"Error converting CRS to EPSG:4326: {e}")

        return gdf.geometry.iloc[0]

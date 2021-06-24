# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '14 Jun 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from elasticsearch_dsl import Document, InnerDoc, Nested
from elasticsearch_dsl import DateRange, GeoShape
from .utils import Coordinates, rgetattr

from typing import Optional, List, Dict


class Extent(InnerDoc):

    temporal = DateRange()
    spatial = GeoShape()


class ElasticsearchCollection(Document):
    """
    Collection class
    """
    type = 'Collection'
    extent = Nested(Extent)

    @classmethod
    def search(cls, **kwargs):
        s = super().search(**kwargs)
        s = s.filter('term', type='collection')

        return s

    def decompose(self):



        return self.to_dict()


class ElasticsearchItem(Document):
    type = 'Feature'

    @classmethod
    def search(cls, **kwargs):
        s = super().search(**kwargs)
        s = s.filter('term', type__keyword='item')

        return s

    def search_assets(self):
        s = ElasticsearchAsset.search()
        s = s.filter('term', collection_id__keyword=self.meta.id)
        return s

    @property
    def assets(self):
        return list(self.search_assets())

    def get_stac_assets(self):
        return {asset.meta.id: asset.to_stac() for asset in self.assets}

    def get_properties(self) -> Dict:

        try:
            properties = getattr(self, 'properties')
        except AttributeError:
            return {}

        return properties.to_dict()

    def get_bbox(self):
        """
        Return a WGS84 formatted bbox

        :return:
        """

        try:
            coordinates = rgetattr(self, 'spatial.bbox.coordinates')
        except AttributeError:
            return

        return Coordinates.from_geojson(coordinates).wgs84_format()


class ElasticsearchAsset(Document):

    def get_url(self) -> str:
        """
        Convert the path into a url where you can access the asset
        """
        if self.media_type == 'POSIX':
            return f'http://data.ceda.ac.uk{self.filepath_type_location}'

    def get_roles(self) -> Optional[List]:

        try:
            roles = getattr(self, 'categories')
        except AttributeError:
            return

        return list(roles)

    def to_stac(self) -> Dict:
        """
        Convert Elasticsearch DSL asset into a STAC asset.
        """

        asset = dict(
            href=self.get_url(),
            type=getattr(self, 'magic_number', None),
            title=getattr(self, 'filename', None),
            roles=self.get_roles()
        )

        return asset
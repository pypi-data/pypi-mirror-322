from ._base import SarvModule
from ._mixins import UrlMixins

class ObjIndicators(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'OBJ_Indicators'
    _label_en = 'Indicators'
    _label_pr = 'شاخص'
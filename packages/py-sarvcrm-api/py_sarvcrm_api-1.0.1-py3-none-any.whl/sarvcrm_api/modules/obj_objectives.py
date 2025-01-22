from ._base import SarvModule
from ._mixins import UrlMixins

class ObjObjectives(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'OBJ_Objectives'
    _label_en = 'Objectives'
    _label_pr = 'اهداف'
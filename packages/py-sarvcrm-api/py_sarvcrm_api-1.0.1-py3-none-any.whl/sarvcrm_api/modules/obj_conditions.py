from ._base import SarvModule
from ._mixins import UrlMixins

class ObjConditions(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'OBJ_Conditions'
    _label_en = 'Conditions'
    _label_pr = 'شرایط شاخص'
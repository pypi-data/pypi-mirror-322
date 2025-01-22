from ._base import SarvModule
from ._mixins import UrlMixins

class Leads(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Leads'
    _label_en = 'Leads'
    _label_pr = 'سرنخ'
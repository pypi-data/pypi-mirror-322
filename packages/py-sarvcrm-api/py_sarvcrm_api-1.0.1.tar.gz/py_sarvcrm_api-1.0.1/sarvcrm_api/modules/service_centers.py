from ._base import SarvModule
from ._mixins import UrlMixins

class ServiceCenters(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'Service_Centers'
    _label_en = 'Service Centers'
    _label_pr = 'مراکز سرویس'
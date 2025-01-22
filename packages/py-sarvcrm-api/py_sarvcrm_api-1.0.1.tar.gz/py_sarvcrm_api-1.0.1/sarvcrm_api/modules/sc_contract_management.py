from ._base import SarvModule
from ._mixins import UrlMixins

class ScContractManagement(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'sc_contract_management'
    _label_en = 'Services'
    _label_pr = 'خدمات'
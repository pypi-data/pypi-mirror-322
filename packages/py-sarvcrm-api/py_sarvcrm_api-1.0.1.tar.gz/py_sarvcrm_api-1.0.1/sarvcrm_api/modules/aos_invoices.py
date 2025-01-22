from ._base import SarvModule
from ._mixins import UrlMixins

class AosInvoices(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'AOS_Invoices'
    _label_en = 'Invoices'
    _label_pr = 'فاکتورها'
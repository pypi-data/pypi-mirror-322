from ._base import SarvModule
from ._mixins import UrlMixins

class ScCompetitor(SarvModule, UrlMixins.DetailView, UrlMixins.ListView, UrlMixins.EditView):
    _module_name = 'sc_competitor'
    _label_en = 'Competitor'
    _label_pr = 'رقبا'
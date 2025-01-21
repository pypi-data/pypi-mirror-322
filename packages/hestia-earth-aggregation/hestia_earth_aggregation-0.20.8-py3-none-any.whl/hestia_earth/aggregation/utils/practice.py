from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import filter_list_term_type
from hestia_earth.utils.tools import flatten


_PRACTICE_AGGREGATE_BY_UNITS = {
    TermTermType.LANDUSEMANAGEMENT: ['ratio', 'number', 'days']
}
_PRACTICE_AGGREGATE_DEFAULT_TERM_TYPES = [
    t.value
    for t in TermTermType
    if t not in _PRACTICE_AGGREGATE_BY_UNITS
]


def filter_practices(practices: list):
    return filter_list_term_type(practices, _PRACTICE_AGGREGATE_DEFAULT_TERM_TYPES) + flatten([
        p
        for term_type, units in _PRACTICE_AGGREGATE_BY_UNITS.items()
        for p in filter_list_term_type(practices, term_type)
        if p.get('term', {}).get('units') in units
    ])

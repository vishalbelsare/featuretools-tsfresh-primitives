from featuretools.primitives import AggregationPrimitive
from tsfresh.feature_extraction.feature_calculators import agg_linear_trend
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double


class AggLinearTrend(AggregationPrimitive):
    """Calculates a linear least-squares regression for values of the time
    series that were aggregated over chunks versus the sequence from 0 up to
    the number of chunks minus one.

    Args:
        attr (str) : Controls which of the characteristics are returned.
            Possible extracted attributes are: ['pvalue', 'rvalue',
            'intercept', 'slope', 'stderr'].
        chunk_len (int) : How many time series values are in each chunk.
        f_agg (str) : Name of the aggregator function. Possible values are:
            ['max', 'min' or , 'mean', 'median'].

    Docstring source:
    https://tsfresh.readthedocs.io/en/latest/api/tsfresh.feature_extraction.html#tsfresh.feature_extraction.feature_calculators.agg_linear_trend
    """

    name = "agg_linear_trend"
    input_types = [ColumnSchema(semantic_tags={"numeric"})]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={"numeric"})
    stack_on_self = False

    def __init__(self, attr, chunk_len, f_agg):
        self.attr = attr
        self.chunk_len = chunk_len
        self.f_agg = f_agg

    def get_function(self):
        def function(x):
            param = [
                {"attr": self.attr, "f_agg": self.f_agg, "chunk_len": self.chunk_len}
            ]
            values = list(agg_linear_trend(x.to_numpy(), param))
            return values[0][1]

        return function

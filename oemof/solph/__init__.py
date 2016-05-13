"""
The solph-package contains funtionalities for creating and solving an
optimizaton problem. The problem is created from oemof base classes.
Solph depend on pyomo.

"""

class Flow:
    def __init__(self, actual_value, nominal_value, variable_costs, min, max,
                 fixed_costs, summed_min, summed_max, fixed=False):
        """

        """
        self.min = min
        self.max = max
        self.actual_value = actual_value
        self.nominal_value = nominal_value
        self.variable_costs =  variable_costs
        self.fixed_costs = fixed_costs
        self.summed_min = summed_min
        self.summed_max =  summed_min
        self.fixed = fixed



# TODO: create solph sepcific energysystem subclassed from core energy system
class EnergySystem():

    def __init__(self):
        """
        """
        pass

from oemof.network import Source, Sink, Transformer

class Sink(Sink):
    """
    """
    def __init__(self):
        super().__init__()

class Source(Source):
    """
    """
    def __init__(self):
        super().__init__()

class LinearTransformer(Transformer):
    """
    """
    def __init__(self):
        super().__init__()

class Storage(Transformer):
    """
    """
    def __init__(self):

        super().__init__()

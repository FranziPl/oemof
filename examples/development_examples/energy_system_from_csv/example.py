# -*- coding: utf-8 -*-

import logging
import pandas as pd

from oemof.tools import logger
from oemof.core import energy_system as core_es
import oemof.solph as solph
from oemof.solph import OperationalModel
from oemof.solph.options import NodesFromCSV
from oemof.outputlib import to_pandas as tpd
from collections import Iterable


logger.define_logging()

timesteps_max = 25

datetime_index = pd.date_range('1/1/2012', periods=timesteps_max, freq='60min')

es = core_es.EnergySystem(groupings=solph.GROUPINGS, time_idx=datetime_index)

nodes = NodesFromCSV(file_nodes_flows='nodes_flows.csv',
                     file_nodes_flows_sequences='nodes_flows_seq_minimal.csv',
                     delimiter=',')

## print out nodes
#for k, v in nodes.items():
#    attrs = dir(v)
#    print('\n OBJ:', k, type(v))
#    print('--------------------')
#    for i in attrs:
#        if '_' not in i:
#            # dirty hack to print weakref dicts by converting to list
#            o = getattr(v, str(i))
#            if isinstance(o, Iterable) and not isinstance(o, str):
#                o = list(o)
#            print(i, ':', o)

om = OperationalModel(es, timeindex=datetime_index)

om.solve(solver='gurobi', solve_kwargs={'tee': True})

om.write('optimization_problem.lp',
         io_options={'symbolic_solver_labels': True})

logging.info('Done!')

logging.info('Check the results')

myresults = tpd.DataFramePlot(energy_system=es)

date_from = '2012-01-01 00:00:00'
date_to = '2012-12-31 23:00:00'

demand = myresults.slice_by(obj_label='demand1',
                            date_from=date_from,
                            date_to=date_to)
demand.reset_index(inplace=True)
demand.drop(['bus_label', 'type', 'obj_label'], axis=1, inplace=True)
demand.set_index('datetime', inplace=True)


wind = myresults.slice_by(obj_label='wind1',
                          date_from=date_from,
                          date_to=date_to)
wind.reset_index(inplace=True)
wind.drop(['bus_label', 'type', 'obj_label'], axis=1, inplace=True)
wind.set_index('datetime', inplace=True)


solar = myresults.slice_by(obj_label='solar1',
                           date_from=date_from,
                           date_to=date_to)
solar.reset_index(inplace=True)
solar.drop(['bus_label', 'type', 'obj_label'], axis=1, inplace=True)
solar.set_index('datetime', inplace=True)


chp1_in = myresults.slice_by(obj_label='chp1', type='input',
                             date_from=date_from,
                             date_to=date_to)
chp1_in.reset_index(inplace=True)
chp1_in.drop(['bus_label', 'type', 'obj_label'], axis=1, inplace=True)
chp1_in.set_index('datetime', inplace=True)


chp1_out = myresults.slice_by(obj_label='chp1', type='output',
                              date_from=date_from,
                              date_to=date_to)
chp1_out.reset_index(inplace=True)
chp1_out.drop(['bus_label', 'type', 'obj_label'], axis=1, inplace=True)
chp1_out.set_index('datetime', inplace=True)


df = pd.concat([demand, wind, solar, chp1_in, chp1_out], axis=1)
df.columns = ['demand', 'wind', 'solar', 'chp1_in', 'chp1_out']

area = df[['wind', 'solar', 'chp1_in', 'chp1_out']].plot(kind='area',
    stacked=True, alpha=0.5, linewidth=0)
area.set_title('Unit Commitment')
area.set_xlabel('Time')
area.set_ylabel('Power in MW')
df['demand'].plot(ax=area, color='k', style='--')

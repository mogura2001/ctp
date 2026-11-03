"""C1 import adapter only. Importing or load() never emits a recipe.

Unchanged dependencies are the pinned current parent package, not copies of
an earlier policy. A future builder must use these same local overrides and
must separately validate SOURCE-PINS and the root build gate.
"""
from pathlib import Path
import importlib,sys
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
PARENT=ROOT/'PROEVEN/selectie-pad-diagnose/20261020T192500'

def load():
    sys.dont_write_bytecode=True
    for folder in (ROOT/'PROEVEN/production-h3',PARENT,OUT/'reader',OUT):
        sys.path.insert(0,str(folder))
    result={name:importlib.import_module(name) for name in
            ('native','policy','path_diagnostic','path_diagnostic_layout',
             'path_failure_decoder','integration_base','union','plan_layout')}
    for name in ('native','policy','path_diagnostic','path_diagnostic_layout'):
        assert Path(result[name].__file__).resolve()==OUT/(name+'.py')
    assert Path(result['path_failure_decoder'].__file__).resolve()==OUT/'reader/path_failure_decoder.py'
    for name in ('integration_base','union','plan_layout'):
        assert Path(result[name].__file__).resolve()==PARENT/(name+'.py')
    return result

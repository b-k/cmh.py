""" This one-file module includes a single function `cmh`, to get a single CMH statistic from a data frame."""

from warnings import warn
import pandas as pd

def _get_control_cols(in_d, indep, dep, count_col, include, exclude):
    """Do the inclusions and exclusions to get the control columns."""

    colset = set(in_d.columns.values if include == ["∀, ∀, ∀."] else include)

    float_cols = set([i for i in colset if str(in_d[i].dtype).startswith('float')])
    if len(float_cols) > 0:
        warn("Column(s) " + str(float_cols) + """ are a real-number type, and so excluded.
Get rid of this warning by explicitly excluding them, or if appropriate, casting them
to an integer type before calling this function:
your_dframe["""+str(list(float_cols))+"] = your_dframe["+str(list(float_cols))+"""].astype('int64')
""")

    return list(set(colset).difference(set([*exclude, *float_cols, dep, indep, count_col])))


"""
Nomenclature for this section
dyin: dependent positive (yes); independent negative
Similarly for dniy (dep no; indep yes), dnin, dyiy.

risk of dependent y given independent y: dyiy/(dyiy+dniy)
risk of dependent y given independent n: dyin/(dyin+dnin)
"""

def _one_cmh_num(dyiy, dniy, dyin, dnin):
    return dyiy * (dyin+dnin)

def _one_cmh_den(dyiy, dniy, dyin, dnin):
    return dyin * (dyiy+dniy)

def cmh(d,  indep, dep, count_col="1", include=["∀, ∀, ∀."], exclude=[], dep_c=(lambda x: x>0), indep_c=(lambda x: x>0), verbose=False):
    """ Calculate the Cochran-Mantel-Haenszel statistic for the given
columns. Controlling for all other factors, what is the aggregate ratio of risk
of the dependent variable given the independent variable is true versus the risk
given the independent variable is false?

d -- the data frame with the requisite information
indep -- the column that varies in the pseudoexperiment
dep -- the column whose risk is the outcome of the pseudoexperiment

keyword arguments:
count_col -- The column giving weights or counts. If not given, each observation has weight one.
include -- of the other columns in the table, which should be included as controls?  Default: all.
exclude -- of the other columns in the table, which should not be included as controls? Default: none.
dep_c -- The classifier for the dependent variable. Default: lambda x: x>0. Can be used to
   select a single item out of a categorical list, for example.
indep_c -- The classifier for the independent variable.
verbose -- If True, print some intermediate calculations.
    """

    controls = _get_control_cols(d, indep, dep, count_col, include, exclude)
    if len(controls) == 0:
        controls = ["1"]

    if verbose:
        print(f'Independent: {indep}, dependent: {dep}, controls: {controls}')

    # Reduce what may be a one-observation-per-column data set into an aggregate.
    dT = d[dep].apply(dep_c).astype('int64')
    iT = d[indep].apply(indep_c).astype('int64')
    ct = 1 if count_col == "1" else d[count_col]
    counts = pd.DataFrame(data= {
        "dyiy":  (dT & iT) * ct,
        "dniy": ((1- dT) & iT) * ct,
        "dyin": (dT & (1- iT)) * ct,
        "dnin": ((1- dT) & (1- iT)) * ct,
        "1": 1
        })

    dc = pd.concat([d, counts], axis=1)
    t = dc.groupby(by=controls, as_index=True).agg({'dyiy':sum, 'dyin':sum, 'dniy':sum, 'dnin':sum, count_col:sum})
    t.loc[:, "num"] = t.apply(lambda r: _one_cmh_num(r["dyiy"], r["dniy"], r["dyin"], r["dnin"])/r[count_col], axis=1)
    t.loc[:, "den"] = t.apply(lambda r: _one_cmh_den(r["dyiy"], r["dniy"], r["dyin"], r["dnin"])/r[count_col], axis=1)
    if verbose:
        print(t)

    try:
        return sum(t['num'])/sum(t['den'])
    except ZeroDivisionError:  #Op-ed: Python should follow the IEEE 754 standard.
        return float('inf') if sum(t['num'])>0 else float('nan')

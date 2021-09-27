Cochrane-Mantel-Haenszel statistic calculator
=======

This repository supplements "An Analysis of U.S. Domestic Migration via Subset-stable Measures of Administrative Data" [ doi://10.2139/ssrn.3197362 ].

The paper suggested the use of the Cochran-Mantel-Haenszel (CMH) statistic for reporting
all-else-equal measures of the effect of one variable on another:
if we change the value of an independent variable from zero to one but hold all other variables constant,
with what likelihood will the dependent variable change?

This repository includes a single Python file with one external function, `cmh`, to get a
single CMH statistic.

It also includes a Jupyter notebook, `masculinity_demo.ipynb` demonstrating use of the statistic, both in code and
practical terms via a survey of US men about perceptions of masculinity.

Data prep
====

The package operates on Pandas data frames. There should be column names, but row indices
are ignored.

The CMH operates only on categorical values. Binning into categories is often preferred
over regression on continuous variables because there is no assumption of a linear or
other monotonic relation between dependent and independent variables.

The dependent and independent variables can be converted to binary variables using an
arbitrary function, allowing for alternate strategies such as selection of a single
category out of several.

Usage
====

The function acts on Pandas data frames. Given a data frame, the call requires a single
dependent and independent variable.


```
from cmh import cmh

data = a_pandas_data_frame
aggregate_risk_ratio = cmh(data, "dependent", "independent")
```

Try `help(cmh)` for more options.

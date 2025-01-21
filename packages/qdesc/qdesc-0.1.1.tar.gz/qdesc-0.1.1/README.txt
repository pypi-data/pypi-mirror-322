This is a package for quick and easy descriptive analysis.
Required packages include: pandas, numpy, and SciPy version 1.14.1
Be sure to run the following prior to using the "qd.desc" function:

import pandas as pd
import numpy as np
from scipy.stats import anderson
import qdesc as qd

The qdesc package provides a quick and easy approach to do descriptive analysis for quantitative data.

run the function qd.desc(df) to get the following statistics:
count - number of observations
mean - measure of central tendency for normal distribution	
std - measure of spread for normal distribution
median - measure of central tendency for skewed distributions or those with outliers
MAD - measure of spread for skewed distributions or those with outliers; this is manual Median Absolute Deviation (MAD) which is more robust when dealing with non-normal distributions.
min - lowest observed value
max - highest observed value	
AD_stat	- Anderson - Darling Statistic
5% crit_value - critical value for a 5% Significance Level	
1% crit_value - critical value for a 1% Significance Level

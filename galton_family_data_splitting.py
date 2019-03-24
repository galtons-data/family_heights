"""
Automatic splittin of imputated original Galton's Family Heights data file.

It is important to _not_ do what both Galton and Pearson did with this
data, namely: mix it first (in bins), plus 'normalize' it by 'transmuting'
women into men, then joggle the whole array until any resemblance of
cause-effect relationship will be lost. No, we will not do this here,
every point in the final result will be traceable to the record in the
initial data set.

For convenience I separated this code from the imputation code, because
of that it ingests the file 'galton_family_heights_imputed_final.csv',
produced by the 'galton_family_data_imputation.py' program.

The final product are files:

        'galton_family_heights_parents-sons.csv'
        'galton_family_heights_parents-daughters.csv'

"""

# The names of columns in the transcription of the original file:

COLUMNS = ['family ID', 'Father', 'Mother',
           'Son_1', 'Son_2', 'Son_3', 'Son_4', 'Son_5', 'Son_6',
           'Son_7', 'Son_8', 'Son_9', 'Son_10',
           'Daughter_1', 'Daughter_2', 'Daughter_3', 'Daughter_4',
           'Daughter_5', 'Daughter_6', 'Daughter_7', 'Daughter_8',
           'Daughter_9',
           'Number_of_Children']


import pandas
from pandas import DataFrame

data = pandas.read_csv('galton_family_heights_imputed_final.csv',
                       header=None,
                       names=COLUMNS,
                       keep_default_na=True)

# We need to form the DataFrames of sons and daugters 'flattened'
# into rows. Even more important is not to lose the attribution
# of these sons and daughters to their family, as the Great
# Statisticians of the past did. This means that we need to preserve
# the 'family ID' and the heights of parents in the rows with the
# heights of particular sons and daughters.
#       In this way we will always be able to trace back the
# cause-effect relationship and _retrospectively_ calculate
# the parameters of 'Progression from the mean' and of Mixing within
# our distribution.

"""
# 1. Parents

parents = data[COLUMNS[1:3]]   # Parents without the Family ID
parents_means = parents.mean()
parents_stds = parents.std()   # sigma itself
parents_vars = parents.var()   # sigma squared
normalized_parents = (parents - parents_means)/parents_stds

# 2. Sons

sons = data[COLUMNS[3:13]]
all_sons = sons.stack(dropna=True)  # stack all the rows of sons and exclude NaN
sons_mean = all_sons.mean()
sons_std = all_sons.std()
sons_size = all_sons.size
np_sons = all_sons.values      # a numpy array for more sophisticated statistics
"""

np_data = data.values   # numpy array for sophisticated statistics


# This is _very_ non-elegant, but right now I don't have time
# to fight pandas any longer.

# Parents and children. Yes, I have this weird habit to
# initialize my variables myself, just don't look at it
# if you don't like it.

# Parents and Sons.

parents_and_sons = pandas.DataFrame()

for son in COLUMNS[3:13]:
    parents_and_sons = parents_and_sons.append(pandas.DataFrame(data[['family ID', 'Father', 'Mother',son]].values).dropna(how='any'), ignore_index=True)

# Post-processing
#parents_and_sons.dropna(how='any', axis=1)
parents_and_sons.columns = ['family ID', 'Father', 'Mother', 'Son']
parents_and_sons = parents_and_sons.astype({'family ID': int}, copy=True)  # in place doesn't work.

# Parents and Daughters.

parents_and_daughters = pandas.DataFrame()

for daughter in COLUMNS[13:22]:
    parents_and_daughters = parents_and_daughters.append(pandas.DataFrame(data[['family ID', 'Father', 'Mother',daughter]].values).dropna(how='any'), ignore_index=True)

parents_and_daughters.columns = ['family ID', 'Father', 'Mother', 'Daughter']
parents_and_daughters = parents_and_daughters.astype({'family ID': int}, copy=True)

# Output the results to new files

parents_and_sons.to_csv('./processed_data/galton_family_heights_parents-sons.csv',
               index=False, header=False)

parents_and_daughters.to_csv('./processed_data/galton_family_heights_parents-daughters.csv',
               index=False, header=False)

print('Done! Good job, human!')

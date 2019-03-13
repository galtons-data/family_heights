"""
Automatic imputation of numeric data instead of words into the
original Galton's data file.

The inequalities suggest certain values that I used, but you can
change the numbers in the two separate dictionaries for daughters
and sons and redo the imputation. Just don't forget to look into
the file 'galton_family_heights_imputation inequalities' and not
violate the relationships of the original data.

The final product are four files:

        'galton_family_heights_parents.csv'
        'galton_family_heights_sons_imputed.csv'
        'galton_family_heights_daughters_imputed.csv'

        'galton_family_heights_imputed_final.csv' (the main)
"""

# The names of columns in the transcription of the original file:

COLUMNS = ['family ID', 'Father', 'Mother',
           'Son_1', 'Son_2', 'Son_3', 'Son_4', 'Son_5', 'Son_6',
           'Son_7', 'Son_8', 'Son_9', 'Son_10',
           'Daughter_1', 'Daughter_2', 'Daughter_3', 'Daughter_4',
           'Daughter_5', 'Daughter_6', 'Daughter_7', 'Daughter_8',
           'Daughter_9',
           'Number_of_Children']

daughters_imputation = {'idiotic': -3.0,
                        'short': 1.5,
                        'shortish': 2.5,
                        'deformed': 2.5,
                        'medium': 5.0,
                        'tallish': 5.5,
                        'tall': 6.0,
                        'very tall': 7.5} # see the .ods file

sons_imputation = {'short': 4.5,
                        'deformed': 5.5,
                        'medium': 7.0,
                        'tallish': 8.0} # see the .ods file


# The words make the columns 'heterogeneously typed', so...

import pandas

data = pandas.read_csv('galton_family_heights.csv',
                       header=None,
                       names=COLUMNS,
                       keep_default_na=False)

# in order to impute we need to cut out the sons and daughters
# and impute them separately (because all the 'short'-'tall'
# categories are clearly different for boys and girls.

parents = data.loc[:, ['family ID', 'Father', 'Mother']]

sons =    data.loc[:, ['Son_1', 'Son_2', 'Son_3', 'Son_4', 'Son_5',
                    'Son_6', 'Son_7', 'Son_8', 'Son_9', 'Son_10']]

daughters = data.loc[:, ['Daughter_1', 'Daughter_2', 'Daughter_3',
                         'Daughter_4', 'Daughter_5', 'Daughter_6',
                         'Daughter_7', 'Daughter_8', 'Daughter_9']]


# You can look at 'galton_family_heights_imputation_terms.csv'
# and see what in particular is being imputed, then into the
# 'galton_family_heights_imputation_inequalities.csv' and see
# what inequalities can be derived from the data.


# Once we have data in a pandas.DataFrame we don't need to
# iterate over rows and columns to replace the words with
# values, see: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.replace.html


sons.replace(to_replace=sons_imputation,
             value=None, inplace=True)    # replace words with numbers

daughters.replace(to_replace=daughters_imputation,
                  value=None, inplace=True)  # replace words with numbers

imputed_data = pandas.concat([parents, sons, daughters],
                             axis=1,
                             join_axes=[parents.index])  # back to full.

# Output the results to new files

parents.to_csv('galton_family_heights_parents.csv',
               index=False, header=False)

sons.to_csv('galton_family_heights_sons_imputed.csv',
               index=False, header=False)

daughters.to_csv('galton_family_heights_daughters_imputed.csv',
               index=False, header=False)

imputed_data.to_csv('galton_family_heights_imputed_final.csv',
                    index=False, header=False)

print('Done!')

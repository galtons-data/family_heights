"""
Reindexing of imputed original Galton's Family Heights data file.

Houston, we have a problem here... Namely the '136A' non-numeric
family ID that I moved to the last position in the transcribed
table. After a very long deliberation I decided to replace it with
number 205 without reindexing the table and included like that
into the 'galton_family_heights_imputed_final.csv' file.

However! In order to preserve the original principle of ordering
the data by the height of the Father and numbering the families
accordingly I decided to reindex the data set too. The family 205
(former 136A) will become 137 now, the families from 137 to 204
will become 138 - 205 (their orderly number will be incremented by 1).

I separated this code from the imputation code, because
of that it ingests the file 'galton_family_heights_imputed_final.csv',
produced by the 'galton_family_data_imputation.py' program.

The final product is a file:

        'galton_family_heights_imputed_reindexed.csv'

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

data = pandas.read_csv('galton_family_heights_imputed_final.csv',
                       header=None,
                       names=COLUMNS,
                       keep_default_na=True)


# Do it here.

# Not right now.

# Output the results to new files

imputed_reindexed.to_csv('./processed_data/galton_family_heights_imputed_reindexed.csv',
                        index=False, header=False)

print('Done! Good job, human!')

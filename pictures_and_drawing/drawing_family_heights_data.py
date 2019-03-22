"""
Loading and drawing of:

        'galton_family_heights_imputed_final.csv'
"""


import pandas
import numpy
import matplotlib.pyplot as plt
from scipy.stats import norm


# The names of columns in the transcription of the original file:

COLUMNS = ['family ID', 'Father', 'Mother',
           'Son_1', 'Son_2', 'Son_3', 'Son_4', 'Son_5', 'Son_6',
           'Son_7', 'Son_8', 'Son_9', 'Son_10',
           'Daughter_1', 'Daughter_2', 'Daughter_3', 'Daughter_4',
           'Daughter_5', 'Daughter_6', 'Daughter_7', 'Daughter_8',
           'Daughter_9']

# Font for titles

font_d = {'family': 'serif',
          'color':  'black',
          'weight': 'normal',
          'size': 16}


# Read data from the CSV file into a pandas DataFrame.

data = pandas.read_csv('galton_family_heights_imputed_final.csv',
                       header=None,
                       names=COLUMNS,
                       keep_default_na=True)  # for 'stacking' and 'unstacking'

# Create separate DataFrames and exclude the 'family ID
#
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

# 3. Daughters

daughters = data[COLUMNS[13:22]]
all_daughters = daughters.stack(dropna=True)
daughters_mean = all_daughters.mean()
daughters_std = all_daughters.std()
daughters_size = all_daughters.size
np_daughters = all_daughters.values   # numpy array for sophisticated statistics

# Start plotting
#
# Scatter plot of Parents

Fig_1 = parents.plot.scatter(x='Father', y='Mother',
                             figsize=(8, 8),                 # in inches
                             xlim=(1.5, 19),
                             ylim=(-3.5, 12),
                             color='b')

Fig_1.set_title('Parents', fontdict=font_d)
Fig_1.set_xlabel('Fathers. (Height in inches - 60)')
Fig_1.set_ylabel('Mothers. (Height in inches - 60)')

#plt.show()

# Create standard 0.5 inch wide bins for all the histograms

bins = numpy.linspace(-3.25, 19.25, 46)
bin_centers = 0.5*(bins[1:] + bins[:-1])

# Numpy histograms of Parents for precise statistics

histogram_father = numpy.histogram(parents['Father'], bins=bins)
histogram_mother = numpy.histogram(parents['Mother'], bins=bins)

# Plot histograms of Parents

Fig_2 = parents.plot.hist(bins=bins, histtype='step',
                          figsize=(8, 8),
                          xlim=(-3.5, 19.5))

Fig_2.set_title('Parents Heights', fontdict=font_d)
Fig_2.set_xlabel('Height in inches - 60.')
Fig_2.set_ylabel('Number in 205 couples')

# plt.show()

# Density plot and overlapped normal distributions

Fig_3 = parents.plot.hist(bins=bins, histtype='step',
                          density=True,
                          figsize=(8, 8),
                          xlim=(-3.5, 19.5))

Fig_3.set_title('Parents (pdf).', fontdict=font_d)
Fig_3.set_xlabel('Heights in inches - 60.')
Fig_3.set_ylabel('Density')
Fig_3.plot(bin_centers, norm.pdf(bin_centers,
                                 parents_means['Father'],
                                 parents_stds['Father']), 'b-')
Fig_3.plot(bin_centers, norm.pdf(bin_centers,
                                 parents_means['Mother'],
                                 parents_stds['Mother']), 'r-')

"""
Fig_3.vlines(x=parents_means, ymin=0,
             ymax=norm.pdf(parents_means, # x points
                           parents_means, # the means for the distribution
                           parents_stds), # the stds for the distributions
             label='mean',
             linewidth=1,
             color=['b','r'],
             alpha=1)
"""

plt.show()

# Normalized scatter plot of parents

Fig_4 = normalized_parents.plot.scatter(x='Father', y='Mother',
                                        figsize=(8, 8),              # in inches
                                        xlim=(-3.2, 3.55),
                                        ylim=(-3.5, 3.5),
                                        color='m')

Fig_4.set_title('Parents normalized', fontdict=font_d)
Fig_4.set_xlabel('Fathers.  ( Mean = {:05.3f}, '
                 'Standard Deviation = {:05.3f} )'.format(parents_means['Father'],
                                                          parents_stds['Father']))
Fig_4.set_ylabel('Mothers.  ( Mean = {:05.3f}, '
                 'Standard Deviation = {:05.3f} )'.format(parents_means['Mother'],
                                                          parents_stds['Mother']))

plt.show()

# Create a separate numpy array histogram of sons for stat analysis

histogram_sons = numpy.histogram(all_sons, bins=bins)

# Sons hist plot done by pandas native method

Fig_5 = all_sons.plot.hist(bins=bins, histtype='step',
                           figsize=(8, 8),
                           xlim=(-3.5, 19.5))

Fig_5.set_title('All sons.', fontdict=font_d)
Fig_5.set_xlabel('Height in inches - 60.')
Fig_5.set_ylabel('Number. ( All in all ={:4.0f} )'.format(sons_size))

plt.show()

# Density plot and overlapped normal distribution

Fig_6 = all_sons.plot.hist(bins=bins, histtype='step',
                           density=True,
                           figsize=(8, 8),
                           xlim=(-3.5, 19.5))

Fig_6.set_title('All sons (pdf).', fontdict=font_d)
Fig_6.set_xlabel('Height in inches - 60')
Fig_6.set_ylabel('Density')
Fig_6.legend(['Mean = {:06.4f} \nStd    = {:06.4f}'.format(sons_mean, sons_std)], loc='upper left')
Fig_6.plot(bin_centers, norm.pdf(bin_centers, sons_mean, sons_std), 'b-')

plt.show()

histogram_daughters = numpy.histogram(all_daughters, bins=bins)

Fig_7 = all_daughters.plot.hist(bins=bins, histtype='step',
                                color='r',
                                figsize=(8, 8),
                                xlim=(-3.5, 19.5))

Fig_7.set_title('All daughters.', fontdict=font_d)
Fig_7.set_xlabel('Height in inches - 60.')
Fig_7.set_ylabel('Number. ( All in all ={:4.0f} )'.format(daughters_size))

plt.show()

# Density plot and overlapped normal distribution

Fig_8 = all_daughters.plot.hist(bins=bins, histtype='step',
                                density=True,
                                color='r',
                                figsize=(8, 8),
                                xlim=(-3.5, 19.5))

Fig_8.set_title('All daughters (pdf).', fontdict=font_d)
Fig_8.set_xlabel('Height in inches - 60.')
Fig_8.set_ylabel('Density')
Fig_8.legend(['Mean = {:06.4f} \nStd    = {:06.4f}'.format(daughters_mean, daughters_std)])
Fig_8.plot(bin_centers, norm.pdf(bin_centers, daughters_mean, daughters_std), 'r-')

plt.show()

print('Done!')

"""
xyA=(0.2, 0.2)
xyB=(0.5, 0.8)
con = ConnectionPatch(xyA, xyB,
                      coordsA="data", coordsB="data",
                      arrowstyle="-|>",
                      shrinkA=4, shrinkB=4,
                      mutation_scale=15,   # then kwargs
                      fc="w", color="r")

ax1.plot([xyA[0], xyB[0]], [xyA[1], xyB[1]], "o")
ax1.add_artist(con)
"""

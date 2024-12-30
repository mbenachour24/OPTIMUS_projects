# Generating the graphs based on real interpretations from the analysis
import numpy as np
import matplotlib.pyplot as plt

categories = ['Descriptive/Prescriptive', 'Past/Present/Future', 'Personal/Universal', 'Rational/Empirical', 'Optimistic/Pessimistic', 'Contributive/Critical']
people = ['Mohamed', 'Habib', 'Maude', 'Alex']

# Data based on the analysis:
data = {
    'Mohamed': [0.3, 0.8, 0.1, 0.9, 0.8, 0.7],  # Prescriptive, Future, Universal, Rational, Optimistic, Contributive
    'Habib': [0.6, 0.4, 0.3, 0.7, 0.4, 0.6],  # Balanced, Past, Universal, Rational, Pessimistic, Critical
    'Maude': [0.8, 0.5, 0.9, 0.3, 0.3, 0.4],  # Descriptive, Present, Personal, Empirical, Pessimistic, Critical
    'Alex': [0.7, 0.5, 0.2, 0.8, 0.6, 0.5],  # Descriptive, Past/Future, Universal, Rational, Optimistic, Contributive
}

# Creating the plots
fig, ax = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle("Language Characteristics Analysis (Based on Real Data)", fontsize=16)

# Plot for Mohamed
ax[0, 0].barh(categories, data['Mohamed'], color='blue', alpha=0.7)
ax[0, 0].set_title("Mohamed's Language Characteristics")
ax[0, 0].set_xlim([0, 1])

# Plot for Habib
ax[0, 1].barh(categories, data['Habib'], color='green', alpha=0.7)
ax[0, 1].set_title("Habib's Language Characteristics")
ax[0, 1].set_xlim([0, 1])

# Plot for Maude
ax[1, 0].barh(categories, data['Maude'], color='red', alpha=0.7)
ax[1, 0].set_title("Maude's Language Characteristics")
ax[1, 0].set_xlim([0, 1])

# Plot for Alex
ax[1, 1].barh(categories, data['Alex'], color='purple', alpha=0.7)
ax[1, 1].set_title("Alex's Language Characteristics")
ax[1, 1].set_xlim([0, 1])

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

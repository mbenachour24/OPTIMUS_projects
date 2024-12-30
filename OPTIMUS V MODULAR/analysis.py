# analysis.py
import numpy as np
import matplotlib.pyplot as plt
import logging
from statsmodels.tsa.stattools import grangercausalitytests

def calculate_correlations(caseload_history, normative_inflation_history, temporal_gap_history):
    """Calculate Pearson correlations between caseload, normative inflation, and temporal gap."""
    # Convert lists to arrays
    caseload_array = np.array(caseload_history)
    normative_inflation_array = np.array(normative_inflation_history)
    temporal_gap_array = np.array(temporal_gap_history)

    # Calculate Pearson correlations
    pearson_caseload_normative_inflation = np.corrcoef(caseload_array, normative_inflation_array)[0, 1]
    pearson_caseload_temporal_gap = np.corrcoef(caseload_array, temporal_gap_array)[0, 1]
    pearson_normative_inflation_temporal_gap = np.corrcoef(normative_inflation_array, temporal_gap_array)[0, 1]

    # Log the results
    logging.info(f'Society: Pearson correlation between Caseload and Normative Inflation: {pearson_caseload_normative_inflation}')
    logging.info(f'Society: Pearson correlation between Caseload and Temporal Gap: {pearson_caseload_temporal_gap}')
    logging.info(f'Society: Pearson correlation between Normative Inflation and Temporal Gap: {pearson_normative_inflation_temporal_gap}')

def plot_results(caseload_history, normative_inflation_history, temporal_gap_history):
    """Plot the historical data for caseload, normative inflation, and temporal gap."""
    plt.figure(figsize=(10, 6))

    # Plot Caseload over Time
    plt.subplot(3, 1, 1)
    plt.plot(caseload_history, label='Caseload', color='blue')
    plt.xlabel('Days')
    plt.ylabel('Caseload')
    plt.title('Caseload over Time')
    plt.legend()

    # Plot Normative Inflation over Time
    plt.subplot(3, 1, 2)
    plt.plot(normative_inflation_history, label='Normative Inflation', color='red')
    plt.xlabel('Days')
    plt.ylabel('Number of Norms')
    plt.title('Normative Inflation over Time')
    plt.legend()

    # Plot Temporal Gap over Time
    plt.subplot(3, 1, 3)
    plt.plot(temporal_gap_history, label='Temporal Gap', color='green')
    plt.xlabel('Days')
    plt.ylabel('Temporal Gap (Norms - Caseload)')
    plt.title('Temporal Gap over Time')
    plt.legend()

    plt.tight_layout()
    plt.show()

def perform_granger_test(normative_inflation_history, caseload_history):
    """Perform Granger causality test between normative inflation and caseload."""
    data = np.column_stack((normative_inflation_history, caseload_history))
    max_lag = min(10, len(normative_inflation_history) - 1)  # Dynamically set max lag based on data length
    test_result = grangercausalitytests(data, max_lag, verbose=False)

    # Log Granger causality results for each lag
    for lag, result in test_result.items():
        f_test = result[0]['ssr_ftest']
        logging.info(f"Granger causality test at lag {lag}: F-test = {f_test[0]}, p-value = {f_test[1]}")
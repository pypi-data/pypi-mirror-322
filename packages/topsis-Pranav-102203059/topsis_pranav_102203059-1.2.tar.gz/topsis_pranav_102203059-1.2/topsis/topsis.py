import pandas as pd
import numpy as np
import os

def validate_input_file(data):
    """Validate the input file for the TOPSIS calculation."""
    if data.shape[1] < 3:
        raise ValueError("Input file must have at least 3 columns.")
    if not all(data.iloc[:, 1:].applymap(np.isreal).all()):
        raise ValueError("From the 2nd column onward, all values must be numeric.")

def normalize_data(data):
    """Normalize the data for TOPSIS."""
    return data.div(np.sqrt((data ** 2).sum()))

def calculate_topsis(input_file, weights, impacts, result_file):
    """Perform the TOPSIS calculation and save the results."""
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Error: File '{input_file}' not found.")
    
    data = pd.read_excel(input_file)
    validate_input_file(data)
    
    weights = list(map(float, weights.split(',')))
    impacts = impacts.split(',')
    
    if len(weights) != len(impacts) or len(weights) != data.shape[1] - 1:
        raise ValueError("Number of weights, impacts, and columns (from 2nd to last) must match.")
    if not all(i in ['+', '-'] for i in impacts):
        raise ValueError("Impacts must be '+' or '-'.")
    
    # Normalize the data
    normalized_data = normalize_data(data.iloc[:, 1:])
    
    # Apply weights
    weighted_data = normalized_data.mul(weights)
    
    # Calculate ideal best and worst
    ideal_best = [weighted_data[col].max() if imp == '+' else weighted_data[col].min() 
                  for col, imp in zip(weighted_data.columns, impacts)]
    ideal_worst = [weighted_data[col].min() if imp == '+' else weighted_data[col].max() 
                   for col, imp in zip(weighted_data.columns, impacts)]
    
    # Calculate distances
    distances_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    distances_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))
    
    # Calculate TOPSIS scores
    scores = distances_worst / (distances_best + distances_worst)
    
    # Add scores and rank to the original data
    data['Topsis Score'] = scores
    data['Rank'] = scores.rank(ascending=False).astype(int)
    
    # Save results
    data.to_csv(result_file, index=False)
    print(f"Results saved to '{result_file}'.")

def main():
    """Main function for CLI execution."""
    import sys
    if len(sys.argv) != 5:
        print("Usage: topsis <InputDataFile> <Weights> <Impacts> <ResultFileName>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    result_file = sys.argv[4]
    
    try:
        calculate_topsis(input_file, weights, impacts, result_file)
    except Exception as e:
        print(f"Error: {e}")

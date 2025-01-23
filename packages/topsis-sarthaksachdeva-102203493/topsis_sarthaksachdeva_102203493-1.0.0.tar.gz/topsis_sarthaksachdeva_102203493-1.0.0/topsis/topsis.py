import sys
import pandas as pd
import numpy as np

def topsis(input_file, weights, impacts, output_file):
    try:
        # Read the input file
        data = pd.read_csv(input_file)
        
        # Check if the input file has at least 3 columns
        if data.shape[1] < 3:
            raise Exception("Input file must have at least 3 columns (1 for objects, 2 or more for numeric criteria).")
        
        # Validate that the first column is the object/variable names
        if not data.iloc[:, 0].apply(lambda x: isinstance(x, str)).all():
            raise Exception("The first column must contain object/variable names as strings (e.g., M1, M2).")
        
        # Validate that all other columns contain numeric data
        if not all(np.issubdtype(dtype, np.number) for dtype in data.iloc[:, 1:].dtypes):
            raise Exception("Columns from the 2nd to the last must contain numeric values.")
        
        # Parse weights and impacts
        weights = [float(w) for w in weights.split(',')]
        impacts = impacts.split(',')
        if len(weights) != data.shape[1] - 1 or len(impacts) != data.shape[1] - 1:
            raise Exception("Number of weights and impacts must match the number of numeric criteria.")
        if not all(i in ['+', '-'] for i in impacts):
            raise Exception("Impacts must be '+' or '-' only.")
        
        # Normalize the decision matrix
        matrix = data.iloc[:, 1:].values
        norm_matrix = matrix / np.sqrt((matrix ** 2).sum(axis=0))

        # Calculate the weighted normalized matrix
        weighted_matrix = norm_matrix * weights

        # Determine ideal best and worst
        ideal_best = [max(weighted_matrix[:, i]) if impacts[i] == '+' else min(weighted_matrix[:, i])
                      for i in range(len(weights))]
        ideal_worst = [min(weighted_matrix[:, i]) if impacts[i] == '+' else max(weighted_matrix[:, i])
                       for i in range(len(weights))]

        # Calculate distances from ideal best and worst
        dist_best = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
        dist_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))

        # Calculate TOPSIS score and rank
        scores = dist_worst / (dist_best + dist_worst)
        data['Topsis Score'] = scores
        data['Rank'] = pd.Series(scores).rank(ascending=False).astype(int)

        # Save the result to the output file
        data.to_csv(output_file, index=False)
        print(f"Result saved to {output_file}")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found. Please check the file path and try again.")
    except Exception as e:
        print(f"Error: {e}")

# Main program
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <InputDataFile> <Weights> <Impacts> <ResultFileName>")
    else:
        _, input_file, weights, impacts, output_file = sys.argv
        topsis(input_file, weights, impacts, output_file)

import pandas as pd
import numpy as np

def topsis(input_file, weights, impacts, result_file):
    try:
        # Load the dataset
        data = pd.read_csv(input_file)
        
        if data.shape[1] < 3:
            raise Exception("Input file must have at least three columns.")
        
        # Separate object names and numeric data
        names = data.iloc[:, 0]
        matrix = data.iloc[:, 1:].values
        
        # Validate weights and impacts
        weights = [float(w) for w in weights.split(',')]
        impacts = impacts.split(',')
        
        if len(weights) != matrix.shape[1] or len(impacts) != matrix.shape[1]:
            raise Exception("Number of weights, impacts, and columns must be the same.")
        if not all(i in ['+', '-'] for i in impacts):
            raise Exception("Impacts must be either '+' or '-'.")
        
        # Step 1: Normalize the decision matrix
        norm_matrix = matrix / np.sqrt((matrix**2).sum(axis=0))
        
        # Step 2: Calculate the weighted normalized decision matrix
        weighted_matrix = norm_matrix * weights
        
        # Step 3: Determine the ideal and negative-ideal solutions
        ideal = []
        negative_ideal = []
        for i, impact in enumerate(impacts):
            if impact == '+':
                ideal.append(weighted_matrix[:, i].max())
                negative_ideal.append(weighted_matrix[:, i].min())
            else:
                ideal.append(weighted_matrix[:, i].min())
                negative_ideal.append(weighted_matrix[:, i].max())
        
        # Step 4: Calculate separation measures
        ideal = np.array(ideal)
        negative_ideal = np.array(negative_ideal)
        dist_ideal = np.sqrt(((weighted_matrix - ideal) ** 2).sum(axis=1))
        dist_negative = np.sqrt(((weighted_matrix - negative_ideal) ** 2).sum(axis=1))
        
        # Step 5: Calculate TOPSIS score
        scores = dist_negative / (dist_ideal + dist_negative)
        
        # Step 6: Rank the alternatives
        data['Topsis Score'] = scores
        data['Rank'] = scores.argsort()[::-1] + 1  # Sort in descending order
        
        # Save the results to a CSV file
        data.to_csv(result_file, index=False)
        print(f"Results saved to {result_file}")
    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")

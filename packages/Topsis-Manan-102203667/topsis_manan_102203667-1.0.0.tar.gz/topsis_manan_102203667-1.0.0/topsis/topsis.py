import pandas as pd
import numpy as np

def topsis(input_file, weights, impacts, output_file):
    try:
        data = pd.read_csv(input_file)
        
        if data.shape[1] < 3:
            raise Exception("Input file must contain at least three columns.")

        weights = [float(w) for w in weights.split(',')]
        impacts = impacts.split(',')

        if len(weights) != len(impacts) or len(weights) != (data.shape[1] - 1):
            raise Exception("Number of weights, impacts, and criteria must match.")
        
        norm_data = data.iloc[:, 1:].div(np.sqrt((data.iloc[:, 1:]**2).sum()))
        weighted_data = norm_data.mul(weights)
        
        ideal_best = []
        ideal_worst = []
        for i, impact in enumerate(impacts):
            if impact == '+':
                ideal_best.append(weighted_data.iloc[:, i].max())
                ideal_worst.append(weighted_data.iloc[:, i].min())
            else:
                ideal_best.append(weighted_data.iloc[:, i].min())
                ideal_worst.append(weighted_data.iloc[:, i].max())
        
        distances_best = np.sqrt(((weighted_data - ideal_best)**2).sum(axis=1))
        distances_worst = np.sqrt(((weighted_data - ideal_worst)**2).sum(axis=1))
        scores = distances_worst / (distances_best + distances_worst)

        data['Topsis Score'] = scores
        data['Rank'] = scores.rank(ascending=False).astype(int)
        data.to_csv(output_file, index=False)

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

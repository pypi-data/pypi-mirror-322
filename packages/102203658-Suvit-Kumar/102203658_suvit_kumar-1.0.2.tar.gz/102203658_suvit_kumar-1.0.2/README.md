# TOPSIS - Technique for Order Preference by Similarity to Ideal Solution

TOPSIS is a multi-criteria decision analysis method. It is based on the concept that the chosen alternative should have the shortest geometric distance from the positive ideal solution and the longest geometric distance from the negative ideal solution.

## Features
- Easy implementation of TOPSIS in Python.
- Suitable for ranking and decision-making tasks.
- Handles datasets with multiple criteria and alternatives.

## Installation
You can install the package using pip:
```bash
pip install 102203658_Suvit_Kumar

## Usage

from 102203658_Suvit_Kumar import topsis

# Example usage
criteria_weights = [0.4, 0.3, 0.3]
dataset = [
    [250, 16, 12],
    [200, 20, 8],
    [300, 12, 10],
]
impact = ['+', '+', '-']

ranked_alternatives = topsis(dataset, criteria_weights, impact)
print(ranked_alternatives)

## License
This project is licensed under the MIT License.



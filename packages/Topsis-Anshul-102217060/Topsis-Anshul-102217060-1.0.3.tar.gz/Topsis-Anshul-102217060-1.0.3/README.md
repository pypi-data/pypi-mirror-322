# Topsis-Anshul
# TOPSIS Implementation

This repository contains a Python implementation of the Technique for Order Preference by Similarity to Ideal Solution (TOPSIS). TOPSIS is a powerful multi-criteria decision-making method that assists in ranking a set of alternatives based on their proximity to the ideal solution.

## Table of Contents

1. [Introduction](#introduction)
2. [Usage](#usage)
3. [Command-line Arguments](#command-line-arguments)
6. [Requirements](#requirements)

## Introduction

The Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) is a well-established method for decision-making. This Python implementation allows you to easily apply TOPSIS to your decision matrix and obtain a ranked list of alternatives.

### Key Concepts:

- Decision Matrix: Represents alternatives and criteria.
- Weights: Assign importance to criteria.
- Impacts: Indicate whether higher or lower values are favorable.
- Normalization: Ensures all criteria are on a similar scale.
- Ideal and Worst Solutions: Represent best and worst possible outcomes.
- Similarity and Dissimilarity Measures: Calculate proximity to ideal and dissimilarity to worst.
- TOPSIS Score: Combines similarity and dissimilarity measures.
- Ranking: Alternatives are ranked based on TOPSIS scores.

## Usage

1. Ensure you have Python installed on your system.

2. Clone this repository to your local machine:

   bash
   git clone https://github.com/anshulmahajan14/Topsis-Anshul

3. Navigate to the project directory:

      bash
   git clone https://github.com/anshulmahajan14/Topsis-Anshul

   
4. Run the TOPSIS script with the required command-line arguments:

   
      python 102217060.py 102217060-data.csv "1,1,1,2" "+,+,-,+" result.csv



5. The TOPSIS analysis will be performed, and the result will be saved to the specified CSV file.

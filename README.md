# Burrows-WheelerTransform

# BQ4CY060 Bio-informatique de la génomique | BWT - MAPPING
**Author** : ABDI Feriel, BENKORTEBI Manel, GBABOUA Cassandra

## Table of Contents
1. [Summary](#summary)
2. [System Requirement](#system-requirement)
3. [Installation](#installation)
   - [Clone Repository](#clone-repository)
   - [Install Required Packages](#install-required-packages)
4. [Repository Contents](#repository-contents)
5. [Getting Started](#getting-started)
   - [Basic Usage](#basic-usage)
   - [Inputs](#inputs)
6. [Features and Functions](#features-and-functions)
7. [Packages Used](#packages-used)
8. [Outputs and Examples](#outputs-and-examples)
   - [Examples](#examples)
   - [Outputs](#outputs)
9. [BWT Wiki](https://github.com/cgbaboua/Burrows-WheelerTransform/wiki/BWT-Wiki)

## Summary 
This program implements the Burrows-Wheeler Transform (BWT) for string manipulation and pattern matching, focusing on string transformations, mismatch management, and visualization. The implementation utilizes Python and includes modules for different aspects of BWT processing.The project is part of the "BQ4CY060 Bio-informatique de la génomique" course at the Paris Cité University.

## System requirement
- Python 3.x (Tested on Python 3.11.5)
- Compatible with macOS, UNIX-based operating systems. Windows users can run this project using Windows Subsystem for Linux (WSL)
- Plotly package for visualization (install using `pip install plotly` or `conda install plotly` if using conda)

## Installation

**If you already have the repository on your computer, you can directly skip to [Step 5.Getting Started](#getting-started).**

### Clone Repository

Clone the workflow github repository :

```bash
git clone https://github.com/cgbaboua/Burrows-WheelerTransform.git
```

### Repository contents 
[Burrows-WheelerTransform/](https://github.com/cgbaboua/Burrows-WheelerTransform)
  - [README.md](https://github.com/cgbaboua/Burrows-WheelerTransform/blob/main/README.md)
  - [python/](https://github.com/cgbaboua/Burrows-WheelerTransform/blob/main/python)
    - [BWT.py](https://github.com/cgbaboua/Burrows-WheelerTransform/blob/main/python/BWT.py)
    - [visualization.py](https://github.com/cgbaboua/Burrows-WheelerTransform/blob/main/python/visualization.py)
    - [bwt_no_matrix.py](https://github.com/cgbaboua/Burrows-WheelerTransform/blob/main/python/bwt_no_matrix.py)
    - [mismatches.py](https://github.com/cgbaboua/Burrows-WheelerTransform/blob/main/python/mismatches.py)
  - [examples/](https://github.com/cgbaboua/Burrows-WheelerTransform/blob/main/examples)
    - [seq.txt](https://github.com/cgbaboua/Burrows-WheelerTransform/blob/main/examples/seq.txt)
    - [plot_BANANA.png](https://github.com/cgbaboua/Burrows-WheelerTransform/blob/main/examples/plot_BANANA.png)


## Getting started

### Install Required Packages
Install Plotly for visualization:
```bash
pip install plotly
```
Or, if using Conda:
```bash
conda install plotly
```

### Basic Usage
To launch the program, you can run for example : 
```python
python3 python/BWT.py [--string "YourString"] [--pattern "YourPattern"] [--mismatch 0]
```
OR 

```python
python3 python/BWT.py 
```


### Inputs 
- --string: (Optional) The string to be processed. Can be a plain string or a file path ending in .txt. Default is a predefined ATP8 sequence. If provided, --pattern must also be provided.
- --pattern: (Optional) The pattern to match against the string. Default is "AATC".If provided, --string must also be provided.
- --mismatch: (Optional) The number of allowed mismatches in the pattern matching. Default is 1. Can be provided alone without --string or --pattern.
  
All parameters are optional. If --string and --pattern are not provided, the program uses default values. --mismatch can be provided independently to specify the number of allowed mismatches.


### Features and Functions

`BWT.py`: Main script orchestrating the BWT process, including parsing command-line arguments.
`visualization.py`: Contains functions for visualizing BWT results. Functions include:
  - `plot_BWT_mapping()`: Creates an interactive HTML plot displaying positions of pattern matches in a string.
`bwt_no_matrix.py` : Implements BWT-related functions without using a complete matrix to optimize memory usage. Key functions:
  - `get_BWT_simplified()`: Simplified BWT implementation. It employs a trie (prefix tree) for memory-efficient Burrows-Wheeler Transform, avoiding the need for a full matrix by using recursive trie traversal.
`mismatches.py` : Handles pattern matching with allowed mismatches. Key functions:
  - `get_match_ignore_mismatch()`: Finds matches allowing a specified number of mismatches.


### Packages Used 
- `plotly`: A visualization library used for creating interactive and aesthetically pleasing plots and charts. 
- `argparse`: Command-line parsing library to identify what arguments need to be passed to the script, making it more user-friendly.

## Outputs and Examples

### Examples

To test the program, use the example [seq.txt](https://github.com/cgbaboua/Burrows-WheelerTransform/blob/main/examples/seq.txt) file :
```python
python3 python/BWT.py --string examples/seq.txt --pattern TTGC
```

### Outputs 

- An interactive HTML plot is automatically generated and opened in the default web browser, showcasing the BWT results. The plot is created in the current working directory and can be saved as a PNG file. For a detailed explanation of how to interact with the plot, please refer to the [Navigate the Interactive Graph](https://github.com/cgbaboua/Burrows-WheelerTransform/wiki/BWT-Wiki#navigating-the-interactive-graph) section in our [BWT Wiki](https://github.com/cgbaboua/Burrows-WheelerTransform/wiki/BWT-Wiki).
- Console outputs include the processed string and pattern matching results.

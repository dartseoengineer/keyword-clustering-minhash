# Keyword Clustering with MinHash

This Python script clusters keywords based on the similarity of their associated URLs using MinHash and MinHashLSH. The clustering process helps identify keywords that return similar search engine result pages (SERPs), which can be useful for SEO and content optimization strategies.

## Features

- Groups URLs by keywords.
- Uses MinHash to create similarity sketches of the URLs.
- Applies Locality Sensitive Hashing (LSH) to cluster similar keywords.
- Outputs a CSV file with clustered keywords.

## Prerequisites

- Python 3.x
- pandas
- tqdm
- datasketch

## Installation

Install the required Python packages using `pip`:

```sh
pip install pandas tqdm datasketch
```

## Usage

### Command Line

```sh
python minhash-cluster-cli.py [input_file] [output_file] [-s SEPARATOR] [-k KEYWORD_COL] [-u URL_COL] [-t SIMILARITY_THRESHOLD]
```

### Arguments

- `input_file`: Path to the input CSV file.
- `output_file`: Path to save the output clustered keywords CSV file.
- `-s`, `--separator`: (Optional) Separator of the input file (default is `,`).
- `-k`, `--keyword_col`: (Optional) Name of the keyword column in the input file (default is `Keyword`).
- `-u`, `--url_col`: (Optional) Name of the URL column in the input file (default is `URL`).
- `-t`, `--similarity_threshold`: (Optional) Threshold of similarity (default is `0.6`).

### Example

```sh
python minhash-cluster-cli.py for-clustering.csv clustered_keywords.csv -s ';' -k 'keyword' -u 'url' -t 0.6
```

## Output

The output CSV file will contain two columns:

- `Group`: The cluster ID.
- `Keyword`: The keyword associated with the cluster.

Keywords without URLs will have a cluster ID of `-1`.

## Script Explanation

1. **Load Data**: The script reads the input CSV file and loads the data into a pandas DataFrame.
2. **Group URLs by Keyword**: It groups URLs by keywords and filters out keywords with no URLs.
3. **Create MinHash Objects**: For each keyword, a MinHash object is created based on the URLs.
4. **Create LSH Index**: The MinHash objects are inserted into an LSH index.
5. **Find Clusters**: Keywords are clustered based on MinHash similarity using the LSH index.
6. **Output Results**: The clustered keywords are saved to the output CSV file.

## Developed by

Twitter: [@dartseo](https://twitter.com/dartseo)  
Telegram: [Advanced SEO Blog](https://t.me/advancedseoblog)

Feel free to subscribe and follow for more updates and tools!

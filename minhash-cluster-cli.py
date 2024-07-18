import argparse
from collections import defaultdict
import pandas as pd
from tqdm import tqdm
from datasketch import MinHash, MinHashLSH

def cluster_keywords(input_file, output_file, separator, keyword_col, url_col, similarity_threshold):
    # Load data
    data = pd.read_csv(input_file, sep=separator, engine='python')

    # Similarity Threshold
    similarity_threshold = float(similarity_threshold)

    # Group urls by keyword
    keywords_urls = defaultdict(set)
    for _, row in tqdm(data.iterrows(), total=data.shape[0], desc='Group urls by keyword'):
        keyword, url = row[keyword_col], row[url_col]
        if pd.isna(url) or url == '':
            url = None
        keywords_urls[keyword].add(url)

    # Filter out keywords with no URLs
    unclustered_keywords = [keyword for keyword, urls in keywords_urls.items() if len(urls) == 1 and None in urls]
    keywords_urls = {keyword: urls for keyword, urls in keywords_urls.items() if not (len(urls) == 1 and None in urls)}

    # Create MinHash objects
    minhash_dict = {}
    for keyword, urls in tqdm(keywords_urls.items(), desc='Creating MinHash objects'):
        minhash = MinHash(num_perm=256)
        for url in urls:
            if url is not None:
                minhash.update(url.encode('utf8'))
        minhash_dict[keyword] = minhash

    # Create LSH index
    lsh = MinHashLSH(threshold=similarity_threshold, num_perm=256)
    for keyword, minhash in tqdm(minhash_dict.items(), desc='Inserting into LSH'):
        lsh.insert(keyword, minhash)

    # Find clusters based on MinHash similarity
    clusters = []
    clustered_keywords = set()
    keyword_to_cluster = {}

    for keyword in tqdm(minhash_dict.keys(), desc='Creating clusters'):
        if keyword not in clustered_keywords:
            cluster = lsh.query(minhash_dict[keyword])
            new_cluster = []
            for k in cluster:
                if k not in clustered_keywords:
                    clustered_keywords.add(k)
                    keyword_to_cluster[k] = len(clusters)
                    new_cluster.append(k)
            if new_cluster:
                clusters.append(new_cluster)

    # Prepare the dataframe for clustered keywords
    clustered_keywords_list = [(keyword_to_cluster[keyword], keyword) for keyword in keyword_to_cluster]

    # Add unclustered keywords to cluster -1
    clustered_keywords_list.extend([(-1, keyword) for keyword in unclustered_keywords])

    # Save the result to a csv file
    clustered_keywords_df = pd.DataFrame(clustered_keywords_list, columns=['Group', 'Keyword'])
    clustered_keywords_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cluster keywords by SERP similarity using MinHash", epilog="Example: python minhash-cluster-cli.py -s ';' -k 'keyword' -u 'url' -t 0.6 for-clustering.csv clustered_keywords.csv")
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("output_file", help="Path to save the output clustered keywords")
    parser.add_argument("-s", "--separator", default=',', help="Separator of the input file")
    parser.add_argument("-k", "--keyword_col", default='Keyword', help="Name of the keyword column in input file")
    parser.add_argument("-u", "--url_col", default='URL', help="Name of the URL column in input file")
    parser.add_argument("-t", "--similarity_threshold", default=0.6, help="Threshold of similarity")

    args = parser.parse_args()
    
    cluster_keywords(args.input_file, args.output_file, args.separator, args.keyword_col, args.url_col, args.similarity_threshold)
    print("")
    print("Developed by Dart. Please subscribe:")
    print("Twitter: https://twitter.com/dartseo")
    print("Telegram: https://t.me/advancedseoblog")
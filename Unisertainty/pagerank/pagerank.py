import os
import random
import re
import sys
import copy
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probabilities={}
    length=len(corpus[page])
    if length:
        for x in corpus:
            probabilities[x]=(1-damping_factor)/len(corpus)
        for x in corpus[page]:

            probabilities[x]+=damping_factor/length
    else:
        for x in corpus:
            probabilities[x]=1/len(corpus)
        
    return probabilities



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    probabilities={}
    for page in corpus:
        probabilities[page]=0
    page = random.choice(list(corpus.keys()))
    for i in range (1,n):
        current_prob=transition_model(corpus,page,damping_factor)
        for page in probabilities:
            probabilities[page]=((i-1) * probabilities[page] + current_prob[page]) / i
            page = random.choices(list(probabilities.keys()), list(probabilities.values()), k=1)[0]
    return probabilities


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    probabilities = {}      
    newprrobabilities = {}

    # Assign each page equal probability
    for page in corpus:
        probabilities[page] = 1 / len(corpus)

    repeat = True

    while repeat:
        # Calculate new probabilities depending of previous probabilities
        for page in probabilities:
            newprrobabilities[page] = (1 - damping_factor) / len(corpus) + damping_factor * suma(page,probabilities,corpus)
        repeat = False
        
        # Stop when the value changes by more than 0.001
        for page in probabilities:
            if not math.isclose(newprrobabilities[page], probabilities[page], abs_tol=0.001):
                repeat = True
            # change current probabilities to new probabilities
            probabilities[page] = newprrobabilities[page]

    return probabilities
def suma(page,probabilities, corpus):
    sol=0
    for link in corpus:
        if page in corpus[link]:
            sol += probabilities[link] / len(corpus[link])
        if not corpus[link]:
            sol += probabilities[link] / len(corpus)
    return sol

if __name__ == "__main__":
    main()

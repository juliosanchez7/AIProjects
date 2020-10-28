import nltk
import sys
import os
import math 
import string

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    contents = dict()
    #Search all files in the directory
    for root, dirs, files in os.walk(directory):
        #For each file, open it and save the content on contents directory with the filename
        for name in files:
            f=open(os.path.join(root, name))
            contents[name]=f.read()
    return contents
def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    
    #converting sentence to a list oof its words with word_tokenize.
    words = nltk.word_tokenize(document.lower())
    punct=string.punctuation
    sw=nltk.corpus.stopwords.words("english")
    #Reject all words that contain punctuations and English stopwords.
    words = [word for word in words if word not in punct and word not in sw]
    
    return words 
def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    #Create idfs dictionary
    idfs = dict()
    #calculate the total of documents
    total_documents = len(documents)
    #find words in documents
    words = set(word for sublist in documents.values() for word in sublist)
    for word in words:
        documents_with_word = 0
        #if word appear in documents increment the quantity od documents_with_word
        for doc in documents.values():
            if word in doc:
                documents_with_word += 1
        #Calculate the idf for each word (log(totalDocuments/NumDocumentsContaining(Word)))
        idf = math.log(total_documents / documents_with_word)
        idfs[word] = idf
    
    return idfs
def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    #dictionary of the scores of each file
    scores=dict()
    for file, words in files.items():
        idf = 0
        #For loop to analyse each word of the query
        for w in query:
            #Calculate the idf of the query
            idf += words.count(w) * idfs[w]
        scores[file] = idf
    top_f = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_f = [x[0] for x in top_f]
    return top_f[:n]
def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    scores_sent=dict()
    #find the intersection between query and sentences
    for s, w in sentences.items():
        #idf of sentences
        idf=0
        words=query.intersection(w)
        for word in words:
            idf+=idfs[word]
        
        words_quantity=sum(map(lambda x: x in w, w))
        q_t_density=words_quantity/len(w)
        scores_sent[s]={'idf': idf, 'q_t':q_t_density}
    sentences_top=sorted(scores_sent.items(), key=lambda x: (x[1]['idf'], x[1]['q_t']), reverse=True)
    sentences_top=[x[0] for x in sentences_top]
    return sentences_top[:n]

if __name__ == "__main__":
    main()

# kpop-idol-vectors
Generate word embeddings for youtube comments on Kpop idols.

## [1] Overview
Word embedding projection: embeddings trained on youtube comments on videos about Korean idols. 

## [2] Vector similarity 
![alt text](https://github.com/kaiyoo/kpop-idols-w2v/blob/main/img/most_similar.png?raw=true)

## [3] Data collection
-	Used Youtube API to collect comments on videos about each artist.

## [4] Model
-	Used FastText pretrained Korean embedding and built vocabs from youtube_comments dataset.

## [5] Visualization
- Generating tensor.tsv and metadata.tsv for Embedding projection as an attempt to see neighbors of query. 

query='장원영'

![alt text](https://github.com/kaiyoo/kpop-idols-w2v/blob/main/img/장원영_vector.png?raw=true)

query='카리나'

![alt text](https://github.com/kaiyoo/kpop-idols-w2v/blob/main/img//카리나_vector.png?raw=true)

- Generating all vocab and tensors from FastText's pretrained model will lead to creating files over 10G.
- Therefore, after training on youtube_comment dataset from pretrained model, I extracted only vectors of tokens in my dataset from pretrained model.
- But for more sensible result, try generating tsv files directly from pretrained_model (bearing size issues).

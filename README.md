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


## [6] Limitation
query='하니'

![alt text](https://github.com/kaiyoo/kpop-idols-w2v/blob/main/img//하니_vector.png?raw=true)

- '하니' is a member of girl group New Jeans.
- However, '하니' is one of verb conjugations of verb '하다 (do)' at the same time, and it returned a dissapointing result this time as seen above.
- Pretrained model (, which built new vocabulary from comments dataset) may have more general sense, but failed to catch meaningful similar vectors of '하니'.
- Since the purpose and dataset is very focused on a specific theme, it may be better to train word embedding from scratch, not by loading from pretrained embedding from FastText.

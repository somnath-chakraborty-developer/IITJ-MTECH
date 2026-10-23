# FVL: Foundation of Vision & Language

Two in-class activities for the Foundation of Vision & Language course at IIT Jodhpur, both written as Google Colab notebooks. Every code cell carries a short comment saying what it does.

| Folder | Topic | Notebook |
|---|---|---|
| [`activity2-srilm-ngram`](activity2-srilm-ngram) | n-gram language models and smoothing with SRILM | `srilm_ngram_language_models.ipynb` |
| [`activity3-nltk-pos-tagging`](activity3-nltk-pos-tagging) | tokenization, stemming and POS tagging with NLTK | `NLTK-POS-Tagging.ipynb` |

## Activity 2: SRILM n-gram models

Trains bigram and trigram models on the Brown corpus with the SRILM command line tools and compares them by test perplexity.

- **Exercise 1:** unsmoothed bigram model, and why it produces `-inf` probabilities for unseen bigrams.
- **Exercise 2:** add-one, Good-Turing, Kneser-Ney and Witten-Bell (plain and interpolated) smoothing.
- **Exercise 3:** the same comparison for trigrams.
- **Exercise 4:** removing punctuation and stop words before training.
- **Exercise 5:** interpolating a unigram and a bigram model, tuning the add-alpha value and the mixing weight on the dev set.

The notebook expects the SRILM binaries (`ngram`, `ngram-count`) and the `browndata` folder (`brown-train.txt`, `brown-dev.txt`, `brown-test.txt`) inside `My Drive/SRILM-LAB/InClassActivity2` on Google Drive. Those files come from the course and are not included here. If your folder is somewhere else, change the `os.chdir` line in the second code cell. Then use Runtime, Run all.

## Activity 3: NLTK POS tagging

The tutorial notebook from class, completed with the exercises:

- **Stemmer exercise:** Porter, Snowball and Lancaster compared on a word list; Snowball is picked as the best of the three.
- **Last line of a file** and **FreqDist without a list comprehension.**
- **Exercise 1a:** tag six sentences with the perceptron tagger and comment on the mistakes (only *Colorless* comes out wrong).
- **Exercise 1b:** top 10 tags in the Brown corpus, original and universal tagsets.
- **Exercise 2:** word frequencies on the Penn Treebank sample, compared with Brown.
- **Exercise 3:** tag frequencies on the Penn Treebank sample.

The notebook is saved with its outputs, so you can read the results without running anything. To run it yourself, open it in Colab or locally with `pip install nltk`; the cells download the NLTK data they need (`punkt_tab`, `brown`, `treebank`, `universal_tagset`, `averaged_perceptron_tagger_eng`, `wordnet`).

## Notes

The course data, the SRILM binaries and the original tutorial text belong to the course and are not part of this repository.

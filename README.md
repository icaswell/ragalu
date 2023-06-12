# Simple Carnatic NLP

This directory contains a simplistic tool to get the most common ragalu from some input corpus (default: cache of rasikas.org).
This is all some pretty simplistic processing that I whipped together very quickly because I really wanted to know what, approximately, the distribution of ragalu really is. If you want to improve it please do :)

The scripts do the following:


### `data/wget_everything.sh`, `data/html_to_json.py`
Get posts from rasikas.org; parse all html; store posts in a json with the format {post: [comment1, comment2, ...]}


### `process_data.py`
Use regex to get a bunch of possible ragam names from the cached data from the last step; semi-manually create the mapping of canonical ragam name to variant names. Once this is done, populate `raga_name_variants.py`, and then count occurrences of all variants in text.


### `sample_ragam.py`
Given the ragam frequencies calculated in the last step, sample N ragalu (with replacement). The goal of this script is largely if you want to pick a ragam to quiz yourself on. You can change the sampling temperature to make yourself more likely to get common ragalu (with a lower temperature) or more likely to get less common ragalu (with a higher temperature).

Example of sampling 10 ragalu according to how common they are:
```
python3 sample_ragam.py -n10
```

Example of sampling 10 ragalu with a temperature of 3 (upweighting less comon ragalu):
```
python3 sample_ragam.py -n10 -t3

```

### TODOs

  *  The parsing for raga names is extremely simplistic. A sentence like "Ranjani and Gayatri sang a krti by Shree Venkataramana" will be parsed as having the ragalu "ranjani" and "shree"
  *  Might be a good idea to only look at posts about concerts. Probably doable by looking at some element in the html.
  *  The "canonical" names are the most simplified names, but NOT the best ones! For instance, the "canonical" form is "arabi" when it should be "Arabhi", "ārabhi", "ఆరభి", etc, depending on your preference. 
  *  Some of the rare ragalu in the variant names might actually not be ragalu, or might be different names of more common ones. There are of course also some tricky questions, like whether nariritigaula is the same as reethigowlai.

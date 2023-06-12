"""This script does two separate things:

1. looks for possible raga names, that can then be manually curated;
2. after the output of (1) has been stored in raga_name_variants, look for all mentions of these ragalu.

"""
import json
import re
from collections import Counter
import random
from raga_name_variants import variants


def normalize_translit(text):
  """Mutilates the input, but in doing so also normalizes raga names.

  Note: mangle English words, but should have no problems with transliterations.
  Note 2: "th" --> "t" etc. should make no sense. However, there are no ragalu that differ only by those characters, so this level of mangling is OK.
  """
  # First some wrangling to try to downweight the number of conflations of  Shri as a title with Sri the raga
  text = text.replace("Sri ", "")
  text = text.lower()
  text = re.sub("(^|. |\n)sh?r(ee|i) ", "", text)
  text = text.replace(".", " ").replace(",", " ").replace("\"", " ").replace("'", " ".replace(")", " ".replace("(", " "))).replace("!", " ")
  text = text.replace(" sri ", "")
  for vidwan in ["kumaresh", "dikshitar", "tyagaraja", "thyagaraja", "lalgudi"]:
    text = re.sub(f"(^| )sh?r(ee|i) {vidwan}", " {vidwan}", text)
  text = text.replace("ow", "au").replace("ou", "au")
  text = text.replace("sr", "shr")
  text = text.replace("sw", "shw")
  text = text.replace("shree", "shri")
  text = text.replace("priyaa", "priya")
  text = text.replace("kriya", "priya")
  text = text.replace(" ranjani", "ranjani")
  text = text.replace(" gaula", "gaula")
  text = text.replace("shuddha", "suddha").replace("sudha", "suddha").replace("shuda", "suddha")
  text = text.replace("ee", "i")
  text = text.replace("ii", "i")
  text = text.replace("oo", "u")
  text = text.replace("uu", "u")
  text = text.replace("ai ", "a ")
  text = text.replace("ti ", "thi ")
  text = text.replace("ty ", "thi ")
  text = text.replace("thy ", "thi ")
  text = text.replace("ī", "i")
  text = text.replace("ā", "a")
  text = text.replace("ph", "f")
  text = text.replace("th", "t")
  text = text.replace("kh", "k")
  text = text.replace("bh", "b")
  text = text.replace("dh", "d")
  text = text.replace("gh", "g")
  return text


def normalize(raga):
  return NORMALIZING_DICT.get(raga, raga)

NORMALIZING_DICT = {var_i: normalize_translit(canon) for canon, var in variants.items() for var_i in var}
ALL_RAGALU =  [x  for canon, var in variants.items() for x in var | {canon}]


def not_a_raga(raga):
  if len(raga) > 40 or len(raga) < 3: return True
  if not raga[0].isalpha(): return True
  if "," in raga or "?" in raga: return True
  if raga.startswith("karnataka") or raga.startswith("udaya") :
    if raga.count(" ") > 3: return True
  else:
    if raga.count(" ") > 2: return True
  return False


def is_raga(raga):
  if not_a_raga(raga): return False
  raga = normalize(raga)
  return raga in ALL_RAGALU


def normalize_raga_names_in_post(post):
  assert all(" " not in canon for canon in variants)
  post = normalize_translit(post)
  for variant, canonical in NORMALIZING_DICT.items():
    post = post.replace(f" {variant} ", f" {canonical} ")
  return post

def get_possible_ragam_names(post):
  """Get tokens from a post that may refer to ragalu.

  This function is used for finding variant raga names."""
  def ragalu_from_regex(r, line):
    out = []
    for m in re.findall(r, line):
      raga = normalize(m)
      if not_a_raga(raga): continue
      out.append(raga)
    return out

  ragalu = []
  for line in post.split("\n"):
    ragalu += ragalu_from_regex("composition in ([^ ]*)", line)
    ragalu += ragalu_from_regex("piece in ([^ ]*)", line)
    ragalu += ragalu_from_regex("kri?th?i in ([^ ]*)", line)
    ragalu += ragalu_from_regex("varnam? in ([^ ]*)", line)
    ragalu += ragalu_from_regex("aa?lapana in ([^ ]*)", line)
    ragalu += ragalu_from_regex("in r[aA]a?gam? ([^ ]*)", line)
    ragalu += ragalu_from_regex("^[^-]*-([^-]*)", line)
  return ragalu


SENTENCE_SPLITTER = re.compile("[- \n\.,:;'\"()]")
# def get_all_mentions(post, one_of_each=False, minimum_raga_mentions_per_page=3, minimum_post_chars = 100):
def get_all_mentions(post, one_of_each=True, minimum_raga_mentions_per_page=6, minimum_post_chars = 500):
  post = normalize_raga_names_in_post(post)
  if len(post) < minimum_post_chars: return []
  tokens = SENTENCE_SPLITTER.split(post)
  ret = [normalize(tok) for tok in tokens if is_raga(tok)]
  if one_of_each:
      ret = list(set(ret))
  if len(ret) < minimum_raga_mentions_per_page:
      ret = []
  return ret


def load_json():
  with open("data/combined_raw.json", "r") as f:
    data = json.load(f)
  return data


if __name__ == "__main__":
  ragalu_counter = Counter()
  posts_with_ragalu = 0
  data = load_json()
  for i, (post_id, post) in enumerate(data.items()):
    post_combined = "\n".join(post.values())
    # if you are looking for raga names, use get_possible_ragam_names(post_combined)
    ragalu = get_all_mentions(post_combined)
    if ragalu: posts_with_ragalu += 1
    ragalu_counter.update(ragalu)
  
  print(ragalu_counter.most_common())
  print(f"\nPosts with at least one raga mention: {posts_with_ragalu}/{i}")

from bs4 import BeautifulSoup
import json
from glob import glob


def load_posts_from_html(fname):
  with open(f"/Users/icaswell/Documents/ragalu/data/{fname}", "r") as f:
      text = f.read()
  soup = BeautifulSoup(text, 'html.parser')
  posts = soup.find_all("div", class_="content")
  if not posts: return {}
  posts_dict = {i: post.get_text() for i, post in enumerate(posts)}
  return posts_dict


def html_to_json():
  out = {}
  for i, fname in enumerate(glob("everything_*")):
    if i % 1000 == 0:
        print(f"...{i}", end="")
    posts = load_posts_from_html(fname)
    if sum([len(p) for p in posts.values()]) < 5000: continue
    out[fname] = posts
  print()
  with open("combined_raw.json", "w") as f:
    json.dump(out, f)


html_to_json()

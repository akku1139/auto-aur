#!/bin/env python3
import os
import time
import html
import urllib.parse
from git import Repo
import math
from datetime import datetime

repo = Repo(".")

BASE_URL = "/"

def convert_size(size):
  units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB")
  i = math.floor(math.log(size, 1024)) if size > 0 else 0
  if i == 0:
    return f"{size} B"
  else:
    size = round(size / 1024 ** i, 2)
    return f"{size} {units[i]}"

def remove_first_dir(path):
  return "/".join(list(filter(lambda x: not x == ".", path.split("/")))[1:])

for _root, dirs, files in os.walk("public/repo", followlinks=True):
  output_file = os.path.join(_root, "index.html")
  root = remove_first_dir(_root)
  with open(output_file, "w") as f:
    title = f'Index of {BASE_URL}{root}'
    f.write(
      "<!DOCTYPE html>"
      "<html>"
        "<head>"
          f"<title>{title}</title>"
        "</head>"
        "<body>"
          f'<h1>{title}</h1>'
          "<table>"
            "<tr>"
              #"<th>File Name</th><th>Date</th><th>File Size</th>"
              "<th>File Name</th><th>File Size</th>"
            "</tr>"
            "<tr>"
              '<td><a href="../">../</a></td>'
              #"<td></td>"
              "<td></td>"
            "</tr>"
    )

    for item in sorted(dirs):
      path = os.path.join(_root, item)
      #try:
        #latest_commit = list(repo.iter_commits(max_count=1, paths=path))[0]
        #update_time = datetime.strftime(latest_commit.committed_datetime, r"%Y-%m-%d %H:%M %z")
      #except IndexError:
        #print(f"Couldn't get commit for {path}")
        #update_time = "-"
      f.write(
        "<tr>"
          f'<td><a href="{urllib.parse.quote(item, errors="surrogatepass")}/">{html.escape(item, quote=False)}/</a></td>'
          #f'<td>{update_time}</td>'
          "<td>-</td>"
        "</tr>"
      )

    for item in sorted(files):
      path = os.path.join(_root, item)
      #try:
        #latest_commit = list(repo.iter_commits(max_count=1, paths=path))[0]
        #update_time = datetime.strftime(latest_commit.committed_datetime, r"%Y-%m-%d %H:%M %z")
      #except IndexError:
        #print(f"Couldn't get commit for {path}")
      if item == "index.html":
        continue
      else:
        size = convert_size(os.path.getsize(path))
        f.write(
          "<tr>"
            f'<td><a href="{urllib.parse.quote(item, errors="surrogatepass")}">{html.escape(item, quote=False)}</a></td>'
            #f'<td>{update_time}</td>'
            f'<td>{size}</td>'
          "</tr>"
        )
    f.write(
          "</table>"
        "</body>"
      "</html>"
    )

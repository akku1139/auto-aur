#!/bin/env python3
import os
import time
import html
import urllib.parse
from git import Repo
import math
from datetime import datetime

repo = Repo(".")

BASE_URL = "/auto-aur/"

def convert_size(size):
  units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB")
  i = math.floor(math.log(size, 1024)) if size > 0 else 0
  if i == 0:
    return f"{size} B"
  else:
    size = round(size / 1024 ** i, 2)
    return f"{size} {units[i]}"

def remove_first_dir_slice(path):
  return path[path.find('/', 1) + 1:]

for _root, dirs, files in os.walk("./public", followlinks=True):
  # 各ディレクトリごとにHTMLファイルを作成
  output_file = os.path.join(_root, "index.html")
  root = remove_first_dir_slice(_root)
  with open(output_file, "w") as f:
    title = f'Index of {BASE_URL}{root}'
    f.write(
      "<html>"
        "<head>"
          f"<title>{title}</title>"
        "</head>"
        "<body>"
          f'<h1>{title}</h1>'
          "<table>"
            "<tr>"
              "<th>File Name</th><th>Date</th><th>File Size</th>"
            "</tr>"
            "<tr>"
              '<td><a href="../">../</a></td>'
              "<td></td>"
              "<td></td>"
            "</tr>"
    )

    for item in sorted(dirs):
      path = os.path.join(root, item)
      # ディレクトリの場合、リンクを作成
      f.write(
        "<tr>"
          f'<td><a href="{urllib.parse.quote(item, errors="surrogatepass")}/">{html.escape(item, quote=False)}/</a></td>'
          f'<td>{update_time}</td>'
          "<td>-</td>"
        "</tr>"
      )

    for item in sorted(files):
      path = os.path.join(root, item)
      latest_commit = list(repo.iter_commits(max_count=1, paths=path))[0]
      update_time = datetime.strftime(latest_commit.committed_datetime, r"%Y-%m-%d %H:%M %z")
      if item == "index.html":
        continue
      else:
        # ファイルの場合
        size = convert_size(os.path.getsize(path))
        f.write(
          "<tr>"
            f'<td><a href="{urllib.parse.quote(item, errors="surrogatepass")}">{html.escape(item, quote=False)}</a></td>'
            f'<td>{update_time}</td>'
            f'<td>{size}</td>'
          "</tr>"
        )
    f.write(
          "</table>"
        "</body>"
      "</html>"
    )

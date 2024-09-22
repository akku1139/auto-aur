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
    size = round(size / 1024 ** i, 2)

    return f"{size} {units[i]}"

for root, dirs, files in os.walk("./public"):
  # 各ディレクトリごとにHTMLファイルを作成
  output_file = os.path.join(root, "index.html")
  with open(output_file, "w") as f:
    title = f'Index of {BASE_URL}{root}'
    f.write(
      "<html>"
        "<head>"
          f"<title>{title}</title>"
        "</head>"
        "<body>"
          "<table>"
            "<tr>"
              "<th>File Name</th><th>Date</th><th>File Size</th>"
            "</tr>"
            "<tr>"
              f'<td><a href="{os.path.join(root, "../")}/">../</a></td>'
              "<td></td>"
              "<td></td>"
            "</tr>"
    )
    for item in dirs + files:
      path = os.path.join(root, item)
      latest_commit = list(repo.iter_commits(max_count=1, paths=path))[]
      update_time = tdatetime.strftime(latest_commit.committed_datetime(), r"%Y-%m-%d %H:%M %z")
      if os.path.isdir(path):
        # ディレクトリの場合、リンクを作成
        f.write(
          "<tr>"
            f'<td><a href="{urllib.parse.quote(a, errors="surrogatepass")}/">{html.escape(a, quote=False)}/</a></td>'
            f'<td>{update_time}</td>'
            "<td>-</td>"
          "</tr>"
        )
      else:
        # ファイルの場合
        size = convert_size(os.path.getsize(path))
        f.write(
          "<tr>"
            f'<td><a href="{urllib.parse.quote(a, errors="surrogatepass")}">{html.escape(a, quote=False)}/</a></td><td>{size} bytes</td><td>{mtime}</td>'
            f'<td>{update_time}</td>'
            f'{size}'
          "</tr>"
        )
    f.write(
          "</table>"
        "</body>"
      "</html>"
    )

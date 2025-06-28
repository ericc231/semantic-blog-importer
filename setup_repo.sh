#!/bin/bash

# 初始化 Git
git init

# 提示輸入 GitHub 使用者名稱與 repo 名
read -p "GitHub 使用者名稱（例如：eric231）: " USERNAME
read -p "Repository 名稱（例如：semantic-blog-importer）: " REPONAME

# 加入所有檔案
git add .

# 初始 commit
git commit -m "Initial commit: Import semantic blog system"

# 設定 GitHub 遠端位址（使用 SSH）
git remote add origin git@github.com:$USERNAME/$REPONAME.git

# 將當前專案推送至 main 分支
git branch -M main
git push -u origin main

echo "✅ 專案已成功推送至 GitHub: https://github.com/$USERNAME/$REPONAME"

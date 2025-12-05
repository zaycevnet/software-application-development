#!/bin/bash

# Получаем последний тег
latest_tag=$(git describe --tags --abbrev=0)

# Получаем все коммиты с момента последнего тега
commits=$(git log $latest_tag..HEAD --pretty=format:"%h - %s")

# Получаем текущую дату и версию
current_date=$(date +'%Y-%m-%d')
version="v$(git describe --tags)"

# Записываем в changelog.md
echo "## $version - $current_date" > changelog.md
echo "$commits" >> changelog.md

echo "Changelog generated successfully!"

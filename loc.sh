#!/bin/bash

WHITELIST=("py" "js" "html" "sql" "ts" "tsx" "jsx")

declare -A user_loc
temp_file=$(mktemp)

for ext in "${WHITELIST[@]}"; do
    find . -type f -name "*.$ext" -not -path "*/node_modules/*" | while read -r file; do
        git blame --line-porcelain "$file" 2>/dev/null | \
            awk '/^author / {authors[$2]++} END {for (a in authors) print a, authors[a]}' >> "$temp_file"
    done
done

while read -r author lines; do
    user_loc["$author"]=$((user_loc["$author"] + lines))
done < <(sort "$temp_file" | awk '{a[$1]+=$2} END {for (i in a) print i, a[i]}')

echo "Lines of Code per User:"
for user in "${!user_loc[@]}"; do
    echo "$user: ${user_loc[$user]} lines"
done

rm "$temp_file"

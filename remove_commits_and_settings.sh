mkdir ~/temppp
cp src/core/settings.py ~/temppp
cp src/core/secret_settings.py ~/temppp
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch src/core/settings.py' --prune-empty --tag-name-filter cat -- --all
echo "settings.py" >> .gitignore
git add .gitignore
git commit -m "Added personal settings to .gitignore"
git push origin --force --all
git push origin --force --tags
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now

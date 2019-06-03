# Get current release name
CURRENT_RELEASE=$(git tag | tail -1)

# Get lastest release name
RELEASE=$(curl --silent "https://github.com/getsentry/sentry/releases/latest" | sed 's#.*tag/\(.*\)\".*#\1#')

# Exit script if already up to date
if [ "v${RELEASE}" = $CURRENT_RELEASE ]; then
  exit 0
fi

# Replace version line in requirements.txt with the new release
sed -i "s#sentry==.*#sentry==${RELEASE}#" requirements.txt
sed -i "s#sentry-plugins==.*#sentry-plugins==${RELEASE}#" requirements.txt

# Replace README link to grafana release
SENTRY_BADGE="[![Sentry](https://img.shields.io/badge/Sentry-${RELEASE}-blue.svg)](https://github.com/getsentry/sentry/releases/tag/${RELEASE})"
sed -i "s#\[\!\[Sentry\].*#${SENTRY_BADGE}#" README.md

# Push changes
git add requirements.txt README.md
git commit -m "Update to sentry version v${RELEASE}"
git push origin master

# Create tag
git tag "v${RELEASE}"
git push --tags

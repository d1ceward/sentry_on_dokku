# Get lastest release name
RELEASE_SENTRY=$(curl --silent "https://github.com/getsentry/sentry/releases/latest" | sed 's#.*tag/\(.*\)\".*#\1#' | cut -f2 -d 'v')
RELEASE_SENTRY_PLUGINS=$(curl --silent "https://github.com/getsentry/sentry-plugins/releases/latest" | sed 's#.*tag/\(.*\)\".*#\1#' | cut -f2 -d 'v')

# Replace version line in requirements.txt with the new release
sed -i "s#sentry==.*#sentry==${RELEASE_SENTRY}#" requirements.txt
sed -i "s#sentry-plugins==.*#sentry-plugins==${RELEASE_SENTRY_PLUGINS}#" requirements.txt

# Replace README link to grafana release
SENTRY_BADGE="[![Sentry](https://img.shields.io/badge/Sentry-${RELEASE_SENTRY}-blue.svg)](https://github.com/getsentry/sentry/releases/tag/${RELEASE_SENTRY})"
sed -i "s#\[\!\[Sentry\].*#${SENTRY_BADGE}#" README.md

# Push changes
git add Dockerfile README.md
git commit -m "Update to sentry version v${RELEASE_SENTRY}"
git push origin master

# Create tag
git tag "v${RELEASE_SENTRY}"
git push --tags

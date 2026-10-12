#!/bin/bash
# Cache-busting: stamp a content hash into index.html (VER) and version.json. Run before each commit.
cd "$(dirname "$0")/.."
V=$( (sed "s/const VER='[^']*'/const VER=''/" index.html; cat data/guilds.json) | sha1sum | cut -c1-10)
sed -i "s/const VER='[^']*'/const VER='$V'/" index.html
echo "{\"v\":\"$V\"}" > version.json; echo "stamped $V"

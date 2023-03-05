set -e

COMMIT_MSG=$1
if [[ -z $COMMIT_MSG ]]; then
    echo "missing commit message"
    exit 1
fi

echo "commit message: $COMMIT_MSG"

./render.py

cp *.html ../kkloberdanz.github.io/
cp -r style ../kkloberdanz.github.io/
cp -r image ../kkloberdanz.github.io/

cd ../kkloberdanz.github.io
git add --all
git commit -m "$COMMIT_MSG"
git push

echo "CHANGES TO WEBSITE ARE NOW LIVE"

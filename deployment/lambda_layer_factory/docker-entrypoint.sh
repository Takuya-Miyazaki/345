#!/bin/bash

echo "================================================================================"
echo "Installing the packages listed in requirements.txt:"
echo "================================================================================"

cat /packages/requirements.txt

for i in "$@"
do
    echo "Installing for Python version $i"
    mkdir -p /packages/lambda_layer-python-$i/python/lib/python$i/site-packages
    pip$i install -q -r /packages/requirements.txt -t /packages/lambda_layer-python-$i/python/lib/python$i/site-packages    
done

echo "================================================================================"
echo "Installing MediaInfo package"
echo "================================================================================"
# Use specified mediainfo version in case the latest version is not compatible in future updates.
VERSION="23.07"
echo "MediaInfo latest version = v$VERSION"
URL=https://mediaarea.net/download/binary/libmediainfo0/${VERSION}/MediaInfo_DLL_${VERSION}_Lambda_x86_64.zip
echo "Downloading MediaInfo from $URL"
cd /
curl $URL -o mediainfo.tgz || exit 1
echo "Checking md5sum for MediaInfo source..."
# Check the md5sum for MediaInfo 19.09:
echo "4fcb1d40994fc1c2a56d0b6df4860f61  mediainfo.tgz" > mediainfo.md5 
md5sum --check mediainfo.md5 || exit 1
unzip -d mediainfo-lambda-lib mediainfo.tgz
echo "Copying MediaInfo library into lambda layer folder"

for i in "$@"
do
    echo "Copying to Python version $i directory"
    cp mediainfo-lambda-lib/lib/* /packages/lambda_layer-python-$i/python/ || exit 1
done
echo "Finished copying MediaInfo library files"

echo "================================================================================"
echo "Creating zip files for Lambda layers"
echo "================================================================================"
for i in "$@"
do
    echo "Copying zip files to Python version $i directory"
    cd /packages/lambda_layer-python-$i/
    zip -q -r /packages/lambda_layer-python$i.zip .
done

echo "================================================================================"
echo "Cleaning up Build environments"
echo "================================================================================"
cd /packages/
for i in "$@"
do
    echo "Removing environments for Python version $i"
    rm -rf /packages/pymediainfo-$i/
    rm -rf /packages/lambda_layer-python-$i/
done

echo "Zip files have been saved"
echo "================================================================================"

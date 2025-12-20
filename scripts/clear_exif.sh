#!/bin/bash

# Script for removing EXIF data of all images in the craft section

images=$(git ls-files --others --cached --exclude-standard '*.png' '*.jpg' '*.jpeg' | grep -E "^content/craft")

for image in $images; do
	echo "Image: $image"
	# Clear EXIF data
	exiftool -all= $image
	# Remove backup image
	yes | exiftool -delete_original $image
done

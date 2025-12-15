#!/bin/bash

# Script for removing EXIF data of all images in the Craft section

images=$(find content/craft/ -name "*.png" -o -name "*.jpg" -o -name "*.jpeg")

for image in $images; do
	echo "Image: $image"
	# Clear EXIF data
	exiftool -all= $image
	# Remove backup image
	yes | exiftool -delete_original $image
done

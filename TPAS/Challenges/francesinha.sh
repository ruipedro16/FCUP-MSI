#!/bin/sh

echo "$(exiftool intercepted-image.jpg | grep -oE "GPS Position.+")       # Location of Cafe Aviz"
echo "TPAS{Cafe Aviz}"

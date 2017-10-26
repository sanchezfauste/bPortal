#!/bin/bash

SVG_ICONS_FOLDER=dark
FAVICON_FOLDER=favicon

for svg_file in $SVG_ICONS_FOLDER/*.svg; do
    favicon_file=$FAVICON_FOLDER/$(basename $svg_file .svg).ico
    echo "Generating $favicon_file";
    convert -density 384 -background transparent $svg_file -define icon:auto-resize -colors 256 $favicon_file;
done

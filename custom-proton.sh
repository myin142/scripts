#!/bin/sh

version="5.21-GE-1"
name="Proton-$version"
file="$name.tar.gz"
url="https://github.com/GloriousEggroll/proton-ge-custom/releases/download/$version/$file"
location="$HOME/.steam/root/compatibilitytools.d"

if [ ! -d "$location" ]; then
    mkdir -p $location
fi

if [ ! -f "$file" ]; then
    wget $url
fi

if [ ! =d "$name" ]; then
    tar xzf $file
fi

if [ ! -d "$location/$name" ]; then
    cp -r $name $location
fi
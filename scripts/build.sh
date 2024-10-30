#!/usr/bin/bash
PROJECT_NAME="music-list-player"
CONFIGURATION_FILE_PATH="configuration.toml"
DOCUMENTATION_FILE_PATH="README.md"
PLAYLIST_FILE_PATH="playlist.txt"
DEFAULT_CACHE_DIRECTORY_NAME=".cache"

APPLICATION_BUILD_DIRECTORY_PATH="dist"
OUTPUT_DIRECTORY_BUILD_PATH="${APPLICATION_BUILD_DIRECTORY_PATH}/${PROJECT_NAME}"
declare -a DATA_TO_INCLUDE_IN_BUILD=(
    $CONFIGURATION_FILE_PATH
    $DOCUMENTATION_FILE_PATH
    $PLAYLIST_FILE_PATH
)

# Generate the application executable
pyinstaller main.py --clean --noconfirm \
    --onedir \
    --name $PROJECT_NAME \
    --additional-hooks-dir=hooks

# Include the necessary files and directory
for file_path in "${DATA_TO_INCLUDE_IN_BUILD[@]}"
do
    info "copying $file_path"
    cp $file_path $OUTPUT_DIRECTORY_BUILD_PATH
done
mkdir "$OUTPUT_DIRECTORY_BUILD_PATH/$DEFAULT_CACHE_DIRECTORY_NAME"

# Archive the build
cd $APPLICATION_BUILD_DIRECTORY_PATH
tar -czvf "${PROJECT_NAME}.tar.gz" "${PROJECT_NAME}"
cd -

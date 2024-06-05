#!/usr/bin/bash
PROJECT_NAME="music-list-player"
CONFIGURATION_FILE_PATH="configuration.toml"
DOCUMENTATION_FILE_PATH="README.md"

APPLICATION_BUILD_DIRECTORY_PATH="dist"
OUTPUT_DIRECTORY_BUILD_PATH="${APPLICATION_BUILD_DIRECTORY_PATH}/${PROJECT_NAME}"
declare -a DATA_TO_INCLUDE_IN_BUILD=(
    $CONFIGURATION_FILE_PATH
    $DOCUMENTATION_FILE_PATH
)

# Generate the application executable
pyinstaller main.py --clean --noconfirm \
    --onedir \
    --name $PROJECT_NAME \
    --additional-hooks-dir=hooks

# Include the necessary files
for file_path in "${DATA_TO_INCLUDE_IN_BUILD[@]}"
do
    info "copying $file_path"
    cp $file_path $OUTPUT_DIRECTORY_BUILD_PATH
done

# Archive the build
cd $APPLICATION_BUILD_DIRECTORY_PATH
tar -czvf "${PROJECT_NAME}.tar.gz" "${PROJECT_NAME}"
cd -

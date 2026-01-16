DIR_PATHS=(
    "data/EMA/downloads"
    # "data/Swissmedic/downloads"
    # "data/PMDA/downloads"
    "data/Australia/downloads"
)

for DIR_PATH in "${DIR_PATHS[@]}"; do
    python src/clean_filenames.py\
        --dir_path "$DIR_PATH"
done

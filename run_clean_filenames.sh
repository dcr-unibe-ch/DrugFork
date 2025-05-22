DIR_PATHS=(
    "data/EMA/EMA_downloads"
    "data/SwissPar/SwissPAR_Jan19_2025"
)

for DIR_PATH in "${DIR_PATHS[@]}"; do
    python src/clean_filenames.py\
        --dir_path "$DIR_PATH"
done

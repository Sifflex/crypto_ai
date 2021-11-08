# /usr/bin/sh

DATA_DIR="data/csv"

for path in ${DATA_DIR}/*; do
    IFS='/' read -ra ADDR <<< "$path"
    filename="${ADDR[3]}"
    if [[ $filename == csv15* ]]; then
        updated_filename="15MIN_${filename:5:42}"
        mv ${DATA_DIR}/$filename ${DATA_DIR}/$updated_filename
    elif [[ $filename == csv1* ]]; then
        updated_filename="1MIN_${filename:4:42}"
        mv ${DATA_DIR}/$filename ${DATA_DIR}/$updated_filename
    fi
done

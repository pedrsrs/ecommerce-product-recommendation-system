#!/bin/bash

CONTAINER_NAME="postgres"
DB_USER="admin"
DB_NAME="ecommerce_data"
categories=("All_Beauty" "Amazon_Fashion" "Appliances" "Arts_Crafts_and_Sewing" "Automotive" "Baby_Products" "Beauty_and_Personal_Care" "Books" "CDs_and_Vinyl" "Cell_Phones_and_Accessories" "Clothing_Shoes_and_Jewelry" "Electronics" "Grocery_and_Gourmet_Food" "Handmade_Products" "Health_and_Household" "Health_and_Personal_Care" "Home_and_Kitchen" "Industrial_and_Scientific" "Musical_Instruments" "Office_Products" "Pet_Supplies" "Sports_and_Outdoors" "Tools_and_Home_Improvement" "Toys_and_Games" "Video_Games")

cd product_data

download_and_preprocess() {
    local name="$1"
    echo "Downloading $name..."
    
    url="https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/meta_categories/meta_${name}.jsonl.gz"
    output_file="${name}.jsonl.gz"
    
    curl -L -o "$output_file" "$url"
    gunzip -c "$output_file" > "${name}.jsonl"
    head -n 100000 "${name}.jsonl" > "${name}_100k.jsonl"
    
    echo "main_category,title,average_rating,rating_number,features,description,price,store,categories,details,parent_asin" > "${name}.csv"
    echo "parent_asin,thumb,large,variant,hi_res" > "${name}_images.csv"
    
    jq -r '
    . as $p |
    [   
        $p.main_category,
        $p.title,
        ($p.average_rating),
        ($p.rating_number),
        ($p.features | @json),
        ($p.description | @json),
        (
            $p.price
            | if . == null then "" else tostring end  # Convert null to empty string
            | gsub("[^0-9.]"; "")                    # Clean non-numeric characters
            | if . == "" then null else (tonumber? // null) end  # Empty → null, invalid → null
        ),
        $p.store,
        ($p.categories | @json),
        ($p.details | @json),
        $p.parent_asin
    ] | @csv' "${name}_100k.jsonl" >> "${name}.csv"
    
    jq -r '
    . as $p |
    .images[]? | 
    [
        $p.parent_asin,
        .thumb,
        .large,
        .variant,
        .hi_res
    ] | @csv' "${name}_100k.jsonl" >> "${name}_images.csv"
    
    echo "$name processing complete."
}

cleanup_files() {
    rm -rf *.jsonl*
}

db_import() {
    local csv_file="$1"
    
    if [[ "$csv_file" == *_images.csv ]]; then
        table_name="product_images"
    else
        table_name="products"
    fi
    
    cat "$csv_file" | docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c \
        "COPY $table_name FROM STDIN WITH DELIMITER ',' CSV HEADER NULL ''"
    
    echo "File '$csv_file' imported into table $table_name"
}

for name in "${categories[@]}"; do
    download_and_preprocess "$name"
done

cleanup_files

for csv_file in ./*.csv; do
    db_import "$csv_file"
done

echo "All files processed!"
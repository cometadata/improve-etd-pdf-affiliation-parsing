# Sample ETD OA URLs from OpenAlex

Fetches open access dissertation URLs from OpenAlex API and saves to CSV, filtering for dissertations with open access URLs but no raw affiliation strings.

## Usage

```bash
python sample_etd_oa_urls_from_openalex.py -n <sample_size> -o <output_file> [-s <seed>]
```

## Options

- `-n, --sample_size`: Number of records to fetch (required, max 10,000)
- `-o, --output_file`: Output CSV filename (required)
- `-s, --seed`: Random seed for reproducible sampling (required for >200 records)

## Output

CSV with columns: `work_id`, `oa_url`
# Download ETD PDFs from OA URLs

Script for validating URLs, detecting PDFs, and downloading files from a CSV dataset derived from OpenAlex OA URLs.

## Installation


```bash
requests
```

## Usage

```bash
python download_etd_pdfs_from_oa_urls.py -i <input_csv> [-o <output_csv>] [-d <download_directory>]
```

### Parameters

- `-i, --input`: Path to input CSV file
- `-o, --output`: Path for output CSV file (default: [input_filename]_processed.csv)
- `-d, --directory`: Directory to save downloaded PDFs (default: [input_filename]_pdfs/)
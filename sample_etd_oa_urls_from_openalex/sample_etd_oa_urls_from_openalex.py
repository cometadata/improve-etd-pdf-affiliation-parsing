import csv
import sys
import math
import argparse
import requests


def parse_arguments(max_sample_size_const, max_results_per_page_const):
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--sample_size", type=int, required=True)
    parser.add_argument("-o", "--output_file", type=str, required=True)
    parser.add_argument("-s", "--seed", type=int)

    args = parser.parse_args()

    if args.sample_size > max_sample_size_const:
        print(f"Error: Sample size cannot exceed {max_sample_size_const}.")
        sys.exit(1)
    if args.sample_size <= 0:
        print("Error: Sample size must be a positive integer.")
        sys.exit(1)

    num_pages = math.ceil(args.sample_size / max_results_per_page_const)
    if num_pages > 1 and args.seed is None:
        print(f"Error: A seed value is required when sampling more than {max_results_per_page_const} records.")
        sys.exit(1)

    return args


def fetch_page_from_api(api_url, params):
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"API Response Text: {e.response.text}")
        return None


def process_api_results(api_response_json):
    processed_records = []
    if not api_response_json or 'results' not in api_response_json:
        return processed_records

    for record in api_response_json['results']:
        work_id = record.get('id')
        oa_url = None

        open_access_info = record.get('open_access')
        if open_access_info and open_access_info.get('is_oa'):
            oa_url = open_access_info.get('oa_url')

        if work_id:
            processed_records.append(
                {'work_id': work_id, 'oa_url': oa_url if oa_url else ''})

    return processed_records


def save_to_csv(data, output_file):
    if not data:
        print("No data to save.")
        return

    keys = data[0].keys()
    try:
        with open(output_file, 'w', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"Successfully saved {len(data)} records to {output_file}")
    except IOError as e:
        print(f"Error writing to CSV file {output_file}: {e}")


def main():
    openalex_api_url = "https://api.openalex.org/works"
    max_results_per_page = 200
    max_sample_size_limit = 10000

    args = parse_arguments(max_sample_size_limit, max_results_per_page)

    print(f"Starting to fetch {args.sample_size} works...")

    all_processed_records = []

    filters = "type:dissertation,open_access.is_oa:true,has_raw_affiliation_strings:false"
    select_fields = "id,open_access"

    num_pages = math.ceil(args.sample_size / max_results_per_page)

    for page_num in range(1, num_pages + 1):
        current_per_page = max_results_per_page
        if page_num == num_pages:
            remaining_records = args.sample_size - \
                ((page_num - 1) * max_results_per_page)
            if remaining_records < max_results_per_page:
                current_per_page = remaining_records

        if current_per_page <= 0:
            break

        params = {
            'filter': filters,
            'select': select_fields,
            'sample': args.sample_size,
            'per-page': current_per_page,
            'page': page_num
        }
        if args.seed is not None:
            params['seed'] = args.seed

        print(f"Fetching page {page_num}/{num_pages} with up to {current_per_page} records...")

        api_response = fetch_page_from_api(openalex_api_url, params)

        if api_response:
            processed_page_records = process_api_results(api_response)
            all_processed_records.extend(processed_page_records)
            print(f"Fetched {len(processed_page_records)} records from page {page_num}. Total fetched: {len(all_processed_records)}")

            if len(processed_page_records) < current_per_page or len(all_processed_records) >= args.sample_size:
                break
        else:
            print(f"Failed to fetch page {page_num}. Stopping.")
            break

    if all_processed_records:
        final_records_to_save = all_processed_records[:args.sample_size]
        save_to_csv(final_records_to_save, args.output_file)
    else:
        print("No records were fetched or processed.")


if __name__ == "__main__":
    main()

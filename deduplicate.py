import csv
import requests
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from requests.exceptions import RequestException

def deduplicate_file(input_path, output_path):
    seen = {}
    failed_urls = []
    successful_count = 0
    total_urls = 0
    header = None

    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    def check_url(row):
        nonlocal successful_count
        url = row[0].strip()
        try:
            start_time = time.time()
            response = requests.get(url, timeout=5)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                if elapsed > 1:  # 超过1秒视为慢速
                    logging.warning(f"⚠️ {url} is slow (took {elapsed:.2f}s)")
                    return (False, row)
                logging.info(f"✅ {url} is reachable (took {elapsed:.2f}s)")
                return (True, row)
            else:
                logging.warning(f"❌ {url} returned {response.status_code}")
                return (False, row)
        except RequestException as e:
            logging.error(f"URLException {url}: {str(e)}")
            return (False, row)

    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [row for row in reader if row]
        
        # 检查是否有表头(第一行与其他行格式不同)
        # if len(rows) > 1 and len(rows[0]) != len(rows[1]):
        if False:
            header = rows[0]
            rows = rows[1:]
        else:
            header
            rows=rows
            
        total_urls = len(rows)
        logging.info(f"Total URLs to process: {total_urls}")

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_row = {executor.submit(check_url, row): row for row in rows}
            for future in as_completed(future_to_row):
                row = future_to_row[future]
                try:
                    result, data = future.result()
                    if result:
                        url = data[0].strip()
                        if url not in seen:
                            seen[url] = data
                            successful_count +=1
                except Exception as exc:
                    logging.error(f"Unexpected error processing {row}: {exc}")

    logging.info(f"✅ Completed {input_path}: {successful_count}/{total_urls} URLs valid")
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        # 如果有表头先写入表头
        if header:
            f.write(','.join(header) + '\n')
        # 写入去重后的内容
        for row in seen.values():
            f.write(','.join(row) + '\n')

if __name__ == '__main__':
    print(f"Starting deduplication main function process...")
    import sys
    import os
    import shutil
    
    if len(sys.argv) != 3:
        print("Usage: python deduplicate.py <input_file> <output_file>")
        sys.exit(1)
        
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # 创建备份
    backup_path = f"{input_path}.bak"
    shutil.copy2(input_path, backup_path)
    print(f"Created backup at {backup_path}")
    
    try:
        deduplicate_file(input_path, output_path)
        print(f"Successfully deduplicated {input_path} -> {output_path}")
    except Exception as e:
        print(f"Error during deduplication: {str(e)}")
        print(f"Restoring from backup {backup_path}")
        shutil.move(backup_path, input_path)
        sys.exit(1)

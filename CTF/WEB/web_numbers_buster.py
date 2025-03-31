import requests
import concurrent.futures

url = "http://targetlist.deadface.io:3001/pages?page="

def fetch_page(page_number):
    response = requests.get(url + str(page_number))
    return f"Page: {page_number}, Size: {len(response.content)} bytes"

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    page_numbers = range(1, 1000)
    results = executor.map(fetch_page, page_numbers)

for result in results:
    print(result)

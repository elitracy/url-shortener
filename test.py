import requests
from tqdm import tqdm

def import_urls(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def generate_shortened_url(url):
    payload = {"url": url} 
    response = requests.post("http://localhost:8000/url/shorten", json=payload, headers={"Connection": "close"})
    return response

def check_shortened_url(shortened_url):
    response = requests.get(shortened_url, allow_redirects=False)
    return response


def main():
    file_path = "urls-med.txt"
    urls = import_urls(file_path)
    url_dict = {}


    print("Generating URLs")

    for url in tqdm(urls):
        create_res = generate_shortened_url(url)
        if create_res.status_code == 400:
            print(f"Error generating url: {url}")
            return

        short_url = create_res.json()['short_url']
        url_dict[url] = short_url

    print("URLs generated successfully!")
    print("Checking URLs")

    for url, shortened_url  in tqdm(url_dict.items()):
        check_res = check_shortened_url(shortened_url)
        if check_res.status_code == 404:
            print(f"URL not stored: {url}, {shortened_url}")
            return

    print("All urls are stored correctly!")


if __name__ == "__main__":
    main()



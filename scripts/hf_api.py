import requests
import json
import argparse


def get_data(output_path: str):
    """
    Fetches data from the specified API endpoint and saves it to a file.

    Args:
        output_path (str): The path to the file where the data will be stored.
    """
    url = "https://agents-course-unit4-scoring.hf.space/questions"
    headers = {
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Request successful: {response.status_code}")
        data = response.json()
        with open(output_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        return data
    else:
        print(f"Request failed with status code {response.status_code}")

def get_files(output_dir: str, data: dict):
    """
    Fetches auxiliary files from the specified API endpoint and saves them to a directory.

    Args:
        output_dir (str): The path to the directory where the files will be stored.
    """
    url = "https://agents-course-unit4-scoring.hf.space/files"
    headers = {
        "accept": "application/json"
    }

    for sample in data:
        task_id = sample.get("task_id")
        file_url = f"{url}/{task_id}"
        file_response = requests.get(file_url)
        if file_response.status_code == 200:
            print(f"File request successful: {file_response.status_code}")
            content_disposition = file_response.headers.get("content-disposition")
            if content_disposition and "filename=" in content_disposition:
                file_name = content_disposition.split("filename=")[-1].strip('"')
            else:
                file_name = f"{task_id}.json"
                print("Filename not found in headers, using default filename.")
            with open(f"{output_dir}/{file_name}", "wb") as f:
                f.write(file_response.content)
        else:
            print(f"File request failed with status code {file_response.status_code}")
            continue


def main(output_path: str):
    """
    Get data and all auxiliary files.
    """
    data = get_data(output_path)
    # Add any other auxiliary file fetching functions here
    get_files("../data/", data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch data from API and save to a file.")
    parser.add_argument(
        "--output_path",
        type=str,
        default="../data/questions.json",
        help="Path to the file where the data will be stored."
    )
    args = parser.parse_args()

    main(args.output_path)
        
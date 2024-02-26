from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import argparse
import json

# define credential file path
CREDENTIAL_FILE_PATH = "credentials.json"

# define mapping file path
SITE_MAPPING_FILE_PATH = "site_mapping.json"

# define default wait component timeout
DEFAULT_WAIT_COMPONENT_TIMEOUT = 20


def load_credentials(path: str) -> any:
    # open file
    with open(path, "r") as file:
        json_data = file.read()
    return json.loads(json_data)


def get_arguments() -> list:
    # parse arguments
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-s", "--sites", type=str, help="Site name")
    args = parser.parse_args()
    if "sites" not in args:
        return {}
    
    if args.sites is None:
        return {}
    
    # split sites
    sites = args.sites.split()
    return {
        "sites": sites
    }


def load_site_mapping(path: str) -> any:
    with open(path, "r") as file:
        json_data = file.read()
    return json.loads(json_data)


def handle_site_flow(driver: WebDriver, url: str, fields: dict, credentials: dict) -> None:
    if url == "":
        raise Exception("url empty")

    # open url
    driver.get(url)

    # process each fields
    for field in fields:
        if "type" not in field:
            raise Exception("please provide field type")
        
        if "name" not in field:
            raise Exception("please provide field name")
        
        if "find_by" not in field:
            raise Exception("please provide field find_by")
        
        if "identifier" not in field:
            raise Exception("please provide field identifier")

        # handle input field
        if field["type"] == "input":
            if field["name"] not in credentials:
                raise Exception(f"{field['name']} value empty")

            input = WebDriverWait(driver=driver, timeout=DEFAULT_WAIT_COMPONENT_TIMEOUT).until(EC.visibility_of_element_located((field["find_by"], field["identifier"])))
            input.send_keys(credentials[field["name"]])
            
        # handle button
        elif field["type"] == "button":
            button = WebDriverWait(driver=driver, timeout=DEFAULT_WAIT_COMPONENT_TIMEOUT).until(EC.element_to_be_clickable((field["find_by"], field["identifier"])))
            button.click()


def main() -> None:
    try:
        # load site mapping json
        site_mapping = load_site_mapping(SITE_MAPPING_FILE_PATH)
        credentials = load_credentials(CREDENTIAL_FILE_PATH)

        # parse arguments
        args = get_arguments()
        if "sites" not in args:
            raise Exception("please provide sites argument")
        
        sites = args["sites"]

        # init chrome browser
        driver = webdriver.Chrome()

        # process each site
        for idx, site in enumerate(sites):
            if site not in site_mapping:
                raise Exception(f"site {site} not found in mapping file")
            
            if site not in credentials:
                raise Exception(f"credential {site} not found in mapping file")
            
            # open new window for non first site
            if idx > 0:
                driver.execute_script("window.open('', '_blank');")
                driver.switch_to.window(driver.window_handles[idx])

            # handle flow
            handle_site_flow(driver=driver, url=site_mapping[site]["url"], fields=site_mapping[site]["fields"], credentials=credentials[site])

        # keep program alive
        while True:
            sleep(1)
        
    except Exception as e:
        print("Something went wrong: ", e)

if __name__ == "__main__":
    main()

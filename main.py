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
SITE_MAPPING_FILE_PATH = "site_fields_mapping.json"

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
    parser.add_argument("-s", "--sites", type=str, help="sites")
    parser.add_argument("-m", "--site-mapping-path", type=str, help="site mapping path")
    parser.add_argument("-c", "--credential-path", type=str, help="credential path")
    args = parser.parse_args()
    if "sites" not in args:
        return {}
    
    if args.sites is None:
        return {}
    
    # split sites
    sites = args.sites.split()

    # override site_mapping_path if data provided
    site_mapping_path = ""
    if "site_mapping_path" in args and args.site_mapping_path is not None:
        site_mapping_path = args.site_mapping_path

    # override credential_path if data provided
    credential_path = ""
    if "credential_path" in args and args.credential_path is not None:
        credential_path = args.credential_path

    return {
        "sites": sites,
        "site_mapping_path": site_mapping_path,
        "credential_path": credential_path
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
        
        if field["find_by"] not in [By.ID, By.XPATH, By.LINK_TEXT, By.PARTIAL_LINK_TEXT, By.NAME, By.TAG_NAME, By.CLASS_NAME, By.CSS_SELECTOR]:
            raise Exception("unsupported find_by value")
        
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
        # parse arguments
        args = get_arguments()
        if "sites" not in args:
            raise Exception("please provide sites argument")
        
        sites = args["sites"]

        # override site_mapping_path if data provided
        site_mapping_path = SITE_MAPPING_FILE_PATH
        if args["site_mapping_path"] != "":
            site_mapping_path = args["site_mapping_path"]

        # override credential_path if data provided
        credential_path = SITE_MAPPING_FILE_PATH
        if args["credential_path"] != "":
            credential_path = args["credential_path"]


        # load site mapping json
        site_mapping = load_site_mapping(site_mapping_path)

        # load credential json
        credentials = load_credentials(credential_path)

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

from selenium import webdriver
from time import sleep
import argparse
import json
import github
import twitter

# define supported sites
supportedSites = ["github", "twitter"]

def loadCredentials() -> any:
    with open("credentials.json", "r") as file:
        json_data = file.read()
    return json.loads(json_data)

def main() -> None:
    try:
        # parse site from argument
        parser = argparse.ArgumentParser(description="")
        parser.add_argument("-s", "--sites", type=str, help="Site name")
        args = parser.parse_args()
        sites = args.sites.split()

        credentials = loadCredentials()

        # init driver
        driver = webdriver.Chrome()

        # loop and handle for each site
        for idx, site in enumerate(sites):
            if site not in supportedSites:
                continue

            # open new tab for non first site
            if idx > 0:
                driver.execute_script("window.open('', '_blank');")
                driver.switch_to.window(driver.window_handles[idx])

            if site == "github":
                github.exec(driver, credentials["github"])
            elif site == "twitter":
                twitter.exec(driver, credentials["twitter"])

        # keep program running until user close chrome
        while True:
            sleep(1)

    except Exception as e:
        print("Something went wrong: ", e)

if __name__ == "__main__":
    main()

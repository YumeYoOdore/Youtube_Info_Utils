import sys
import argparse

from selenium.webdriver.common.by import By
#use export PYTHONPATH='path/to/WebDriverTorso' in bash 
from WebDriverTorso import WebDriverTorso

def get_unavailable_urls(scraper):
    #OPTIONAL
    #subroutine to click on "show unavailable videos"
    options_button_class_name = 'yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-button '
    options_button_xpath = '//button[@class = "%s" and @aria-label = "Action menu"]' % options_button_class_name

    scraper.wait_element_click(options_button_xpath)
    show_unavailable_videos = scraper.driver.find_element('xpath', '//a[@class = "yt-simple-endpoint style-scope ytd-menu-navigation-item-renderer"]')
    show_unavailable_videos.click()


def get_playlist_urls(scraper, options = {}):
    url_list = []
    url_list_file = 'url_list.txt'
    scraper.run()

    if options.get('include_unavailable_urls'):
        get_unavailable_urls(scraper)

    try:
        playlist_main_container = scraper.driver.find_element(By.TAG_NAME, 'ytd-playlist-video-renderer')
        
        href_lookup = playlist_main_container.find_elements('xpath', '//a[contains(@href, "/watch?")]')
        for href in href_lookup:
            url = href.get_attribute('href')
            print(f'found url: {url}')
            url_list.append(url.partition("&list=")[0]) #getting only URL without list indicator
    except:
        print("Error finding HTML tags, make sure the provided list has videos or it's videos aren't hidden. Try running the scraper without headless mode (flag -nh)")

    if url_list:
        with open(url_list_file, 'w') as file:
            file.write('\n'.join(url_list))

    
def main():
    scraper = WebDriverTorso(params)
    get_playlist_urls(scraper, options)
    scraper.finis()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, help='target playlist URL', required=True)
    parser.add_argument('-nh', '--no_headless', help='add this flag if want to run webdriver with an open window: default is off', action="store_true")
    parser.add_argument('-ua', '--unavailable_videos_include', help='add this flag if want to include unavailable videos on the scrape', action="store_true")

    args = parser.parse_args()

    params = {
        'url': args.url,
        'headless_mode': not args.no_headless
    }

    print(params)

    options = {
        'include_unavailable_urls': args.unavailable_videos_include
    }

    main()
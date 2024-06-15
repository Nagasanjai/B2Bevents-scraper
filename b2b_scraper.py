import requests
from bs4 import BeautifulSoup
import csv

event_urls = [
    'https://b2bmarketingleaders.com.au/singapore/',
    'https://www.eventbrite.com/e/engage-2024-tickets-781606475007',
    'https://www.marketingaiinstitute.com/events/marketing-artificial-intelligence-conference',
    'https://www.saastrannual2024.com/',
    'https://events.joinpavilion.com/gtm2024?utm_medium=banner&utm_campaign=GTM2024&utm_source=Website&utm_content=&utm_term=',
]

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def scrape_b2b_marketingleaders(soup):
    main_div = soup.find('div', class_='col-md-6 col-sm-push-1 col-sm-10 intro-txt white-color')
    headings_text = [heading.get_text(strip=True) for heading in main_div.find_all(['h2', 'h3', 'h4'])]

    event_name = headings_text[1]
    event_date, location = headings_text[0].split('|')
    description = headings_text[2]

    ul_element = soup.find('ul', class_='speakers-wrapper')
    speaker_names = [li.find('h2').find('a').get_text(strip=True) for li in ul_element.find_all('li') if li.find('h2') and li.find('h2').find('a')]

    categories = [div.find('div', class_='wpb_wrapper').find('h3').get_text(strip=True) for div in soup.find_all('div', class_='wpb_column vc_column_container vc_col-sm-4')[:18]]

    register = soup.find('a', title='Register!')['href']

    return {
        'Event Name': event_name,
        'Event Date(s)': event_date.strip(),
        'Location': location.strip(),
        'Description': description,
        'Key Speakers': ", ".join(speaker_names),
        'Agenda/Schedule': "N/A",
        'Registration Details': register,
        'Pricing': "N/A",
        'Categories': ", ".join(categories),
        'Audience Type': "N/A"
    }


def scrape_pavilion(soup):
    event_name = soup.find('h2', class_='xxxl-blue').get_text(strip=True)
    description = soup.find('div', class_='atom-main full-width margin-custom-element element-12384895').find('div').find('p').get_text(strip=True)
    location, event_date = soup.find('h4', class_='headline-m white').get_text(strip=True).split('|')

    return {
        'Event Name': event_name,
        'Event Date(s)': event_date.strip(),
        'Location': location.strip(),
        'Description': description,
        'Key Speakers': "N/A",
        'Agenda/Schedule': "N/A",
        'Registration Details': "N/A",
        'Pricing': "N/A",
        'Categories': "N/A",
        'Audience Type': "N/A"
    }

def scrape_eventbrite(soup):
    event_name = soup.find('h1', class_='event-title css-0').get_text(strip=True)
    event_date = soup.find('span', class_='date-info__full-datetime').get_text(strip=True)
    location = soup.find('p', class_='location-info__address-text').get_text(strip=True)
    description = soup.find('div', class_='eds-text--left').get_text(strip=True)

    return {
        'Event Name': event_name,
        'Event Date(s)': event_date,
        'Location': location,
        'Description': description,
        'Key Speakers': "N/A",
        'Agenda/Schedule': "N/A",
        'Registration Details': "N/A",
        'Pricing': "N/A",
        'Categories': "N/A",
        'Audience Type': "N/A"
    }

def scrape_marketing_ai(soup):
    all_divs = soup.find('div', class_='hhs-rich-text')
    headings = [h.get_text() for h in all_divs.find_all('h1')]

    event_name, event_date, location = headings[0], headings[1], headings[2]

    key_speakers = [profile_card.find('div', class_='hhs-profile-content').find('h4').get_text(strip=True) for profile_card in soup.find_all('div', class_='hhs-profile-card')]

    description = soup.find('p').get_text()

    agenda_response = requests.get('https://www.marketingaiinstitute.com/events/marketing-artificial-intelligence-conference/agenda')
    agenda_soup = BeautifulSoup(agenda_response.content, 'html.parser')
    agenda = agenda_soup.find('h3').get_text()

    register = soup.find('a')['href']

    return {
        'Event Name': event_name,
        'Event Date(s)': event_date,
        'Location': location,
        'Description': description,
        'Key Speakers': ", ".join(key_speakers),
        'Agenda/Schedule': agenda,
        'Registration Details': register,
        'Pricing': "N/A",
        'Categories': "N/A",
        'Audience Type': "N/A"
    }

def scrape_saastr(soup):
    event_name = soup.find('div', class_='sqs-html-content').find('h1').get_text(strip=True)
    event_date, location = soup.find('div', class_='sqs-html-content').find('h4').get_text(strip=True).split('|')
    description = soup.find('div', class_='sqs-block html-block sqs-block-html').find('div', class_='sqs-block-content').find('div', class_='sqs-html-content').get_text(strip=True)

    speakers_list = soup.find('ul', class_='user-items-list-item-container user-items-list-simple').find_all('li')
    key_speakers = [speaker.find('div', class_='list-item-content').find('div').find('div').find('p').get_text().split(',')[0] for speaker in speakers_list]
    audience_type = [speaker.find('div', class_='list-item-content').find('div').find('div').find('p').get_text().split(',')[1] for speaker in speakers_list]
    register = soup.find('a')['href']

    return {
        'Event Name': event_name,
        'Event Date(s)': event_date.strip(),
        'Location': location.strip(),
        'Description': description,
        'Key Speakers': ", ".join(key_speakers),
        'Agenda/Schedule': "N/A",
        'Registration Details': register,
        'Pricing': "N/A",
        'Categories': "N/A",
        'Audience Type': ", ".join(audience_type)
    }

def scrape_event_data(url):
    soup = get_soup(url)
    if "b2bmarketingleaders" in url:
        return scrape_b2b_marketingleaders(soup)
    elif "joinpavilion" in url:
        return scrape_pavilion(soup)
    elif "marketingaiinstitute" in url:
        return scrape_marketing_ai(soup)
    elif "saastrannual" in url:
        return scrape_saastr(soup)
    elif "eventbrite" in url:
        return scrape_eventbrite(soup)


all_event_data = []

for url in event_urls:
    event_data = scrape_event_data(url)
    event_data['Website URL'] = url
    all_event_data.append(event_data)

# store the data to csv
csv_file = 'b2b_events.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=all_event_data[0].keys())
    writer.writeheader()
    writer.writerows(all_event_data)

print(f'Data saved to {csv_file}')

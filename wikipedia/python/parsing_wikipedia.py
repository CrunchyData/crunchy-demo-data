import bs4 as bs
import requests
import json
import sys

ONE_MINUTE = 60
urls_to_call = []


def custom_county_rules(the_response, url):
    county_info = {}

    if 'Denver' in url:
        county_info['full_name_list'] = ['Denver', 'Colorado']
        county_info['json_content'] = the_response.json()
        county_info['keystore'] = the_response.headers
        print('handled the exception')
    elif 'Baltimore' in url:
        county_info['full_name_list'] = ['Baltimore', 'Maryland']
        county_info['json_content'] = the_response.json()
        county_info['keystore'] = the_response.headers
        print('handled the exception')
    elif 'Brooklyn' in url:
        county_info['full_name_list'] = ['Brooklyn', 'New York']
        county_info['json_content'] = the_response.json()
        county_info['keystore'] = the_response.headers
        print('handled the exception')
    elif 'Queens' in url:
        county_info['full_name_list'] = ['Queens', 'New York']
        county_info['json_content'] = the_response.json()
        county_info['keystore'] = the_response.headers
        print('handled the exception')
    elif 'Guam' in url:
        print("Handled the exception by skipping guam")
    elif 'Saipan' in url:
        print("Handled the exception by skipping saipan")
    elif'Tinian' in url:
        print("Handled the exception by skipping Tinian")
    else:
        print("!!!!!!!NO IDEA WHAT DO WITH THAT ONE")

    return county_info


def get_county_json(url):
    wiki_json = requests.get(url)

    #Todo put in some exception catching here and see which one and why is throwing an error

    county_dict = {}
    try:
        county_dict['full_name_list'] = wiki_json.json()['query']['normalized'][0]['to'].split(',')
        county_dict['json_content'] = wiki_json.json()
        county_dict['keystore'] = wiki_json.headers
    except:
        print("we threw an exception: " + str(sys.exc_info()[0]) + " || on this page: " + url)

        ### Started with Denver being non standard but we shall see where we end up
        county_dict = custom_county_rules(wiki_json, url)


    return county_dict

def sql_string(county_dict):
    sql_statement = ''
    try:
        # using ^ as a delimeter because there are both " and ' used in the body of the text.
        # ESCAPE
        # Specifies the character that should appear before a data character that matches the QUOTE value. The default
        # is the same as the QUOTE value (so that the quoting character is doubled if it appears in the data). This must
        # be a single one-byte character. This option is allowed only when using CSV format.

        json_string = json.dumps(county_dict['json_content']).replace('^', '^^')

        sql_statement = sql_statement + '^' + county_dict['full_name_list'][0] + '^,^' + county_dict['full_name_list'][1] + '^,'
        sql_statement = sql_statement + '^' + json_string + '^,^'

        response_headers = county_dict['keystore']
        hstore_string = ''
        for key, value in response_headers.items():
            # need to escape out all " and ' inside of the keys or values
            hstore_string = hstore_string + '"' + key + '"=>"' + value.replace('"', '\\\"').replace("'", "\\\'") + '",'
        hstore_string = hstore_string[:-1]

        sql_statement = sql_statement + hstore_string + "^\n"
    except:
        print("we threw an exception: " + str(sys.exc_info()[0]) + " || on this dictionary" + str(county_dict))
    return sql_statement

if __name__ == '__main__':

    county_html = requests.get('https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county_equivalents')
    soup = bs.BeautifulSoup(county_html.text,'html.parser')
    table = soup.find('table', class_='wikitable')
    table_body = table.find('tbody')

    table_rows = table_body.find_all('tr')

    print('Processing the county page to extract URLs endings')

    # Need to skip the first tr row because it contains the column headers
    index = 1
    for tr in table_rows:
        if index == 1:
            index = index + 1
        else:
            tag_we_want = tr.contents[1].a.get('href')
            #everything we need is here and all we are doing is making the URL to call later
            position_to_start = tag_we_want.find('wiki/')
            just_string = tag_we_want[position_to_start + 5:]
            urls_to_call.append(just_string)
    print("Done getting the information for URLs")

    print("Now getting all the JSON and making the output file")

    front_url = 'https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&formatversion=2&titles='

    data_array = []

    # gather all the individual pages
    i = 0
    for county_name in urls_to_call:
        data_array.append(get_county_json(front_url + county_name))
        if ((i % 100) == 0):
            print("Just finished: " + str(i))
        i = i + 1

    print("Finished with the requests now making the CSV file")
    i = 0
    with open('../output/wikipedia_copy.txt', 'w') as write_file:
        for county_dict in data_array:

            # Empty dictionaries were put in for counties (such as Guam) we are skipping
            if any(county_dict):
                to_write = sql_string(county_dict)
                write_file.write(to_write)
            if ((i % 100) == 0):
                print("Just finished: " + str(i))
            i = i + 1

    print("done")



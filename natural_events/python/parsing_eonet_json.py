import json

#####  Set this to True to make spatial columns in the data
make_geo = False

if __name__ == '__main__':
    # read a line from the file
    with open('../events.json', 'r' ) as json_file:
        with open('../output/natural_events.csv', 'w') as outfile:
            data = json.load(json_file)
            if make_geo:
               print("We haven't done the geo piece yet")
            else:
                for event in data['events']:
                    outfile.write('"' + event['id'] + '"|' + json.dumps(event) + '\n')
        print("Done")
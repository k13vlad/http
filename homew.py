import requests
import csv


DevTestConsumption = []
Consumption = []
regions = []
minimal = 0
maximum = 0
avg = 0
difference = []


print('Getting list of regions\n')

rr = requests.get("https://prices.azure.com/api/retail/prices")

data1 = rr.json()
get_items = data1['Items']

for x in get_items:
    regions.append(x['armRegionName'])

print('Just got list of regions\nSorting will take some time')


for location in regions:
    ask = requests.get("https://prices.azure.com/api/retail/prices?$filter=armRegionName eq '{}' and productName eq 'Virtual Machines FS Series Windows' and skuName eq 'F4s Low Priority'".format(location))
    data = ask.json()
    list_of_data = data['Items']

    for x in list_of_data:
        a = x['type']
        if 'DevTestConsumption' in a:
            DevTestConsumption.append(x['retailPrice'])
        else:
            Consumption.append(x['retailPrice'])

print('Sorting finished\nWriting to a file')

difference = list()
for item1, item2 in zip(Consumption, DevTestConsumption):
    difference.append(item1-item2)


minimal = min(difference)
maximum = max(difference)
avg = sum(difference)/len(difference)


with open('file_with_data.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(regions, difference))
f.close()

f = open('file_with_data.csv', "a")
f.write('Minimal value is: {}\nmaximal value is: {}\nthe average is: {}'.format(minimal, maximum, avg))
f.close()

print('Done')
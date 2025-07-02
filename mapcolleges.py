import json
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline

# Load data
with open('schools.geojson') as f:
    geo_data = json.load(f)
with open('univ.json') as f:
    univ_data = json.load(f)

big12 = []
for school in univ_data:
    if school['NCAA']['NAIA conference number football (IC2020)'] == 108:
        big12.append(school)

with open('big12_schools.json', 'w') as outfile:
    json.dump(big12, outfile, indent=4)

lons, lats, texts,  = [], [], []

for school in big12:
    for feature in geo_data['features']:
        if feature['properties']['NAME'] == school['instnm']:
            lon = school['Longitude location of institution (HD2020)']
            lat = school['Latitude location of institution (HD2020)']
            name = school['instnm']
            enrollment = school['Total enrollment (DRVEF2020)']
            address = (
                feature['properties']['street'] + ', ' +
                feature['properties']['city'] + ', ' +
                feature['properties']['state'] + ' ' +
                feature['properties']['zip']
            )
            male = school.get('male_enrollment', 'N/A')
            female = school.get('Percent of total enrollment that are women (DRVEF2020)', 'N/A')
            text = (
                f"{name} {address} "
                f"Total Enrollment: {enrollment} "
                f"Male: {male} "
                f"Female: {female}"
            )
            lons.append(lon)
            lats.append(lat)
            texts.append(text)
            
    


data = [{
    'type': 'scattergeo',
    'lon': lons,
    'lat': lats,
    'text': texts,
    'marker': {
        'size': [school['Total enrollment (DRVEF2020)'] for school in big12],
        'color': [school['Total enrollment (DRVEF2020)'] for school in big12],
        'colorscale': 'Viridis',
        'reversescale': True,
        'colorbar': {'title': 'Enrollment'},
        'line': {'width': 0.5, 'color': 'black'}
    }
}]

layout = Layout(title='Big 12 Universities (Enrollment)')
offline.plot({'data': data, 'layout': layout}, filename='big12_universities.html')

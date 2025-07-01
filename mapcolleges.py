import json
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline

with open('schools.geojson') as f:
    geo_data = json.load(f)
with open('univ.json') as f:
    univ_data = json.load(f)

big12 = [s for s in geo_data['features'] if s['properties'].get('NCAA') == 108]

lons, lats, texts, sizes, colors = [], [], [], [], []

for school in big12:
    props = school['properties']
    name = props['INSTNM']
    coords = school['geometry']['coordinates']
    lon, lat = coords

    match = next((u for u in univ_data if u['name'].strip() == name.strip()), None)
    if match:
        enrollment = match.get('total_enrollment', 0)
        lons.append(lon)
        lats.append(lat)
        texts.append(f"{name}<br>{enrollment:,} students")
        sizes.append(enrollment / 1500)
        colors.append(enrollment)

# Plot it
data = [Scattergeo(
    lon=lons,
    lat=lats,
    text=texts,
    marker=dict(
        size=sizes,
        color=colors,
        colorscale='Viridis',
        colorbar=dict(title='Enrollment'),
        line=dict(width=0.5, color='black')
    )
)]

layout = Layout(title='Big 12 Universities (Enrollment)', geo=dict(scope='usa', showland=True))
offline.plot({'data': data, 'layout': layout}, filename='big12_universities.html')

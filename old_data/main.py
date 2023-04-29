import earthaccess

auth = earthaccess.login()

results = earthaccess.search_data(
    short_name='ATL06',
    version="005",
    cloud_hosted=True,
    bounding_box=(-10, 20, 10, 50),
    temporal=("2020-02", "2020-03"),
    count=100
)

print(results)
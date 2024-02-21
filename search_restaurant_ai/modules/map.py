import folium
import requests
from streamlit_folium import st_folium


def get_coordinates_osm(place_name: str) -> tuple[float, float] | tuple[None, None]:
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place_name,
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if response.status_code == 200 and data:
        # 最初の結果を使用する
        location = data[0]
        lat = location["lat"]
        lon = location["lon"]
        return float(lat), float(lon)
    else:
        return None, None


def show_map(names: list[str], zoom_start=18, width=725) -> None:
    lat_lng: list[tuple[float, float] | tuple[None, None]] = [get_coordinates_osm(name) for name in names]
    lat_center = sum([lat for lat, _ in lat_lng if lat is not None]) / len([lat for lat, _ in lat_lng if lat is not None])
    lng_center = sum([lng for _, lng in lat_lng if lng is not None]) / len([lng for _, lng in lat_lng if lng is not None])
    m = folium.Map(location=[lat_center, lng_center], zoom_start=zoom_start)
    for (lat, lng), name in zip(lat_lng, names):
        if lat is not None and lng is not None:
            folium.Marker([lat, lng], popup=name).add_to(m)
    st_folium(m, width=width)

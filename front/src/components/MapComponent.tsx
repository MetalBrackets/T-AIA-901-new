import { onMount } from 'solid-js';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const MapComponent = () => {
  let mapContainer: HTMLDivElement | undefined;

  onMount(() => {
    const map = L.map(mapContainer!).setView([51.505, -0.09], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    const geoJsonData: GeoJSON.FeatureCollection = {
      type: "FeatureCollection",
      features: [
        {
          type: "Feature",
          properties: { name: "Location A" },
          geometry: {
            type: "Point",
            coordinates: [-0.09, 51.505]
          }
        }
      ]
    };

    L.geoJSON(geoJsonData).addTo(map);
  });

  return <div ref={mapContainer} style={{ height: '500px' }}></div>;
};

export default MapComponent;

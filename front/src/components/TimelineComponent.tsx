import { createSignal, onMount } from "solid-js";
import "../styles/style.css";

const timelineComponent = () => {
  const [stops, setStops] = createSignal([]);
  const [duration, setDuration] = createSignal<number | undefined>(undefined);

  const formatDuration = (minutes) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}min`;
  };
  
  
  onMount(async () => {

    const data = JSON.parse(localStorage.getItem("path"));
    const formattedStops = data.map((station, index) => {
      // Condition pour définir les détails
      if (index === 0) {
        return {
          station,
          details: `Départ`,
        };
      } else if (index === data.length - 1) {
        return {
          station,
          details: `Arrivée`,
        };
      } else {
        // Compter les arrêts intermédiaires à partir de la première gare intermédiaire
        const intermediateIndex = index; // Compte chaque gare intermédiaire
        return {
          station,
          details: `Arrêt ${intermediateIndex}`,
        };
      }
    });

    setDuration(localStorage.getItem("duration"));
    setStops(formattedStops);
  });
  return (
    <div class="w-full p-5 bg-danger">
      <div class="flex mb-6 justify-between border-b-4 border-b-gray-300">
        <h1 class="text-center font-bold text-xl">Votre itinéraire de voyage</h1>
        <h2 class="text-xl font-semibold">Temps : {duration() ? formatDuration(duration()) : "Calcul en cours..."}</h2>
      </div>
      <div class="timeline-container">
        {stops().map((stop, index) => (
          <div class="timeline-item" key={index}>
            <div class="timeline-content">
              <h3 class="font-bold">{stop.station}</h3>
              <p>{stop.details}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default timelineComponent;

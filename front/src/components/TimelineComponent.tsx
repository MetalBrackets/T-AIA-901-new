import {createSignal, onMount} from "solid-js";
import "../styles/style.css"



const timelineComponent = () => {
    const [stops, setStops] = createSignal([]);
    const [duration, setDuration] = createSignal<number | undefined>(undefined);

    onMount(async () => {
        const response = await fetch("/api/v1/shortest-path");
        const data = await response.json()
        const formattedStops = data.path.map((station, index) => {
      // Condition pour définir les détails
        if (index === 0) {
            return {
            station,
            details: `Départ`,
        };
        } else if (index === data.path.length - 1) {
            return {
            station,
            details: `Arrivée`,
        };
        } else {
            // Compter les arrêts intermédiaires à partir de la première gare intermédiaire
            const intermediateIndex = index; // Compte chaque gare intermédiaire
            return {
            station,
            details: `Arrêt ${intermediateIndex}`, // Affiche le numéro de l'arrêt
            };
        }
        });

        setDuration(data.distance)
        setStops(formattedStops);

    })
    return (
        <div class="w-full p-5 bg-danger">
            <div class="flex mb-6 justify-between border-b-4 border-b-gray-300">
                <h1 class="text-center uppercase font-bold text-xl">Votre itinéraire de voyage</h1>
                <h2 class="text-xl text-capitalize font-semibold text-green-600">Temps : {duration()} minutes</h2>
            </div>
            <div class="timeline-container">
                {stops().map((stop, index) => (
                    <div class="timeline-item" key={index}>
                    <div class="timeline-content p-5 my-10">
                            <h3 class="font-bold">{stop.station}</h3>
                            <p>{stop.details}</p>
                        </div>
                    </div>
                ))}
            </div>

        </div>
    )
};


export default timelineComponent;
import {createSignal, onMount} from "solid-js";

const DisplayMap = () => {
    const [mapUrl, setMapUrl] = createSignal("");

    onMount(() =>{
        fetch("/api/v1/travel")
            .then((response) => {
                if(response.ok){
                    return response.text();
                }else {
                    console.error("Erreur lors de la récupération de la carte.")
                }
            })
            .then((htmlContent) => {
                const blob = new Blob([htmlContent], { type: "text/html"})
                const url = URL.createObjectURL(blob);
                setMapUrl(url)
            })
            .catch((error) => console.error("Error", error))
    })
    return (
        <div class="max-w-xxl p-4 bg-white border border-gray-200 m-5 ounded-lg shadow ">
            {mapUrl() ? (
                <iframe src={mapUrl()} width="100%" height="500px"/>
            ) : (
                <p>Chargement de la carte...</p>
            )}
        </div>
    )
}

export default DisplayMap;
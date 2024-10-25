import {createSignal} from "solid-js";


const ItineraryInput = () => {
    const [departure, setDeparture] = createSignal("")
    const [arrival, setArrival] = createSignal("")
    const handleSubmit = async (e: Event) => {
        e.preventDefault();
    }
    return (
    <div class="p-4 m-5">
        <form class="w-full">
            <div class="flex flex-wrap mb-6">
                <div class="w-full md:w-1/2 mb-6 md:mb-0 pr-2">
                    <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2">
                        Départ
                    </label>
                    <input
                        class="appearance-none block w-full bg-gray-200 text-gray-700 border rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"
                        id="departure" type="text" value={departure()} onInput={setDeparture(e.target.value)} placeholder="Départ"/>
                    {/*<p class="text-red-500 text-xs italic">Please fill out this field.</p>*/}
                </div>
                <div class="w-full md:w-1/2 pr-2">
                    <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2">
                        Arrivée
                    </label>
                    <input
                        class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                        id="destination" type="text" value={arrival()} onInput={setArrival(e.target.value)} placeholder="Destination"/>
                </div>
            </div>
        </form>
    </div>
    )
}
export default ItineraryInput;
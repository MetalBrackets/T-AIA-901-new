import { createSignal } from "solid-js";

function SpeechToText() {
  const [transcriptionStart, setTranscriptionStart] = createSignal("");
  const [transcriptionEnd, setTranscriptionEnd] = createSignal("");

  let mediaRecorder: MediaRecorder;
  let audioChunks: BlobPart[] | undefined = [];


  const path_finder = () => {

  }

  const startRecording = () => {
    audioChunks = [];
    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
      mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
      mediaRecorder.start();

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        const formData = new FormData();
        formData.append("audio", audioBlob, "audio.webm");

        // @ts-ignore
        fetch("/api/v1/travel", {
          method: "POST",
          body: formData,
        })
          .then((response) =>
            //response.text())
            response.json()
          )
          .then((data) => {
            console.log("La réponse du serveur:", data);
            //const transcription = data.text
            //console.log(transcription)
            setTranscriptionStart(data.result.Departure);
            setTranscriptionEnd(data.result.Destination);
          })
          .catch((error) => console.error("Error:", error));
      };
    });
  };

  const stopRecording = () => {
    mediaRecorder.stop();
  };

  return (
    <>
      <div class="flex justify-around p-4 m-5">
        <div>
          {" "}
          <label>Départ :</label>
          <input
            type="text"
            class="bg-blue-100 w-full rounded-lg shadow capitalize px-2 mr-2"
            value={transcriptionStart() || ""}
            placeholder="Départ"
            onInput={(e) => setTranscriptionStart(e.target.value)} // Permettre de modifier la transcription
          />
        </div>
        <div>
          {" "}
          <label>Arrivée :</label>
          <input
            type="text"
            class="bg-blue-100 w-full rounded-lg shadow capitalize px-2 mr-2"
            value={transcriptionEnd() || ""}
            placeholder="Arrivée"
            onInput={(e) => setTranscriptionEnd(e.target.value)} // Permettre de modifier la transcription
          />
        </div>
        <div>
          <button
            class="text-green-700 hover:text-white border
                border-green-700 hover:bg-green-800
                focus:ring-4 focus:outline-none focus:ring-green-300
                font-medium rounded-lg text-sm px-5 py-2.5 text-center
                me-2 mb-2 dark:border-green-500 dark:text-green-500 dark:hover:text-white
                dark:hover:bg-green-600 dark:focus:ring-green-800"
            onClick={startRecording}
          >
            <svg enable-background="new 0 0 141.732 141.732" height="20px" id="Livello_1" version="1.1" viewBox="0 0 141.732 141.732" width="20px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
              <g id="Livello_7">
                <path
                  d="M91.192,59.623V21.946c0.043-0.534,0.068-1.073,0.068-1.618C91.262,9.102,82.161,0,70.935,0
                    c-11.229,0-20.33,9.104-20.33,20.328c0,0.545,0.024,1.084,0.066,1.618v37.677c-0.042,0.535-0.066,1.073-0.066,1.621
                    c0,11.229,9.103,20.326,20.329,20.326c11.227,0,20.327-9.1,20.327-20.326C91.262,60.696,91.235,60.158,91.192,59.623    M120.942,50.219c0-3.084-2.5-5.584-5.584-5.584c-3.082,0-5.582,2.5-5.582,5.584c0,0.047,0.004,0.092,0.008,0.139   c-0.076,21.43-17.471,38.779-38.917,38.779c-21.448,0-38.842-17.353-38.917-38.779c0.002-0.047,0.008-0.092,0.008-0.139   c0-3.084-2.5-5.584-5.584-5.584s-5.585,2.5-5.585,5.584c0,25.714,19.388,46.896,44.339,49.743v28.648H38.78   c-2.96,0-5.358,2.402-5.358,5.361c0,2.961,2.398,5.355,5.358,5.355h26.35h11.61h26.35c2.959,0,5.357-2.396,5.357-5.355   c0-2.959-2.398-5.361-5.357-5.361h-26.35V99.945C101.628,97.039,120.942,75.885,120.942,50.219"
                />
              </g>
              <g id="Livello_1_1_" />
            </svg>
          </button>
        </div>
        <div>
          {" "}
          <button
            class="text-red-700 hover:text-white border
                border-red-700 hover:bg-red-800
                focus:ring-4 focus:outline-none focus:ring-red-300 font-medium
                rounded-lg text-sm px-5 py-2.5 text-center
                me-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white
                dark:hover:bg-red-600 dark:focus:ring-red-900"
            onClick={stopRecording}
          >
            Stop
          </button>
        </div>
      </div>

      
    </>
  );
}

export default SpeechToText;
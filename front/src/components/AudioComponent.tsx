import { createSignal } from "solid-js";
import styles from "../App.module.css";
import TimelineComponent from "./TimelineComponent";
function SpeechToText() {
  const [isRecording, setIsRecording] = createSignal(false);
  const [errorMessage, setErrorMessage] = createSignal("");


  let mediaRecorder: MediaRecorder;
  let audioChunks: BlobPart[] | undefined = [];

  const path_finder = () => {};
  const startRecording = () => {
    audioChunks = [];
    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
      mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
      mediaRecorder.start();
      setIsRecording(true);
      setErrorMessage("");

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        const formData = new FormData();
        console.log("Audio: ", audioBlob)
        formData.append("audio", audioBlob, "audio.webm");

        fetch("/api/v1/travel", {
          method: "POST",
          body: formData,
        })
          .then((response) => {
            console.log('Rep: ', response)
            if (!response.ok) {
              throw new Error("Je n'ai pas compris, pouvez-vous répéter votre demande ?");
            }
            return response.json();
          })
          .then((data) => {
            console.log("La réponse du serveur:", data);
            localStorage.setItem("end", data.end);
            localStorage.setItem("start", data.start);
            localStorage.setItem("duration", data.distance);
            localStorage.setItem("path", JSON.stringify(data.path));
            window.location.reload();
          })
          .catch((error) => {
            setErrorMessage("Error: " + error.message);
            console.error("Error:", error);
          });
      };
    });
  };

  const stopRecording = () => {
    mediaRecorder.stop();
    setIsRecording(false);
  };

  return (
    <>
    <div class="flex flex-col items-center">
      <div class="mt-3">
        {isRecording() ? (
          <button
            class="bg-red-400 hover:bg-red-500 text-white border-white border-4 rounded-full w-12 h-12 flex items-center justify-center"
            onClick={stopRecording}
          >
            <svg viewBox="0 0 100 100" fill="white" xmlns="http://www.w3.org/2000/svg">
              <rect width="40" height="40" x="30" y="30" />
            </svg>
          </button>
        ) : (
          <button
            class="bg-lime-500 hover:bg-lime-600 text-white border-white border-4 rounded-full w-12 h-12 flex items-center justify-center"
            onClick={startRecording}
          >
            <svg height="20px" viewBox="0 0 141.732 141.732" width="20px">
              <path
                fill="white"
                d="M91.192,59.623V21.946c0.043-0.534,0.068-1.073,0.068-1.618C91.262,9.102,82.161,0,70.935,0 c-11.229,0-20.33,9.104-20.33,20.328c0,0.545,0.024,1.084,0.066,1.618v37.677c-0.042,0.535-0.066,1.073-0.066,1.621 c0,11.229,9.103,20.326,20.329,20.326c11.227,0,20.327-9.1,20.327-20.326C91.262,60.696,91.235,60.158,91.192,59.623 M120.942,50.219c0-3.084-2.5-5.584-5.584-5.584c-3.082,0-5.582,2.5-5.582,5.584c0,0.047,0.004,0.092,0.008,0.139 c-0.076,21.43-17.471,38.779-38.917,38.779c-21.448,0-38.842-17.353-38.917-38.779c0.002-0.047,0.008-0.092,0.008-0.139 c0-3.084-2.5-5.584-5.584-5.584s-5.585,2.5-5.585,5.584c0,25.714,19.388,46.896,44.339,49.743v28.648H38.78 c-2.96,0-5.358,2.402-5.358,5.361c0,2.961,2.398,5.355,5.358,5.355h26.35h11.61h26.35c2.959,0,5.357-2.396,5.357-5.355 c0-2.959-2.398-5.361-5.357-5.361h-26.35V99.945C101.628,97.039,120.942,75.885,120.942,50.219"
              />
            </svg>
          </button>
        )}
      </div>
      <p class="text-lg mt-5">Départ : {localStorage.getItem("start") || "Non spécifié"}</p>
      <p class="text-lg">Arrivée : {localStorage.getItem("end") || "Non spécifié"}</p>
      {errorMessage() && <div class="error-message mt-5">{errorMessage()}</div>}
     
    </div>  
      
    </>
  );
}

export default SpeechToText;

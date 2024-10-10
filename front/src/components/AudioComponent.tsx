import { createSignal } from "solid-js";


function SpeechToText() {
  const [transcription, setTranscription] = createSignal("");
  let mediaRecorder: MediaRecorder;
  let audioChunks: BlobPart[] | undefined = [];


  const startRecording = () => {
    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
      mediaRecorder = new MediaRecorder(stream, {mimeType: "audio/webm"});
      mediaRecorder.start();

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        const formData = new FormData();
        formData.append("audio", audioBlob, "audio.webm");

        // @ts-ignore
        fetch("/api/v1/audio", {
          method: "POST",
          body: formData,
        })
          .then((response) =>
              //response.text())
              response.json())
          .then((data) => {
            console.log("La réponse du serveur:", data)
            const transcription = data.text
            console.log(transcription)
            setTranscription(transcription)
            })
          .catch((error) => console.error("Error:", error));
        };
    });
  };

  const stopRecording = () => {
    mediaRecorder.stop();
  };

  return (
    <div>
      <button onClick={startRecording}>Start Recording</button>
      <button onClick={stopRecording}>Stop Recording</button>
      <p>Transcription: {transcription()}</p>
    </div>

  );
}

export default SpeechToText;

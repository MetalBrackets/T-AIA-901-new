


const RecordComponent = () => {

    navigator.mediaDevices.getUserMedia({ audio: true })

    const record = () => {
        console.log("Recording")

        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                const mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();

                const audioChunks: any[] = [];

                mediaRecorder.addEventListener("dataavailable", (event) => {
                    audioChunks.push(event.data);
                });

                mediaRecorder.addEventListener("stop", () => {
                    const audioBlob = new Blob(audioChunks);
                    const audioUrl = URL.createObjectURL(audioBlob);
                    const audio = new Audio(audioUrl);
                    audio.play();
                    saveAudio(audioBlob);
                });

                setTimeout(() => {
                    mediaRecorder.stop();
                }, 3000);
            });
    }
    const saveAudio = (audioBlob: Blob) => {
        const link = document.createElement('a');
        link.href = URL.createObjectURL(audioBlob);
        link.download = 'recording.wav';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };
    return (
        <div>
            <h1>Record</h1>
            <button onClick={record}>Record</button>

        </div>
    )
}

export default RecordComponent;

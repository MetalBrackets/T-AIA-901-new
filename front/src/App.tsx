import type { Component } from "solid-js";
import styles from "./App.module.css";
import AudioComponent from "./components/AudioComponent";
import TimelineComponent from "./components/TimelineComponent";

const error = localStorage.getItem("error"); 


const App: Component = () => {
  return (
    <div class={styles.page}>
      <div class={styles.header}>
        <div class={styles.containerCenter}>
          <h1 class="text-4xl font-bold">Réserver un train</h1>
        </div>
        <div class={styles.containerCenter}>
          <div>
          <AudioComponent />  
          </div>
          <div class="error-message">
            <p class="text-red-500">{error}</p>
          </div>
        </div>
      </div>
      {localStorage.getItem('path') && (
        <div class={styles.containerCenter}>
          <TimelineComponent />
        </div>
      )}
    </div>
  );
};

export default App;

import type { Component } from 'solid-js';

import logo from './logo.svg';
import styles from './App.module.css';
import MapComponent from './components/MapComponent';
import RecordComponent from './components/RecordComponent';
import AudioComponent from "./components/AudioComponent";
import DisplayMap from "./components/DisplayMap";
import ItineraryInputComponent from "./components/ItineraryInputComponent";
import TimelineComponent from "./components/TimelineComponent";

const App: Component = () => {
  return (
    <div>
      {/*<RecordComponent />*/}
        <div class="flex justify-center my-5">
            <h1 class="text-4xl font-bold text-red-950">Train travel</h1>
        </div>
        <AudioComponent/>
        {/*<ItineraryInputComponent/>*/}
        <TimelineComponent/>
        <DisplayMap/>
        {/*<MapComponent/>*/}
    </div>
     
  );
};

export default App;

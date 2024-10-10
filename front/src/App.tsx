import type { Component } from 'solid-js';

import logo from './logo.svg';
import styles from './App.module.css';
import MapComponent from './components/MapComponent';
import RecordComponent from './components/RecordComponent';
import AudioComponent from "./components/AudioComponent";

const App: Component = () => {
  return (
    <div>
      {/*<RecordComponent />*/}
        <AudioComponent/>
      <MapComponent/>
    </div>
     
  );
};

export default App;

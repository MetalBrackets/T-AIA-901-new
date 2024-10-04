import type { Component } from 'solid-js';

import logo from './logo.svg';
import styles from './App.module.css';
import MapComponent from './components/MapComponent';
import RecordComponent from './components/RecordComponent';

const App: Component = () => {
  return (
    <div>
      <RecordComponent />
      <MapComponent/>
    </div>
     
  );
};

export default App;

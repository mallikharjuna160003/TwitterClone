import React from 'react';
import { TweetsComponent } from "./tweets";
import './App.css';


function App() {
  const className ='col-10 mx-auto mt-4 col-md-6'

  return (
    <div className="App">
     <TweetsComponent className={className} />
    </div>
  );
}

export default App;

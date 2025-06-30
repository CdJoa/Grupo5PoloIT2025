import React from 'react';  
import '../index.css'
import App from '../App.jsx';
import '../styles/Main.css';
import CarruselDestacados from '../components/CarruselDestacados';
import { useRef, useEffect } from "react";

function Main() {  
  const videoRef = useRef(null);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.playbackRate = 0.4; // mitad de velocidad
    }
  }, []);

    return (  
        <main className="main-container">
      <video
        ref={videoRef}
        src="/videos/cat&dog.mp4"
        autoPlay
        loop
        muted
        playsInline
        className="main-video"
      ></video>

      <h2>Nuestras mascotas</h2>
      <CarruselDestacados />
      
    </main>  
    );  
}  
export default Main;  
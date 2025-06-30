import React from 'react';
import '../styles/About.css';
import Header from './Header';
import Footer from './Footer';
import petmatchImg from '/imgs/header-bg01.jpg'; 

function About() {
  return (
    <>
      
      <main className="about-container">
        <img src={petmatchImg} alt="PetMatch" className="about-banner" />
        <section className="about-content">
          <h1>Sobre Nosotros</h1>
          <p>
            PetMatch es un espacio creado para conectar corazones. Nuestro objetivo es facilitar la adopción responsable de perros y gatos, brindando un lugar seguro y accesible tanto para quienes buscan darle un hogar a un animal como para quienes necesitan encontrar una nueva familia para su mascota. 
          </p>
          <p>
            Creemos en las segundas oportunidades y en el amor incondicional que solo una mascota puede dar.
          </p>
        </section>
      </main>
      <Footer/>
    </>
  );
}

export default About;
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "../styles/Pets.css";
import Card from "./Card";
import Footer from './Footer';

function PetsContainer() {
  const [pets, setPets] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log("Disparo fetch SOLO UNA VEZ");
    fetch("http://127.0.0.1:8000/api/pets/", {
      method: "GET",
      credentials: "include",
    })
      .then((respuesta) => respuesta.json())
      .then((datos) => {
        console.log("Mascotas recibidas:", datos);
        setPets(datos);
        setCargando(false);
      })
      .catch((error) => {
        console.log("Error", error);
        setError("Hubo un error al cargar las mascotas");
        setCargando(false);
      });
  }, []); // <-- array vacío para evitar bucles

  if (cargando) return <p>Cargando...</p>;
  if (error) return <p>{error}</p>;
  if (pets.length === 0) return <p>No hay mascotas para mostrar.</p>;

  return (
    <>
      <div className="pets-container">
        {pets.map((pet) => (
          <Card key={pet.id} pet={pet} />
        ))}
      </div>
      <Footer />
    </>
  );
}

export default PetsContainer;
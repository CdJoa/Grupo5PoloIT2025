import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "../styles/CarruselDestacados.css";

export default function CarruselDestacados() {
  const [pets, setPets] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/pets/")
      .then(res => res.json())
      .then(data => {
        console.log("Pets:", data);
        setPets(data);
      })
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="carrusel-imagenes">
      {pets.map(pet => (
        <Link key={pet.id} to={`/pets01/${pet.id}`}>
          <img
            src={
              pet.imagen && pet.imagen !== ""
                ? pet.imagen
                : "https://via.placeholder.com/150"
            }
            alt={`Pet ${pet.nombre}`}
            className="imagen-carrusel"
          />
        </Link>
      ))}
    </div>
  );
}
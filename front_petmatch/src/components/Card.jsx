import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "../styles/Pets.css";

function Card({ pet }) {
  return (
    <div className="pet-card">
      <Link to={`/pets01/${pet.id}`}>
        <img
          src={pet.imagen ? pet.imagen : "/images/placeholder.png"}
          alt={pet.nombre}
        />
      </Link>
      <h3 className="pet-nombre">{pet.nombre}</h3>
      <p>{pet.descripcion}</p>
      <Link to={`/pets01/${pet.id}`}>
        <button className="pet-button">Ver Mascota</button>
      </Link>
    </div>
  );
}

export default Card;
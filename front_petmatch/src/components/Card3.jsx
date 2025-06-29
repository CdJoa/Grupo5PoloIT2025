import { useState } from "react"
import "../styles/Pets.css"
import { dispararSweetBasico } from "../assets/SweetAlert";
import { Link, Navigate } from "react-router-dom";

function Card({ pet }) {
  return (
    <div className="pet-card">
      <Link to={"/pets01/" + pet.id}>
        <img className="pet-image" src={pet.imagen} alt={pet.nombre} />
      </Link>

      <h2 className="pet-nombre">{pet.nombre}</h2>

      <Link to={"/pets01/" + pet.id}>
        <button className="pet-button">Ver Mascota</button>
      </Link>
    </div>
  );
}

export default Card;
import { useState } from "react"
import "../styles/Pets.css"
import { dispararSweetBasico } from "../assets/SweetAlert";
import { Link, Navigate } from "react-router-dom";

function Card({pet }){
    function navegar(){
        const ruta= "/pets01/" + pet.id
        return <Navigate to={ruta} replace />
       } 
        
 

    return(
        <div className="pet-card">
            <Link to={"/pets01/"+ pet.id}><img className="pet-image" src={pet.imagen}></img></Link>

            <h2 className="pet-nombre">{pet.name}</h2>

            <div className="pet-precio">
                <span>{pet.price} $</span>
            </div>

            <Link to={"/pets01/" + pet.id}>
                <button className="pet-button">Ver Mascota</button>
            </Link>
        </div>
    )
}

export default Card
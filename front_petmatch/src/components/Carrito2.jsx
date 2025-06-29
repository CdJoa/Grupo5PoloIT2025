import "../styles/Carrito.css"
import { useEffect, useState } from "react";
import CarritoCard from "./CarritoCard.jsx";
import { Navigate } from "react-router-dom";

export default function Carrito({petsCarrito, funcionBorrar, usuarioLogeado }) {

    const total = petsCarrito.reduce(
        (subTotal, pet) => subTotal + pet.price * pet.cantidad, 0
    )

    function funcionDisparadora(id){
        funcionBorrar(id)
    }

    console.log("Total: " + total)

    if(!usuarioLogeado){
        return(
            <Navigate to="/login" replace/>
        )
    }

    return(
        <div className="carrito-container">
            <div className="carrito-titulos" >
                <h2 className="carrito-titulo-pet"> Producto </h2>
                <h2 className="carrito-titulo-descrip">Descripción</h2>
                <h2>  </h2>
                <h2> Cantidad </h2>
                <h2> Precio unitario </h2>
                <h2> Sub total </h2>
                <h2>  </h2>
            </div>
            {petsCarrito.length > 0 ? petsCarrito.map((pet) => (                
                <CarritoCard 
                    pet={pet} 
                    funcionDisparadora={funcionDisparadora}
                    />           
            ))
            : <p>Carrito vacio</p>}
            {total > 0 ?  <span>Total: {total.toFixed(2)} $</span> : <></> }
        </div>
    )
}
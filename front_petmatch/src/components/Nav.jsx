import { Link } from "react-router-dom";
import { FaFacebook, FaInstagram, FaTwitter, FaSearch, FaUser, FaHeart, FaUserShield } from "react-icons/fa";
import "../styles/Nav.css";
import { FaPaw } from "react-icons/fa";

function Nav({petsCarrito}) {  
    return (  
        <>
      {/* redes vacías -  buscador, login y admin en íconos  */}
      <div className="top-icons-bar">
        <div className="social-icons">
          <a href="#"><FaInstagram /></a>
          <a href="#"><FaTwitter /></a>
          <a href="#"><FaFacebook /></a>
        </div>
        <div className="action-icons">
          
          <Link to="/login"><FaUser /></Link>
          <Link to="/carrito" className={`carrito-icon ${petsCarrito.length > 0 ? "pulse" : ""}`}>
            <FaHeart />
            {petsCarrito.length > 0 && (
              <span className="carrito-count">{petsCarrito.length}</span>
            )}
          </Link>
          <Link to="/admin"><FaUserShield /></Link>
        </div>
      </div>

      {/* saqué el login y admin*/}
      <nav className="main-nav">
        <ul>
          <li><Link to="/">Inicio</Link></li>
          <li><Link to="/about">About</Link></li>
          <li><Link to="/pets01">Mascotas</Link></li>
          <li><Link to="/contacto">Contacto</Link></li>
          <li className="nav-adopcion">
            <Link to="/adopcion" className="nav-adopcion">
            <FaPaw className="adopcion-icon" />
            ¿Das en adopción?
            <FaPaw className="adopcion-icon" />
            </Link>
          </li>
        </ul>
      </nav>
    </>  
    );  
}  


export default Nav; 
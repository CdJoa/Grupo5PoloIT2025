import React from 'react';  
import { FaPhone, FaEnvelope, FaMapMarkerAlt } from "react-icons/fa";
import "../styles/Footer.css";

function Footer() {
  return (
    <footer className="footer">
  <div className="contacto-footer">
    
    <div className="footer-info-center">
      <p><FaEnvelope /> contacto@petmatch.ar</p>
    </div>
    
  </div>
  
  <p className="footer-copy">&copy; 2025 - PetMatch</p>
</footer>
  );
}

export default Footer;
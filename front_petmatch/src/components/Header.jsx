import React from 'react';  
import "../styles/Header.css";
import Logo from "/imgs/logo_petmatch.png";
import Nav from './Nav';

function Header() {  
    return (  
        <header className="header-container">
            
            <div className="logo">
                <img src={Logo} alt="Logo PetMatch" className="logo-img" />
            </div>
            
        </header>  
    );  
}  
export default Header;
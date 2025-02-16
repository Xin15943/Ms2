import React, {useState} from "react";

import { NavLink } from "react-router-dom";

import "./Navbar.css"

export const Navbar = () => {

    const [menuOpen, setMenuOpen] = useState(false)

    return <nav>
        <div className="menu" onClick={()=> setMenuOpen(!menuOpen) }>
            <span></span>
            <span></span>
            <span></span>

        </div>
        <ul className={menuOpen ? "open" : ""}>
            <li>
                <NavLink to="/" className="title">HOME</NavLink>
            </li>
            <li>
                <NavLink to="/film">FILM</NavLink>
            </li>
            <li>
                <NavLink to ="/customer">CUSTOMER</NavLink>
            </li>

        </ul>
    </nav>
        
    
}
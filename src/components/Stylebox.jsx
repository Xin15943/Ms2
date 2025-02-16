import React, { useState } from "react";

const StyledBox = ({ title, image, description }) => {
    const [showInfo, setShowInfo] = useState(false);

    const boxStyle = {
        border: "1px solid black",
        padding: "10px",
        width: "200px",
        height: "300px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "space-between",
        textAlign: "center",
        cursor: "pointer"
        
    };

    return (
        <div style={boxStyle} onClick={() => setShowInfo(!showInfo)}> 
            <img 
                src={image} 
                alt={title} 
                style={{ width: "100%", height: "150px", objectFit: "cover", borderRadius: "5px" }} 
            />
            <p><strong>{title}</strong></p>

            {showInfo && (
                <div style={{
                    marginTop: "-150px",
                    backgroundColor: "#f0f0f0",
                    padding: "5px",
                    borderRadius: "5px",
                    width: "90%",
                    textAlign: "center",
                    boxShadow: "0px 2px 5px rgba(0, 0, 0, 0.2)",
                    whiteSpace: "pre-line" 
                }}>
                    <p>{description}</p> 
                </div>
            )}
        </div>
    );
};

export default StyledBox;

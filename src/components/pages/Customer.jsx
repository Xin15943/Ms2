import React from "react";
import CustomerTable from "../CustomerTable";  // ✅ Ensure correct import
import "./Customer.css";  // ✅ Ensure Customer.css exists

const Customer = () => {
  return (
    <div className="customer-container">
      <h1>Customers</h1>
      <CustomerTable />
    </div>
  );
};

export default Customer;

import React, { useEffect, useState } from "react";
import "./CustomerTable.css";  

const CustomerTable = () => {
  const [customers, setCustomers] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");  
  const [currentPage, setCurrentPage] = useState(1);  
  const customersPerPage = 5;  

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/customers")  
      .then(response => response.json())
      .then(data => {
        console.log("Fetched customers:", data);
        if (Array.isArray(data)) {
          setCustomers(data);
        } else {
          console.error("API not correct:", data);
          setCustomers([]);  
        }
      })
      .catch(error => {
        console.error("Error fetching customers:", error);
        setCustomers([]);  
      });
  }, []);

  if (!Array.isArray(customers)) {
    console.error("customers not coreet:", customers);
    return <p> FILE API</p>;
  }

  
  const filteredCustomers = customers.filter(customer =>
    customer.customer_id?.toString().includes(searchQuery) ||  
    customer.first_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||   
    customer.last_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||   
    customer.email?.toLowerCase().includes(searchQuery.toLowerCase())
  );


  const totalPages = Math.ceil(filteredCustomers.length / customersPerPage);

 
  const startIndex = (currentPage - 1) * customersPerPage;
  const endIndex = startIndex + customersPerPage;
  const currentCustomers = filteredCustomers.slice(startIndex, endIndex);

 
  const goToPreviousPage = () => {
    setCurrentPage((prev) => Math.max(prev - 1, 1));  
  };

  const goToNextPage = () => {
    setCurrentPage((prev) => Math.min(prev + 1, totalPages));  
  };

  return (
    <div className="customer-table-container">
      <h2>CUSTOMER INFORMATION</h2>
      <input
        type="text"
        placeholder="Name to search..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        className="search-box"
      />
      <table className="customer-table">
        <thead>
          <tr>
            <th>Customer ID</th>
            <th>Store ID</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email</th>
            <th>Address ID</th>
            <th>Active</th>
            <th>Date Of Creation</th>
            <th>Last Update</th>
          </tr>
        </thead>
        <tbody>
          {currentCustomers.length > 0 ? (
            currentCustomers.map((customer, index) => (
              <tr key={index}>
                <td>{customer.customer_id}</td>
                <td>{customer.store_id}</td>
                <td>{customer.first_name}</td>
                <td>{customer.last_name}</td>
                <td>{customer.email}</td>
                <td>{customer.address_id}</td>
                <td>{customer.active === 1 ? "Yes" : "No"}</td>
                <td>{customer.create_date}</td>
                <td>{customer.last_update}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="9" className="no-results">Not found</td>
            </tr>
          )}
        </tbody>
      </table>

     
      <div className="pagination">
        <button onClick={goToPreviousPage} disabled={currentPage === 1}>Previous</button>
        <span>Page {currentPage}  / Total {totalPages} Page</span>
        <button onClick={goToNextPage} disabled={currentPage === totalPages}>Next</button>
      </div>
    </div>
  );
};

export default CustomerTable;

import React, { useEffect, useState } from "react";
import "./CustomerTable.css";

const CustomerTable = () => {
  const [customers, setCustomers] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");  
  const [currentPage, setCurrentPage] = useState(1);
  const customersPerPage = 5;
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [totalPages, setTotalPages] = useState(1);
  const [showForm, setShowForm] = useState(false);
  const [editingCustomer, setEditingCustomer] = useState(null); 
  const [rentalHistory, setRentalHistory] = useState([]);
  const [showRentalModal, setShowRentalModal] = useState(false);
  const [selectedCustomer, setSelectedCustomer] = useState(null);

  const [newCustomer, setNewCustomer] = useState({
    first_name: "",
    last_name: "",
    email: "",
    store_id: "",
    address_id: "",
    active: 1,
  });

  useEffect(() => {
    fetchCustomers();
  }, [currentPage, searchQuery]);

  // 🔥 Fetch Customers with Search & Pagination
  const fetchCustomers = () => {
    setLoading(true);
    fetch(`http://127.0.0.1:5000/api/customers?page=${currentPage}&size=${customersPerPage}&search=${searchQuery}`)
      .then(response => response.json())
      .then(data => {
        setCustomers(data.customers || []);
        setTotalPages(data.total_pages || 1);
      })
      .catch(error => console.error("Error fetching customers:", error))
      .finally(() => setLoading(false));
  };

  // 🔥 Fetch Rental History
  const fetchRentalHistory = (customer_id) => {
    fetch(`http://127.0.0.1:5000/api/customers/${customer_id}/rentals`)
      .then(response => response.json())
      .then(data => {
        if (data.rental_history) {
          setRentalHistory(data.rental_history);
          setSelectedCustomer(customer_id);
          setShowRentalModal(true);
        } else {
          alert("No rental history found for this customer.");
        }
      })
      .catch(error => console.error("Error fetching rental history:", error));
  };

  // 🔥 Handle Input Changes for Add/Edit Forms
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewCustomer(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  // 🔥 Add or Edit Customer
  const handleSubmit = (e) => {
    e.preventDefault();
  
    // 🔥 Check if we are editing or adding a new customer
    const isEditing = editingCustomer !== null;
    const method = isEditing ? "PUT" : "POST";
    const url = isEditing
      ? `http://127.0.0.1:5000/api/customers/${editingCustomer.customer_id}`
      : "http://127.0.0.1:5000/api/customers";
  
    // 🔥 Ensure correct customer data is being sent
    const customerData = {
      first_name: newCustomer.first_name,
      last_name: newCustomer.last_name,
      email: newCustomer.email,
      store_id: Number(newCustomer.store_id), // 🔥 Convert to number
      address_id: Number(newCustomer.address_id), // 🔥 Convert to number
      active: newCustomer.active
    };

    console.log(`Submitting ${method} request to ${url}`, customerData); // ✅ Debugging log

    fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(customerData),
    })
      .then(response => response.json())
      .then((data) => {
        if (data.error) {
          alert(`Error: ${data.error}`);
          return;
        }
  
        console.log("Response from server:", data); // ✅ Debugging log

        setShowForm(false);
        setEditingCustomer(null);
        setSuccessMessage(isEditing ? "Customer updated successfully!" : "Customer added successfully!");
        setNewCustomer({ first_name: "", last_name: "", email: "", store_id: "", address_id: "", active: 1 });

        fetchCustomers(); // 🔥 Refresh the table
        setTimeout(() => setSuccessMessage(""), 3000);
      })
      .catch(error => console.error("Error saving customer:", error));
  };

  // 🔥 Open Edit Form
  const handleEditCustomer = (customer) => {
    console.log("Editing customer:", customer); // ✅ Debugging log

    setNewCustomer({
      first_name: customer.first_name,
      last_name: customer.last_name,
      email: customer.email,
      store_id: String(customer.store_id), // Convert to string for form input
      address_id: String(customer.address_id),
      active: customer.active
    });

    setEditingCustomer(customer);
    setShowForm(true);
  };

  return (
    <div className="customer-table-container">
      <h2>Customer Information</h2>

      {successMessage && <p className="success-message">{successMessage}</p>}

      {/* ✅ Search Bar */}
      <div className="search-container">
        <input
          type="text"
          placeholder="Search by ID, First Name, or Last Name..."
          value={searchQuery}
          onChange={(e) => {
            setSearchQuery(e.target.value);
            setCurrentPage(1);
          }}
          className="search-box"
        />
      </div>

      <button className="add-customer-btn" onClick={() => { setShowForm(true); setEditingCustomer(null); }}>
        + Add New Customer
      </button>

      {loading && <p>Loading customers...</p>}

      {/* ✅ Customer Table */}
      <table className="customer-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Store ID</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email</th>
            <th>Address ID</th>
            <th>Active</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {customers.map((customer) => (
            <tr key={customer.customer_id}>
              <td>{customer.customer_id}</td>
              <td>{customer.store_id}</td>
              <td>{customer.first_name}</td>
              <td>{customer.last_name}</td>
              <td>{customer.email}</td>
              <td>{customer.address_id}</td>
              <td>{customer.active === 1 ? "Yes" : "No"}</td>
              <td>
                <button className="edit-btn" onClick={() => handleEditCustomer(customer)}>✏ Edit</button>
                <button className="delete-btn" onClick={() => handleDeleteCustomer(customer.customer_id)}>🗑 Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* ✅ Add/Edit Customer Form */}
      {showForm && (
        <div className="customer-form">
          <h3>{editingCustomer ? "Edit Customer" : "Add New Customer"}</h3>
          <form onSubmit={handleSubmit}>
            <input type="text" name="first_name" placeholder="First Name" value={newCustomer.first_name} onChange={handleInputChange} required />
            <input type="text" name="last_name" placeholder="Last Name" value={newCustomer.last_name} onChange={handleInputChange} required />
            <input type="email" name="email" placeholder="Email" value={newCustomer.email} onChange={handleInputChange} required />
            <input type="number" name="store_id" placeholder="Store ID" value={newCustomer.store_id} onChange={handleInputChange} required />
            <input type="number" name="address_id" placeholder="Address ID" value={newCustomer.address_id} onChange={handleInputChange} required />
            <button type="submit">{editingCustomer ? "Update" : "Submit"}</button>
            <button type="button" onClick={() => setShowForm(false)}>Cancel</button>
          </form>
        </div>
      )}
    </div>
  );
};

export default CustomerTable;

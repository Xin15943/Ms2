import './App.css'
import { Navbar } from './components/Navbar'
import { Home , Customer,Film } from './components/pages'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';



function App() {
  return(
    <div className="App">
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/Film" element={<Film />} />
        <Route path="/customer" element={<Customer />} />
      </Routes>

    </div>
  )

}

export default App

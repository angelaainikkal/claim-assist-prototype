import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <div style={{
      display: "flex",
      justifyContent: "space-between",
      padding: "15px 40px",
      backgroundColor: "#1E3A8A",
      color: "white"
    }}>
      <h2>ClaimAssist</h2>

      <div>
        <Link to="/" style={{ color: "white", marginRight: "20px" }}>Home</Link>
        <Link to="/claim" style={{ color: "white", marginRight: "20px" }}>Claim</Link>
        <Link to="/dashboard" style={{ color: "white", marginRight: "20px" }}>Dashboard</Link>
        <Link to="/login" style={{ color: "white" }}>Login</Link>
      </div>
    </div>
  );
}
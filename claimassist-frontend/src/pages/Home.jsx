import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div style={{ padding: "60px", fontFamily: "Arial" }}>
      <h1 style={{ color: "#1E3A8A" }}>ClaimAssist</h1>
      <p>AI-powered Insurance Claim Processing Platform</p>

      <h3>How It Works:</h3>
      <ol>
        <li>Select Insurance Type</li>
        <li>Upload Required Documents</li>
        <li>AI Validates Documents</li>
        <li>Track Claim Status</li>
      </ol>

      <br />

      <Link to="/login">
        <button style={{
          padding: "10px 20px",
          backgroundColor: "#1E3A8A",
          color: "white",
          border: "none",
          cursor: "pointer"
        }}>
          Get Started
        </button>
      </Link>
    </div>
  );
}
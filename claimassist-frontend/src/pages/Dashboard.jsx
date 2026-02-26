export default function Dashboard() {
  const claims = [
    {
      id: 1,
      type: "Health",
      amount: 50000,
      status: "Approved",
      requestDate: "2026-02-20",
      approvalDate: "2026-02-23"
    },
    {
      id: 2,
      type: "Vehicle",
      amount: 30000,
      status: "Pending",
      requestDate: "2026-02-24",
      approvalDate: "-"
    },
    {
      id: 3,
      type: "Travel",
      amount: 20000,
      status: "Rejected",
      requestDate: "2026-02-15",
      approvalDate: "2026-02-18"
    }
  ];

  const approved = claims.filter(c => c.status === "Approved").length;
  const pending = claims.filter(c => c.status === "Pending").length;
  const rejected = claims.filter(c => c.status === "Rejected").length;

  return (
    <div style={{ padding: "60px" }}>
      <h2>Dashboard</h2>

      <div style={{ marginBottom: "30px" }}>
        <p>Total Claims: {claims.length}</p>
        <p>Approved: {approved}</p>
        <p>Pending: {pending}</p>
        <p>Rejected: {rejected}</p>
      </div>

      <h3>Claim Details</h3>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Type</th>
            <th>Amount</th>
            <th>Status</th>
            <th>Request Date</th>
            <th>Approval Date</th>
          </tr>
        </thead>
        <tbody>
          {claims.map((claim) => (
            <tr key={claim.id}>
              <td>{claim.type}</td>
              <td>₹{claim.amount}</td>
              <td>{claim.status}</td>
              <td>{claim.requestDate}</td>
              <td>{claim.approvalDate}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
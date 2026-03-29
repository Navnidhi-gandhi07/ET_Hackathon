import React, { useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [file, setFile] = useState(null);
  const [snapshots, setSnapshots] = useState([]);
  const [loading, setLoading] = useState(false);

  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [confidence, setConfidence] = useState(null);
  const [citations, setCitations] = useState([]);

  // ================= UPLOAD =================
  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:5000/upload", formData);
      setSnapshots(res.data.snapshots);
    } catch (err) {
      alert("Upload failed: " + err.message);
    }

    setLoading(false);
  };

  // ================= QUERY =================
  const handleQuery = async () => {
    if (!query) return;

    try {
      const res = await axios.post("http://localhost:5000/query", {
        query: query,
      });

      setAnswer(res.data.answer);
      setConfidence(res.data.confidence);
      setCitations(res.data.citations || []);
    } catch (err) {
      alert("Query failed: " + err.message);
    }
  };

  return (
    <div>
      {/* Navbar */}
      <nav className="navbar navbar-dark bg-gradient">
        <div className="container">
          <span className="navbar-brand fw-bold fs-4">
            🚆 Sanchaalan
          </span>
        </div>
      </nav>

      {/* Hero */}
      <header className="text-center py-5 bg-light">
        <h1 className="fw-bold">AI Document Intelligence</h1>
        <p className="text-muted">
          Upload → Analyze → Decide → Act
        </p>
      </header>

      {/* Upload */}
      <div className="container mt-4">
        <form onSubmit={handleUpload} className="card p-4 shadow">
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="form-control mb-3"
            accept=".pdf,.docx,.eml"
          />

          <button className="btn btn-gradient">
            {loading ? "Processing..." : "Upload & Process"}
          </button>
        </form>

        {/* Snapshots */}
        {snapshots.length > 0 && (
          <div className="card mt-4 p-4 shadow">
            <h4>Snapshots</h4>

            {snapshots.map((s, i) => (
              <div key={i} className="d-flex justify-content-between mb-2">
                <span>{s.role}</span>
                <a
                  href={`http://localhost:5000/snapshots/${s.snapshot_file}`}
                  className="btn btn-sm btn-outline-primary"
                >
                  Download
                </a>
              </div>
            ))}
          </div>
        )}

        {/* Query */}
        <div className="card mt-4 p-4 shadow">
          <h4>Ask Questions</h4>

          <input
            type="text"
            placeholder="Ask about the document..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="form-control mb-3"
          />

          <button className="btn btn-dark" onClick={handleQuery}>
            Ask AI
          </button>

          {/* Answer */}
          {answer && (
            <div className="mt-4">
              <h5>Answer</h5>
              <p>{answer}</p>

              <p>
                <strong>Confidence:</strong> {confidence}%
              </p>

              {/* Citations */}
              {citations.length > 0 && (
                <>
                  <h6>Sources</h6>
                  <ul>
                    {citations.map((c, i) => (
                      <li key={i}>
                        {c.doc_id} (Page {c.page})
                      </li>
                    ))}
                  </ul>
                </>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="text-center mt-5 mb-3 text-muted">
        Built with AI ⚡
      </footer>

      {/* Styles */}
      <style>{`
        .bg-gradient {
          background: linear-gradient(135deg, #4f46e5, #3b82f6);
        }
        .btn-gradient {
          background: linear-gradient(135deg, #6366f1, #3b82f6);
          color: white;
          border: none;
        }
      `}</style>
    </div>
  );
}

export default App;
import { useState } from "react";
import axios from "axios";
import "./index.css";

export default function ResumeMatcher() {
  const [resume, setResume] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [matchScore, setMatchScore] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post("https://csv-excel-automation-python.onrender.com/match", {
        resume,
        job_description: jobDescription,
      });
      setMatchScore(response.data.match_score);
    } catch (error) {
      console.error("Error fetching match score", error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <h2 className="text-xl font-bold mb-4">Resume Matcher</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          className="w-full p-2 border rounded"
          placeholder="Paste your Resume here"
          value={resume}
          onChange={(e) => setResume(e.target.value)}
          rows={4}
        />
        <textarea
          className="w-full p-2 border rounded"
          placeholder="Paste Job Description here"
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          rows={4}
        />
        <button
          type="submit"
          className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
          disabled={loading}
        >
          {loading ? "Matching..." : "Get Match Score"}
        </button>
        <div className="border-4px">
            <label>Upload your Resume</label>
            <input type="file" accept=".pdf,.docx,.txt" className="mb-2" />
        </div>
      </form>
      {matchScore !== null && (
        <div className="mt-4 text-lg font-semibold">
          Match Score: {Math.round(matchScore * 100)}%
        </div>
      )}
    </div>
  );
}

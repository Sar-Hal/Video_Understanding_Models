import React, { useState } from "react";

// Set this to your Hugging Face API key, or leave blank for anonymous/free tier demo
const HUGGINGFACE_API_KEY = ""; // Optional: "hf_xxx..."

const MODEL_ENDPOINT =
  "https://api-inference.huggingface.co/models/SmolVLM/SmolVLM2-Video-LLaVA";

function App() {
  const [videoFile, setVideoFile] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!videoFile || !prompt) {
      setResult("Please upload a video and enter a prompt.");
      return;
    }
    setLoading(true);
    setResult("");

    // Build multipart request (video + prompt as JSON)
    const formData = new FormData();
    formData.append("video", videoFile);
    formData.append(
      "parameters",
      JSON.stringify({
        prompt: prompt,
      })
    );

    try {
      const response = await fetch(MODEL_ENDPOINT, {
        method: "POST",
        headers: HUGGINGFACE_API_KEY
          ? {
              Authorization: `Bearer ${HUGGINGFACE_API_KEY}`,
            }
          : {},
        body: formData,
      });

      if (!response.ok) {
        const err = await response.text();
        throw new Error(err || "Request failed");
      }

      const data = await response.json();
      // SmolVLM2 returns a JSON with "text" field for result
      setResult(data.text || JSON.stringify(data));
    } catch (error) {
      setResult("Error: " + error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 480, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h2>Video Understanding Demo (SmolVLM2)</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <input
            type="file"
            accept="video/*"
            onChange={(e) => setVideoFile(e.target.files[0])}
          />
        </div>
        <div style={{ margin: "1rem 0" }}>
          <input
            type="text"
            style={{ width: "100%" }}
            placeholder="e.g. Count number of steps when a person climbs the stairs"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Processing..." : "Submit"}
        </button>
      </form>
      <div style={{ marginTop: "2rem", minHeight: 40 }}>
        {result && (
          <div>
            <b>Result:</b>
            <pre>{result}</pre>
          </div>
        )}
      </div>
      <div style={{ marginTop: 32, fontSize: "0.9em", color: "#666" }}>
        Powered by <a href="https://huggingface.co/SmolVLM/SmolVLM2-Video-LLaVA" target="_blank" rel="noopener noreferrer">SmolVLM2</a> on Hugging Face 🤗
      </div>
    </div>
  );
}

export default App;
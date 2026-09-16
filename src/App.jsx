import { useState } from "react";
import "./App.css";

function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState("");
  const [confidence, setConfidence] = useState(0);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (event) => {
    const selectedImage = event.target.files[0];

    if (selectedImage) {
      setImage(selectedImage);
      setPreview(URL.createObjectURL(selectedImage));
      setResult("");
      setConfidence(0);
    }
  };

  const handleAnalyze = async () => {
    if (!image) {
      alert("Please upload a chest X-ray image first.");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", image);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/predict",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error("Prediction failed");
      }

      setResult(data.prediction);
      setConfidence(data.confidence);
    } catch (error) {
      console.error(error);
      alert("Unable to connect to the AI server.");
    }

    setLoading(false);
  };

  return (
    <div className="app">

      {/* TOP HEADER */}
      <header className="top-header">

        <div className="brand">
          <div className="brand-icon">🫁</div>

          <div>
            <h2>Pneumonia Detection</h2>
            <p>AI Powered Chest X-Ray Analysis</p>
          </div>
        </div>

        <div className="header-right">
          <span className="shield">🛡️</span>

          <div>
            <strong>Better Insights</strong>
            <br />
            <span>for Healthier Lives</span>
          </div>
        </div>

      </header>


      {/* MAIN CONTENT */}
      <main className="container">

        {/* TITLE */}
        <section className="main-title">

          <div className="large-lung">
            🫁
          </div>

          <h1>Pneumonia Detection</h1>

          <p>
            Upload a chest X-ray image for AI analysis
          </p>

        </section>


        {/* UPLOAD SECTION */}
        <section className="upload-section">

          <div className="section-number">
            1
          </div>

          <h2>Upload X-Ray Image</h2>

          <p className="upload-info">
            Supported formats: JPG, JPEG, PNG &nbsp;|&nbsp; Max size: 10MB
          </p>

          <div className="upload-box">

            <input
              type="file"
              accept="image/jpeg,image/jpg,image/png"
              onChange={handleImageChange}
            />

            {preview && (
              <img
                src={preview}
                alt="Chest X-Ray Preview"
                className="preview"
              />
            )}

          </div>

        </section>


        {/* ANALYZE BUTTON */}
        <button
          className="analyze-button"
          onClick={handleAnalyze}
          disabled={loading}
        >
          {loading ? (
            "Analyzing..."
          ) : (
            <>
              🔍 &nbsp; Analyze X-Ray
            </>
          )}
        </button>


        {/* RESULT */}
        {result && (

          <section
            className={`result-card ${
              result.toLowerCase() === "pneumonia"
                ? "pneumonia"
                : "normal"
            }`}
          >

            {/* RESULT LEFT */}
            <div className="result-left">

              <div className="result-icon">
                🫁
              </div>

              <div className="result-content">

                <p className="result-title">
                  Prediction Result
                </p>

                <h2>{result}</h2>

                <p className="confidence-text">
                  Confidence:{" "}
                  <strong>{confidence}%</strong>
                </p>

                {/* CONFIDENCE BAR */}
                <div className="progress-row">

                  <div className="progress-container">

                    <div
                      className="progress-bar"
                      style={{
                        width: `${confidence}%`,
                      }}
                    ></div>

                  </div>

                  <span className="progress-value">
                    {confidence}%
                  </span>

                </div>

                <span className="confidence-label">
                  {confidence >= 80
                    ? "High confidence"
                    : confidence >= 60
                    ? "Moderate confidence"
                    : "Low confidence"}
                </span>

              </div>

            </div>


            {/* INTERPRETATION */}
            <div className="interpretation">

              <h3>
                ⓘ &nbsp; Result Interpretation
              </h3>

              <p>
                The AI model analyzed the uploaded
                chest X-ray and generated the above
                prediction.
              </p>

            </div>

          </section>

        )}


        {/* DISCLAIMER */}
        <div className="warning">

          🛡️ &nbsp;
          This AI result is for educational and research
          purposes only and should not be considered a
          medical diagnosis.

        </div>

      </main>

    </div>
  );
}

export default App;
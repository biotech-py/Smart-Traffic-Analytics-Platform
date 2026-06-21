import { useState, useEffect, useRef } from "react";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import "./App.css";

function App() {

  const [mode, setMode] = useState("live");

  const [file, setFile] = useState(null);

  const [uploadStatus, setUploadStatus] =
    useState("");

  const [vehiclesPassed,
    setVehiclesPassed] =
    useState(0);

  const [trafficStatus,
    setTrafficStatus] =
    useState("LOW");

  const [vehiclesPerMinute,
    setVehiclesPerMinute] =
    useState(0);

  const [trafficHistory,
    setTrafficHistory] =
    useState([]);

  const [processedVideo,
    setProcessedVideo] =
    useState("");

  const [processedFrame,
    setProcessedFrame] =
    useState("");

  const [loading,
    setLoading] =
    useState(false);

  const videoRef =
    useRef(null);

  const canvasRef =
    useRef(null);

  // ===================================
  // START BROWSER CAMERA
  // ===================================

  const startBrowserCamera =
    async () => {

      try {

        const stream =
          await navigator
            .mediaDevices
            .getUserMedia({
              video: true
            });

        if (videoRef.current) {

          videoRef.current.srcObject =
            stream;

        }

      } catch (error) {

        console.error(error);

        alert(
          "Unable to access camera"
        );

      }

    };

  // ===================================
  // CAMERA START
  // ===================================

  useEffect(() => {

    if (mode !== "live")
      return;

    startBrowserCamera();

  }, [mode]);

  // ===================================
  // SEND FRAME TO FASTAPI
  // ===================================

  useEffect(() => {

    if (mode !== "live")
      return;

    const interval =
      setInterval(
        async () => {

          if (
            !videoRef.current ||
            !canvasRef.current
          ) {
            return;
          }

          const video =
            videoRef.current;

          if (
            video.videoWidth === 0
          ) {
            return;
          }

          const canvas =
            canvasRef.current;

          const ctx =
            canvas.getContext("2d");

          canvas.width =
            video.videoWidth;

          canvas.height =
            video.videoHeight;

          ctx.drawImage(
            video,
            0,
            0
          );

          canvas.toBlob(
            async (blob) => {

              try {

                const response =
                  await fetch(
                    "https://smart-traffic-backend-6df6.onrender.com/detect_frame",
                    {
                      method:
                        "POST",
                      body: blob
                    }
                  );

                const data =
                  await response.json();

                // ------------------
                // Update Dashboard
                // ------------------

                setTrafficStatus(
                  data.traffic_status
                );

                setVehiclesPerMinute(
                  data.vehicle_count
                );

                setVehiclesPassed(
                  data.vehicle_count
                );

                // ------------------
                // Display YOLO Frame
                // ------------------

                if (data.image) {

                  setProcessedFrame(
                    "data:image/jpeg;base64," +
                    data.image
                  );

                }

                // ------------------
                // Graph
                // ------------------

                setTrafficHistory(
                  (prev) => {

                    const updated =
                      [
                        ...prev,
                        {
                          frame:
                            prev.length + 1,
                          vehicles:
                            data.vehicle_count
                        }
                      ];

                    return updated.slice(
                      -20
                    );

                  }
                );

              } catch (error) {

                console.error(
                  error
                );

              }

            },
            "image/jpeg"
          );

        },
        300
      );

    return () =>
      clearInterval(
        interval
      );

  }, [mode]);

  // ===================================
  // VIDEO UPLOAD
  // ===================================

  const uploadVideo =
    async () => {

      if (!file) {

        alert(
          "Select a video"
        );

        return;

      }

      const formData =
        new FormData();

      formData.append(
        "file",
        file
      );

      try {

        const response =
          await fetch(
            "https://smart-traffic-backend-6df6.onrender.com/upload",
            {
              method: "POST",
              body: formData
            }
          );

        const data =
          await response.json();

        setUploadStatus(
          `Uploaded: ${data.filename}`
        );

      } catch {

        setUploadStatus(
          "Upload Failed"
        );

      }

    };

  // ===================================
  // ANALYZE VIDEO
  // ===================================

  const analyzeVideo =
    async () => {

      if (!file) {

        alert(
          "Upload a video first"
        );

        return;

      }

      try {

        setLoading(true);

        const response =
          await fetch(
            `https://smart-traffic-backend-6df6.onrender.com/analyze?filename=${file.name}`,
            {
              method: "POST"
            }
          );

        const data =
        await response.json();
        console.log("ANALYZE RESPONSE:", data);  

        setLoading(false);

        if (data.output) {

          setProcessedVideo(
            `https://smart-traffic-backend-6df6.onrender.com/${data.output}?t=${Date.now()}`
          );

        }

        setTrafficStatus(
          data.traffic_status
        );

        setVehiclesPerMinute(
          data.vehicles_per_minute
        );

        setVehiclesPassed(
          (data.cars || 0) +
          (data.bikes || 0) +
          (data.buses || 0) +
          (data.trucks || 0)
        );

        const graphData =
          data.traffic_history
            ? data.traffic_history.map(
                (
                  value,
                  index
                ) => ({
                  frame:
                    index + 1,
                  vehicles:
                    value
                })
              )
            : [];

        setTrafficHistory(
          graphData
        );

      } catch {

        setLoading(false);

        alert(
          "Analysis Failed"
        );

      }

    };

  return (

    <div className="dashboard">

      <div className="header">

        <h1>
          Smart Traffic Analytics Platform
        </h1>

        <p>
          Real-Time Traffic Monitoring &
          Video Analytics
        </p>

        <div className="mode-switch">

          <button
            className={
              mode === "live"
                ? "active-mode"
                : ""
            }
            onClick={() =>
              setMode("live")
            }
          >
            Live Camera
          </button>

          <button
            className={
              mode === "upload"
                ? "active-mode"
                : ""
            }
            onClick={() =>
              setMode("upload")
            }
          >
            Upload Video
          </button>

        </div>

      </div>

      <div className="stats-row">

        <div className="stat-card">
          <h2>{vehiclesPerMinute}</h2>
          <span>Vehicles</span>
        </div>

        <div className="stat-card">
          <h2>{trafficStatus}</h2>
          <span>Traffic Status</span>
        </div>

        <div className="stat-card">
          <h2>{vehiclesPassed}</h2>
          <span>Count</span>
        </div>

        <div className="stat-card">
          <h2>LIVE</h2>
          <span>Monitoring</span>
        </div>

      </div>

      <div className="video-section">

        {mode === "live" ? (

          <>

            <div className="panel-header">
              Browser Camera Detection
            </div>

            <div style={{ position: "relative" }}>

              <video
                ref={videoRef}
                className="live-feed"
                autoPlay
                muted
                playsInline
                style={{
                  display: processedFrame
                    ? "none"
                    : "block"
                }}
              />

              {processedFrame && (

                <img
                  src={processedFrame}
                  className="live-feed"
                  alt="Detection Feed"
                />

              )}

            </div>

            <canvas
              ref={canvasRef}
              style={{
                display: "none"
              }}
            />

          </>

        ) : (

          <>

            <div className="panel-header">
              Upload Traffic Video
            </div>

            <div className="controls">

              <input
                type="file"
                accept="video/*"
                onChange={(e) =>
                  setFile(
                    e.target.files[0]
                  )
                }
              />

              <button
                onClick={
                  uploadVideo
                }
              >
                Upload
              </button>

              <button
                onClick={
                  analyzeVideo
                }
                disabled={
                  loading
                }
              >
                {
                  loading
                    ? "Processing..."
                    : "Analyze"
                }
              </button>

              <span className="upload-status">
                {uploadStatus}
              </span>

            </div>

            {processedVideo && (

              <video
                className="live-feed"
                controls
              >
                <source
                  src={
                    processedVideo
                  }
                  type="video/mp4"
                />
              </video>

            )}

          </>

        )}

      </div>

      <div className="bottom-grid">

        <div className="graph-section">

          <div className="panel-header">
            Traffic Density Trend
          </div>

          <ResponsiveContainer
            width="100%"
            height={250}
          >

            <LineChart
              data={trafficHistory}
            >

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis
                dataKey="frame"
              />

              <YAxis />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="vehicles"
                stroke="#3b82f6"
                strokeWidth={3}
              />

            </LineChart>

          </ResponsiveContainer>

        </div>

        <div className="status-panel">

          <h3>Live Status</h3>

          <div className="status-big">
            {trafficStatus}
          </div>

          <p>
            Vehicles:
            {" "}
            {vehiclesPerMinute}
          </p>

          <p>
            Count:
            {" "}
            {vehiclesPassed}
          </p>

          <div className="live-dot">
            ● LIVE
          </div>

        </div>

      </div>

    </div>

  );

}
export default App;


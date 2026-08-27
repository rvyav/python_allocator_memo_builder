import { useState } from "react";
import type { ChangeEvent } from "react";
import apiClient from "./api/HttpRequest";

import "./App.css";

import {
  liquidityOptions,
  volatilityOptions,
  drawdownOptions,
  strategyOptions,
} from "./utils/constants";

interface UploadResponse {
  message: string;
  rows?: unknown[];
}

const App = () => {
  const [liquidity, setLiquidity] = useState("");
  const [volatility, setVolatility] = useState("");
  const [drawdown, setDrawdown] = useState("");
  const [strategies, setStrategies] = useState<string[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const canUpload =
    liquidity !== "" &&
    volatility !== "" &&
    drawdown !== "" &&
    strategies.length > 0;

  const handleStrategyChange = (
    event: ChangeEvent<HTMLSelectElement>
  ) => {
    const selected = Array.from(
      event.target.selectedOptions,
      (option) => option.value
    );

    setStrategies(selected);
  };

  const handleFileChange = (
    event: ChangeEvent<HTMLInputElement>
  ) => {
    const selectedFile =
      event.target.files?.[0] ?? null;

    if (
      selectedFile &&
      !selectedFile.name
        .toLowerCase()
        .endsWith(".csv")
    ) {
      alert("Please select a CSV file.");

      event.target.value = "";
      setFile(null);

      return;
    }

    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!canUpload || !file) {
      return;
    }

    setIsUploading(true);

    try {
      const formData = new FormData();

      // Add the CSV file
      formData.append("file", file);

      // Add document preferences
      formData.append(
        "document_preferences",
        JSON.stringify({
          liquidity,
          target_volatility: volatility,
          max_drawdown: drawdown,
          strategies,
        })
      );

      const response =
        await apiClient.post<
          UploadResponse,
          FormData
        >("/api/upload/", formData);

      console.log(
        "Upload successful:",
        response
      );

      alert("Document uploaded successfully.");
    } catch (error) {
      console.error(
        "Upload error:",
        error
      );
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <main className="home-page">
      <div className="upload-layout">

        <aside className="preferences">
          <h2>
            Document preferences
          </h2>
          <div className="field">
            <label htmlFor="liquidity">
              Liquidity requirement
            </label>

            <select
              id="liquidity"
              value={liquidity}
              onChange={(event) =>
                setLiquidity(
                  event.target.value
                )
              }
            >
              <option value="">
                Select liquidity requirement
              </option>

              {liquidityOptions.map(
                (option) => (
                  <option
                    key={option}
                    value={option}
                  >
                    {option}
                  </option>
                )
              )}
            </select>
          </div>

          <div className="field">
            <label htmlFor="volatility">
              Target volatility
            </label>

            <select
              id="volatility"
              value={volatility}
              onChange={(event) =>
                setVolatility(
                  event.target.value
                )
              }
            >
              <option value="">
                Select target volatility
              </option>

              {volatilityOptions.map(
                (option) => (
                  <option
                    key={option.value}
                    value={option.value}
                  >
                    {option.label}
                  </option>
                )
              )}
            </select>
          </div>
          <div className="field">
            <label htmlFor="drawdown">
              Max drawdown tolerance
            </label>

            <select
              id="drawdown"
              value={drawdown}
              onChange={(event) =>
                setDrawdown(
                  event.target.value
                )
              }
            >
              <option value="">
                Select drawdown tolerance
              </option>

              {drawdownOptions.map(
                (option) => (
                  <option
                    key={option.value}
                    value={option.value}
                  >
                    {option.label}
                  </option>
                )
              )}
            </select>
          </div>
          <div className="field">
            <label htmlFor="strategies">
              Strategy
              preferences/exclusions
            </label>

            <select
              id="strategies"
              multiple
              value={strategies}
              onChange={
                handleStrategyChange
              }
              size={6}
            >
              {strategyOptions.map(
                (option) => (
                  <option
                    key={option}
                    value={option}
                  >
                    {option}
                  </option>
                )
              )}
            </select>

            <small>
              Select at least one strategy.
            </small>
          </div>
          <div
            className={`status ${canUpload
              ? "status-ready"
              : "status-incomplete"
              }`}
          >
            {canUpload
              ? "✓ All preferences selected"
              : "Select an option in all four sections"}
          </div>
        </aside>

        <section className="upload-section">
          <h1>
            Upload document
          </h1>

          <div className="upload-box">
            <label
              htmlFor="csv-file"
              className="file-label"
            >
              <span>
                {file
                  ? file.name
                  : "Choose a CSV file"}
              </span>

              <input
                id="csv-file"
                type="file"
                accept=".csv,text/csv"
                onChange={
                  handleFileChange
                }
                disabled={
                  !canUpload ||
                  isUploading
                }
              />
            </label>

            <p className="upload-hint">
              {canUpload
                ? "Select a CSV file to upload."
                : "Complete all preferences to enable file upload."}
            </p>

            <button
              type="button"
              onClick={handleUpload}
              disabled={
                !canUpload ||
                !file ||
                isUploading
              }
              className="upload-button"
            >
              {isUploading
                ? "Uploading..."
                : "Generate Memo"}
            </button>
          </div>
        </section>
      </div>
    </main>
  );
};

export default App;

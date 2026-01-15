// static/app.js
/*
WHY THIS FILE EXISTS (short version):
- This is the bridge between the dashboard UI (HTML) and the API (FastAPI).
- It calls /api/summary, /api/metrics, /api/predictions and renders results.

PROJECT MAPPING:
- "Dashboard" layer
- This is not CI/CD, not transformation. It's the UI consumer.
*/

async function fetchJson(path) {
  const res = await fetch(path);
  if (!res.ok) {
    throw new Error(`Request failed: ${path} (${res.status})`);
  }
  return res.json();
}

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

function renderPredictions(items) {
  const body = document.getElementById("predictions_body");
  body.innerHTML = "";

  for (const row of items) {
    const tr = document.createElement("tr");

    const tdId = document.createElement("td");
    tdId.textContent = row.id;

    const tdX = document.createElement("td");
    tdX.textContent = row.feature_x;

    const tdPred = document.createElement("td");
    tdPred.textContent = row.prediction;

    const tdActual = document.createElement("td");
    tdActual.textContent = row.actual;

    tr.appendChild(tdId);
    tr.appendChild(tdX);
    tr.appendChild(tdPred);
    tr.appendChild(tdActual);

    body.appendChild(tr);
  }
}

async function loadDashboard() {
  try {
    const summary = await fetchJson("/api/summary");
    setText("pipeline_status", summary.pipeline_status);
    setText("last_run_utc", summary.last_run_utc);
    setText("rows_ingested", summary.rows_ingested);
    setText("model_version", summary.model_version);

    const metrics = await fetchJson("/api/metrics");
    setText("metric_name", metrics.metric_name);
    setText("metric_value", metrics.metric_value);

    const preds = await fetchJson("/api/predictions?limit=10");
    renderPredictions(preds.items);
  } catch (err) {
    console.error(err);
    setText("pipeline_status", "ERROR");
    setText("metric_value", "Failed to load");
  }
}

loadDashboard();

import { apiFetch } from "./api.js";
const apiStatus = document.getElementById("api-status");

apiFetch("/health")
  .then((res) => res.json())
  .then((data) => {
    apiStatus.textContent = `API status: ${data.status}`;
  })
  .catch(() => {
    apiStatus.textContent = "API unreachable.";
  });

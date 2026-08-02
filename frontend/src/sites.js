import { fetchJson, postJson, renderList, setFormMessage } from "./api.js";

const apiStatus = document.getElementById("api-status");
const siteList = document.getElementById("site-list");
const siteForm = document.getElementById("site-form");
const siteNameInput = document.getElementById("site-name");
const siteFormMessage = document.getElementById("site-form-message");

async function loadSites() {
  try {
    const sites = await fetchJson("/sites/");
    renderList(siteList, sites, (s) => s.name);
  } catch {
    siteList.innerHTML = '<li class="empty">Could not load sites.</li>';
  }
}

siteForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const name = siteNameInput.value.trim();
  if (!name) return;

  setFormMessage(siteFormMessage, "Creating…");
  try {
    await postJson("/sites/", { name });
    siteForm.reset();
    setFormMessage(siteFormMessage, "Site created.", "success");
    loadSites();
  } catch {
    setFormMessage(siteFormMessage, "Could not create site.", "error");
  }
});

fetch("/health")
  .then((res) => res.json())
  .then((data) => {
    apiStatus.textContent = `API status: ${data.status}`;
  })
  .catch(() => {
    apiStatus.textContent = "API unreachable.";
  });

loadSites();

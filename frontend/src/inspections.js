import { fetchJson, postJson, renderEmpty, fillOptions, setFormMessage } from "./api.js";

const apiStatus = document.getElementById("api-status");
const inspectionList = document.getElementById("inspection-list");

async function loadTemplateOptions() {
  try {
    const templates = await fetchJson("/templates/");
    fillOptions(document.getElementById("inspection-template"), templates, {
      placeholder: "Select a template…",
      labelFor: (t) => t.title,
    });
  } catch {
    // Template select stays on its placeholder if templates fail to load.
  }
}

function renderInspections(inspections) {
  inspectionList.innerHTML = "";
  if (inspections.length === 0) {
    renderEmpty(inspectionList, "No inspections yet.");
    return;
  }

  for (const inspection of inspections) {
    const li = document.createElement("li");
    const title = document.createElement("span");
    title.textContent = inspection.title;
    const badge = document.createElement("span");
    badge.className = `status-badge ${inspection.status}`;
    badge.textContent = inspection.status;
    li.append(title, badge);
    inspectionList.append(li);
  }
}

async function loadInspections() {
  try {
    renderInspections(await fetchJson("/inspections/"));
  } catch {
    renderEmpty(inspectionList, "Could not load inspections.");
  }
}

const inspectionForm = document.getElementById("inspection-form");
const inspectionTemplateSelect = document.getElementById("inspection-template");
const inspectionTitleInput = document.getElementById("inspection-title");
const inspectionFormMessage = document.getElementById("inspection-form-message");

inspectionForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const templateId = inspectionTemplateSelect.value;
  const title = inspectionTitleInput.value.trim();
  if (!templateId || !title) return;

  setFormMessage(inspectionFormMessage, "Creating…");
  try {
    await postJson("/inspections/", { template_id: Number(templateId), title });
    inspectionForm.reset();
    setFormMessage(inspectionFormMessage, "Inspection created.", "success");
    loadInspections();
  } catch {
    setFormMessage(inspectionFormMessage, "Could not create inspection.", "error");
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

loadTemplateOptions();
loadInspections();

import { fetchJson, postJson, renderEmpty, fillOptions, setFormMessage } from "./api.js";

const apiStatus = document.getElementById("api-status");
const actionList = document.getElementById("action-list");

let sitesById = new Map();
let usersById = new Map();

async function loadReferenceData() {
  const [inspections, sites, users] = await Promise.all([
    fetchJson("/inspections/"),
    fetchJson("/sites/"),
    fetchJson("/users/"),
  ]);
  sitesById = new Map(sites.map((s) => [s.id, s]));
  usersById = new Map(users.map((u) => [u.id, u]));

  fillOptions(document.getElementById("action-inspection"), inspections, {
    placeholder: "Standalone (no inspection)",
    labelFor: (i) => i.title,
  });
  fillOptions(document.getElementById("action-site"), sites, {
    placeholder: "No site",
    labelFor: (s) => s.name,
  });
  fillOptions(document.getElementById("action-user"), users, {
    placeholder: "Unassigned",
    labelFor: (u) => u.name,
  });
}

function renderActions(actions) {
  actionList.innerHTML = "";

  if (actions.length === 0) {
    renderEmpty(actionList, "No actions yet.");
    return;
  }

  for (const action of actions) {
    const li = document.createElement("li");

    const title = document.createElement("span");
    title.className = "list-item-title";
    title.textContent = action.description;

    const meta = document.createElement("span");
    meta.className = "list-item-meta";
    const parts = [action.inspection_id ? `From inspection #${action.inspection_id}` : "Standalone"];
    if (action.site_id) parts.push(sitesById.get(action.site_id)?.name ?? `Site #${action.site_id}`);
    if (action.assigned_user_id) {
      parts.push(usersById.get(action.assigned_user_id)?.name ?? `User #${action.assigned_user_id}`);
    }
    if (action.frequency !== "once") parts.push(action.frequency);
    meta.textContent = parts.join(" · ");

    const badge = document.createElement("span");
    badge.className = `status-badge ${action.status}`;
    badge.textContent = action.status.replace("_", " ");

    li.append(title, meta, badge);
    actionList.append(li);
  }
}

async function loadActions() {
  try {
    renderActions(await fetchJson("/actions/"));
  } catch {
    renderEmpty(actionList, "Could not load actions.");
  }
}

const actionForm = document.getElementById("action-form");
const actionDescriptionInput = document.getElementById("action-description");
const actionInspectionSelect = document.getElementById("action-inspection");
const actionSiteSelect = document.getElementById("action-site");
const actionUserSelect = document.getElementById("action-user");
const actionFrequencySelect = document.getElementById("action-frequency");
const actionDueDateInput = document.getElementById("action-due-date");
const actionFormMessage = document.getElementById("action-form-message");

actionForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const description = actionDescriptionInput.value.trim();
  if (!description) return;

  setFormMessage(actionFormMessage, "Creating…");
  try {
    await postJson("/actions/", {
      description,
      inspection_id: actionInspectionSelect.value ? Number(actionInspectionSelect.value) : null,
      site_id: actionSiteSelect.value ? Number(actionSiteSelect.value) : null,
      assigned_user_id: actionUserSelect.value ? Number(actionUserSelect.value) : null,
      frequency: actionFrequencySelect.value,
      due_date: actionDueDateInput.value || null,
    });
    actionForm.reset();
    setFormMessage(actionFormMessage, "Action created.", "success");
    loadActions();
  } catch {
    setFormMessage(actionFormMessage, "Could not create action.", "error");
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

async function init() {
  await loadReferenceData();
  loadActions();
}

init();

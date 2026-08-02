import { fetchJson, postJson, renderEmpty, fillOptions, setFormMessage } from "./api.js";

const apiStatus = document.getElementById("api-status");
const scheduleList = document.getElementById("schedule-list");

let templatesById = new Map();
let sitesById = new Map();
let usersById = new Map();

async function loadReferenceData() {
  const [templates, sites, users] = await Promise.all([
    fetchJson("/templates/"),
    fetchJson("/sites/"),
    fetchJson("/users/"),
  ]);
  templatesById = new Map(templates.map((t) => [t.id, t]));
  sitesById = new Map(sites.map((s) => [s.id, s]));
  usersById = new Map(users.map((u) => [u.id, u]));

  fillOptions(document.getElementById("schedule-template"), templates, {
    placeholder: "Select a template…",
    labelFor: (t) => t.title,
  });
  fillOptions(document.getElementById("schedule-site"), sites, {
    placeholder: "No site",
    labelFor: (s) => s.name,
  });
  fillOptions(document.getElementById("schedule-user"), users, {
    placeholder: "Unassigned",
    labelFor: (u) => u.name,
  });
}

function renderSchedules(schedules) {
  scheduleList.innerHTML = "";

  if (schedules.length === 0) {
    renderEmpty(scheduleList, "No schedules yet.");
    return;
  }

  for (const schedule of schedules) {
    const li = document.createElement("li");

    const title = document.createElement("span");
    title.className = "list-item-title";
    title.textContent = templatesById.get(schedule.template_id)?.title ?? `Template #${schedule.template_id}`;

    const meta = document.createElement("span");
    meta.className = "list-item-meta";
    const parts = [`Starts ${schedule.start_date}`];
    if (schedule.site_id) parts.push(sitesById.get(schedule.site_id)?.name ?? `Site #${schedule.site_id}`);
    if (schedule.assigned_user_id) {
      parts.push(usersById.get(schedule.assigned_user_id)?.name ?? `User #${schedule.assigned_user_id}`);
    }
    meta.textContent = parts.join(" · ");

    const badge = document.createElement("span");
    badge.className = "status-badge";
    badge.textContent = schedule.frequency;

    li.append(title, meta, badge);
    scheduleList.append(li);
  }
}

async function loadSchedules() {
  try {
    renderSchedules(await fetchJson("/schedules/"));
  } catch {
    renderEmpty(scheduleList, "Could not load schedules.");
  }
}

const scheduleForm = document.getElementById("schedule-form");
const scheduleTemplateSelect = document.getElementById("schedule-template");
const scheduleFrequencySelect = document.getElementById("schedule-frequency");
const scheduleStartDateInput = document.getElementById("schedule-start-date");
const scheduleSiteSelect = document.getElementById("schedule-site");
const scheduleUserSelect = document.getElementById("schedule-user");
const scheduleFormMessage = document.getElementById("schedule-form-message");

scheduleForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const templateId = scheduleTemplateSelect.value;
  const startDate = scheduleStartDateInput.value;
  if (!templateId || !startDate) return;

  setFormMessage(scheduleFormMessage, "Creating…");
  try {
    await postJson("/schedules/", {
      template_id: Number(templateId),
      frequency: scheduleFrequencySelect.value,
      start_date: startDate,
      site_id: scheduleSiteSelect.value ? Number(scheduleSiteSelect.value) : null,
      assigned_user_id: scheduleUserSelect.value ? Number(scheduleUserSelect.value) : null,
    });
    scheduleForm.reset();
    setFormMessage(scheduleFormMessage, "Schedule created.", "success");
    loadSchedules();
  } catch {
    setFormMessage(scheduleFormMessage, "Could not create schedule.", "error");
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
  loadSchedules();
}

init();

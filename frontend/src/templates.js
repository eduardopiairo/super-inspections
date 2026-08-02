import { fetchJson, postJson, renderEmpty, setFormMessage } from "./api.js";

const apiStatus = document.getElementById("api-status");
const templateList = document.getElementById("template-list");

function renderTemplates(templates) {
  templateList.innerHTML = "";
  if (templates.length === 0) {
    renderEmpty(templateList, "No templates yet.");
    return;
  }

  for (const template of templates) {
    const li = document.createElement("li");
    const title = document.createElement("span");
    title.className = "template-title";
    title.textContent = template.title;
    const description = document.createElement("span");
    description.className = "template-description";
    description.textContent = template.description || "No description";
    li.append(title, description);
    templateList.append(li);
  }
}

async function loadTemplates() {
  try {
    renderTemplates(await fetchJson("/templates/"));
  } catch {
    renderEmpty(templateList, "Could not load templates.");
  }
}

const templateForm = document.getElementById("template-form");
const templateTitleInput = document.getElementById("template-title");
const templateDescriptionInput = document.getElementById("template-description");
const templateFormMessage = document.getElementById("template-form-message");

templateForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const title = templateTitleInput.value.trim();
  if (!title) return;

  setFormMessage(templateFormMessage, "Creating…");
  try {
    await postJson("/templates/", {
      title,
      description: templateDescriptionInput.value.trim(),
      sections: [],
    });
    templateForm.reset();
    setFormMessage(templateFormMessage, "Template created.", "success");
    loadTemplates();
  } catch {
    setFormMessage(templateFormMessage, "Could not create template.", "error");
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

loadTemplates();

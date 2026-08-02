import { fetchJson, postJson, renderList, setFormMessage } from "./api.js";

const apiStatus = document.getElementById("api-status");
const userList = document.getElementById("user-list");
const userForm = document.getElementById("user-form");
const userNameInput = document.getElementById("user-name");
const userEmailInput = document.getElementById("user-email");
const userFormMessage = document.getElementById("user-form-message");

async function loadUsers() {
  try {
    const users = await fetchJson("/users/");
    renderList(userList, users, (u) => `${u.name} · ${u.email}`);
  } catch {
    userList.innerHTML = '<li class="empty">Could not load users.</li>';
  }
}

userForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const name = userNameInput.value.trim();
  const email = userEmailInput.value.trim();
  if (!name || !email) return;

  setFormMessage(userFormMessage, "Creating…");
  try {
    await postJson("/users/", { name, email });
    userForm.reset();
    setFormMessage(userFormMessage, "User created.", "success");
    loadUsers();
  } catch {
    setFormMessage(userFormMessage, "Could not create user.", "error");
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

loadUsers();

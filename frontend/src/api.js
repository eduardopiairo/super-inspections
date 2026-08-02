export async function fetchJson(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Request to ${path} failed`);
  return res.json();
}

export async function postJson(path, body) {
  const res = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`Request to ${path} failed`);
  return res.json();
}

export function renderEmpty(el, message) {
  el.innerHTML = `<li class="empty">${message}</li>`;
}

export function renderList(el, items, labelFor) {
  el.innerHTML = "";
  if (items.length === 0) {
    renderEmpty(el, "None yet.");
    return;
  }
  for (const item of items) {
    const li = document.createElement("li");
    li.textContent = labelFor(item);
    el.append(li);
  }
}

export function fillOptions(select, items, { placeholder, labelFor }) {
  const current = select.value;
  select.innerHTML = "";

  const placeholderOption = document.createElement("option");
  placeholderOption.value = "";
  placeholderOption.textContent = placeholder;
  if (select.required) placeholderOption.disabled = true;
  select.append(placeholderOption);

  for (const item of items) {
    const option = document.createElement("option");
    option.value = item.id;
    option.textContent = labelFor(item);
    select.append(option);
  }

  if ([...select.options].some((o) => o.value === current)) select.value = current;
  else placeholderOption.selected = true;
}

export function setFormMessage(el, text, type) {
  el.textContent = text;
  el.className = `form-message ${type ?? ""}`.trim();
}

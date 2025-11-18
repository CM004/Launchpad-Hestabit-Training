// simple todo with localStorage (title-based lookup)
let tasks = JSON.parse(localStorage.getItem("tasks")) || [];

const save = () => localStorage.setItem("tasks", JSON.stringify(tasks));

function render() {
  const list = document.querySelector(".list");
  list.innerHTML = tasks.map(t =>
    `<li class="item">
      <span class="${t.done ? "done" : ""}">${t.title}</span>
      <div class="actions">
        <button onclick="toggleDone(this)">Done</button>
        <button onclick="editTask(this)">Edit</button>
        <button onclick="removeTask(this)">Delete</button>
      </div>
    </li>`).join("");
}

// add
function addTask() {
  const input = document.querySelector(".form-input");
  const text = input.value.trim();
  if (!text) return;
  tasks.push({ title: text, done: false });
  save();
  render();
  input.value = "";
}

// remove
function removeTask(btn) {
  const li = btn.closest(".item");
  const title = li.querySelector("span").innerText;
  tasks = tasks.filter(t => t.title !== title);
  save();
  render();
}

// toggle done
function toggleDone(btn) {
  const li = btn.closest(".item");
  const span = li.querySelector("span");
  const title = span.innerText;
  span.classList.toggle("done");
  const idx = tasks.findIndex(t => t.title === title);
  if (idx !== -1) {
    tasks[idx].done = span.classList.contains("done");
    save();
  }
}

// edit (store original title on <li> before editing)
function editTask(btn) {
  const li = btn.closest(".item");
  const span = li.querySelector("span");

  if (btn.innerText === "Edit") {
    li.dataset.old = span.innerText;      // store original
    btn.innerText = "Save";
    span.contentEditable = "true";
    span.focus();
  } else {
    btn.innerText = "Edit";
    span.contentEditable = "false";

    const oldTitle = li.dataset.old;
    const newTitle = span.innerText.trim();
    if (!newTitle) { span.innerText = oldTitle; return; }

    const i = tasks.findIndex(t => t.title === oldTitle);
    if (i !== -1) { tasks[i].title = newTitle; save(); }
    render();
  }
}

// handlers
document.querySelector(".form-btn").addEventListener("click", e => { e.preventDefault(); addTask(); });
document.querySelector(".form-input").addEventListener("keydown", e => { if (e.key === "Enter") { e.preventDefault(); addTask(); } });

// initial render
render();

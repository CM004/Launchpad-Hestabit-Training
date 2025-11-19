// Minimal selectors
const productsList = document.getElementById("products");
const status = document.getElementById("status");
const search = document.getElementById("search");
const sort = document.getElementById("sort");

let products = [];

// Clear list + status
const clear = () => {
  productsList.innerHTML = "";
  status.textContent = "";
};

// Show a message
const showMsg = (txt) => {
  clear();
  status.textContent = txt;
};

// Create a product card
function addCard(p) {
  const li = document.createElement("li");
  li.className = "product-item";
  li.innerHTML = `
    <div class="card">
      <img src="${p.images?.[0] || p.thumbnail || ''}" alt="">
      <h3 class="product-title">${p.title}</h3>
      <p class="product-price">$${p.price}</p>
    </div>`;
  productsList.appendChild(li);
}

// Render many products
function render(list) {
  clear();
  if (!list.length) return showMsg("No products found.");
  list.forEach(addCard);
}

// Simple debounce
function debounce(fn, time = 300) {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), time);
  };
}

// Search (debounced)
const doSearch = debounce((text) => {
  const q = text.toLowerCase();
  const filtered = products.filter(p => p.title.toLowerCase().includes(q));
  render(filtered);
}, 300);

// Sort high → low
function sortHigh() {
  const sorted = [...products].sort((a, b) => b.price - a.price);
  render(sorted);
}

// Fetch products
async function load() {
  try {
    showMsg("Loading products…");
    const res = await fetch("https://dummyjson.com/products");
    const data = await res.json();
    products = data.products;
    render(products);
  } catch (err) {
    showMsg("Failed to load products.");
    console.error(err);
  }
}

// Event listeners
search.addEventListener("input", e => doSearch(e.target.value));
sort.addEventListener("change", sortHigh);

// Start
load();

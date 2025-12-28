const userId = localStorage.getItem("user_id");

const API_BASE = window.location.origin;

let currentQuery = localStorage.getItem("last_query") || "";

document.getElementById("searchQuery").value = currentQuery;

async function performSearch(query, filters = {}) {
  try {
    const user = await (await fetch(`/user/${userId}`)).json();
    const linked_sites = user.linked_sites || [];

    // sanitize filters
    const price = parseInt(document.getElementById("maxPrice").value);
    const safeFilters = {
      max_price: isNaN(price) ? undefined : price,
      color: document.getElementById("colorFilter").value || undefined,
      max_delivery_date: document.getElementById("maxDelivery").value || undefined
    };

    const res = await fetch("/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, linked_sites, filters: safeFilters })
    });
    const results = await res.json();
    const ul = document.getElementById("searchResults");
    ul.innerHTML = "";
    results.forEach(item => {
      const li = document.createElement("li");
      li.innerHTML = `<b>${item.title}</b> - ₹${item.price} - ${item.platform}<br>
        Color: ${item.color} | Delivery: ${item.delivery_date} <br>
        <a href="${item.url}" target="_blank">View</a>`;
      ul.appendChild(li);
    });
  } catch (err) {
    alert("Something went wrong. Please try again.");
  }
}

function searchNow() {
  currentQuery = document.getElementById("searchQuery").value;
  localStorage.setItem("last_query", currentQuery);
  performSearch(currentQuery);
}

function applyFilters() {
  performSearch(currentQuery);
}

function goHome() {
  window.location.href = "home.html";
}

// On load
performSearch(currentQuery);

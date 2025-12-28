// SIGNUP

const API_BASE = "";

document.getElementById("signupForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const sites = Array.from(document.querySelectorAll(".site:checked")).map(i => i.value);
  const body = {
    email: email.value,
    password: password.value,
    linked_sites: sites
  };
  const res = await fetch(`/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  const data = await res.json();
  if (res.ok) {
    alert(data.msg || "Signed up!");
    window.location.href = "login.html";
  } else {
    alert(data.msg || "Signup failed.");
  }
});

// LOGIN
document.getElementById("loginForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const res = await fetch(`/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email: email.value,
      password: password.value
    })
  });
  const data = await res.json();
  if (data.user_id) {
    localStorage.setItem("user_id", data.user_id);
    window.location.href = "home.html";
  } else {
    alert(data.msg || "Login failed");
  }
});
const userId = localStorage.getItem("user_id");

const API_BASE = "";

// Upload image and get dress descriptions
async function uploadImages() {
  const files = document.getElementById("imageUpload").files;
  if (files.length === 0) return alert("Please select image(s)");

  const spinner = document.getElementById("uploadSpinner");
  const btn = document.getElementById("uploadBtn");
  spinner.classList.add("spinning");
  btn.disabled = true;

  const formData = new FormData();
  for (const f of files) {
    if (!f.type.startsWith("image/")) {
      alert("Only image files allowed.");
      spinner.classList.remove("spinning");
      btn.disabled = false;
      return;
    }
    formData.append("images", f);
  }

  try {
    console.log("Uploading to: ", `/image/upload/${userId}`);
    const res = await fetch(`/image/upload/${userId}`, {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
        console.log("Res not okay!")
        let errorText = "Unknown error";
        try {
            const err = await res.json();
            errorText = err.error || JSON.stringify(err);
        } catch (_) {}
        alert("Upload error: " + errorText);
        return;
    }

    console.log("Res okay!")
    const data = await res.json();
    alert("Descriptions added: " + data.descriptions.join(", "));
    loadRecommendations();

  } catch (err) {
    console.log("Caught JS error: ", err);
  } finally {
    spinner.classList.remove("spinning");
    btn.disabled = false;
  }
}

// Go to profile
function goProfile() {
  window.location.href = "profile.html";
}

function gotofeed() {
  window.location.href = "feed.html";
}

function logout() {
  localStorage.removeItem("user_id");
  window.location.href = "login.html";
}

function gotorec() {
  window.location.href = "rec.html";
}
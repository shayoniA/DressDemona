const userId = localStorage.getItem("user_id");

// Upload image and get dress descriptions
async function uploadImages() {
  const files = document.getElementById("imageUpload").files;
  if (files.length === 0) return alert("Please select image(s)");

  const formData = new FormData();
  for (const f of files) {
    if (!f.type.startsWith("image/")) {
      alert("Only image files allowed.");
      return;
    }
    formData.append("images", f);
  }

  try {
    console.log("Uploading to: ", `http://127.0.0.1:5000/image/upload/${userId}`);
    const res = await fetch(`http://127.0.0.1:5000/image/upload/${userId}`, {
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
const userId = localStorage.getItem("user_id");

function convertToLocalUrl(originalPath) {
  const keyword = "buyfast";
  const baseUrl = "http://127.0.0.1:5500";

  const startIndex = originalPath.indexOf(keyword);
  if (startIndex === -1) {
    console.error("The keyword 'buyfast' was not found in the path.");
    return originalPath;
  }

  const newPath = originalPath.substring(startIndex + keyword.length);
  const finalUrl = baseUrl + newPath.replace(/\\/g, "/"); // normalize slashes
  return finalUrl;
}

async function loadProfile() {
  const res = await fetch(`http://127.0.0.1:5000/user/${userId}`);
  const data = await res.json();
  const details = document.getElementById("mydetailsdiv");
  details.innerHTML = `EMAIL - ${data.email}`;
  const container = document.getElementById("postsDiv");
  const container2 = document.getElementById("likesDiv");
  const imagePaths = data.post_images;
  const likesPaths = data.likes;
  if (!imagePaths || imagePaths.length === 0) {
    const noPosts = document.createElement("p");
    noPosts.innerText = "-----";
    noPosts.style.textAlign = "center";
    noPosts.style.color = "#ffffff";
    noPosts.style.position = "relative";
    noPosts.style.right = "15px";
    container.appendChild(noPosts);
  } else {
    for (let i = 0; i < imagePaths.length; i++) {
      console.log("This is the image path: ", convertToLocalUrl(imagePaths[i]));
      const img = document.createElement("img");
      img.src = convertToLocalUrl(imagePaths[i]);
      img.alt = `Image ${i + 1}`;
      img.style.width = "187px";
      img.style.margin = "10px";
      container.appendChild(img);
      img.classList.add("postImages");
    }
  }
  if (!likesPaths || likesPaths.length === 0) {
    const noLikes = document.createElement("p");
    noLikes.innerText = "-----";
    noLikes.style.textAlign = "center";
    noLikes.style.color = "#ffffff";
    noLikes.style.position = "relative";
    noLikes.style.right = "15px";
    container2.appendChild(noLikes);
  } else {
    for (let i = 0; i < likesPaths.length; i++) {
      console.log("This is the image path: ", convertToLocalUrl(likesPaths[i]));
      const img2 = document.createElement("img");
      img2.src = convertToLocalUrl(likesPaths[i]);
      img2.alt = `Like ${i + 1}`;
      img2.style.width = "187px";
      img2.style.margin = "10px";
      container2.appendChild(img2);
      img2.classList.add("postImages");
    }
  }
}

function goHome() {
  window.location.href = "home.html";
}

loadProfile();

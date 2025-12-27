const userId = localStorage.getItem("user_id");
let currentIndex = 0;
let images = [];

async function fetchFeed() {
    try {
        const userRes = await fetch(`http://127.0.0.1:5000/user/${userId}`);
        const userData = await userRes.json();
        userLikes = userData.likes || [];

        const response = await fetch(`http://127.0.0.1:5000/feed/${userId}`);
        const data = await response.json();
        console.log("This is the feed data:  ", data.feed);
        images = data.feed;

        if (images.length === 0) {
            document.getElementById("main-image").alt = "No images to show.";
            return;
        }

        const otherUserId = images[currentIndex].user_id;
        if(otherUserId != userId)
            displayImage(currentIndex, otherUserId);
    } catch (error) {
        console.error("Error fetching feed:", error);
    }
}

function getPathAfterUploads(fullPath) {
    const normalized = fullPath.replace(/\\/g, "/");
    const parts = normalized.split("uploads/");
    return parts.length > 1 ? parts[1] : null;
}

function convertForMatch(path) {
    return path.replace(/\//g, "\\");
}

async function updateUpvoteButtonColor(imagePath) {
    const upvoteBtn = document.getElementById("upvote-btn");
    const user_me = await fetch(`http://127.0.0.1:5000/user/${userId}`);
    const data_me = await user_me.json();
    console.log("Real string of like: ", data_me.likes[0]);
    if(data_me.likes.includes(convertForMatch(imagePath)))
        upvoteBtn.style.color = "rgb(187, 9, 83)";
    else
        upvoteBtn.style.color = "white";
}

async function displayImage(index, otherUserId) {
    const imgElement = document.getElementById("main-image");
    const username = document.getElementById("user_name");
    imgElement.src = `../../../uploads/${getPathAfterUploads(images[index].image)}`;
    const res_ponse = await fetch(`http://127.0.0.1:5000/user/${otherUserId}`);
    const da_ta = await res_ponse.json();
    username.textContent = da_ta.email+" ⫷";
    const currentImagePath = images[index].image.replace(/\\/g, "/");
    console.log("Real string of imagepath: ", currentImagePath);
    updateUpvoteButtonColor(currentImagePath);
}

document.getElementById("left-arrow").addEventListener("click", () => {
    if (images.length === 0) return;
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    const otherUserId = images[currentIndex].user_id;
    displayImage(currentIndex, otherUserId);
});

document.getElementById("right-arrow").addEventListener("click", () => {
    if (images.length === 0) return;
    currentIndex = (currentIndex + 1) % images.length;
    const otherUserId = images[currentIndex].user_id;
    displayImage(currentIndex, otherUserId);
});

document.getElementById("upvote-btn").addEventListener("click", async () => {
    const upvoteBtn = document.getElementById("upvote-btn");
    upvoteBtn.style.color = "rgb(187, 9, 83)";

    if (images.length === 0) return;
    const postIndex = images[currentIndex].post_index;
    const postUserId = images[currentIndex].user_id;
    const upvoterId = localStorage.getItem("user_id");

    if(!upvoterId) {
        alert("Please log in to upvote.");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/upvote/${postUserId}/${postIndex}?upvoter_id=${upvoterId}`, {
            method: "POST"
        });
        const data = await response.json();
        if (response.ok) {
            images[currentIndex].upvotes += 1;
            document.getElementById("upvote-count").textContent = images[currentIndex].upvotes;
            const imgPath = images[currentIndex].image.replace(/\\/g, "/");
            userLikes.push(imgPath);
            updateUpvoteButtonColor(imgPath);
            console.log("Upvoted successfully!");
        }
    } catch (error) {
        console.error("Upvote failed:", error);
    }
});

// Run on page load
fetchFeed();

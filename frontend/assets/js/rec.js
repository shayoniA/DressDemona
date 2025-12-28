const loader = document.getElementById("loader");

const API_BASE = "";

function showLoader() {
  loader.style.display = "flex";
}

function hideLoader() {
  loader.style.display = "none";
}






const userId = localStorage.getItem("user_id");

function truncateText(text, n) {
  return text.length > n ? text.slice(0, n) + '...' : text;
}

const logoMap = {
  // flipkart: "./assets/images/fkLogo.jpg",
  amazon: "./assets/images/amazonLogo.jpg",
  zara: "./assets/images/zaraLogo.jpg",
  // hm: "./assets/images/hmLogo.png"
};

function filterRecommendations(rec) {
  // if(rec.recommendations.Flipkart) {
  //   const flipkartData = rec.recommendations.Flipkart;
  //   const withTitle = flipkartData.filter(item => item.title && item.title.trim() !== '');
  //   const withoutTitle = flipkartData.filter(item => !item.title || item.title.trim() === '');
  //   let finalList;
  //   if (withTitle.length > 5)
  //     finalList = withTitle.slice(0, 5);
  //   else {
  //     const x = withTitle.length;
  //     finalList = withTitle.concat(withoutTitle.slice(0, (5-x)));
  //   }
  //   finalList = finalList.map(item => {
  //     if (!item.title || item.title.trim() === '') {
  //       return { ...item, title: "Featured Product by Flipkart" };
  //     }
  //     return item;
  //   });
  //   rec.recommendations.Flipkart = finalList;
  // }

  // if(rec.recommendations.HM) {
  //   const hmData = rec.recommendations.HM;
  //   const withTitleH = hmData.filter(item => !item.image || !item.image.includes('gif'));
  //   const withoutTitleH = hmData.filter(item => item.image && item.image.includes('gif'));

  //   let finalListH;
  //   if (withTitleH.length > 5)
  //     finalListH = withTitleH.slice(0, 5);
  //   else {
  //     const x = withTitleH.length;
  //     finalListH = withTitleH.concat(withoutTitleH.slice(0, (5-x)));
  //   }
  //   finalListH = finalListH.map(item => {
  //     if (!item.title || item.title.trim() === '') {
  //       return { ...item, title: "Featured Product by H&M" };
  //     }
  //     return item;
  //   });
  //   rec.recommendations.HM = finalListH;
  // }

  if(rec.recommendations.Amazon) {
    const amazonData = rec.recommendations.Amazon;
    const withTitleA = amazonData.filter(item => item.title && item.title.trim() !== '');
    const withoutTitleA = amazonData.filter(item => !item.title || item.title.trim() === '');
    let finalListA;
    if (withTitleA.length > 5)
      finalListA = withTitleA.slice(0, 5);
    else {
      const xA = withTitleA.length;
      finalListA = withTitleA.concat(withoutTitleA.slice(0, (5-xA)));
    }
    finalListA = finalListA.map(item => {
      if (!item.title || item.title.trim() === '') {
        return { ...item, title: "Featured Product by Ajio" };
      }
      return item;
    });
    rec.recommendations.Amazon = finalListA;
  }

  if(rec.recommendations.Zara) {
    const zaraData = rec.recommendations.Zara;
    const withTitleZ = zaraData.filter(item => !item.image || !item.image.includes('transparent'));
    const withoutTitleZ = zaraData.filter(item => item.image && item.image.includes('transparent'));
    let finalListZ;
    if (withTitleZ.length > 5)
      finalListZ = withTitleZ.slice(0, 5);
    else {
      const xZ = withTitleZ.length;
      finalListZ = withTitleZ.concat(withoutTitleZ.slice(0, (5-xZ)));
    }
    finalListZ = finalListZ.map(item => {
      if (!item.title || item.title.trim() === '') {
        return { ...item, title: "Featured Product by Zara" };
      }
      return item;
    });
    rec.recommendations.Zara = finalListZ;
  }
  
  return rec;
}

function removeAfterDot(str) {
  return str.split('.')[0];
}

function extractNumbersOnly(input) {
  const str = removeAfterDot(input);
  const str1 = str.replace(/[^0-9,]/g, '');
  return ("₹ "+str1);
}

async function loadRecommendations() {
  showLoader();
  try {
    console.log("Trying to get recommendations...");
    const res = await fetch(`/user/recommendations/${userId}`, {
      method: "POST",
    });
    if (!res.ok) {
      console.log("Res not okay 222");
      alert("Failed to fetch recommendations");
      return;
    }
    console.log("Res okay 222");
    const unfiltered_data = await res.json();
    const data = filterRecommendations(unfiltered_data);
    console.log(data);
    const recDiv = document.getElementById("recdiv");
    recDiv.innerHTML = "";

    ["Zara", "Amazon"].forEach(site => {
      const items = data.recommendations[site];
      if (!items) return;
      const logoImg = document.createElement("img");
      logoImg.src = logoMap[site.toLowerCase()] || "";
      logoImg.alt = site;
      logoImg.classList.add("site-logo");
      recDiv.appendChild(logoImg);

      items.forEach((item, index) => {
        const card = document.createElement("div");
        card.style.padding = "10px";
        card.style.display = "inline-block";
        card.style.width = "180px";
        card.classList.add("onecard");
        if (index === 0)
          card.classList.add("firstcard");

        const img = document.createElement("img");
        img.src = item.image;
        img.style.width = "100%";
        card.appendChild(img);
        img.classList.add("cardimages");

        const name = document.createElement("h4");
        name.innerText = truncateText(item.title, 50);
        card.appendChild(name);
        name.classList.add("cardnames");

        const price = document.createElement("p");
        price.innerText = extractNumbersOnly(item.price);
        card.appendChild(price);
        price.classList.add("cardprices");

        recDiv.appendChild(card);
      });
    });
  } catch (err) {
    console.error("Error fetching recommendations:", err);
    alert("Error fetching recommendations");
  } finally {
    hideLoader();
  }
}

function logout() {
  localStorage.removeItem("user_id");
  window.location.href = "login.html";
}

// Trigger default load
loadRecommendations();
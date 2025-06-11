// window.onload = function () {
//     window.focus(); // Ensure the window is focused
//     document.body.scrollTop = 0; // Reset the scroll position to the top
//     document.documentElement.scrollTop = 0;
// };

function sendMessageToWhatsApp(propertyName, location, phoneNumber) {
  // console.log('sirrrathyhhhhhhh');

  const message = `Hello, I am interested in the property from buysel.in "${propertyName}" located in "${location}". Please provide more details.`;
  const encodedMessage = encodeURIComponent(message); // Ensures the message is URL-safe
  const whatsappUrl = `https://api.whatsapp.com/send?phone=${phoneNumber}&text=${encodedMessage}`;
  window.open(whatsappUrl, "_blank");
}

document.addEventListener("DOMContentLoaded", () => {
  console.log("haiiiiiii", location.href);
  if (location.href.includes("agent")) {
    handleNavbarActive("agent-nav");
  } else if (location.href.includes("about")) {
    handleNavbarActive("about-nav");
  } else if (location.href.includes("service")) {
    handleNavbarActive("service-nav");
  } else if (location.href.includes("properties")) {
    handleNavbarActive("properties-nav");
  } else if (location.href.includes("features")) {
    handleNavbarActive("features-nav");
  } else {
    handleNavbarActive("home-nav");
  }
});

function handleNavbarActive(tab) {
  const tabElement = document.getElementById(tab);
  const allTabs = document.getElementsByClassName("nav-option-li");

  // Reset styles for all tabs
  for (let i = 0; i < allTabs.length; i++) {
    allTabs[i].style.textDecoration = "none";
    allTabs[i].style.textUnderlineOffset = "";
    allTabs[i].style.borderRadius = "";
    allTabs[i].style.color = "";
    allTabs[i].style.textDecorationThickness = "";
  }

  // Apply styles to the selected tab
  tabElement.style.textDecoration = "underline";
  tabElement.style.textUnderlineOffset = "10px";
  tabElement.style.borderRadius = "5px";
  tabElement.style.color = "#8bc83f";
  tabElement.style.textDecorationThickness = "3px";
}

document.addEventListener("DOMContentLoaded", eventFunction);

function createNewImageDiv(idNo, array, index, mobile) {
  if (mobile) {
    const imageSection = document.querySelector(".image-section-mobile");
    const newDiv = document.createElement("img");
    newDiv.className = "image-box-mobile";

    newDiv.id = `box-mobile${idNo}`;

    newDiv.style.height = "100%";
    newDiv.style.width = "0";
    newDiv.src = `${array[index]}`;
    newDiv.style.objectFit = "cover";
    newDiv.style.objectPosition = "center";

    imageSection.appendChild(newDiv);
  } else {
    const imageSection = document.querySelector(".image-section");
    const newDiv = document.createElement("img");
    newDiv.className = "image-box";
    newDiv.id = `box${idNo}`;
    newDiv.style.height = "100%";
    newDiv.style.width = "0";
    newDiv.src = `${array[index]}`;
    newDiv.style.objectFit = "cover";
    newDiv.style.objectPosition = "center";
    // newDiv.style.backgroundRepeat = 'no-repeat'

    imageSection.appendChild(newDiv);
  }
}

function eventFunction() {
  let imageCount = 0;
  let imageIndex = 0;

  if (window.screen.width < 1336) {
    setInterval(() => {
      const images = [
        "static/img/10p.jpg",
        "static/img/11p.jpg",
        "static/img/9p.jpg",
      ];

      const imageArray = document.querySelectorAll(".image-box-mobile");

      imageArray[imageCount].style.width = 0;
      imageArray[imageCount].style.marginLeft = 0;
      imageArray[imageCount + 1].style.width = "15.5rem";
      imageArray[imageCount + 1].style.marginLeft = "5px";
      imageArray[imageCount + 2].style.width = "5.5rem";
      imageArray[imageCount + 3].style.width = "2.375rem";
      createNewImageDiv(imageCount + 4, images, imageIndex, true);

      imageCount++;

      if (imageIndex == 2) {
        imageIndex = 0;
      } else {
        imageIndex++;
      }
    }, 2000);
  } else {
    setInterval(() => {
      const images = [
        "static/img/10p.jpg",
        "static/img/11p.jpg",
        "static/img/9p.jpg",
      ];

      const imageArray = document.querySelectorAll(".image-box");

      imageArray[imageCount].style.width = 0;
      imageArray[imageCount].style.marginLeft = 0;
      imageArray[imageCount + 1].style.width = "22.5rem";
      imageArray[imageCount + 2].style.width = "12.5rem";
      imageArray[imageCount + 3].style.width = "9.375rem";
      createNewImageDiv(imageCount + 4, images, imageIndex, false);

      imageCount++;

      if (imageIndex == 2) {
        imageIndex = 0;
      } else {
        imageIndex++;
      }
    }, 2000);
  }
}

// Cache elements to avoid repeated DOM queries
const buttons = document.querySelectorAll(".filter-btn");
const cards = document.querySelectorAll(".card");
const noPropMessage = document.getElementById("no-property-message");

function filterProperties(category) {
  // --- Instantly Update Active State of Filter Buttons ---
  buttons.forEach((button) => {
    button.classList.remove("active");
  });

  // Get the clicked button and activate it immediately
  const activeButton = document.querySelector(
    `.filter-btn[data-category="${category}"]`
  );
  if (activeButton) {
    activeButton.classList.add("active");

    // ✅ Force the browser to apply the style update immediately
    activeButton.offsetHeight; // Triggers a reflow

    // ✅ Prevent hover from overriding active state
    activeButton.classList.add("clicked");
  }

  // --- Use requestAnimationFrame to Optimize Filtering ---
  requestAnimationFrame(() => {
    let visibleCount = 0;

    cards.forEach((card) => {
      let isVisible =
        category === "all" || card.getAttribute("data-category") === category;

      // ✅ Ensure cards update smoothly
      card.style.opacity = isVisible ? "1" : "0";
      card.style.visibility = isVisible ? "visible" : "hidden";
      card.style.position = isVisible ? "relative" : "absolute";

      if (isVisible) visibleCount++;
    });

    // --- Show/Hide "No Properties Found" Message ---
    noPropMessage.style.display = visibleCount === 0 ? "block" : "none";
  });
}

// document.getElementById('navbar-toggle').addEventListener('click', function () {
//     var navOptions = document.getElementById('nav-options');
//     navOptions.classList.toggle('active');
//   });

let isNavOpened = false;

function handleToggle() {
  console.log("haaaaaahaaa");

  var navOptions = document.getElementById("mobile-navbar");
  const bar1 = document.getElementById("bar1");
  const bar2 = document.getElementById("bar2");
  const bar3 = document.getElementById("bar3");

  if (isNavOpened) {
    navOptions.style.marginTop = "-100vh";
    isNavOpened = false;
    bar1.style.transform = "rotate(0deg)";
    bar2.style.transform = "rotate(0deg)";
    bar3.style.display = "block";
    bar1.style.marginBottom = "4px";
  } else {
    navOptions.style.marginTop = "0";
    isNavOpened = true;
    bar1.style.transform = "rotate(45deg)";
    bar2.style.transform = "rotate(-45deg)";
    bar3.style.display = "none";
    bar1.style.marginBottom = "-4px";
  }
}

function handleImage(media, url) {
  console.log(url, "urlll");

  const shareUrl = url;
  const message =
    "Looking to buy or sell property? buysel.in offers great deals for buyers and quick listings for sellers. Find homes, apartments, and commercial spaces at the best prices.";

  if (media == "whatsapp") {
    const whatsappUrl = `https://wa.me/?text=${encodeURIComponent(
      message + " " + shareUrl
    )}`;
    window.open(whatsappUrl, "_blank");
  } else if (media == "fb") {
    const facebookUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(
      shareUrl
    )}`;
    window.open(facebookUrl, "_blank");
  } else if (media == "x") {
    const twitterUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(
      shareUrl
    )}&text=${encodeURIComponent(message)}`;
    window.open(twitterUrl, "_blank");
  } else if (media == "linkedin") {
    const linkedinUrl = `https://www.linkedin.com/shareArticle?mini=true&url=${encodeURIComponent(
      shareUrl
    )}&title=${encodeURIComponent(message)}`;
    window.open(linkedinUrl, "_blank");
  } else {
    const telegramUrl = `https://t.me/share/url?url=${encodeURIComponent(
      shareUrl
    )}&text=${encodeURIComponent(message)}`;
    window.open(telegramUrl, "_blank");
  }
}

function controlShareButton(id) {
  console.log(id, "this is id");

  var modal = document.getElementById(`share-btn-modal-${id}`);

  const allModal = document.querySelectorAll(".modal");

  allModal.forEach((element) => {
    console.log(element);

    element.style.display = "none";
  });

  modal.style.display = "block";
}

function handleModalClose(id) {
  const closingModal = document.getElementById(`share-btn-modal-${id}`);
  closingModal.style.display = "none";
}

function captureScreenshotAndUpload(elementId, objectId, modelName) {
  let element = document.getElementById(elementId);

  if (!element) {
    console.error("Element not found:", elementId);
    return;
  }

  html2canvas(element).then((canvas) => {
    canvas.toBlob((blob) => {
      let formData = new FormData();
      formData.append("screenshot", blob, "screenshot.png");
      formData.append("object_id", objectId);
      formData.append("model_name", modelName);

      fetch("/save-screenshot/", {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            console.log("Screenshot uploaded successfully!");
          } else {
            console.error("Upload failed:", data.error);
          }
        })
        .catch((error) => console.error("Error:", error));
    }, "image/png");
  });
}

// CSRF token helper function (needed for Django)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    document.cookie.split(";").forEach((cookie) => {
      let trimmedCookie = cookie.trim();
      if (trimmedCookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(
          trimmedCookie.substring(name.length + 1)
        );
      }
    });
  }
  return cookieValue;
}

// function handleSession() {
//   console.log("worked...");

//   localStorage.setItem("sample", "nmeapp");

//   const username = document.getElementById('username-agent')
//   const password = document.getElementById('password-agent')

//   console.log(username,password,'passworededd');

//     fetch("agentslogin", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({ username: username.value, password: password.value}),
//     })
//       .then((response) => response.json())
//       .then((data) => console.log(data))
//       .catch((error) => console.error("Error:", error));
// }

function handleSession(event) {
  event.preventDefault(); // stops default form submission

  console.log("worked...");

  const username = document.getElementById("username-agent").value;
  const password = document.getElementById("password-agent").value;

  console.log("Username:", username);
  console.log("Password:", password);

  const ratelimit = localStorage.getItem("ratelimit");

  //  localStorage.setItem('ratelimit',0)

  const lastFailedTimeStr = localStorage.getItem("lastFailed");

  if (lastFailedTimeStr && ratelimit && ratelimit >= 5) {
    // Parse the stored time into a Date object
    const lastFailedTime = new Date(lastFailedTimeStr);

    // Add 2 hours to the stored time
    const twoHoursLater = new Date(lastFailedTime.getTime() + 2 * 60 * 60 * 1000);

    // Get current time
    const currentTime = new Date();

    if (currentTime >= twoHoursLater) {
      localStorage.setItem("ratelimit", 0);

      fetch("http://127.0.0.1:8000/agents/agentslogin/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ username, password }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status == "error") {
            if (ratelimit <= 5) {
              localStorage.setItem("ratelimit", 1);
              localStorage.setItem("lastFailed", new Date().toISOString());
              alert("Wrong username or password");
            } else if (ratelimit) {
              localStorage.setItem("ratelimit", +ratelimit + 1);
              localStorage.setItem("lastFailed", new Date().toISOString());
            } else {
              localStorage.setItem("ratelimit", 0);
              localStorage.setItem("lastFailed", new Date().toISOString());
            }
          } else {
            localStorage.setItem("ratelimit", 0);
            localStorage.setItem("lastFailed", Date.now());
            window.location.href = data.redirect_url;
          }
          console.log("Response from server:", data);
        })
        .catch((error) => console.error("Error:", error));
    } else {
      alert("2 minitue ayilleda myreee");
    }
  } else {
    fetch("http://127.0.0.1:8000/agents/agentslogin/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ username, password }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status == "error") {
          if (ratelimit >= 5) {
            localStorage.setItem("ratelimit", 1);
            localStorage.setItem("lastFailed", new Date().toISOString());
            alert("Wrong username or password");
          } else if (ratelimit) {
            localStorage.setItem("ratelimit", +ratelimit + 1);
            localStorage.setItem("lastFailed", new Date().toISOString());
            alert("Wrong username or password");
          } else {
            localStorage.setItem("ratelimit", 0);
            localStorage.setItem("lastFailed", new Date().toISOString());
            alert("Wrong username or password");
          }
        } else {
          localStorage.setItem("ratelimit", 0);
          localStorage.setItem("lastFailed", Date.now());
          window.location.href = data.redirect_url;
        }
        console.log("Response from server:", data);
      })
      .catch((error) => console.error("Error:", error));
  }
}

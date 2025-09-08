
// document.addEventListener("contextmenu", function(e){
//         e.preventDefault();
//     });

//     document.onkeydown = function(e) {
//         if (e.keyCode == 123) { 
//             return false;
//         }
//         if (e.ctrlKey && e.shiftKey && (e.keyCode == 'I'.charCodeAt(0) ||
//                                         e.keyCode == 'J'.charCodeAt(0) ||
//                                         e.keyCode == 'C'.charCodeAt(0))) {
//             return false;
//         }
//         if (e.ctrlKey && (e.keyCode == 'U'.charCodeAt(0))) { 
//             return false;
//         }
//     };








// property card in home page 


  function toggleSidebar() {
    const sidebar = document.getElementById("sidebarFilter");
    sidebar.classList.toggle("translate-x-full");
  }

  function filterCards(type, button) {
    const cards = document.querySelectorAll('.property-card');
    const noResultsMsg = document.getElementById('no-results-msg');
    let matchCount = 0;

    cards.forEach(card => {
      const cardType = card.getAttribute('data-type');
      if (type === 'all' || cardType === type) {
        card.classList.remove('hidden');
        matchCount++;
      } else {
        card.classList.add('hidden');
      }
    });

   
    const allButtons = document.querySelectorAll('.filter-btn');
    allButtons.forEach(btn => {
      btn.classList.remove('bg-[#8bc83f]', 'text-white');
      btn.classList.add('bg-gray-100', 'text-gray-700');
    });
    button.classList.remove('bg-gray-100', 'text-gray-700');
    button.classList.add('bg-[#8bc83f]', 'text-white');

   
    if (matchCount === 0) {
      noResultsMsg.classList.remove('hidden');

      cards.forEach(card => card.classList.remove('hidden'));
    } else {
      noResultsMsg.classList.add('hidden');
    }
  }





// list view of property card

 function toggleViewMode() {

      document.querySelectorAll('.property-card').forEach(el => el.classList.toggle('hidden'));
      document.querySelectorAll('.list-view').forEach(el => el.classList.toggle('hidden'));
    }







  const images = [
    './static/images/demo.png',
    './static/images/about1.png',
    './static/images/addproperty.png'
  ];

  const imageEl = document.getElementById('propertyImage');
  const dots = document.querySelectorAll('.dot');

  function changeImage(index) {
    imageEl.src = images[index];

    // Reset all dots
    dots.forEach(dot => {
      dot.classList.remove('w-1.5', 'h-1.5', 'opacity-100');
      dot.classList.add('w-1.5', 'h-1.5', 'opacity-70');
    });

    // Highlight active dot
    dots[index].classList.remove('w-1.5', 'h-1.5', 'opacity-70');
    dots[index].classList.add('w-2', 'h-2', 'opacity-100');
  }

  // Load first image by default
  window.onload = () => changeImage(0);



  // faq

   document.querySelectorAll('.faq-toggle').forEach(button => {
    button.addEventListener('click', () => {
      const answer = button.nextElementSibling;
      const icon = button.querySelector('svg');

      // Close all other answers
      document.querySelectorAll('.faq-toggle').forEach(btn => {
        if (btn !== button) {
          btn.nextElementSibling.classList.add('hidden');
          btn.querySelector('svg').classList.remove('rotate-180');
        }
      });

      // Toggle current answer
      answer.classList.toggle('hidden');
      icon.classList.toggle('rotate-180');
    });
  });




  // toggle

   const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const closeMenuBtn = document.getElementById('close-menu');
  const mobileMenu = document.getElementById('mobile-menu');

  mobileMenuBtn.addEventListener('click', () => {
    mobileMenu.classList.remove('translate-x-full');
  });

  closeMenuBtn.addEventListener('click', () => {
    mobileMenu.classList.add('translate-x-full');
  });















// 

function showMessageButton() {
      document.getElementById("floatMessageBtn").classList.remove("hidden");
    }

    function requestLocation() {
      document.getElementById("locationBox").classList.add("hidden");
      showMessageButton();

      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          position => {
            console.log("Lat:", position.coords.latitude, "Long:", position.coords.longitude);
          },
          error => {
            console.log("Location access denied or unavailable.");
          }
        );
      } else {
        alert("Geolocation is not supported by this browser.");
      }
    }

    function denyLocation() {
      document.getElementById("locationBox").classList.add("hidden");
      showMessageButton();
    }

    function openMessageModal() {
  const modal = document.getElementById("messageModal");
  const content = document.getElementById("modalContent");

  modal.classList.remove("hidden");
  // Trigger animation
  setTimeout(() => {
    content.classList.remove("opacity-0", "scale-95");
    content.classList.add("opacity-100", "scale-100");
  }, 10);
}

function closeMessageModal() {
  const modal = document.getElementById("messageModal");
  const content = document.getElementById("modalContent");

  content.classList.remove("opacity-100", "scale-100");
  content.classList.add("opacity-0", "scale-95");

  // Wait for animation to finish before hiding modal
  setTimeout(() => {
    modal.classList.add("hidden");
  }, 300); // same as duration-300
}









// scrolling smooth 

function scrollToSection(event) {
  event.preventDefault();  // prevents the jump
  document.getElementById("properties").scrollIntoView({
    behavior: "smooth"
  });
}

// property form modal

 function openPropertyModal() {
    document.getElementById("propertyModal").classList.remove("hidden");
  }

  function closePropertyModal() {
    document.getElementById("propertyModal").classList.add("hidden");
  }

// agent form modal

 function openAgentModal() {
    document.getElementById('agentModal').classList.remove('hidden');
  }

  function closeAgentModal() {
    document.getElementById('agentModal').classList.add('hidden');
  }







    // blogs


  function openModal() {
  document.getElementById('blogModal').classList.remove('hidden');
  document.body.classList.add('overflow-hidden');
}

function closeModal() {
  document.getElementById('blogModal').classList.add('hidden');
  document.body.classList.remove('overflow-hidden');
}




// agents scrolling in home page
function scrollAgents(direction) {
    const container = document.querySelector('.animate-marquee');
    const scrollAmount = 150;
    container.parentElement.scrollBy({
      left: direction === 'left' ? -scrollAmount : scrollAmount,
      behavior: 'smooth'
    });
  }


// learn more content

 function toggleContent() {
    const content = document.getElementById("extra-content");
    const btn = document.getElementById("toggle-btn");

    if (content.style.maxHeight && content.style.maxHeight !== "0px") {
      content.style.maxHeight = "0px";
      btn.innerText = "Learn more";
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
      btn.innerText = "Show less";
    }
  }


// share button for property

   const openBtn = document.getElementById('openShareModal');
  const closeBtn = document.getElementById('closeShareModal');
  const shareModal = document.getElementById('shareModal');

  openBtn.addEventListener('click', () => {
    shareModal.classList.remove('hidden');
  });

  closeBtn.addEventListener('click', () => {
    shareModal.classList.add('hidden');
  });

  // Optional: click outside to close
  window.addEventListener('click', (e) => {
    if (e.target === shareModal) {
      shareModal.classList.add('hidden');
    }
  });
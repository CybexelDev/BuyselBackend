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

















// Add Amenity Field (works for any container)
// function addAmenityField(value = "", containerId) {
//   const container = document.getElementById(containerId);

//   const wrapper = document.createElement("div");
//   wrapper.className = "flex items-center space-x-2";

//   const input = document.createElement("input");
//   input.type = "text";
//   input.placeholder = "Enter Amenity";
//   input.value = value;
//   input.className = "w-full border px-3 py-2 rounded";

//   const delBtn = document.createElement("button");
//   delBtn.type = "button";
//   delBtn.innerHTML = "&#10006;";
//   delBtn.className = "text-red-500 hover:text-red-700 text-lg font-bold px-2";
//   delBtn.onclick = () => wrapper.remove();

//   wrapper.appendChild(input);
//   wrapper.appendChild(delBtn);

//   container.appendChild(wrapper);
// }



// Add Amenity Field (works for any container)
function addAmenityField(value = "", containerId) {
  const container = document.getElementById(containerId);

  const wrapper = document.createElement("div");
  wrapper.className = "flex items-center space-x-2";

  const input = document.createElement("input");
  input.type = "text";
  input.name = "amenities";   // ✅ key point
  input.placeholder = "Enter Amenity";
  input.value = value;
  input.className = "w-full border px-3 py-2 rounded";

  const delBtn = document.createElement("button");
  delBtn.type = "button";
  delBtn.innerHTML = "&#10006;";
  delBtn.className = "text-red-500 hover:text-red-700 text-lg font-bold px-2";
  delBtn.onclick = () => wrapper.remove();

  wrapper.appendChild(input);
  wrapper.appendChild(delBtn);

  container.appendChild(wrapper);
}





// function openAdminPropertyEditModal(button) {
//   // Show modal
//   document.getElementById("editModal").classList.remove("hidden");

//   // Populate fields
//   document.getElementById("editCategory").value = button.dataset.category;
//   document.getElementById("editPurpose").value = button.dataset.purpose;
//   document.getElementById("editLabel").value = button.dataset.label;
//   document.getElementById("editArea").value = button.dataset.land_area;
//   document.getElementById("editSqft").value = button.dataset.sqft;
//   document.getElementById("editDesc").value = button.dataset.description;
//   document.getElementById("editPrice").value = button.dataset.price;
//   document.getElementById("editOwner").value = button.dataset.owner;
//   document.getElementById("editPhone").value = button.dataset.phone;
//   document.getElementById("editWhatsappNumber").value = button.dataset.whatsapp;
//   document.getElementById("editLocation").value = button.dataset.location;
//   document.getElementById("editCity").value = button.dataset.city;
//   document.getElementById("editDistrict").value = button.dataset.district;
//   document.getElementById("editPin").value = button.dataset.pincode;
//   document.getElementById("editLandmark").value = button.dataset.landmark;
//   document.getElementById("editPaid").value = button.dataset.paid;
//   document.getElementById("editAddedBy").value = button.dataset.added_by;
//   document.getElementById("editDuration").value = button.dataset.duration;

//   // Image preview
//   if (button.dataset.image) {
//     document.getElementById("editImagePreview").src = button.dataset.image;
//   }
// }

// function closeAdminPropertyEditModal() {
//   document.getElementById("editModal").classList.add("hidden");
// }






// function openEditModal(button) {
//   document.getElementById("editModal").classList.remove("hidden");

//   document.getElementById("editPropertyId").value = button.dataset.id;
//   document.getElementById("editCategory").value = button.dataset.category;
//   document.getElementById("editPurpose").value = button.dataset.purpose;
//   document.getElementById("editLabel").value = button.dataset.label;
//   document.getElementById("editLandArea").value = button.dataset.landArea;
//   document.getElementById("editSqft").value = button.dataset.sqft;
//   document.getElementById("editDesc").value = button.dataset.description;
//   document.getElementById("editPrice").value = button.dataset.perprice;
//   document.getElementById("editTotalPrice").value = button.dataset.price;
//   document.getElementById("editOwner").value = button.dataset.owner;
//   document.getElementById("editPhone").value = button.dataset.phone;
//   document.getElementById("editWhatsapp").value = button.dataset.whatsapp;
//   document.getElementById("editLocation").value = button.dataset.location;
//   document.getElementById("editCity").value = button.dataset.city;
//   document.getElementById("editDistrict").value = button.dataset.district;
//   document.getElementById("editPin").value = button.dataset.pincode;
//   document.getElementById("editLandmark").value = button.dataset.landmark;
//   document.getElementById("editPaid").value = button.dataset.paid;
//   document.getElementById("editAddedBy").value = button.dataset.addedBy;
//   document.getElementById("agentDuration").value = button.dataset.duration;

//   // amenities split
//   const amenitiesContainer = document.getElementById("formAmenitiesContainer");
//   amenitiesContainer.innerHTML = "";
//   if (button.dataset.amenities) {
//     button.dataset.amenities.split(",").forEach(am => {
//       addAmenityField(am.trim(), "formAmenitiesContainer");
//     });
//   }

//   // image preview
//   if (button.dataset.image) {
//     let preview = document.createElement("img");
//     preview.src = button.dataset.image;
//     preview.className = "w-32 h-24 object-cover border rounded mb-2";
//     amenitiesContainer.parentNode.insertBefore(preview, amenitiesContainer);
//   }

//   // ✅ set action to /edit/{id}/
//   document.getElementById("editPropertyForm").action = `/edit/${button.dataset.id}/`;
// }

// function closeEditModal() {
//   document.getElementById("editModal").classList.add("hidden");
// }







function addAgentAmenityField(type = "modal", value = "") {
  const containerId =
    type === "modal" ? "editAmenitiesContainer" : "agentFormAmenitiesContainer";
  const container = document.getElementById(containerId);
  if (!container) return;

  const wrapper = document.createElement("div");
  wrapper.className = "flex items-center space-x-2";

  const input = document.createElement("input");
  input.type = "text";
  input.placeholder = "Enter Amenity";
  input.value = value;
  input.className = "w-full border px-3 py-2 rounded";

  const delBtn = document.createElement("button");
  delBtn.type = "button";
  delBtn.innerHTML = "&#10006;";
  delBtn.className = "text-red-500 hover:text-red-700 text-lg font-bold px-2";
  delBtn.onclick = () => wrapper.remove();

  wrapper.appendChild(input);
  wrapper.appendChild(delBtn);
  container.appendChild(wrapper);
}

window.onload = () => {
  const formContainer = document.getElementById("agentFormAmenitiesContainer");
  if (formContainer && formContainer.children.length === 0) addAgentAmenityField("form");
};


function openAgentPropertyEditModal(button) {
  const row = button.closest("tr");
  const cells = row.querySelectorAll("td");

  const category   = cells[1].innerText;
  const purpose    = cells[2].innerText;
  const label      = cells[3].innerText;
  const area       = cells[4].innerText;
  const sqft       = cells[5].innerText;
  const desc       = cells[6].innerText;
  const amenitiesText = cells[7].innerText;
  const location   = cells[8].innerText;
  const landmark   = cells[9].innerText;
  const city       = cells[10].innerText;
  const district   = cells[11].innerText;
  const price      = cells[12].innerText;
  const totalPrice = cells[13].innerText;
  const phone      = cells[14].innerText;
  const whatsapp   = cells[15].innerText;
  const pinCode    = cells[16].innerText;
  const duration   = cells[17] ? cells[17].innerText : "";

  // Fill modal fields
  document.getElementById("editCategory").value = category;
  document.getElementById("editPurpose").value = purpose;
  document.getElementById("editLabel").value = label;
  document.getElementById("editArea").value = area;
  document.getElementById("editSqft").value = sqft;
  document.getElementById("editDesc").value = desc;
  document.getElementById("editLocation").value = location;
  document.getElementById("editLandmark").value = landmark;
  document.getElementById("editCity").value = city;
  document.getElementById("editDistrict").value = district;
  document.getElementById("editPrice").value = price;
  document.getElementById("editTotalPrice").value = totalPrice;
  document.getElementById("editPhone").value = phone;
  document.getElementById("editWhatsappNumber").value = whatsapp;
  document.getElementById("editPinCode").value = pinCode;
  document.getElementById("editDuration").value = duration;

  // Amenities
  const container = document.getElementById("editAmenitiesContainer");
  container.innerHTML = "";
  const amenities = amenitiesText.split(",");
  if (amenitiesText.trim() !== "" && amenities.length > 0) {
    amenities.forEach((a) => {
      if (a.trim() !== "") addAgentAmenityField("modal", a.trim());
    });
  } else {
    addAgentAmenityField("modal");
  }

  // Show modal
  document.getElementById("editModal").classList.remove("hidden");
}


function closeAgentPropertyEditModal() {
  document.getElementById("editModal").classList.add("hidden");
}

window.onload = () => {
  const formContainer = document.getElementById("editAmenitiesContainerForm");
  if (formContainer && formContainer.children.length === 0) addAgentAmenityField("form");
};












// agent profile



  // function openAgentProfileEditModal(name) {
  //   document.getElementById('editModal').classList.remove('hidden');
  //   document.querySelector('input[name="name"]').value = name; 
  // }

  // function closeAgentProfileEditModal() {
  //   document.getElementById('editModal').classList.add('hidden');
  // }







    function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('-translate-x-full');
  }




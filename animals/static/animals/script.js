// script.js
// Talks to the Django backend instead of using a hard-coded object.
// window.API_SEARCH_URL and window.API_ANIMAL_DETAIL_BASE are injected
// by animals/templates/animals/index.html via {% url %}.

const searchInput = document.getElementById("searchInput");
const animalContainer = document.getElementById("animalContainer");

const modalOverlay = document.getElementById("modalOverlay");
const modalTitle = document.getElementById("modalTitle");
const modalText = document.getElementById("modalText");
const modalClose = document.getElementById("modalClose");


// ---- Learn More modal ----

function openModal(title, text) {
    modalTitle.textContent = title;
    modalText.textContent = text;
    modalOverlay.classList.add("active");
}

function closeModal() {
    modalOverlay.classList.remove("active");
}

modalClose.addEventListener("click", closeModal);

modalOverlay.addEventListener("click", function (event) {
    if (event.target === modalOverlay) {
        closeModal();
    }
});

async function showAnimal(animalId) {
    try {
        const response = await fetch(window.API_ANIMAL_DETAIL_BASE + animalId + "/");
        if (!response.ok) {
            throw new Error("Animal not found");
        }
        const animal = await response.json();
        openModal(
            (animal.emoji ? animal.emoji + " " : "") + animal.name,
            animal.full_description
        );
    } catch (err) {
        openModal("Oops!", "Couldn't load details for this animal right now.");
    }
}

// Delegate clicks on "Learn More" buttons (works even for cards
// re-rendered by the search below).
animalContainer.addEventListener("click", function (event) {
    const btn = event.target.closest(".learn-more-btn");
    if (btn) {
        showAnimal(btn.dataset.id);
    }
});


// ---- Search (queries the Django backend) ----

function renderCards(animals) {
    if (animals.length === 0) {
        animalContainer.innerHTML = "<p>No animals match your search.</p>";
        return;
    }

    animalContainer.innerHTML = animals.map(function (animal) {
        return `
            <div class="animal-card" data-id="${animal.id}">
                <img src="${animal.image_url}" alt="${animal.name}">
                <div class="card-content">
                    <h3>${animal.emoji ? animal.emoji + " " : ""}${animal.name}</h3>
                    <p>${animal.short_description}</p>
                    <button class="learn-more-btn" data-id="${animal.id}">
                        Learn More
                    </button>
                </div>
            </div>
        `;
    }).join("");
}

let searchTimeout = null;

searchInput.addEventListener("keyup", function () {
    clearTimeout(searchTimeout);

    // Small debounce so we don't hit the server on every keystroke.
    searchTimeout = setTimeout(async function () {
        const query = searchInput.value.trim();

        try {
            const response = await fetch(
                window.API_SEARCH_URL + "?q=" + encodeURIComponent(query)
            );
            const data = await response.json();
            renderCards(data.results);
        } catch (err) {
            animalContainer.innerHTML = "<p>Search is unavailable right now.</p>";
        }
    }, 250);
});

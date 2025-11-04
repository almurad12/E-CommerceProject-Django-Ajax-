
// JS category data
const categories = [
    {
        name: "Fruits",
        image: "{% static 'img/1737531358122.jpeg' %}",
        link: "/cart/"
    },
    {
        name: "Vegetables",
        image: "{% static 'img/1737531358122.jpeg' %}",
        link: "/cart/"
    },
    {
        name: "Dry Fruits",
        image: "{% static 'img/1737531358122.jpeg' %}",
        link: "/cart/"
    }
];

function renderCategoryCarousel() {
    const container = document.getElementById("category-carousel");
    container.innerHTML = ""; // Clear any existing content

    categories.forEach(cat => {
        const card = `
            <div class="card align-items-center pt-2 border-primary category-card mb-0">
                <img src="${cat.image}" class="card-img-top img-fluid rounded-circle"
                    style="width: 10%;" alt="${cat.name}">
                <div class="card-body text-center mx-auto pt-1 position-relative">
                    <a href="${cat.link}" class="text-dark stretched-link text-center small-link">
                        ${cat.name}
                    </a>
                </div>
            </div>
        `;
        container.innerHTML += card;
    });

    // Initialize Owl Carousel
    $("#category-carousel").owlCarousel({
        loop: true,
        margin: 10,
        nav: true,
        responsive: {
            0: { items: 2 },
            600: { items: 3 },
            1000: { items: 5 }
        }
    });
    console.log("load perfectly")
}

document.addEventListener("DOMContentLoaded", renderCategoryCarousel);

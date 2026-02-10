document.addEventListener("DOMContentLoaded", () => {

    const categoryButtons = document.querySelectorAll(".category");
    const products = document.querySelectorAll(".product-card");
    const searchBox = document.getElementById("searchBox");

    let activeCategory = "all";

    // CATEGORY FILTER (your original logic – safe)
    categoryButtons.forEach(button => {
        button.addEventListener("click", () => {

            categoryButtons.forEach(btn => btn.classList.remove("active"));
            button.classList.add("active");

            activeCategory = button.innerText.toLowerCase();
            filterProducts();
        });
    });

    // SEARCH FILTER (only if searchBox exists)
    if (searchBox) {
        searchBox.addEventListener("keyup", () => {
            filterProducts();
        });
    }

    function filterProducts() {
        const searchValue = searchBox ? searchBox.value.toLowerCase().trim() : "";

        products.forEach(product => {
            const productCategory = product.dataset.category;
            const productName = product.querySelector("h3").innerText.toLowerCase();

            const matchCategory =
                activeCategory === "all" || activeCategory === productCategory;

            const matchSearch =
                productName.includes(searchValue);

            if (matchCategory && matchSearch) {
                product.style.display = "block";
            } else {
                product.style.display = "none";
            }
        });
    }

});

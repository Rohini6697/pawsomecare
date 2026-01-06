document.addEventListener("DOMContentLoaded", () => {
    const categoryButtons = document.querySelectorAll(".category");
    const products = document.querySelectorAll(".product-card");

    categoryButtons.forEach(button => {
        button.addEventListener("click", () => {

            categoryButtons.forEach(btn => btn.classList.remove("active"));
            button.classList.add("active");

            const selectedCategory = button.innerText.toLowerCase();

            products.forEach(product => {
                const productCategory = product.dataset.category;

                if (selectedCategory === "all") {
                    product.style.display = "block";
                }
                else if (selectedCategory === productCategory) {
                    product.style.display = "block";
                }
                else {
                    product.style.display = "none";
                }
            });
        });
    });
});

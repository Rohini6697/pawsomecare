document.addEventListener("DOMContentLoaded", () => {
    const categoryButtons = document.querySelectorAll(".category");
    const products = document.querySelectorAll(".product-card");

    categoryButtons.forEach(button => {
        button.addEventListener("click", () => {

            // Remove active class from all
            categoryButtons.forEach(btn => btn.classList.remove("active"));
            button.classList.add("active");

            const selectedCategory = button.innerText.toLowerCase();

            products.forEach(product => {
                const productCategory = product.dataset.category;

                if (selectedCategory === "all") {
                    product.style.display = "block";
                } 
                else if (selectedCategory.includes("food") && productCategory === "food") {
                    product.style.display = "block";
                } 
                else if (selectedCategory === "toys" && productCategory === "toys") {
                    product.style.display = "block";
                } 
                else if (selectedCategory === "accessories" && productCategory === "accessories") {
                    product.style.display = "block";
                } 
                else {
                    product.style.display = "none";
                }
            });
        });
    });
});

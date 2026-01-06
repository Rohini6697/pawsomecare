document.addEventListener("DOMContentLoaded", () => {

    const serviceButtons = document.querySelectorAll(".service");
    const providers = document.querySelectorAll(".provider-card");

    serviceButtons.forEach(button => {
        button.addEventListener("click", () => {

            // active state
            serviceButtons.forEach(btn => btn.classList.remove("active"));
            button.classList.add("active");

            const selectedService = button.dataset.service;

            providers.forEach(provider => {
                const providerServices = provider.dataset.services.split(",");

                if (selectedService === "all") {
                    provider.style.display = "block";
                } 
                else if (providerServices.includes(selectedService)) {
                    provider.style.display = "block";
                } 
                else {
                    provider.style.display = "none";
                }
            });

        });
    });

});

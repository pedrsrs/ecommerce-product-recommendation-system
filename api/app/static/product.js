document.addEventListener("DOMContentLoaded", () => {
    const pathParts = window.location.pathname.split("/");
    const productId = pathParts[pathParts.length - 1];  // Get last part of the URL

    if (productId) {
        fetchProductDetails(productId);
    } else {
        console.error("Product ID not found in URL");
    }
});

async function fetchProductDetails(productId) {
    try {
        let response = await fetch(`/api/products/${productId}`);  // Correct API call
        if (!response.ok) throw new Error("Product not found");

        let product = await response.json();
        renderProduct(product);
    } catch (error) {
        console.error("Error fetching product:", error);
    }
}

function renderProduct(product) {
    document.getElementById("product-title").innerText = product.title;
    document.getElementById("product-price").innerText = `$${product.price}`;
    document.getElementById("product-image").src = product.image_large;
}

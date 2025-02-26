document.addEventListener("DOMContentLoaded", async () => {
    const path_parts = window.location.pathname.split("/");
    const product_id = path_parts[path_parts.length - 1];  

    if (!product_id) {
        console.error("Invalid Product ID");
        return;
    }
    try {
        let response = await fetch(`/api/products/${product_id}`);
        if (!response.ok) throw new Error("Product not found");

        let product = await response.json();
        renderProduct(product);
    } catch (error) {
        console.error("Error fetching product:", error);
        alert("Product not found");
    }
});

function renderProduct(product) {
    const title_element = document.getElementById("product-title");
    const price_element = document.getElementById("product-price");
    const image_element = document.getElementById("product-image");
    const description_element = document.getElementById("product-description");

    if (title_element) title_element.innerText = product.title;
    if (price_element) price_element.innerText = `$${product.price}`;
    if (image_element) image_element.src = product.image_large;
    if (description_element) description_element.textContent = product.description;
}

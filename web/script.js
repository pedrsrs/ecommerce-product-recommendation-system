let currentPage = 1;  
const limit = 50; 
let isLoading = false;  

async function fetchProducts() {  
    if (isLoading) return;  
    isLoading = true;  

    try {  
        let response = await fetch(`/api/products/search?limit=${limit}&page=${currentPage}`);  
        let data = await response.json();  

        if (data.length > 0) {  
            renderProducts(data);  
            currentPage++;  
        }  
    } catch (error) {  
        console.error("Error fetching products:", error);  
    } finally {  
        isLoading = false;  
    }  
}  

function renderProducts(products) {  
    let productList = document.getElementById("product-list");  
    productList.className = "row row-cols-2 row-cols-md-3 row-cols-lg-5 g-2";  

    products.forEach(product => {  
        let truncatedTitle = product.title.length > 40 ?  
            product.title.substring(0, 40) + "..." : product.title;  

        let card = document.createElement("div");  
        card.className = "col mb-2";  
        card.innerHTML = `  
            <a href="/api/product/${product.parent_asin}" class="card-link text-decoration-none text-dark">  
                <div class="card h-100">  
                    <div class="ratio ratio-4x3">  
                        <img src="${product.image_large}"   
                             class="card-img-top"   
                             alt="${product.title}"   
                             style="object-fit: contain;">  
                    </div>  
                    <div class="card-body p-2">  
                        <h6 class="card-title fs-6 mb-1" title="${product.title}">${truncatedTitle}</h6>  
                        <p class="card-text small mb-0"><strong>Price:</strong> $${product.price}</p>  
                    </div>  
                </div>  
            </a>  
        `;  
        productList.appendChild(card);  
    });  
}

function handleScroll() {  
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 100) {  
        fetchProducts();  
    }  
}  

document.addEventListener("DOMContentLoaded", () => {  
    fetchProducts();  
    window.addEventListener("scroll", handleScroll);  
});  

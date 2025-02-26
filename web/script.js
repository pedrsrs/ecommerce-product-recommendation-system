let current_page = 1;  
const limit = 50; 
let is_loading = false;  

async function fetch_products() {  
    if (is_loading) return;  
    is_loading = true;  

    try {  
        let response = await fetch(`/api/products/search?limit=${limit}&page=${current_page}`);  
        let data = await response.json();  

        if (data.length > 0) {  
            render_products(data);  
            current_page++;  
        }  
    } catch (error) {  
        console.error("Error fetching products:", error);  
    } finally {  
        is_loading = false;  
    }  
}  

function render_products(products) {  
    let product_list = document.getElementById("product-list");  
    product_list.className = "row row-cols-2 row-cols-md-3 row-cols-lg-5 g-2";  

    products.forEach(product => {  
        let truncated_title = product.title.length > 40 ?  
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
                        <h6 class="card-title fs-6 mb-1" title="${product.title}">${truncated_title}</h6>  
                        <p class="card-text small mb-0"><strong>Price:</strong> $${product.price}</p>  
                    </div>  
                </div>  
            </a>  
        `;  
        product_list.appendChild(card);  
    });  
}

function handle_scroll() {  
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 100) {  
        fetch_products();  
    }  
}  

document.addEventListener("DOMContentLoaded", () => {  
    fetch_products();  
    window.addEventListener("scroll", handle_scroll);  
});

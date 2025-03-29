# ecommerce-product-recommendation-system
Implementing a Multi-Armed Bandits recommendation system on an e-commerce platform, combining it with Milvus, a vectorial database, to find matches between products.

## Pipeline Planning
![IMG-20250213-WA0041](https://github.com/user-attachments/assets/5588335b-c13f-409d-be15-5147809bbf8d)

## Stack Choices

#### Multi-Armed Bandit Algorithm
Multi-Armed Bandit fits well in the project by balancing explore x exploit, recommending products related to the user's activity as well as experimenting new product types. The main "Arms" used are built out of vectorial database similarity matches, products of the same category, products of the same brand and random recommendations.

#### Milvus
Milvus stores vectors representing each product, allowing for KNN searches and similarity matches. It provides similar products to the ones the user visited and feeds the search engine.

#### API
FastAPI was chosen due to it's simplicity to implement Multi-Armed Bandit.

#### Frontend
Bootstrap is used to generate the e-commerce frontend. It's a very simple framework, but the use of JavaScript allows better customization of the store pages.

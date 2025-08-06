## Project Setup ##
- Before please ensure uv installed in system 
- uv installation guide :- https://docs.astral.sh/uv/getting-started/installation/#standalone-installer (Pypy is preferred)

1) First clone the project :-
    git clone https://github.com/DebanKsahu/Inventory-Management-API.git
2) Move to project directory :-
    cd "Inventory-Management-API"
3) Sync with project (using UV package manager) :-
    uv sync
4) Run the server :-
    uv run uvicorn app.main:app --reload
- Your server can be available at http://127.0.0.1:8000 
- You can access the DOC at http://127.0.0.1:8000/docs

##  Products Endpoints ##

1) POST - `/products/` :- Add the product to DB
2) GET - `/products/` :- Get all products details
3) GET - `/products/{id}` :- Get the specific product detail whose product_id = id
4) PUT - `/products/{id}` :- Update the specific product detail
5) DELETE - `/products/{id}` :- Delete the specific product whose product_id = id

##  Stock Endpoints ##
1) POST - `/stock/` :- Add new stock transaction
2) GET - `/stock/`  :- Get all stock transaction
3) GET - `/stock/product/{product_id}`  :- Get transactions of a specific product

Postman Workspace Link :- https://temp99-6344.postman.co/workspace/Assignment-Workspace~5eccd0d5-320a-4e58-be2f-d243e69176d4/folder/45046859-84c52bd8-e8e7-4667-a17e-56ee6c1de113?action=share&creator=45046859&ctx=documentation
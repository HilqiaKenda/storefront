from locust import HttpUser, task, between
from random import randint

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    
    @task(2)
    def view_products(self):
        collection_id = randint(3, 6)
        self.client.get(f'http://localhost:8000/store/products/?collection_id={collection_id}', 
                        name='http://localhost:8000/store/products')
        
    @task(4)
    def view_product(self):
        product_id = randint(1, 1000)
        self.client.get(f'http://localhost:8000/store/products/{product_id}', 
                        name='http://localhost:8000/store/products/:id')
        
    @task(1)
    def add_to_cart(self):        
        product_id = randint(1, 1000)
        self.client.post(f'http://localhost:8000/store/carts/{self.cart_id}/items/', 
                         name='http://localhost:8000/store/carts/items/', 
                         json={'product_id': product_id, 'quantity': 1})

    @task(3)
    def say_hello(self):
        self.client.get('http://localhost:8000/playground/hello/')
        
    def on_start(self):
        response = self.client.post('http://localhost:8000/store/carts/')
        result = response.json()
        self.cart_id = result['id']
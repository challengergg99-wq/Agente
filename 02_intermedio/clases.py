# # Original Product class (for context)
# class Product:
#     def __init__(self, name, description, price, product_id):
#         self.name = name
#         self.description = description
#         self.price = price
#         self.product_id = product_id
#         self.stock = 0
#         self.reviews = []

#     def add_to_stock(self, quantity):
#         if quantity > 0:
#             self.stock += quantity
        
#     def remove_from_stock(self, quantity):
#         if quantity > 0 and self.stock >= quantity:
#             self.stock -= quantity
#             return True
#         return False
    
#     def is_available_for_purchase(self, quantity):
#         return self.stock >= quantity
           
        
# a = Product("laptop","razer",1500,"sku113")

# a.add_to_stock(20)

# print(f"{a.name}")
# print(f"{a.stock}")
# print(f"hay disponible 5:{a.is_available_for_purchase(5)}")
# print(f"hay disponible 15:{a.is_available_for_purchase(15)}")


# Original Customer class (for context)


# class Customer:
#     def __init__(self, customer_id, name, email):
#         self.customer_id = customer_id
#         self.name = name
#         self.email = email
#         self.purchase_history = []
#         self.shipping_address = None

#     def add_purchase(self, product_name, quantity, purchase_date):
#         self.purchase_history.append({
#             "product": product_name,
#             "quantity": quantity,
#             "date": purchase_date
#         })
#     def get_recent_purchases(self, num_purchases):
#         return self.purchase_history[-num_purchases:]
    
# cliente = Customer(1,"chicago","holitas@gmail.com")


# cliente.add_purchase("laptop",5,"25-01-2026")
# cliente.add_purchase("tv",1,"25-01-2027")
# cliente.add_purchase("pc",5,"25-01-2028")

# print("\nusuario:")
# print(f"historial de:{cliente.name}")


# print("\nÚltima compra (1):")
# print(f"compra:{cliente.get_recent_purchases(1)}")

# print("\nÚltimas 3  compras:")
# recientes = cliente.get_recent_purchases(3)
# for i in recientes:
#     print(f"{i['product'],({i['date']}),({i['quantity']})}")


 

        
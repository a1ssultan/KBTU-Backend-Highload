import random
from django.core.management.base import BaseCommand
from marketplace.models import Product, Order, OrderItem
from authentication.models import User
from marketplace.models import Category


class Command(BaseCommand):
    help = 'Generate 10,000 products and 500 orders in the database'

    def handle(self, *args, **options):
        categories = list(Category.objects.all())

        for i in range(10000):
            name = f'Product {i + 1}'
            description = f'Description for product {i + 1}.'
            price = round(random.uniform(5, 500), 2)
            stock = random.randint(1, 100)

            category = random.choice(categories)

            Product.objects.create(
                name=name,
                description=description,
                price=price,
                stock=stock,
                category=category
            )

        users = User.objects.all()
        for i in range(500):
            user = random.choice(users)

            order = Order.objects.create(user=user)

            for _ in range(random.randint(1, 5)):
                product = random.choice(Product.objects.all())
                quantity = random.randint(1, 3)

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )

        print('Products and orders created successfully!')

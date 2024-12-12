# Database Design and Optimization

This document outlines the steps taken to optimize the database design and queries in the e-commerce project to ensure scalability, efficiency, and high performance.

---

## **1. Indexing**
Indexes were added to frequently queried fields to improve query performance, particularly for filtering, sorting, and lookups. Key indexed fields include:

- **Products**:
  - `Product.name`: Optimized for product name lookups.
- **Categories**:
  - `Category.name`: Optimized for category filtering.
- **Orders**:
  - `Order.user`: Optimized for retrieving user orders.
  - `Order.order_status`: Optimized for filtering by order status.
- **Order Items**:
  - `OrderItem.order`: Optimized for retrieving items in an order.
  - `OrderItem.product`: Optimized for product lookups in orders.
- **Shopping Cart**:
  - `ShoppingCart.user`: Optimized for retrieving a user's cart.
  - `CartItem.cart`: Optimized for retrieving cart items.
  - `CartItem.product`: Optimized for product lookups in the cart.
- **Payments**:
  - `Payment.order`: Optimized for retrieving payment details for orders.
  - `Payment.payment_method`: Optimized for filtering by payment method.
  - `Payment.status`: Optimized for filtering by payment status.
- **Reviews**:
  - `Review.product`: Optimized for retrieving reviews for a product.
  - `Review.user`: Optimized for filtering reviews by user.
  - `Review.rating`: Optimized for sorting/filtering by rating.
- **Wishlists**:
  - `Wishlist.user`: Optimized for retrieving user-specific wishlists.
  - `WishlistItem.wishlist`: Optimized for retrieving items in a wishlist.
  - `WishlistItem.product`: Optimized for filtering wishlist items by product.

---

## **2. Query Optimization**
Efforts were made to reduce the number of queries and improve query efficiency using Django ORM's `select_related` and `prefetch_related`. Key optimizations include:

### **General Optimizations**
- **Foreign Key Optimizations**:
  - Used `select_related` for foreign key relationships, such as `Product.category`, `Order.user`, and `Review.user`, to reduce database hits.
- **One-to-Many Relationships**:
  - Used `prefetch_related` for preloading related objects in relationships such as `Category.products`, `Order.items`, and `Wishlist.items`.
- **Avoiding N+1 Queries**:
  - Reduced redundant queries in key views, including `OrderViewSet`, `ShoppingCartViewSet`, and `ReviewViewSet`.

### **Endpoint-Specific Optimizations**
- **Order Management**:
  - Optimized `OrderViewSet` queries using `select_related` for `user` and `prefetch_related` for `items` and their associated `products`.
- **Shopping Cart**:
  - Preloaded cart items and their associated products to reduce query overhead when retrieving cart details.
- **Reviews**:
  - Optimized review queries by preloading associated `user` and `product` objects.
  - Ensured efficient sorting by `created_at` for displaying recent reviews.
- **Wishlists**:
  - Minimized queries for retrieving wishlist items and their associated products by using `prefetch_related`.

---

## **3. Pagination**
Pagination was implemented for all list-based API responses to limit large datasets and reduce the load on the database.

- **Implementation**:
  - Used Django REST Framework's built-in pagination (`PageNumberPagination`) with a default page size of 10 items.
- **Benefits**:
  - Reduced memory and database usage for endpoints like `ProductListView`, `OrderListView`, and `ReviewListView`.

---

These improvements ensure the system can handle high traffic loads while maintaining a smooth user experience.

### Security in High-Load Systems

To ensure secure handling of user authentication and registration endpoints, I conducted a security audit and implemented multiple security measures in the project. These changes ensure protection against common vulnerabilities and adhere to best practices for high-load systems.

1. **Enhanced JWT Authentication:**
   - Customized CustomTokenObtainPairView to include additional claims (e.g., user email) in the JWT.
   - Added email-based validation for user authentication.
    - ![img_5.png](img_5.png)
2. **Permission Management:**
   - Configured granular permissions:
     - AllowAny for registration endpoints, getting products and categories.
     - IsAuthenticated for user actions such as updating or deleting accounts, order creating, shopping cart and wishlist management.
     - ![img_6.png](img_6.png)
3. **Audit Logging**:
   - Used Django signals to log user creation and updates for monitoring and security purposes.
4. **Rate Limiting**
   - Integrated django-ratelimit middleware to prevent brute-force attacks on login and registration endpoints.
   - ![img.png](img.png)
   - ![img_1.png](img_1.png)
5. **Middleware for IP Whitelisting**
   - Implemented middleware to restrict access to authentication endpoints from specific IP ranges.
   - ![img_2.png](img_2.png)
   - ![img_3.png](img_3.png)
6. **Audit Logging:**
   - Used Django signals to log user creation and updates for monitoring and security purposes.
   - ![img_4.png](img_4.png)

These measures significantly enhance the security of high-load systems, ensuring safe handling of sensitive user data.

# Subscriptions App 
Apps contains logic for 
- Adding subscriptions for users
- Mangaing Subscriptions
- Managing Plans 
- Razorpay Payments/Orders

## Subscription Flow
1. UI displays, all active plans
2. User Selects plans
3. Order is created, for respective **`user <==> plans`**.
    - Razorpay order is created refer [razorpay-order-docs], store credential like group id, razorpay order id etc. in postgres database.
4. Payments is initiated for the subscriptions.
5. On payment success, 
    - Subscriptions entry is added in subscriptions tables
    - Invoice details are generated(Can be downloaded through dashboard)

Refer [**Razorpay**][razorpay] api.



## Resources : 
- Razorpay : https://razorpay.com/docs/api/
- Order Creation :  https://razorpay.com/docs/api/orders/
- Invoice Generation : https://razorpay.com/docs/api/invoices/

[razorpay-order-docs]: https://razorpay.com/docs/api/orders/
[invoice-creation-razorpay]: https://razorpay.com/docs/api/invoices/
[razorpay]: https://razorpay.com/docs/api/
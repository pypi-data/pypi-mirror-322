# OpenWebPOS

OpenWebPOS is an open-source, web-based Point of Sale (POS) system designed specifically for restaurants and mobile food
vendors. Built with Python and Flask, it leverages modern front-end and back-end technologies to provide a reliable,
efficient, and customizable POS experience. This project is ideal for small businesses looking for a free, flexible POS
solution.

## Demo

[//]: # ( TODO 1/23/25 : Provide a live demo link and screenshots of key features. Include images of Order management interface, Inventory dashboard, Responsive UI on mobile, tablet, and desktop.)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

1. __User Management__
    - [ ] Permission-based access control.
    - [ ] Create custom roles for each user.
    - [X] Secure user authentication.
    - [ ] password recovery via email (Flask-Mailman integration).
    - [ ] User activity tracking for auditing.
2. __Order Management__
    - [ ] Easy order creation and management with real-time updates.
    - [ ] Support for dine-in, takeout, and delivery orders.
    - [ ] Integration with table and pager management.
    - [ ] Order status tracking (Pending, In-Progress, Completed, Cancelled).
    - [ ] Receipt generation and printing.
3. __Inventory Management__
    - [ ] Add, update, and delete inventory items.
    - [ ] Track stock levels and set low-stock alerts.
    - [ ] Support for inventory categorization(e.g., ingredients, supplies).
    - [ ] Supplier information tracking
4. __Table and Pager Management__
    - [ ] Assign and manage tables for dine-in customers.
    - [ ] Real-time table availability status.
    - [ ] Support for pager notifications for customers waiting for tables or orders.
5. __Reports and Analytics__
    - [ ] Daily, weekly, and monthly sales reports.
    - [ ] Inventory usage and trends analysis.
    - [ ] User activity and performance tracking.
    - [ ] Order trends for popular menu items.
6. __Multi-Device Support__
    - [ ] Responsive design with MaterializeCSS for use on desktop, tablets, and mobile devices.
    - [ ] Integration with external devices like receipt printers and pagers.
7. __Payment Handling__
    - [ ] Support for multiple payment methods: cash, credit card, and digital wallets.
    - [ ] Payment summary and invoice management.
    - [ ] Integration with payment APIs(e.g., Stripe, Square).
8. __Customizable Menu__
    - [ ] Add, edit, and organize menu items with descriptions, pricing, and images.
    - [ ] Menu categories for better organization(e.g., Appetizers, Mains, Desserts, Drinks).
    - [ ] Dynamic updates for specials and seasonal items.
9. __API Integration__
    - [ ] RESTful API for external integrations(e.g., mobile aps, third-party delivery platforms).
    - [ ] API endpoints for order management, inventory sync, and user data.
10. __Notification System__
    - [ ] Email and SMS notifications for order updates, low inventory, and sales summaries.
    - [ ] Alerts for kitchen staff for new or urgent orders.
11. __Localization and Time Zones__
    - [ ] Support for multiple languages for global use.
    - [ ] Timezone-aware scheduling for reports and notifications (using pytz)
12. __Secure and Scalable__
    - [ ] Secure login
    - [ ] Modular design using Flask Blueprints for easy scalability.
    - [ ] Database migrations with Flask-Migrate for version-controlled updates.
13. __Kitchen Display System (KDS)__
    - [ ] Real-time display of orders for the kitchen staff.
14. __Customer Feedback__
    - [ ] Collect feedback and ratings on orders.
15. __Loyalty Program__
    - [ ] Points tracking and discounts for returning customers.
16. __Offline Mode__
    - [ ] Ability to process orders without internet and sync later.

## Installation

[//]: # ( TODO 1/23/25 : Detail steps to set up the project locally)
Basic installation:

1. create your virtual environment using your prefered package manager (poetry, uv, virtualenv, etc.)
2. Install `openwebpos` by following the instructions on how to add packages from your package manager. (e.g., poetry
   add openwebpos)
3. create a app.py or wsgi.py file.
    ```python
   from openwebpos import create_app

   app = create_app()

   if __name__ == "__main__":
       app.run()
   
   ```
4. Run the application: ```openwebpos init --populate```
5. Visit [127.0.0.1:5000](http://127.0.0.1:5000) or the host and port you specify.

## Usage

[//]: # ( TODO 1/23/25 : Explain how to use the application)

## Technologies Used

Tools and Frameworks powering the project

* __Backend__ : Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-WTF.
* __Frontend__ : MaterializeCSS, HTMX, Google Material Icons.
* __Database__ : SQLite/PostgreSQL.
* __Other__ : Python-dotenv, Flask-Mailman, pytz, Python-Slugify, Poetry, Black.

## Contributing

We welcome contributors from the community! Here's how you can get involved:

1. Fork the repository and create a new branch for your feature or bug fix.
2. Make your changes and ensure the app runs smoothly.
3. Commit and push your changes to your branch.
4. Open a __Pull Request__ and describe your changes in detail.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

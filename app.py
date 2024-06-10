from flask import Flask, render_template, request
from models import  db, Offices, Employees, Customers, Products, Orders, OrderDetails, Payments
from sqlalchemy import func, desc
from datetime import timedelta
from os import environ

app = Flask(__name__)

# Database configuration
SQLALCHEMY_DATABASE_URI = 'mysql://root:root123@localhost/classicmodels'
                          #"mysql://" + \
                          #  environ.get('DB_USER') + ":" + \
                          #  environ.get('DB_PASSWORD') + "@" + \
                          #  environ.get('DB_HOSTNAME') + "/" + \
                          #  environ.get('DB_NAME')
                          

app.config['SQLALCHEMY_DATABASE_URI']           = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']    = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/offices')
def office():
    offices = Offices.query.all()
    
    sort_by = request.args.get('sort_by')
    sort_order = request.args.get('sort_order', 'asc')

    office_details = []
    for office in offices:
        num_employees = Employees.query.filter(Employees.officeCode == office.officeCode).count() # Number of employees of each office

        num_customers = Customers.query.join(Employees, Customers.salesRepEmployeeNumber == Employees.employeeNumber)\
                                       .filter(Employees.officeCode == office.officeCode)\
                                       .count() # Number of customers of each office

        office_details.append(
            # Create a dictionary and append:
            { 
             'office'       : office,           # The office information (Office Code and City)
             'num_employees': num_employees,    # The number of employees
             'num_customers': num_customers     # The number of customers
            }
        )

    if sort_by == 'num_employees':
        office_details.sort(key=lambda x: x['num_employees'], reverse=(sort_order == 'desc'))
    elif sort_by == 'office_code':
        office_details.sort(key=lambda x: x['office'].officeCode, reverse=(sort_order == 'desc'))       
    elif sort_by == 'num_customers':
        office_details.sort(key=lambda x: x['num_customers'], reverse=(sort_order == 'desc'))
    elif sort_by == 'city':
        office_details.sort(key=lambda x: x['office'].city, reverse=(sort_order == 'desc'))

    return render_template('offices.html', office_details=office_details, sort_by=sort_by, sort_order=sort_order)

@app.route('/products')
def product():
    
    products = Products.query.all() # All products information

    low_stock_products = Products.query.order_by(Products.quantityInStock).limit(5).all() # Top 5 low stock products

    quantityOrdered_per_product = db.session.query(Products.productCode, Products.productName, Products.productLine, Products.productScale, Products.productVendor, Products.productDescription,
                                                    func.sum(OrderDetails.quantityOrdered)
                                                        .label('total_quantity')) # Create a tuple with productCode, productName and sum of quantityOrdered of each product 

    best_selling_products = quantityOrdered_per_product.join(OrderDetails, Products.productCode == OrderDetails.productCode)\
                                                       .group_by(Products.productCode)\
                                                       .order_by(func.sum(OrderDetails.quantityOrdered).desc())\
                                                       .limit(5)\
                                                       .all() # Top 5 best-selling products
    
    return render_template('products.html', products=products, low_stock_products=low_stock_products, best_selling_products=best_selling_products)


@app.route('/employees')
def employees():

    # Find the date of the last order (2005-05-31)
    last_order_date = db.session.query(func.max(Orders.orderDate)).scalar() 
    # Calculate the date one year ago from the last order (2004-05-31)
    one_year_ago = last_order_date - timedelta(days=365)

    sales_volume_per_employee = db.session.query(Employees.employeeNumber, Employees.firstName, Employees.lastName,
                                                func.sum(OrderDetails.quantityOrdered * OrderDetails.priceEach)\
                                                    .label('sales_volume_employee'))
    
    # Total sales volume for each employee from the last year
    sales_volume = sales_volume_per_employee.join(Customers, Customers.salesRepEmployeeNumber == Employees.employeeNumber)\
                                            .join(Orders, Orders.customerNumber == Customers.customerNumber)\
                                            .join(OrderDetails, OrderDetails.orderNumber == Orders.orderNumber)\
                                            .filter(Orders.orderDate >= one_year_ago)\
                                            .group_by(Employees.employeeNumber)\
                                            .order_by(func.sum(OrderDetails.quantityOrdered * OrderDetails.priceEach)\
                                                            .desc())\
                                            .all()

    # Frequency of purchases for each employee over the last year
    freq_purchases_per_employee = db.session.query(Employees.employeeNumber, Employees.firstName, Employees.lastName, 
                                                            func.count(Orders.orderNumber)\
                                                                .label('frequency_of_purchases_employee'))\

    freq_of_purchases = freq_purchases_per_employee.join(Customers, Customers.salesRepEmployeeNumber == Employees.employeeNumber)\
                                                                .join(Orders, Orders.customerNumber == Customers.customerNumber)\
                                                                .filter(Orders.orderDate >= one_year_ago)\
                                                                .group_by(Employees.employeeNumber)\
                                                                .order_by(func.count(Orders.orderNumber)\
                                                                              .desc())\
                                                                .all()
    # Dict that returns the promotion score of each employee
    promotion = [
        {
            'employee_number': sales.employeeNumber,
            'firstName': sales.firstName,
            'lastName': sales.lastName,
            'promotion_score': sales.sales_volume_employee * freq.frequency_of_purchases_employee
        }
        for sales, freq in zip(sales_volume, freq_of_purchases)
    ]

    # Dict that returns the sales volume of each employee
    sales_volume = [
        {
            'employee_number': sales.employeeNumber,
            'firstName': sales.firstName,
            'lastName': sales.lastName,
            'sales_volume': sales.sales_volume_employee
        }
        for sales in sales_volume
    ]

    # Dict that returns the frequency of purchases of each employee
    freq_of_purchases = [
        {
            'employee_number': purchases.employeeNumber,
            'firstName': purchases.firstName,
            'lastName': purchases.lastName,
            'purchase_frequency': purchases.frequency_of_purchases_employee
        }
        for purchases in freq_of_purchases
    ]

    return render_template('employees.html', sales_volume=sales_volume, freq_of_purchases=freq_of_purchases, promotion=promotion)


@app.route('/customers')
def customers():
    
    total_spent_per_customer = db.session.query(Customers.customerNumber, Customers.customerName,\
                                                func.sum(Payments.amount)\
                                                    .label('total_spent'))

    top_customers_spent = total_spent_per_customer.join(Payments, Payments.customerNumber == Customers.customerNumber)\
                                                  .group_by(Customers.customerNumber)\
                                                  .order_by(desc(func.sum(Payments.amount)))
    
    total_spent_per_customer = top_customers_spent.all()

    # Determine the number of top customers (top 20%)
    num_of_20_percent = int(0.2 * len(total_spent_per_customer))

    # List of the top 20% customers
    top_20_percent = [
        {
            'customer_number': customer.customerNumber,
            'customer_name': customer.customerName,
            'total_spent': customer.total_spent
        }
        for customer in total_spent_per_customer[:num_of_20_percent]
    ]

    return render_template('customers.html', top_customers_spent=top_20_percent)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
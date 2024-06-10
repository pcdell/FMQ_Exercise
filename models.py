from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Numeric, Text, Date, ForeignKey, MetaData

# Inicializar o SQLAlchemy
db = SQLAlchemy()
metadata = MetaData()

class Employees(db.Model):
    __table__ = Table('employees', metadata,
                      Column('employeeNumber', Integer, primary_key=True),
                      Column('lastName', String(50)),
                      Column('firstName', String(50)),
                      Column('officeCode', String(10)),
                      )

    def __repr__(self):
        return '<Employee %r>' % self.employeeNumber

class Offices(db.Model):
    __table__ = Table('offices', metadata,
                Column('officeCode', String(10), primary_key=True),
                Column('city', String(50)),
                )

    def __repr__(self):
        return '<Office %r>' % self.city

class Customers(db.Model):
    __table__ = Table('customers', metadata,
                  Column('customerNumber', Integer, primary_key=True),
                  Column('customerName', String(50)),
                  Column('salesRepEmployeeNumber', Integer),
                  )

    def __repr__(self):
        return '<Customer %r>' % self.customerName
    
class Products(db.Model):
    __table__ = Table('products', metadata,
                 Column('productCode', String(15), primary_key=True),
                 Column('productName', String(70)),
                 Column('productLine', String(50)),
                 Column('productScale', String(10)),
                 Column('productVendor', String(50)),
                 Column('productDescription', Text),
                 Column('quantityInStock', Integer),
                 )
    def __repr__(self):
        return '<Product %r>' % self.productCode
    
class Orders(db.Model):
    __table__ = Table('orders', metadata,
                     Column('orderNumber', Integer, primary_key=True),
                     Column('customerNumber', Integer, ForeignKey('customers.customerNumber')),
                     Column('orderDate', Date),
                     )
    def __repr__(self):
        return '<Order %r>' % self.orderNumber

class OrderDetails(db.Model):
    __table__ = Table('orderdetails', metadata,
                     Column('orderNumber', Integer, ForeignKey('orders.orderNumber'), primary_key=True),
                     Column('productCode', String(15), ForeignKey('products.productCode'), primary_key=True),
                     Column('quantityOrdered', Integer),
                     Column('priceEach', Numeric(10, 2)),
                     )

    def __repr__(self):
        return '<OrderDetail %r>' % self.orderNumber

class Payments(db.Model):
    __table__ = Table('payments', metadata,
                     Column('customerNumber', Integer, ForeignKey('customers.customerNumber'), primary_key=True),
                     Column('checkNumber', String(50), primary_key=True),
                     Column('amount', Numeric(10, 2)),
                     )

    def __repr__(self):
        return '<Payment %r>' % self.checkNumber
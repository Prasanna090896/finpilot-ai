from sqlalchemy.orm import Session
from models import Customer


def add_customer(
    db: Session,
    name: str,
    age: int,
    retirement_age: int,
    pension: float,
    monthly_contribution: float,
    annual_return: float,
):

    customer = Customer(
        name=name,
        age=age,
        retirement_age=retirement_age,
        pension=pension,
        monthly_contribution=monthly_contribution,
        annual_return=annual_return,
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


def get_customers(db: Session):
    return db.query(Customer).all()


def get_customer(db: Session, customer_id: int):
    return (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )


def update_customer(
    db: Session,
    customer_id: int,
    name: str,
    age: int,
    retirement_age: int,
    pension: float,
    monthly_contribution: float,
    annual_return: float,
):

    customer = get_customer(db, customer_id)

    if customer:

        customer.name = name
        customer.age = age
        customer.retirement_age = retirement_age
        customer.pension = pension
        customer.monthly_contribution = monthly_contribution
        customer.annual_return = annual_return

        db.commit()
        db.refresh(customer)

    return customer


def delete_customer(db: Session, customer_id: int):

    customer = get_customer(db, customer_id)

    if customer:

        db.delete(customer)
        db.commit()

    return customer
   
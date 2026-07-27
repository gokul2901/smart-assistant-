from fastapi import APIRouter, Depends, HTTPException

from src.admin.dashboard import AdminDashboard
from src.admin.analytics import Analytics
from src.admin.reports import Reports


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# Temporary admin authentication
# Later replace with JWT authentication

async def verify_admin():

    return {
        "role": "admin"
    }



# Admin dashboard

@router.get("/dashboard")
async def get_dashboard(
    admin=Depends(verify_admin)
):

    data = await AdminDashboard.get_dashboard_data()

    return {
        "status": "success",
        "dashboard": data
    }



# Analytics summary

@router.get("/analytics")
async def get_analytics(
    admin=Depends(verify_admin)
):

    data = await Analytics.get_dashboard_summary()

    return {
        "status": "success",
        "analytics": data
    }



# Daily sales report

@router.get("/reports/daily-sales")
async def daily_sales_report(
    admin=Depends(verify_admin)
):

    report = await Reports.daily_sales_report()

    return {
        "status": "success",
        "report": report
    }



# Monthly sales report

@router.get("/reports/monthly-sales")
async def monthly_sales_report(
    admin=Depends(verify_admin)
):

    report = await Reports.monthly_sales_report()

    return {
        "status": "success",
        "report": report
    }



# Top selling products

@router.get("/reports/top-products")
async def top_products(
    admin=Depends(verify_admin)
):

    products = await Reports.top_products()

    return {
        "status": "success",
        "products": products
    }



# Low stock alert

@router.get("/inventory/low-stock")
async def low_stock(
    admin=Depends(verify_admin)
):

    products = await Reports.low_stock_report()

    return {
        "status": "success",
        "low_stock_products": products
    }
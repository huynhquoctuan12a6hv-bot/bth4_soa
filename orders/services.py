import os
import requests


PRODUCT_SERVICE_URL = os.getenv(
    'PRODUCT_SERVICE_URL',
    'http://localhost:8001'
)


def kiem_tra_san_pham(product_id, quantity):
    """
    Gọi Product Service để kiểm tra sản phẩm
    và số lượng tồn kho.
    """

    url = f"{PRODUCT_SERVICE_URL}/products/{product_id}/"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 404:
            return False, "Không tìm thấy sản phẩm."

        response.raise_for_status()

        product = response.json()

        if product.get('stock', 0) < quantity:
            return False, "Số lượng sản phẩm trong kho không đủ."

        return True, product

    except requests.RequestException:
        return False, "Không thể kết nối đến Product Service."
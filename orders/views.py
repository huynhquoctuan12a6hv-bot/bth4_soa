from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    # API cập nhật trạng thái đơn hàng
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):

        order = self.get_object()

        trang_thai_moi = request.data.get('status')

        danh_sach_trang_thai = [
            'pending',
            'completed',
            'cancelled'
        ]

        if trang_thai_moi not in danh_sach_trang_thai:
            return Response(
                {
                    'message': 'Trạng thái không hợp lệ.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = trang_thai_moi
        order.save()

        return Response(
            {
                'message': 'Cập nhật trạng thái thành công.',
                'order': OrderSerializer(order).data
            },
            status=status.HTTP_200_OK
        )


class OrderItemViewSet(viewsets.ModelViewSet):

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
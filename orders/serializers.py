from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product_id',
            'product_name',
            'quantity',
            'unit_price',
            'total_price'
        ]
        read_only_fields = ['id', 'total_price']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Số lượng phải lớn hơn 0."
            )
        return value


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer_name',
            'customer_email',
            'total_amount',
            'status',
            'created_at',
            'updated_at',
            'items'
        ]

        read_only_fields = [
            'id',
            'total_amount',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        order = Order.objects.create(**validated_data)

        tong_tien = 0

        for item_data in items_data:
            item_data['total_price'] = (
                item_data['quantity'] * item_data['unit_price']
            )

            item = OrderItem.objects.create(
                order=order,
                **item_data
            )

            tong_tien += item.total_price

        order.total_amount = tong_tien
        order.save()

        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if items_data is not None:
            instance.items.all().delete()

            tong_tien = 0

            for item_data in items_data:
                item_data['total_price'] = (
                    item_data['quantity'] * item_data['unit_price']
                )

                item = OrderItem.objects.create(
                    order=instance,
                    **item_data
                )

                tong_tien += item.total_price

            instance.total_amount = tong_tien

        instance.save()

        return instance
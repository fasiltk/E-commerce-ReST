from urllib import request, response
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from django.shortcuts import get_object_or_404
import random
import string


# Create your views here.
User=get_user_model()

@api_view(['GET'])
def product_list(request):
    products=Product.objects.filter(featured=True)
    serializer=ProductListSerializers(products,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request,slug):
    product=Product.objects.get(slug=slug)
    serializer=ProductDetailSerializers(product)
    return Response(serializer.data)

@api_view(['GET'])
def category_list(request):
    catogories=Category.objects.all()
    serializer=CategoryListSerializers(catogories,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def category_detail(request,slug):
    category=Category.objects.get(slug=slug)
    serializer=CategoryDetailSerializers(category)
    return Response(serializer.data)

@api_view(['POST'])
def add_to_cart(request):
    cart_code=request.data.get("cart_code")
    product_id=request.data.get("product_id")

    cart,created=Cart.objects.get_or_create(cart_code=cart_code)
    product=Product.objects.get(id=product_id)
    cartitem,created=CartItem.objects.get_or_create(product=product,cart=cart)
    cartitem.quantity=1
    cartitem.save()
    serializer=CartSerializer(cart)
    return Response(serializer.data)


@api_view(['PUT'])
def update_cartitem_quantity(request):
    cartitem_id=request.data.get("item_id")
    quantity=request.data.get("quantity")
    quantity=int(quantity)
    cartitem=CartItem.objects.get(id=cartitem_id)
    cartitem.quantity=quantity
    cartitem.save()

    serializer=CartItemSerializer(cartitem)
    return Response({"data":serializer.data,"message":"Cartitem uploaded successfullly"})



@api_view(['POST'])
def add_review(request):
    product_id = request.data.get("product_id")
    email = request.data.get("email")
    rating = request.data.get("rating")
    review_text = request.data.get("review")

    product = Product.objects.get(id=product_id)
    user = User.objects.get(email=email)

    # Check if review already exists
    existing_review = Review.objects.filter(product=product, user=user).first()
    if existing_review:
        existing_review.rating = rating
        existing_review.review = review_text
        existing_review.save()
        serializer = ReviewSerializer(existing_review)
        return Response({"message": "Review updated", "data": serializer.data})


    # Create new review if none exists
    review = Review.objects.create(product=product, user=user, rating=rating, review=review_text)
    serializer = ReviewSerializer(review)
    return Response({"message": "Review created", "data": serializer.data})



@api_view(['PUT'])
def update_review(request, pk):
    review = get_object_or_404(Review, id=pk)
    review.rating = request.data.get("rating")
    review.review = request.data.get("review")
    review.save()
    serializer = ReviewSerializer(review)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_review(request, pk):
    review = get_object_or_404(Review, id=pk)
    review.delete()
    return Response({"message": "Review deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def product_rating_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    rating, created = ProductRating.objects.get_or_create(product=product)

    serializer = ProductRatingSerializer(rating)
    return Response(serializer.data, status=status.HTTP_200_OK)

# views.py

@api_view(['POST'])
def add_rating(request):
    email = request.data.get("email")
    product_id = request.data.get("product_id")
    rating = request.data.get("rating")
    review_text = request.data.get("review", "")

    if not (email and product_id and rating):
        return Response({"error": "email, product_id, and rating are required."}, status=400)

    try:
        user = User.objects.get(email=email)
        product = Product.objects.get(id=product_id)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=404)

    review, created = Review.objects.get_or_create(
        user=user,
        product=product,
        defaults={"rating": rating, "review": review_text}
    )

    if not created:
        review.rating = rating
        # Only update review text if not already provided
        if not review.review and review_text:
            review.review = review_text
        review.save()

    serializer = ReviewSerializer(review)
    return Response({
        "message": "Rating submitted" if created else "Rating updated",
        "data": serializer.data
    })


def generate_cart_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=11))


@api_view(['POST'])
def add_to_cart(request):
    try:
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        cart_code = request.data.get('cart_code')

        if not product_id:
            return Response({'error': 'Product ID is required.'}, status=400)

        product = Product.objects.get(id=product_id)

        # Get or create cart
        cart, created = Cart.objects.get_or_create(cart_code=cart_code or generate_cart_code())

        # Get or create cart item
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not item_created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        serializer = CartSerializer(cart)
        return Response({'message': 'Item added to cart', 'cart': serializer.data}, status=200)

    except Product.DoesNotExist:
        return Response({'error': 'Product not found.'}, status=404)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['DELETE'])
def delete_from_cart(request):
    try:
        product_id = request.data.get('product_id')
        cart_code = request.data.get('cart_code')

        if not product_id or not cart_code:
            return Response({'error': 'Product ID and cart code are required.'}, status=400)

        cart = Cart.objects.get(cart_code=cart_code)
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()

        return Response({'message': 'Item deleted from cart'}, status=200)

    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found.'}, status=404)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found.'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
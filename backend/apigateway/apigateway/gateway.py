import requests
from django.http import JsonResponse

MICROSERVICES = {
    "customer_service": "http://localhost:8001",
    "cart_service": "http://localhost:8002",
    "order_service": "http://localhost:8003",
    "product_service": "http://localhost:8004",
    "payment_service": "http://localhost:8005",
    "shipment_service": "http://localhost:8006",
}

def forward_request(service_name, endpoint, method, request):
    """Forwards API requests to the appropriate microservice"""
    if service_name not in MICROSERVICES:
        return JsonResponse({"error": "Service not found"}, status=404)

    service_url = MICROSERVICES[service_name] + endpoint

    headers = {"Authorization": request.headers.get("Authorization", "")}
    
    # Forward request based on HTTP method
    if method == "GET":
        response = requests.get(service_url, headers=headers)
    elif method == "POST":
        response = requests.post(service_url, json=request.data, headers=headers)
    elif method == "PUT":
        response = requests.put(service_url, json=request.data, headers=headers)
    elif method == "DELETE":
        response = requests.delete(service_url, headers=headers)
        return JsonResponse({"message": "Success"}, status=response.status_code)
    else:
        return JsonResponse({"error": "Method not supported"}, status=405)

    return JsonResponse(response.json(), status=response.status_code, safe=False)

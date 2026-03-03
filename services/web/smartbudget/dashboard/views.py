from django.shortcuts import render
import json
from django.db.models import Sum, Count
from .models import Transaction, Category, User

# параметр request - содержит всё о входящем запросе: кто зашёл, какой метод (GET/POST), cookies и т.д. Django передаёт его автоматически в каждую view.

def index(request):
    transactions = Transaction.objects.select_related("category", "user").order_by("-created_at")[:20] # objects - через это делаем все запросы к БД (менелжер запросов)
    
    stats = Transaction.objects.values( 
        "category__name",
        "category__emoji"
    ).annotate(
        total=Sum("amount"),
        count=Count("id")
    ).order_by("-total")
    
    total_spent = Transaction.objects.aggregate(Sum("amount"))["amount__sum"] or 0
    
    # Конвертируем для графика
    stats_json = json.dumps([
        {
            "category__name": s["category__name"],
            "category__emoji": s["category__emoji"],
            "total": float(s["total"])
        }
        for s in stats
    ])
    
    context = {
        "transactions": transactions,
        "stats": stats,
        "stats_json": stats_json,
        "total_spent": total_spent,
    }
    
    return render(request, "dashboard/index.html", context)
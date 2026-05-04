from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Menu

# 🔐 LOGIN
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        # mock login
        if username == "admin" and password == "1234":
            return JsonResponse({"message": "success"})
        else:
            return JsonResponse({"error": "invalid"}, status=401)

    return JsonResponse({"error": "Only POST allowed"})


# 📋 MENU
@csrf_exempt
def menu_list(request):

    # 📥 GET
    if request.method == 'GET':
        menus = []
        for m in Menu.objects.all():
            menus.append({
                "id": m.id,
                "name": m.name,
                "ingredients": m.ingredients,
                "steps": m.steps,
                "image": m.image.url if m.image else None
            })
        return JsonResponse(menus, safe=False)

    # ➕ POST
    elif request.method == 'POST':
        menu_id = request.POST.get('id')  # ดึง ID มาเช็คก่อน
        name = request.POST.get('name')
        ingredients = request.POST.get('ingredients')
        steps = request.POST.get('steps')
        image = request.FILES.get('image')

        if menu_id:
            # --- PART: UPDATE (กรณีมี ID ส่งมา) ---
            try:
                menu = Menu.objects.get(id=menu_id)
                menu.name = name
                menu.ingredients = ingredients
                menu.steps = steps
                if image: # อัปเดตรูปเฉพาะเมื่อมีการส่งไฟล์ใหม่มาเท่านั้น
                    menu.image = image
                menu.save()
                return JsonResponse({"message": "updated", "id": menu.id})
            except Menu.DoesNotExist:
                return JsonResponse({"error": "Menu not found"}, status=404)

        else:
            # --- PART: CREATE (กรณีกดเพิ่มใหม่ ไม่มี ID) ---
            menu = Menu.objects.create(
                name=name,
                ingredients=ingredients,
                steps=steps,
                image=image
            )
            return JsonResponse({"message": "created", "id": menu.id})

    # ❌ DELETE
    elif request.method == 'DELETE':
        body = json.loads(request.body)
        Menu.objects.get(id=body['id']).delete()
        return JsonResponse({"message": "deleted"})
    
    # PUT
    elif request.method == 'PUT':
        menu = Menu.objects.get(id=request.POST.get('id'))

        menu.name = request.POST.get('name')
        menu.ingredients = request.POST.get('ingredients')
        menu.steps = request.POST.get('steps')

        # 🔥 อัปเดตรูปถ้ามี
        if request.FILES.get('image'):
            menu.image = request.FILES.get('image')

        menu.save()

        return JsonResponse({"message": "updated"})

        
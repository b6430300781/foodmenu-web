<script setup>
import { ref, onMounted, computed } from 'vue' // ✅ เพิ่ม computed

const menus = ref([])
const name = ref('')
const ingredients = ref('')
const steps = ref('')
const image = ref(null)
const editId = ref(null)
const preview = ref(null)
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = 12

// 🔐 กันเข้าหน้า admin
onMounted(() => {
  if (!localStorage.getItem("isLogin")) {
    window.location.href = "/login"
  }
  fetchMenus()
})

// กรองข้อมูลตาม Search ก่อน
const filteredMenus = computed(() => {
  return menus.value.filter(m => 
    m.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    m.ingredients.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// คำนวณจำนวนหน้าทั้งหมด
const totalPages = computed(() => {
  return Math.ceil(filteredMenus.value.length / itemsPerPage)
})

// ฟังก์ชันเปลี่ยนหน้า และเลื่อนขึ้นบนอัตโนมัติ
const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

// รีเซ็ตหน้ากลับไปที่ 1 เมื่อมีการพิมพ์ค้นหา
const onSearchChange = () => {
  currentPage.value = 1
}

//ตัดข้อมูลที่จะแสดงในแต่ละหน้า (Slice)
const paginatedMenus = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredMenus.value.slice(start, end)
})

// 📥 ดึงข้อมูล
const fetchMenus = async () => {
  const res = await fetch('http://127.0.0.1:8000/api/menus/')
  menus.value = await res.json()
}

// ➕ เพิ่ม
const addMenu = async () => {
  const formData = new FormData()
  formData.append("name", name.value)
  formData.append("ingredients", ingredients.value)
  formData.append("steps", steps.value)
  if (image.value) formData.append("image", image.value)

  await fetch("http://127.0.0.1:8000/api/menus/", {
    method: "POST",
    body: formData,
  })
  clearForm()
  fetchMenus()
}

// ✏️ เลือกแก้ไข
const editMenu = (menu) => {
  editId.value = menu.id
  name.value = menu.name
  ingredients.value = menu.ingredients
  steps.value = menu.steps
  preview.value = menu.image ? 'http://127.0.0.1:8000' + menu.image : null

  // ✅ 3. เด้งไปด้านบน
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 🔄 UPDATE
const updateMenu = async () => {
  const formData = new FormData()
  formData.append("id", editId.value)
  formData.append("name", name.value)
  formData.append("ingredients", ingredients.value)
  formData.append("steps", steps.value)

  // ✅ ส่งรูปไปด้วยถ้ามีการเลือกใหม่
  if (image.value) {
    formData.append("image", image.value)
  }

  await fetch('http://127.0.0.1:8000/api/menus/', {
    method: 'POST', 
    body: formData
  })
  clearForm()
  fetchMenus()
}

// ❌ ลบ
const deleteMenu = async (id) => {
  if(!confirm("ยืนยันการลบเมนูนี้?")) return
  await fetch('http://127.0.0.1:8000/api/menus/', {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id })
  })
  fetchMenus()
}

const clearForm = () => {
  editId.value = null 
  name.value = '' 
  ingredients.value = '' 
  steps.value = '' 
  image.value = null 
  preview.value = null 
}

const logout = () => {
  localStorage.removeItem("isLogin")
  window.location.href = "/login"
}

const handleFile = (e) => {
  const file = e.target.files[0]
  if (!file) return
  image.value = file
  preview.value = URL.createObjectURL(file)
}

const removeImage = () => {
  image.value = null
  preview.value = null
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 p-4 md:p-8">
    <div class="max-w-6xl mx-auto">

      <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-4">
        <div>
          <h1 class="text-4xl font-black text-slate-800 tracking-tight">Dashboard</h1>
          <p class="text-slate-500 font-medium">จัดการรายการเมนูอาหารทั้งหมดของคุณ</p>
        </div>
        <button @click="logout" 
                class="flex items-center gap-2 bg-white text-red-500 border border-red-100 px-6 py-2.5 rounded-2xl shadow-sm hover:bg-red-50 transition-all font-bold">
          <span>Logout</span>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
        </button>
      </div>

      <div class="bg-white rounded-[2.5rem] shadow-xl shadow-slate-200/60 border border-slate-100 overflow-hidden mb-12">
        <div class="p-8 md:p-10">
          <div class="flex items-center gap-3 mb-8">
            <div :class="editId ? 'bg-yellow-100 text-yellow-600' : 'bg-blue-100 text-blue-600'" 
                 class="w-12 h-12 rounded-2xl flex items-center justify-center text-2xl shadow-inner">
              {{ editId ? '✏️' : '➕' }}
            </div>
            <h2 class="text-2xl font-black text-slate-800">
              {{ editId ? "แก้ไขเมนูอาหาร" : "เพิ่มเมนูใหม่เข้าคลัง" }}
            </h2>
          </div>

          <div class="grid lg:grid-cols-5 gap-10">
            <div class="lg:col-span-3 space-y-6">
              <div class="group">
                <label class="block text-sm font-bold text-slate-700 mb-2 ml-1 transition-colors group-focus-within:text-blue-500">ชื่อเมนูอาหาร</label>
                <input v-model="name" placeholder="ระบุชื่อเมนู..." 
                       class="w-full bg-slate-50 border-none rounded-2xl p-4 focus:ring-4 focus:ring-blue-100 outline-none transition-all placeholder:text-slate-400 font-medium text-slate-700"/>
              </div>

              <div class="grid md:grid-cols-2 gap-6">
                <div class="group">
                  <label class="block text-sm font-bold text-slate-700 mb-2 ml-1 group-focus-within:text-blue-500">วัตถุดิบหลัก</label>
                  <textarea v-model="ingredients" placeholder="ใส่วัตถุดิบทีละบรรทัด..." 
                            class="w-full bg-slate-50 border-none rounded-2xl p-4 h-40 focus:ring-4 focus:ring-blue-100 outline-none transition-all resize-none font-medium"></textarea>
                </div>
                <div class="group">
                  <label class="block text-sm font-bold text-slate-700 mb-2 ml-1 group-focus-within:text-blue-500">ขั้นตอนการทำ</label>
                  <textarea v-model="steps" placeholder="บอกวิธีการทำเป็นข้อๆ..." 
                            class="w-full bg-slate-50 border-none rounded-2xl p-4 h-40 focus:ring-4 focus:ring-blue-100 outline-none transition-all resize-none font-medium"></textarea>
                </div>
              </div>
            </div>

            <div class="lg:col-span-2">
              <label class="block text-sm font-bold text-slate-700 mb-2 ml-1">รูปภาพประกอบ</label>
              <div class="relative group h-[300px] w-full">
                <div :class="preview ? 'border-none' : 'border-4 border-dashed border-slate-200'" 
                     class="relative w-full h-full rounded-[2rem] flex flex-col items-center justify-center overflow-hidden transition-all group-hover:border-blue-300 bg-slate-50">
                  <img v-if="preview" :src="preview" class="absolute w-full h-full object-cover shadow-inner"/>
                  <div v-if="!preview" class="text-center p-6 pointer-events-none">
                    <div class="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center mx-auto mb-4 text-2xl">📸</div>
                    <p class="text-slate-500 font-bold">คลิกเพื่ออัปโหลด</p>
                    <p class="text-slate-400 text-xs mt-1">แนะนำขนาด 800x800px</p>
                  </div>
                  <input type="file" @change="handleFile" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
                </div>
                <button v-if="preview" @click="removeImage" 
                        class="absolute -top-3 -right-3 bg-red-500 text-white w-8 h-8 rounded-full shadow-lg hover:bg-red-600 transition-all flex items-center justify-center font-bold">✕</button>
              </div>
            </div>
          </div>

          <div class="mt-10 flex justify-end gap-4">
            <button v-if="editId" @click="clearForm" 
                    class="px-8 py-3 rounded-2xl font-bold text-slate-500 hover:bg-slate-100 transition-all">ยกเลิก</button>
            <button @click="editId ? updateMenu() : addMenu()" 
                    :class="editId ? 'bg-yellow-400 hover:bg-yellow-500' : 'bg-blue-600 hover:bg-blue-700 shadow-blue-200'"
                    class="px-10 py-4 text-white rounded-2xl font-bold shadow-lg transition-all transform active:scale-95 flex items-center gap-2">
              <span>{{ editId ? "อัปเดตข้อมูลเมนู" : "ยืนยันการเพิ่มเมนู" }}</span>
            </button>
          </div>
        </div>
      </div>

      <div class="space-y-6 pb-20">
        <div class="flex items-center justify-between">
          <h3 class="text-xl font-bold text-slate-800">รายการเมนูทั้งหมด ({{ filteredMenus.length }})</h3>
          <div class="relative w-full max-w-md">
            <span class="absolute inset-y-0 left-4 flex items-center text-slate-400">🔍</span>
            <input v-model="searchQuery" @input="onSearchChange" type="text" placeholder="ค้นหาชื่อเมนูหรือวัตถุดิบ..." 
                   class="w-full pl-12 pr-6 py-3 bg-white border-none rounded-2xl shadow-sm focus:ring-2 focus:ring-blue-400 outline-none transition-all" />
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          <div v-for="m in paginatedMenus" :key="m.id" 
               class="group bg-white rounded-[2rem] shadow-md hover:shadow-2xl transition-all duration-300 border border-slate-50 overflow-hidden">
            <div class="relative h-48 overflow-hidden">
              <img v-if="m.image" :src="'http://127.0.0.1:8000' + m.image" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"/>
              <div v-else class="w-full h-full bg-slate-100 flex items-center justify-center text-slate-300 italic">No Image</div>
              <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
            </div>

            <div class="p-6">
              <h2 class="text-xl font-black text-slate-800 line-clamp-1 mb-2">{{ m.name }}</h2>
              <div class="space-y-1 mb-6">
                <p class="text-xs text-slate-400 font-bold uppercase tracking-wider">ส่วนผสม</p>
                <p class="text-sm text-slate-600 line-clamp-2 leading-relaxed">{{ m.ingredients }}</p>
              </div>

              <div class="flex gap-3">
                <button @click="editMenu(m)" 
                        class="flex-1 py-2.5 bg-yellow-50 text-yellow-600 rounded-xl font-bold text-sm hover:bg-yellow-400 hover:text-white transition-all flex items-center justify-center gap-1">
                  ✏️ แก้ไข
                </button>
                <button @click="deleteMenu(m.id)" 
                        class="flex-1 py-2.5 bg-red-50 text-red-500 rounded-xl font-bold text-sm hover:bg-red-500 hover:text-white transition-all flex items-center justify-center gap-1">
                  🗑️ ลบ
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="totalPages > 1" class="flex justify-center items-center gap-2 mt-12">
          <button @click="changePage(currentPage - 1)" 
                  :disabled="currentPage === 1"
                  class="w-10 h-10 flex items-center justify-center rounded-xl bg-white border border-slate-200 text-slate-500 hover:bg-blue-50 hover:text-blue-600 disabled:opacity-30 transition-all">
            &lt;
          </button>

          <div class="flex gap-2">
            <button v-for="page in totalPages" :key="page"
                    @click="changePage(page)"
                    :class="currentPage === page ? 'bg-blue-600 text-white shadow-lg shadow-blue-200' : 'bg-white text-slate-600 hover:bg-slate-100'"
                    class="w-10 h-10 rounded-xl font-bold transition-all">
              {{ page }}
            </button>
          </div>

          <button @click="changePage(currentPage + 1)" 
                  :disabled="currentPage === totalPages"
                  class="w-10 h-10 flex items-center justify-center rounded-xl bg-white border border-slate-200 text-slate-500 hover:bg-blue-50 hover:text-blue-600 disabled:opacity-30 transition-all">
            &gt;
          </button>
        </div>

        <div v-if="filteredMenus.length === 0" class="text-center py-24 bg-white rounded-[3rem] border border-dashed border-slate-200">
          <p class="text-4xl mb-4">🏜️</p>
          <h3 class="text-xl font-bold text-slate-800">ไม่พบเมนูที่คุณค้นหา</h3>
          <p class="text-slate-400">ลองเปลี่ยนคำค้นหา หรือเพิ่มเมนูใหม่ดูนะ</p>
        </div>
      </div>
    </div>
  </div>
</template>
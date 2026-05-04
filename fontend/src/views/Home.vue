<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const menus = ref([])
const search = ref('')           // ค้นหาจากชื่อ
const searchIngredient = ref('') // ค้นหาจากวัตถุดิบ
const favorites = ref([])        // เก็บ ID ของเมนูที่กดใจ
const showOnlyFavorites = ref(false) // สถานะการแสดงเฉพาะที่ถูกใจ

//ส่วนที่เพิ่มสำหรับ Pagination
const currentPage = computed(() => parseInt(route.query.page) || 1)
const itemsPerPage = 15 // แสดง 15 เมนู

const fetchMenus = async () => {
  const res = await fetch('http://127.0.0.1:8000/api/menus/')
  menus.value = await res.json()
}

// โหลดรายการหัวใจที่เคยบันทึกไว้
onMounted(() => {
  fetchMenus()
  const savedFavs = localStorage.getItem('myFavorites')
  if (savedFavs) favorites.value = JSON.parse(savedFavs)
})

// ฟังก์ชันสำหรับกดใจ
const toggleFavorite = (id) => {
  if (favorites.value.includes(id)) {
    favorites.value = favorites.value.filter(favId => favId !== id)
  } else {
    favorites.value.push(id)
  }
  localStorage.setItem('myFavorites', JSON.stringify(favorites.value))
}

//กรองข้อมูล (กรองเฉพาะเมนูที่ถูกใจ)
const filteredMenus = computed(() => {
  return menus.value.filter(m => {
    const matchName = m.name.toLowerCase().includes(search.value.toLowerCase())
    const matchIngredient = m.ingredients.toLowerCase().includes(searchIngredient.value.toLowerCase())
    
    // ถ้าเปิดโหมดหัวใจ ให้กรองเอาเฉพาะ ID ที่อยู่ใน favorites
    if (showOnlyFavorites.value) {
      return matchName && matchIngredient && favorites.value.includes(m.id)
    }
    
    return matchName && matchIngredient
  })
})

//คำนวณจำนวนหน้า
const totalPages = computed(() => {
  return Math.ceil(filteredMenus.value.length / itemsPerPage)
})

//ตัดข้อมูลแสดงผลแค่ 15 ชิ้นต่อหน้า
const paginatedMenus = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredMenus.value.slice(start, end)
})

//ฟังก์ชันเปลี่ยนหน้า
const changePage = (page) => {
  router.push({ 
    query: { ...route.query, page: page } 
  })
  window.scrollTo({ top: 400, behavior: 'smooth' })
}

//เมื่อพิมพ์ค้นหา หรือเปลี่ยนโหมด ให้กลับไปหน้า 1
const onSearchChange = () => {
  router.push({ 
    query: { ...route.query, page: 1 } 
  })
}

//ฟังก์ชันสลับโหมดดูเมนูถูกใจ
const toggleShowFavorites = () => {
  showOnlyFavorites.value = !showOnlyFavorites.value
  
  // แทนที่จะสั่ง currentPage.value = 1 (ซึ่งจะ Error)
  // ให้สั่ง push URL ใหม่แทน เพื่อ Reset หน้า
  router.push({ 
    query: { ...route.query, page: 1 } 
  })
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 p-4 md:p-10">
    <div class="max-w-6xl mx-auto">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-4xl font-extrabold text-gray-900 tracking-tight">
          🍽️ <span class="text-orange-500">Food</span>Menu
        </h1>
        <router-link to="/login" class="bg-gray-800 hover:bg-black text-white px-5 py-2 rounded-full transition shadow-md">
          Admin Login
        </router-link>
      </div>
      <div class="mb-10 text-center">
        <h1 class="text-4xl font-black text-gray-800 mb-2">ค้นหาเมนูโปรด</h1>
        <p class="text-gray-500">อยากกินอะไร หรือมีวัตถุดิบอะไร ลองพิมพ์บอกเราดูสิ!</p>
      </div>

      <div class="flex flex-col md:flex-row gap-4 mb-12">
        <div class="flex-1 bg-white p-4 rounded-3xl shadow-xl shadow-gray-200/50 grid md:grid-cols-2 gap-4 border border-gray-100">
          <div class="relative">
            <span class="absolute inset-y-0 left-4 flex items-center text-gray-400">🔍</span>
            <input v-model="search" 
                   @input="onSearchChange"
                   type="text" 
                   placeholder="ค้นหาชื่อเมนู..." 
                   class="w-full pl-12 pr-4 py-3 bg-gray-50 rounded-2xl focus:ring-2 focus:ring-orange-400 outline-none transition-all" />
          </div>
          <div class="relative">
            <span class="absolute inset-y-0 left-4 flex items-center text-gray-400">🥬</span>
            <input v-model="searchIngredient" 
                   @input="onSearchChange"
                   type="text" 
                   placeholder="มีวัตถุดิบอะไรบ้าง? (เช่น หมู, ไข่...)" 
                   class="w-full pl-12 pr-4 py-3 bg-gray-50 rounded-2xl focus:ring-2 focus:ring-green-400 outline-none transition-all" />
          </div>
        </div>

        <button @click="toggleShowFavorites"
                :class="showOnlyFavorites ? 'bg-red-500 text-white border-red-500' : 'bg-white text-gray-400 border-gray-100'"
                class="md:w-20 h-[88px] rounded-3xl shadow-xl border flex flex-col items-center justify-center transition-all hover:scale-105 active:scale-95 group">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 transition-transform group-hover:scale-110" :fill="showOnlyFavorites ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
          <span class="text-[10px] font-bold mt-1 uppercase">{{ showOnlyFavorites ? 'Liked' : 'Fav' }}</span>
        </button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="m in paginatedMenus" :key="m.id" 
             class="group relative bg-white rounded-[2rem] overflow-hidden shadow-md hover:shadow-2xl transition-all duration-500">
          
          <button @click.stop="toggleFavorite(m.id)" 
                  class="absolute top-4 right-4 z-10 w-10 h-10 rounded-full flex items-center justify-center transition-all shadow-lg backdrop-blur-md"
                  :class="favorites.includes(m.id) ? 'bg-red-500 text-white' : 'bg-white/80 text-gray-400 hover:text-red-500'">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" :fill="favorites.includes(m.id) ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </button>

          <div class="aspect-[4/5] overflow-hidden">
            <img v-if="m.image" 
                 :src="'http://127.0.0.1:8000' + m.image" 
                 class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"/>
            
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-80"></div>
            
            <div class="absolute bottom-0 left-0 p-6 w-full">
              <span v-if="currentPage === 1 && !showOnlyFavorites" 
                class="inline-block px-3 py-1 bg-orange-500 text-white text-xs font-bold rounded-full mb-3 uppercase tracking-widest shadow-lg">
                แนะนำ
              </span>

              <h2 class="text-2xl font-bold text-white mb-2 group-hover:text-orange-300 transition-colors">
                {{ m.name }}
              </h2>
              
              <p class="text-gray-300 text-sm line-clamp-1 mb-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                🛒 {{ m.ingredients }}
              </p>
              
              <router-link :to="'/menu/' + m.id" 
              class="w-full block text-center py-3 bg-white/10 backdrop-blur-md border border-white/20 text-white font-semibold rounded-xl hover:bg-white hover:text-black transition-all">
                ดูสูตรอาหาร
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <div v-if="totalPages > 1" class="flex justify-center items-center gap-2 mt-16 mb-10">
        <button @click="changePage(currentPage - 1)" 
                :disabled="currentPage === 1"
                class="w-12 h-12 flex items-center justify-center rounded-2xl bg-white border border-gray-200 text-gray-500 hover:bg-orange-50 hover:text-orange-500 disabled:opacity-30 transition-all shadow-sm">
          &lt;
        </button>

        <div class="flex gap-2">
          <button v-for="page in totalPages" :key="page"
                  @click="changePage(page)"
                  :class="currentPage === page ? 'bg-orange-500 text-white shadow-lg shadow-orange-200' : 'bg-white text-gray-600 hover:bg-gray-100'"
                  class="w-12 h-12 rounded-2xl font-bold transition-all shadow-sm">
            {{ page }}
          </button>
        </div>

        <button @click="changePage(currentPage + 1)" 
                :disabled="currentPage === totalPages"
                class="w-12 h-12 flex items-center justify-center rounded-2xl bg-white border border-gray-200 text-gray-500 hover:bg-orange-50 hover:text-orange-500 disabled:opacity-30 transition-all shadow-sm">
          &gt;
        </button>
      </div>

      <div v-if="filteredMenus.length === 0" class="text-center py-20 bg-white rounded-3xl border-2 border-dashed border-gray-200">
        <span class="text-6xl mb-4 block">{{ showOnlyFavorites ? '❤️' : '🍳' }}</span>
        <h3 class="text-xl font-bold text-gray-800">
          {{ showOnlyFavorites ? 'ยังไม่มีรายการที่ถูกใจ' : 'ไม่พบเมนูที่คุณค้นหา' }}
        </h3>
        <p class="text-gray-500">
          {{ showOnlyFavorites ? 'ลองกดหัวใจให้กับเมนูที่คุณชื่นชอบสิ!' : 'ลองเปลี่ยนคำค้นหา หรือใช้ชื่อวัตถุดิบอื่นดูนะ' }}
        </p>
      </div>
    </div>
  </div>
</template>
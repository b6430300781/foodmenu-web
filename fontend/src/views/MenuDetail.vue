<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router' // เพิ่ม useRouter

const route = useRoute()
const router = useRouter() // สร้างตัวแปร router
const menu = ref(null)
const loading = ref(true)

const fetchMenu = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/menus/')
    const data = await res.json()
    menu.value = data.find(m => m.id == route.params.id)
  } catch (error) {
    console.error("Error:", error)
  } finally {
    loading.value = false
  }
}

const ingredientList = computed(() => {
  if (!menu.value?.ingredients) return []

  return menu.value.ingredients.split('\n') 
})

onMounted(fetchMenu)
</script>

<template>
  <div class="min-h-screen bg-slate-50 pb-20">
    
    <div class="max-w-4xl mx-auto px-6 py-6 flex justify-between items-center">
      <button @click="router.back()" 
              class="group flex items-center gap-2 text-slate-500 hover:text-orange-500 transition-all font-medium">
        <span class="bg-white p-2 rounded-full shadow-sm group-hover:shadow-md transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </span>
        ย้อนกลับ
      </button>

      <div class="text-slate-300 text-sm">รายละเอียดเมนูอาหาร</div>
    </div>

    <div v-if="menu" class="max-w-4xl mx-auto px-4">
      <div class="bg-white rounded-[2.5rem] shadow-xl overflow-hidden border border-slate-100">
        
        <div class="relative h-96 overflow-hidden">
          <img v-if="menu.image" :src="'http://127.0.0.1:8000' + menu.image" class="w-full h-full object-cover" />
          <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
          <h1 class="absolute bottom-8 left-8 text-4xl font-black text-white">{{ menu.name }}</h1>
        </div>

        <div class="p-8 md:p-12">
          <div class="grid md:grid-cols-3 gap-12 mb-12">
            <div class="md:col-span-1">
              <h2 class="text-xl font-bold mb-6 text-slate-800 flex items-center gap-2">
                <span class="text-orange-500">🛒</span> วัตถุดิบ
              </h2>
              <ul class="space-y-3">
                <li v-for="(item, index) in ingredientList"  :key="item" class="text-slate-600 flex items-start gap-2">
                  <span class="text-orange-300">•</span> {{ item.trim() }}
                </li>
              </ul>
            </div>

            <div class="md:col-span-2">
              <h2 class="text-xl font-bold mb-6 text-slate-800 flex items-center gap-2">
                <span class="text-green-500">🍳</span> ขั้นตอนการทำ
              </h2>
              <p class="text-slate-600 leading-relaxed whitespace-pre-line bg-slate-50 p-6 rounded-2xl">
                {{ menu.steps }}
              </p>
            </div>
          </div>

          <div class="flex justify-center border-t border-slate-100 pt-10">
            <button @click="router.push('/')" 
                    class="px-10 py-3 bg-slate-800 text-white rounded-full hover:bg-black transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1 font-bold">
              🏠 กลับสู่หน้าหลัก
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="loading" class="flex flex-col items-center justify-center h-[60vh]">
      <div class="w-12 h-12 border-4 border-t-orange-500 border-slate-200 rounded-full animate-spin"></div>
    </div>
  </div>
</template>

<style scoped>
/* เพิ่ม Font Google (Inter) เพื่อความ Modern ในหน้าหลักของคุณด้วยจะดีมากครับ */
</style>
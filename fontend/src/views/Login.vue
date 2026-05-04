<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const router = useRouter()
const isLoading = ref(false) // เพิ่มสถานะโหลด

const login = async () => {
  isLoading.value = true
  try {
    const res = await fetch('http://127.0.0.1:8000/api/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })

    if (res.status === 200) {
      localStorage.setItem("isLogin", "true")
      router.push('/admin')
    } else {
      alert("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง ❌")
    }
  } catch (error) {
    alert("การเชื่อมต่อเซิร์ฟเวอร์ผิดพลาด")
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-100 to-slate-300 px-4">
    
    <div class="bg-white/80 backdrop-blur-md p-8 rounded-[2rem] shadow-2xl shadow-slate-400/50 w-full max-w-md border border-white">
      
      <div class="text-center mb-10">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-blue-500 text-white rounded-2xl shadow-lg shadow-blue-200 mb-4 text-2xl">
          🔒
        </div>
        <h2 class="text-3xl font-black text-slate-800">ยินดีต้อนรับ</h2>
        <p class="text-slate-500 mt-2">กรุณาเข้าสู่ระบบเพื่อจัดการเมนูอาหาร</p>
      </div>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-bold text-slate-700 mb-1 ml-1">Username</label>
          <input v-model="username"
                 type="text"
                 placeholder="กรอกชื่อผู้ใช้"
                 class="w-full px-5 py-3 bg-white border border-slate-200 rounded-2xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 outline-none transition-all placeholder:text-slate-400"/>
        </div>

        <div>
          <label class="block text-sm font-bold text-slate-700 mb-1 ml-1">Password</label>
          <input v-model="password"
                 type="password"
                 placeholder="••••••••"
                 class="w-full px-5 py-3 bg-white border border-slate-200 rounded-2xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 outline-none transition-all placeholder:text-slate-400"/>
        </div>
      </div>

      <div class="mt-8 space-y-3">
        <button @click="login"
                :disabled="isLoading"
                class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-2xl shadow-lg shadow-blue-200 transition-all transform active:scale-[0.98] disabled:opacity-70 flex items-center justify-center">
          <span v-if="!isLoading">เข้าสู่ระบบ</span>
          <div v-else class="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
        </button>
        
        <router-link to="/"
                     class="w-full flex items-center justify-center py-3 text-slate-500 font-medium hover:text-slate-800 transition-colors">
          ← กลับหน้าหลัก
        </router-link>
      </div>

      <p class="text-center text-slate-400 text-xs mt-8">
        &copy; 2026 Food Menu Admin System
      </p>

    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'

const menus = ref([])
const name = ref('')
const description = ref('')
const editId = ref(null)

const fetchMenus = async () => {
  const res = await fetch('http://127.0.0.1:8000/api/menus/')
  menus.value = await res.json()
}

const addMenu = async () => {
  await fetch('http://127.0.0.1:8000/api/menus/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: name.value, description: description.value })
  })
  name.value = ''
  description.value = ''
  fetchMenus()
}

const deleteMenu = async (id) => {
  await fetch('http://127.0.0.1:8000/api/menus/', {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id })
  })
  fetchMenus()
}

const editMenu = (menu) => {
  editId.value = menu.id
  name.value = menu.name
  description.value = menu.description
}

const updateMenu = async () => {
  await fetch('http://127.0.0.1:8000/api/menus/', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: editId.value,
      name: name.value,
      description: description.value
    })
  })
  editId.value = null
  name.value = ''
  description.value = ''
  fetchMenus()
}

onMounted(fetchMenus)
</script>

<template>
  <router-view />
</template>
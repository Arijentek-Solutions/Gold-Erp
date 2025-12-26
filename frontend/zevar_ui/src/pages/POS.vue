<template>
  <div class="flex h-screen w-screen bg-gray-50">
    <div class="w-64 bg-white border-r border-gray-200 flex flex-col">
      <div class="h-16 flex items-center justify-center border-b border-gray-100">
        <h1 class="text-xl font-bold text-gray-800">Zevar POS</h1>
      </div>
      <div class="p-4 space-y-2">
        <button class="w-full text-left px-4 py-2 bg-gray-100 text-gray-900 rounded-md font-medium">
          💍 New Sale
        </button>
        <button class="w-full text-left px-4 py-2 text-gray-600 hover:bg-gray-50 rounded-md">
          📜 History
        </button>
      </div>
    </div>

    <div class="flex-1 flex flex-col">
      <header class="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-8">
        <span class="text-lg font-medium text-gray-700">Today's Dashboard</span>
        <button @click="logout" class="text-sm text-red-600 hover:text-red-800 font-medium">
          Logout
        </button>
      </header>

      <main class="p-8">
        <div class="bg-white p-8 rounded-lg shadow-sm border border-gray-200 text-center">
          <h2 class="text-2xl font-bold text-gray-800 mb-2">Welcome, {{ user.data ? user.data.full_name : 'User' }}!</h2>
          <p class="text-gray-500">You are ready to start selling.</p>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { createResource } from 'frappe-ui';
import { useRouter } from 'vue-router';

const router = useRouter();

// 1. Fetch the logged-in user's details
const user = createResource({
  url: 'frappe.auth.get_logged_user',
  auto: true,
});

// 2. Logout Logic
const session = createResource({
  url: 'logout',
  onSuccess() {
    router.push('/login');
    window.location.reload(); // Hard reload to clear cache
  }
});

function logout() {
  session.submit();
}
</script>
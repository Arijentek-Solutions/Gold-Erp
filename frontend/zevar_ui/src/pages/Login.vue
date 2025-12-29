<template>
  <div class="flex h-screen w-screen items-center justify-center bg-gray-100">
    <div class="w-full max-w-md overflow-hidden rounded-lg bg-white shadow-xl">
      <div class="bg-gray-900 px-8 py-6">
        <h2 class="text-2xl font-bold text-white">Zevar POS</h2>
        <p class="text-gray-400">Sign in to start your shift</p>
      </div>
      
      <form @submit.prevent="login" class="p-8">
        <div class="mb-4">
          <label class="mb-2 block text-sm font-semibold text-gray-700">Username</label>
          <input 
            v-model="email" 
            type="text" 
            class="w-full rounded border border-gray-300 px-3 py-2 focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900" 
            placeholder="Administrator"
          >
        </div>
        
        <div class="mb-6">
          <label class="mb-2 block text-sm font-semibold text-gray-700">Password</label>
          <input 
            v-model="password" 
            type="password" 
            class="w-full rounded border border-gray-300 px-3 py-2 focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900" 
            placeholder="••••••••"
          >
        </div>
        
        <button 
          type="submit" 
          class="w-full rounded bg-gray-900 px-4 py-2 font-bold text-white hover:bg-gray-800 focus:outline-none disabled:bg-gray-400"
          :disabled="auth.loading"
        >
          {{ auth.loading ? 'Signing in...' : 'Sign In' }}
        </button>

        <p v-if="auth.error" class="mt-4 text-center text-sm text-red-600">
          {{ auth.error.message }}
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { createResource } from 'frappe-ui';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const router = useRouter();

const auth = createResource({
  url: 'login',
  makeParams() {
    return {
      usr: email.value,
      pwd: password.value,
    };
  },
  onSuccess(data) {
    router.push('/'); 
  }
});

function login() {
  auth.submit();
}
</script>
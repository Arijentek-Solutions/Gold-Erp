<template>
  <div class="flex h-screen w-screen items-center justify-center bg-gray-100">
    <div class="w-full max-w-md bg-white p-8 rounded-lg shadow-md">
      <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Zevar POS Login</h2>
      
      <form @submit.prevent="login.submit">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Username or Email</label>
            <input 
              v-model="email" 
              type="email" 
              class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
              required
              placeholder="e.g. Administrator"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700">Password</label>
            <input 
              v-model="password" 
              type="password" 
              class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
              required 
            />
          </div>

          <div v-if="login.error" class="text-red-500 text-sm text-center">
            {{ login.error.message }}
          </div>

          <button 
            type="submit" 
            :disabled="login.loading"
            class="w-full bg-gray-900 text-white py-2 rounded-md hover:bg-gray-800 transition-colors disabled:opacity-50"
          >
            {{ login.loading ? 'Logging in...' : 'Login' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { createResource } from 'frappe-ui';
import { useRouter } from 'vue-router';

const router = useRouter();
const email = ref('');
const password = ref('');

const login = createResource({
  url: 'login',
  makeParams() {
    return {
      usr: email.value,
      pwd: password.value,
    };
  },
  onSuccess(data) {
    router.push('/pos');
  },
  onError(err) {
    console.error(err);
  }
});
</script>
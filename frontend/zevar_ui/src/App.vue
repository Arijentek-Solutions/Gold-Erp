<template>
<!-- <AppLayout>
    <div class="max-w-4xl mx-auto">
      
      <div v-if="!session.currentWarehouse" class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6 rounded-r">
        <div class="flex">
          <div class="ml-3">
            <p class="text-sm text-yellow-700">
              ⚠️ Please select a <strong>Store Location</strong> from the top bar to start selling.
            </p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-10 text-center">
        <h2 class="text-3xl font-bold text-gray-800 mb-2">Ready to Sell</h2>
        <p class="text-gray-500 mb-8">Select a product from the catalog to begin.</p>
        
        <div class="border-2 border-dashed border-gray-200 rounded-lg h-64 flex items-center justify-center bg-gray-50">
          <span class="text-gray-400 font-medium">✨ Item Grid Component Loading... (Coming Next)</span>
        </div>
      </div>

    </div>
  </AppLayout>   -->
  <router-view />
</template>

<script setup>

</script>
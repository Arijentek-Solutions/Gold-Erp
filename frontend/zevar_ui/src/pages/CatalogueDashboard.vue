<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 transition-colors">
    
    <!-- Header -->
    <Header 
      :isDark="isDark" 
      :activeCategory="activeCategory"
      @toggleTheme="toggleTheme"
      @search="performSearch"
      @selectCategory="handleCategorySelect"
    />

    <!-- Hero Banner -->
    <section class="relative h-[500px] overflow-hidden">
      <img 
        src="https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=1920&q=80" 
        class="w-full h-full object-cover"
        alt="Zevar Jewelry Collection"
      />
      <div class="absolute inset-0 bg-gradient-to-r from-black/70 via-black/50 to-transparent">
        <div class="max-w-7xl mx-auto px-6 h-full flex items-center">
          <div class="max-w-xl">
            <p class="text-[#C9A962] text-sm tracking-[0.3em] uppercase mb-4">New Collection</p>
            <h1 class="text-5xl md:text-6xl font-serif font-bold text-white mb-6">
              Celebrate Every <span class="text-[#C9A962]">Moment</span>
            </h1>
            <p class="text-gray-200 text-lg mb-8">
              Discover our exquisite collection of handcrafted jewelry, designed to make every occasion special.
            </p>
            <button 
              @click="scrollToSection('collections')" 
              class="px-8 py-4 bg-[#C9A962] text-black font-bold rounded hover:bg-[#b89d52] transition-all shadow-lg"
            >
              Explore Now
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Category Grid -->
    <section id="collections" class="py-16 bg-gray-50 dark:bg-gray-800">
      <div class="max-w-7xl mx-auto px-6">
        <div class="text-center mb-12">
          <p class="text-[#C9A962] text-sm tracking-[0.3em] uppercase mb-2">Shop by Category</p>
          <h2 class="text-4xl font-serif font-bold text-gray-900 dark:text-white">Explore Our Collections</h2>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          <div 
            v-for="cat in categories" 
            :key="cat.id"
            @click="handleCategorySelect(cat.id)"
            class="group cursor-pointer"
          >
            <div class="relative overflow-hidden rounded-lg aspect-square">
              <img 
                :src="cat.image" 
                :alt="cat.name"
                class="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-500"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end p-4">
                <h3 class="text-white font-bold text-lg">{{ cat.name }}</h3>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Rings Collection -->
    <section v-if="activeCategory === 'all' || activeCategory === 'rings'" class="py-16 bg-white dark:bg-gray-900">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex items-center justify-between mb-8">
          <div>
            <h2 class="text-3xl font-serif font-bold text-gray-900 dark:text-white">Rings</h2>
            <p class="text-gray-600 dark:text-gray-400 mt-1">Symbols of love & commitment</p>
          </div>
          <button @click="handleCategorySelect('rings')" class="text-[#C9A962] font-medium hover:underline flex items-center gap-2">
            View All
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <ProductCard 
            v-for="item in displayItems.rings" 
            :key="item.item_code" 
            :product="item"
            :isDark="isDark"
            @click="openProduct(item)"
          />
        </div>
      </div>
    </section>

    <!-- Earrings Collection -->
    <section v-if="activeCategory === 'all' || activeCategory === 'earrings'" class="py-16 bg-gray-50 dark:bg-gray-800">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex items-center justify-between mb-8">
          <div>
            <h2 class="text-3xl font-serif font-bold text-gray-900 dark:text-white">Earrings</h2>
            <p class="text-gray-600 dark:text-gray-400 mt-1">Elegance that speaks volumes</p>
          </div>
          <button @click="handleCategorySelect('earrings')" class="text-[#C9A962] font-medium hover:underline flex items-center gap-2">
            View All
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <ProductCard 
            v-for="item in displayItems.earrings" 
            :key="item.item_code" 
            :product="item"
            :isDark="isDark"
            @click="openProduct(item)"
          />
        </div>
      </div>
    </section>

    <!-- Chains Collection -->
    <section v-if="activeCategory === 'all' || activeCategory === 'chains'" class="py-16 bg-white dark:bg-gray-900">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex items-center justify-between mb-8">
          <div>
            <h2 class="text-3xl font-serif font-bold text-gray-900 dark:text-white">Chains & Necklaces</h2>
            <p class="text-gray-600 dark:text-gray-400 mt-1">Classic pieces for every occasion</p>
          </div>
          <button @click="handleCategorySelect('chains')" class="text-[#C9A962] font-medium hover:underline flex items-center gap-2">
            View All
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <ProductCard 
            v-for="item in displayItems.chains" 
            :key="item.item_code" 
            :product="item"
            :isDark="isDark"
            @click="openProduct(item)"
          />
        </div>
      </div>
    </section>

    <!-- Bracelets Collection -->
    <section v-if="activeCategory === 'all' || activeCategory === 'bracelets'" class="py-16 bg-gray-50 dark:bg-gray-800">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex items-center justify-between mb-8">
          <div>
            <h2 class="text-3xl font-serif font-bold text-gray-900 dark:text-white">Bracelets</h2>
            <p class="text-gray-600 dark:text-gray-400 mt-1">Adorn your wrists with elegance</p>
          </div>
          <button @click="handleCategorySelect('bracelets')" class="text-[#C9A962] font-medium hover:underline flex items-center gap-2">
            View All
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <ProductCard 
            v-for="item in displayItems.bracelets" 
            :key="item.item_code" 
            :product="item"
            :isDark="isDark"
            @click="openProduct(item)"
          />
        </div>
      </div>
    </section>

    <!-- Pendants Collection -->
    <section v-if="activeCategory === 'all' || activeCategory === 'pendants'" class="py-16 bg-white dark:bg-gray-900">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex items-center justify-between mb-8">
          <div>
            <h2 class="text-3xl font-serif font-bold text-gray-900 dark:text-white">Pendants</h2>
            <p class="text-gray-600 dark:text-gray-400 mt-1">Personal & meaningful</p>
          </div>
          <button @click="handleCategorySelect('pendants')" class="text-[#C9A962] font-medium hover:underline flex items-center gap-2">
            View All
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <ProductCard 
            v-for="item in displayItems.pendants" 
            :key="item.item_code" 
            :product="item"
            :isDark="isDark"
            @click="openProduct(item)"
          />
        </div>
      </div>
    </section>

    <!-- Product Modal -->
    <ProductModal 
      :show="showProductModal" 
      :item-code="selectedItemCode"
      @close="showProductModal = false; selectedItemCode = null"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Header from '@/components/Header.vue'
import ProductCard from '@/components/JewelryProductCard.vue'
import ProductModal from '@/components/ProductModal.vue'
import { createResource } from 'frappe-ui'

// Theme
const isDark = ref(false)
const activeCategory = ref('all')
const showProductModal = ref(false)
const selectedItemCode = ref(null)

// Placeholder data with Unsplash images
const categories = [
  { id: 'rings', name: 'Rings', image: 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=400&q=80' },
  { id: 'earrings', name: 'Earrings', image: 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=400&q=80' },
  { id: 'chains', name: 'Chains', image: 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&q=80' },
  { id: 'bracelets', name: 'Bracelets', image: 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400&q=80' },
  { id: 'pendants', name: 'Pendants', image: 'https://images.unsplash.com/photo-1603561591411-07134e71a2a9?w=400&q=80' }
]

// Sample product data with images
const createDemoItem = (id, name, category, price, image) => ({
  item_code: `DEMO-${id}`,
  item_name: name,
  jewelry_type: category,
  price: price,
  image: image,
  metal: '14K Gold',
  purity: '14K',
  stock_qty: 5,
  is_featured: Math.random() > 0.7
})

const displayItems = computed(() => ({
  rings: [
    createDemoItem(1, 'Diamond Solitaire Ring', 'Rings', 2499, 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=600&q=80'),
    createDemoItem(2, 'Gold Engagement Ring', 'Rings', 1899, 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&q=80'),
    createDemoItem(3, 'Rose Gold Band', 'Rings', 1299, 'https://images.unsplash.com/photo-1603561596112-0a132b757442?w=600&q=80'),
    createDemoItem(4, 'Eternity Diamond Ring', 'Rings', 3299, 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600&q=80')
  ],
  earrings: [
    createDemoItem(5, 'Diamond Stud Earrings', 'Earrings', 1799, 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=600&q=80'),
    createDemoItem(6, 'Gold Hoop Earrings', 'Earrings', 899, 'https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?w=600&q=80'),
    createDemoItem(7, 'Pearl Drop Earrings', 'Earrings', 1299, 'https://images.unsplash.com/photo-1630019329417-60d5e968e02b?w=600&q=80'),
    createDemoItem(8, 'Chandelier Earrings', 'Earrings', 2199, 'https://images.unsplash.com/photo-1596944924591-4e2f08656a2e?w=600&q=80')
  ],
  chains: [
    createDemoItem(9, 'Gold Chain Necklace', 'Chains', 1599, 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600&q=80'),
    createDemoItem(10, 'Diamond Pendant Chain', 'Necklaces', 2899, 'https://images.unsplash.com/photo-1602751584552-8ba73aad10e1?w=600&q=80'),
    createDemoItem(11, 'Layered Gold Necklace', 'Necklaces', 1799, 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600&q=80'),
    createDemoItem(12, 'Statement Necklace', 'Necklaces', 3499, 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&q=80')
  ],
  bracelets: [
    createDemoItem(13, 'Tennis Bracelet', 'Bracelets', 2799, 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600&q=80'),
    createDemoItem(14, 'Gold Bangle', 'Bracelets', 1499, 'https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=600&q=80'),
    createDemoItem(15, 'Charm Bracelet', 'Bracelets', 1899, 'https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=600&q=80'),
    createDemoItem(16, 'Diamond Link Bracelet', 'Bracelets', 3299, 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&q=80')
  ],
  pendants: [
    createDemoItem(17, 'Heart Pendant', 'Pendants', 1299, 'https://images.unsplash.com/photo-1603561591411-07134e71a2a9?w=600&q=80'),
    createDemoItem(18, 'Diamond Cross Pendant', 'Pendants', 1999, 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600&q=80'),
    createDemoItem(19, 'Initial Pendant', 'Pendants', 899, 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&q=80'),
    createDemoItem(20, 'Gemstone Pendant', 'Pendants', 2299, 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600&q=80')
  ]
}))

function handleCategorySelect(categoryId) {
  activeCategory.value = categoryId
  scrollToSection('collections')
}

function openProduct(item) {
  selectedItemCode.value = item.item_code
  showProductModal.value = true
}

function scrollToSection(id) {
  const element = document.getElementById(id)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

function toggleTheme() {
  isDark.value = !isDark.value
}

function performSearch(query) {
  console.log('Search:', query)
}

onMounted(() => {
  const theme = localStorage.getItem('zevar-theme')
  isDark.value = theme === 'dark'
})
</script>

<template>
  <div class="relative w-full overflow-hidden rounded-2xl" :class="isDark ? 'shadow-2xl shadow-black/50' : 'shadow-xl'">
    <!-- Main Banner -->
    <div 
      class="relative h-[320px] sm:h-[400px] lg:h-[450px] overflow-hidden transition-all duration-700"
      @mouseenter="pauseAutoSlide = true"
      @mouseleave="pauseAutoSlide = false"
    >
      <!-- Banner Slides -->
      <div 
        v-for="(banner, index) in banners" 
        :key="banner.id"
        class="absolute inset-0 transition-all duration-700 ease-out"
        :class="[
          index === activeIndex ? 'opacity-100 translate-x-0' : 
          index < activeIndex ? 'opacity-0 -translate-x-full' : 'opacity-0 translate-x-full'
        ]"
      >
        <!-- Background Gradient -->
        <div 
          class="absolute inset-0"
          :style="{ background: banner.gradient }"
        ></div>
        
        <!-- Decorative Elements -->
        <div class="absolute inset-0 overflow-hidden">
          <!-- Sparkles/Stars -->
          <div v-for="n in 8" :key="n" 
            class="absolute w-1 h-1 bg-white/40 rounded-full animate-pulse"
            :style="{ 
              top: `${10 + (n * 10)}%`, 
              right: `${5 + (n * 8)}%`,
              animationDelay: `${n * 0.2}s`
            }"
          ></div>
          
          <!-- Floating jewelry icons -->
          <div class="absolute top-10 right-20 text-6xl opacity-20 animate-float">💎</div>
          <div class="absolute bottom-20 right-32 text-4xl opacity-15 animate-float-delayed">✨</div>
          <div class="absolute top-1/3 right-1/4 text-5xl opacity-10 animate-float">💍</div>
        </div>
        
        <!-- Content -->
        <div class="relative h-full flex items-center px-8 sm:px-12 lg:px-16">
          <div class="max-w-lg">
            <!-- Badge -->
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium mb-4"
              :style="{ background: 'rgba(255,255,255,0.15)', color: 'white' }">
              <span class="w-2 h-2 rounded-full bg-white animate-pulse"></span>
              {{ banner.badge }}
            </div>
            
            <!-- Brand -->
            <div class="text-white/70 text-sm font-medium tracking-widest uppercase mb-2">ZEVAR</div>
            
            <!-- Title (Script Font) -->
            <h2 class="text-4xl sm:text-5xl lg:text-6xl font-serif italic text-white mb-4 leading-tight">
              {{ banner.title }}
            </h2>
            
            <!-- Offer -->
            <div class="flex items-baseline gap-2 mb-6">
              <span class="text-2xl sm:text-3xl font-bold text-white">{{ banner.offer }}</span>
              <span class="text-white/60 text-sm">{{ banner.offerSubtext }}</span>
            </div>
            
            <!-- CTA Button -->
            <button 
              class="px-8 py-3 bg-white text-gray-900 font-semibold rounded-lg hover:bg-gray-100 transition-all hover:scale-105 hover:shadow-lg"
            >
              {{ banner.cta }}
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Navigation Dots -->
    <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-2">
      <button 
        v-for="(banner, index) in banners" 
        :key="banner.id"
        @click="goToSlide(index)"
        class="w-2 h-2 rounded-full transition-all duration-300"
        :class="index === activeIndex ? 'bg-white w-6' : 'bg-white/40 hover:bg-white/60'"
      ></button>
    </div>
    
    <!-- Arrow Navigation -->
    <button 
      @click="prevSlide" 
      class="absolute left-4 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center text-white hover:bg-white/20 transition-all"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
      </svg>
    </button>
    <button 
      @click="nextSlide" 
      class="absolute right-4 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center text-white hover:bg-white/20 transition-all"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

defineProps({
  isDark: { type: Boolean, default: true }
})

const activeIndex = ref(0)
const pauseAutoSlide = ref(false)
let slideInterval = null

const banners = [
  {
    id: 'valentines',
    badge: 'Limited Time Offer',
    title: "Valentine's Special",
    offer: 'FLAT 20% OFF',
    offerSubtext: 'on all heart designs',
    cta: 'SHOP NOW',
    gradient: 'linear-gradient(135deg, #8B3A62 0%, #C9A962 50%, #6B2D5B 100%)'
  },
  {
    id: 'wedding',
    badge: 'Bridal Collection 2025',
    title: "Wedding Season",
    offer: 'UP TO 30% OFF',
    offerSubtext: 'on bridal sets',
    cta: 'EXPLORE BRIDAL',
    gradient: 'linear-gradient(135deg, #C9A962 0%, #8B7355 50%, #1a1a1a 100%)'
  },
  {
    id: 'anniversary',
    badge: 'Celebrate Love',
    title: "Anniversary Gifts",
    offer: 'FREE ENGRAVING',
    offerSubtext: 'on select rings',
    cta: 'FIND GIFTS',
    gradient: 'linear-gradient(135deg, #1a1a1a 0%, #C9A962 50%, #8B3A62 100%)'
  },
  {
    id: 'mothers-day',
    badge: 'Coming Soon',
    title: "Mother's Day",
    offer: 'EARLY BIRD 25% OFF',
    offerSubtext: 'pre-order now',
    cta: 'PRE-ORDER',
    gradient: 'linear-gradient(135deg, #D4A5A5 0%, #C9A962 50%, #8B7355 100%)'
  }
]

function nextSlide() {
  activeIndex.value = (activeIndex.value + 1) % banners.length
}

function prevSlide() {
  activeIndex.value = (activeIndex.value - 1 + banners.length) % banners.length
}

function goToSlide(index) {
  activeIndex.value = index
}

function startAutoSlide() {
  slideInterval = setInterval(() => {
    if (!pauseAutoSlide.value) {
      nextSlide()
    }
  }, 5000)
}

onMounted(() => {
  startAutoSlide()
})

onUnmounted(() => {
  if (slideInterval) {
    clearInterval(slideInterval)
  }
})
</script>

<style scoped>
@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(10deg); }
}

@keyframes float-delayed {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-15px) rotate(-5deg); }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animate-float-delayed {
  animation: float-delayed 8s ease-in-out infinite;
  animation-delay: 1s;
}
</style>

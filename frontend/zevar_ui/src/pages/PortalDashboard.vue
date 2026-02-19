<template>
  <PortalLayout>
    <div class="px-10 pb-10 flex flex-col gap-8 font-display">
      <!-- Welcome Section -->
      <section class="mt-4">
        <div class="flex flex-wrap items-end justify-between gap-6">
          <div>
            <h2 class="text-5xl font-extrabold tracking-tight mb-2">
              Welcome back! <span class="rainbow-text">👋</span>
            </h2>
            <p class="text-white/50 text-lg font-medium">It's a beautiful Monday morning at Zevar.</p>
          </div>
          <div class="flex gap-3">
            <button class="flex items-center gap-2 px-6 py-4 bg-white/5 hover:bg-white/10 text-white font-bold rounded-full transition-all border border-white/10">
              <span class="material-symbols-outlined">description</span>
              Export Report
            </button>
            <button class="flex items-center gap-2 px-8 py-4 bg-portal-primary text-portal-bg-dark font-black rounded-full shadow-lg shadow-portal-primary/20 hover:scale-105 transition-all">
              <span class="material-symbols-outlined">login</span>
              Check In
            </button>
          </div>
        </div>
      </section>

      <!-- Stats Cards -->
      <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="glass-card glass-card-hover p-8 rounded-xl flex flex-col gap-4 relative overflow-hidden group">
          <div class="absolute -top-6 -right-6 size-24 bg-portal-primary/10 rounded-full blur-3xl group-hover:bg-portal-primary/20 transition-colors"></div>
          <div class="flex justify-between items-start">
            <div class="size-12 rounded-2xl bg-portal-primary/10 flex items-center justify-center">
              <span class="material-symbols-outlined text-portal-primary text-3xl">schedule</span>
            </div>
            <span class="text-portal-accent-teal text-sm font-bold bg-portal-accent-teal/10 px-3 py-1 rounded-full">+2.5%</span>
          </div>
          <div>
            <p class="text-white/50 font-medium text-sm mb-1 uppercase tracking-widest">Hours Worked</p>
            <p class="text-4xl font-black tracking-tight">38.5h</p>
          </div>
        </div>

        <div class="glass-card glass-card-hover p-8 rounded-xl flex flex-col gap-4 relative overflow-hidden group">
          <div class="absolute -top-6 -right-6 size-24 bg-portal-accent-teal/10 rounded-full blur-3xl group-hover:bg-portal-accent-teal/20 transition-colors"></div>
          <div class="flex justify-between items-start">
            <div class="size-12 rounded-2xl bg-portal-accent-teal/10 flex items-center justify-center">
              <span class="material-symbols-outlined text-portal-accent-teal text-3xl">flight_takeoff</span>
            </div>
            <span class="text-white/40 text-sm font-bold bg-white/5 px-3 py-1 rounded-full">Used 6</span>
          </div>
          <div>
            <p class="text-white/50 font-medium text-sm mb-1 uppercase tracking-widest">Remaining PTO</p>
            <p class="text-4xl font-black tracking-tight">14 Days</p>
          </div>
        </div>

        <div class="glass-card glass-card-hover p-8 rounded-xl flex flex-col gap-4 relative overflow-hidden group">
          <div class="absolute -top-6 -right-6 size-24 bg-portal-accent-indigo/10 rounded-full blur-3xl group-hover:bg-portal-accent-indigo/20 transition-colors"></div>
          <div class="flex justify-between items-start">
            <div class="size-12 rounded-2xl bg-portal-accent-indigo/10 flex items-center justify-center">
              <span class="material-symbols-outlined text-portal-accent-indigo text-3xl">payments</span>
            </div>
            <span class="text-orange-400 text-sm font-bold bg-orange-400/10 px-3 py-1 rounded-full">In 4 Days</span>
          </div>
          <div>
            <p class="text-white/50 font-medium text-sm mb-1 uppercase tracking-widest">Next Payday</p>
            <p class="text-4xl font-black tracking-tight">$4,250</p>
          </div>
        </div>

        <div class="glass-card glass-card-hover p-8 rounded-xl flex flex-col gap-4 relative overflow-hidden group">
          <div class="absolute -top-6 -right-6 size-24 bg-portal-primary/10 rounded-full blur-3xl group-hover:bg-portal-primary/20 transition-colors"></div>
          <div class="flex justify-between items-start">
            <div class="size-12 rounded-2xl bg-portal-primary/10 flex items-center justify-center">
              <span class="material-symbols-outlined text-portal-primary text-3xl">celebration</span>
            </div>
          </div>
          <div>
            <p class="text-white/50 font-medium text-sm mb-1 uppercase tracking-widest">Birthdays</p>
            <div class="flex items-center gap-2">
              <p class="text-4xl font-black tracking-tight">2 Today</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Activity & Mood Section -->
      <section class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 glass-card rounded-xl p-8">
          <div class="flex items-center justify-between mb-8">
            <div>
              <h3 class="text-2xl font-bold tracking-tight text-white">Recent Activity</h3>
              <p class="text-white/50 text-sm font-portal">Review your latest check-ins and logs</p>
            </div>
            <button class="text-portal-primary font-bold text-sm hover:underline">View All</button>
          </div>
          <div class="flex flex-col gap-4 font-portal">
            <div class="flex items-center gap-4 p-4 rounded-2xl hover:bg-white/5 transition-colors group">
              <div class="size-12 rounded-full bg-portal-accent-teal/10 flex items-center justify-center shrink-0">
                <span class="material-symbols-outlined text-portal-accent-teal">login</span>
              </div>
              <div class="flex-1">
                <p class="font-bold">Clocked In</p>
                <p class="text-xs text-white/40">Remote • Monday, 9:00 AM</p>
              </div>
              <div class="text-right">
                <span class="px-3 py-1 rounded-full bg-white/5 text-[10px] font-bold uppercase tracking-widest text-white/60">Verified</span>
              </div>
            </div>
            <div class="flex items-center gap-4 p-4 rounded-2xl hover:bg-white/5 transition-colors group">
              <div class="size-12 rounded-full bg-portal-primary/10 flex items-center justify-center shrink-0">
                <span class="material-symbols-outlined text-portal-primary">description</span>
              </div>
              <div class="flex-1">
                <p class="font-bold">Leave Request Approved</p>
                <p class="text-xs text-white/40">Summer Vacation • 4 Days</p>
              </div>
              <div class="text-right">
                <span class="px-3 py-1 rounded-full bg-portal-accent-teal/10 text-[10px] font-bold uppercase tracking-widest text-portal-accent-teal">Complete</span>
              </div>
            </div>
          </div>
        </div>

        <div class="flex flex-col gap-8">
          <div class="glass-card rounded-xl p-8 bg-gradient-to-br from-portal-accent-indigo/10 to-transparent border-portal-accent-indigo/20">
            <div class="flex items-center gap-3 mb-6">
              <div class="size-10 rounded-full bg-portal-accent-indigo/20 flex items-center justify-center">
                <span class="material-symbols-outlined text-portal-accent-indigo">mood</span>
              </div>
              <h3 class="text-xl font-bold tracking-tight">Daily Pulse</h3>
            </div>
            <p class="text-white/60 text-sm mb-6 leading-relaxed font-portal">How are you feeling about work today?</p>
            <div class="flex justify-between gap-2 text-2xl">
              <button class="flex-1 aspect-square rounded-2xl glass-card hover:bg-portal-accent-teal/20 hover:scale-105 transition-all flex items-center justify-center">😊</button>
              <button class="flex-1 aspect-square rounded-2xl glass-card hover:bg-portal-primary/20 hover:scale-105 transition-all flex items-center justify-center">😐</button>
              <button class="flex-1 aspect-square rounded-2xl glass-card hover:bg-orange-400/20 hover:scale-105 transition-all flex items-center justify-center">😔</button>
              <button class="flex-1 aspect-square rounded-2xl glass-card hover:bg-red-400/20 hover:scale-105 transition-all flex items-center justify-center">🔥</button>
            </div>
          </div>
        </div>
      </section>
    </div>
  </PortalLayout>
</template>

<script setup>
import PortalLayout from '@/components/PortalLayout.vue';
</script>

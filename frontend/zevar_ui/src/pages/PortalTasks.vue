<template>
  <PortalLayout>
    <div class="px-10 pb-10 flex flex-col gap-8 font-portal">
      <!-- Header Section -->
      <section class="mt-4">
        <div class="flex flex-wrap items-end justify-between gap-6">
          <div>
            <h1 class="text-4xl font-800 tracking-tight mb-2">My Tasks</h1>
            <p class="text-white/50 text-lg">You have <span class="text-portal-primary font-bold">4 tasks</span> assigned for today.</p>
          </div>
          <button class="neon-glow flex items-center gap-3 bg-gradient-to-r from-portal-primary to-portal-accent-indigo hover:scale-105 transition-transform px-8 py-4 rounded-full font-bold text-lg">
            <span class="material-symbols-outlined">add_circle</span>
            New Task
          </button>
        </div>
      </section>

      <!-- Task Lists -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Assigned / To Do -->
        <div class="flex flex-col gap-6">
          <div class="flex items-center justify-between border-b border-white/10 pb-4">
            <h3 class="text-xl font-bold flex items-center gap-2">
              <span class="size-2 rounded-full bg-portal-primary"></span>
              Assigned
            </h3>
            <span class="bg-white/5 px-3 py-1 rounded-full text-xs font-bold text-white/40">2</span>
          </div>
          
          <div class="flex flex-col gap-4">
            <div v-for="task in assignedTasks" :key="task.id" class="glass-card hover:bg-white/5 p-6 rounded-2xl group cursor-pointer transition-all border border-white/5 hover:border-portal-primary/30">
              <div class="flex justify-between items-start mb-4">
                <span class="text-[10px] font-black uppercase text-portal-primary tracking-widest bg-portal-primary/10 px-2 py-1 rounded">{{ task.category }}</span>
                <span class="material-symbols-outlined text-white/20 group-hover:text-white transition-colors">more_horiz</span>
              </div>
              <h4 class="font-bold text-lg mb-2 group-hover:text-portal-primary transition-colors">{{ task.title }}</h4>
              <p class="text-sm text-white/50 mb-4 line-clamp-2 leading-relaxed">{{ task.description }}</p>
              <div class="flex items-center justify-between pt-4 border-t border-white/5">
                <div class="flex -space-x-2">
                  <div class="size-7 rounded-full border border-portal-bg-dark bg-cover bg-center" style="background-image: url('https://i.pravatar.cc/100?u=1')"></div>
                  <div class="size-7 rounded-full border border-portal-bg-dark bg-cover bg-center" style="background-image: url('https://i.pravatar.cc/100?u=2')"></div>
                </div>
                <div class="flex items-center gap-1 text-white/40 text-xs font-medium">
                  <span class="material-symbols-outlined text-sm">calendar_today</span>
                  {{ task.dueDate }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- In Progress -->
        <div class="flex flex-col gap-6">
          <div class="flex items-center justify-between border-b border-white/10 pb-4">
            <h3 class="text-xl font-bold flex items-center gap-2">
              <span class="size-2 rounded-full bg-portal-accent-indigo"></span>
              In Progress
            </h3>
            <span class="bg-white/5 px-3 py-1 rounded-full text-xs font-bold text-white/40">1</span>
          </div>

          <div class="flex flex-col gap-4">
            <div class="glass-card border-l-4 border-l-portal-accent-indigo p-6 rounded-2xl bg-portal-accent-indigo/5">
              <div class="flex justify-between items-start mb-4">
                <span class="text-[10px] font-black uppercase text-portal-accent-indigo tracking-widest bg-portal-accent-indigo/10 px-2 py-1 rounded">Development</span>
              </div>
              <h4 class="font-bold text-lg mb-2">Portal UI Components</h4>
              <p class="text-sm text-white/50 mb-4">Implementing the new premium design system for the employee portal.</p>
              <div class="w-full bg-white/5 rounded-full h-1.5 mb-4">
                <div class="bg-portal-accent-indigo h-1.5 rounded-full" style="width: 65%"></div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-[10px] font-bold text-portal-accent-indigo">65% Complete</span>
                <span class="text-[10px] text-white/40 font-bold uppercase">Due Today</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Completed -->
        <div class="flex flex-col gap-6">
          <div class="flex items-center justify-between border-b border-white/10 pb-4">
            <h3 class="text-xl font-bold flex items-center gap-2">
              <span class="size-2 rounded-full bg-portal-accent-teal"></span>
              Completed
            </h3>
            <span class="bg-white/5 px-3 py-1 rounded-full text-xs font-bold text-white/40">12</span>
          </div>
          
          <div class="flex flex-col gap-4 opacity-60 grayscale hover:opacity-100 hover:grayscale-0 transition-all">
             <div class="glass-card p-6 rounded-2xl">
              <div class="flex items-center gap-3 mb-4 text-portal-accent-teal">
                <span class="material-symbols-outlined">check_circle</span>
                <span class="text-[10px] font-black uppercase tracking-widest">Done</span>
              </div>
              <h4 class="font-bold text-lg mb-2 line-through">Brand Guidelines Review</h4>
              <p class="text-xs text-white/40 italic">Completed on Feb 15, 2024</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </PortalLayout>
</template>

<script setup>
import PortalLayout from '@/components/PortalLayout.vue';

const assignedTasks = [
  {
    id: 1,
    category: 'Design',
    title: 'Jewelry Catalog Layout',
    description: 'Refine the grid and card design for the premium jewelry collection display.',
    dueDate: 'Feb 20',
  },
  {
    id: 2,
    category: 'Marketing',
    title: 'Spring Campaign Assets',
    description: 'Prepare high-resolution banners and social media graphics for the upcoming sales event.',
    dueDate: 'Feb 21',
  }
];
</script>

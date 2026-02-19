<template>
  <div class="grid grid-cols-12 gap-6 max-w-7xl mx-auto h-[calc(100vh-6rem)]">
    
    <!-- Left Column: Clock & Widgets -->
    <div class="col-span-12 lg:col-span-8 flex flex-col gap-6 h-full">
      
      <!-- Clock Section -->
      <div class="flex-1 flex flex-col items-center justify-center py-2 glass-card rounded-[2rem] border border-white/5 relative bg-gradient-to-b from-white/5 to-transparent overflow-visible">
        <!-- Background decorative elements -->
        <div class="absolute top-0 left-0 w-full h-full diamond-pattern opacity-30 pointer-events-none rounded-[2rem] overflow-hidden"></div>
        <div class="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black/40 pointer-events-none rounded-[2rem]"></div>

        <div class="relative group z-10 scale-100">
          <!-- Outer Bezel (Massive) -->
          <div class="w-[380px] h-[380px] rounded-full metallic-bezel border-[4px] border-[#2a2a2a] flex items-center justify-center relative p-1 shadow-[0_0_60px_rgba(0,0,0,0.8)]">
            <!-- Glowing Border Ring -->
            <div class="absolute inset-0 rounded-full border border-primary/20 shadow-[0_0_40px_rgba(252,211,77,0.1)]"></div>
            
            <!-- Inner Bezel Detail -->
             <div class="w-full h-full rounded-full border-[10px] border-[#0a0c1a] shadow-inner flex items-center justify-center relative bg-[#05070a]">
                
                 <!-- Digital Face -->
                <div class="w-full h-full rounded-full flex flex-col items-center justify-center relative overflow-hidden bg-[radial-gradient(circle_at_center,_#1a1d2d_0%,_#05070a_70%)]">
                    <!-- Subtle grid/texture on face -->
                    <div class="absolute inset-0 opacity-10" style="background-image: radial-gradient(#fff 1px, transparent 1px); background-size: 20px 20px;"></div>

                    <div class="absolute top-[22%] text-[10px] text-white/30 tracking-[0.4em] font-bold uppercase font-display">Current Shift</div>
                    
                    <!-- Huge Timer -->
                    <!-- Adjusted font size to fit HH:MM:SS (8 chars) in ~300px width -->
                    <!-- 360px inner width. 8 chars. ~45px per char. ~2.8rem? Let's try 4rem (approx 64px) condensed -->
                    <div class="text-[4.5rem] leading-none font-mono font-bold tracking-tighter mt-2 transition-colors duration-500 z-10 drop-shadow-2xl tabular-nums"
                        :class="getTimerColor">
                        {{ clockedIn ? elapsedTime : '00:00:00' }}
                    </div>
                    
                     <!-- Active Indicators -->
                    <div class="absolute bottom-[22%] flex gap-3" v-if="clockedIn">
                        <span class="w-2 h-2 rounded-full animate-pulse shadow-[0_0_10px_currentColor]" :class="getDotColor"></span>
                        <span class="w-2 h-2 rounded-full opacity-30" :class="getDotColor"></span>
                        <span class="w-2 h-2 rounded-full opacity-20" :class="getDotColor"></span>
                    </div>
                </div>
             </div>
          </div>
        </div>

        <!-- Buttons -->
        <div class="mt-8 flex gap-4 w-full max-w-sm z-10">
          <button 
            @click="handleClockIn"
            :disabled="clockedIn || loading"
            class="flex-1 h-14 rounded-xl flex items-center justify-center gap-2 transition-all relative font-bold tracking-widest text-sm uppercase"
            :class="[
              !clockedIn 
                ? 'bg-[#FCD34D] text-black hover:bg-[#FDE047] hover:scale-[1.02] shadow-[0_0_30px_rgba(252,211,77,0.3)]' 
                : 'bg-white/5 border border-white/5 text-white/20 cursor-not-allowed'
            ]"
          >
            Clock In
          </button>
          
          <button 
            @click="handleClockOut"
            :disabled="!clockedIn || loading"
            class="flex-1 h-14 rounded-xl flex items-center justify-center gap-2 transition-all relative font-bold tracking-widest text-sm uppercase"
            :class="[
              clockedIn
                ? 'bg-[#1a1a1a] border border-white/10 text-white hover:bg-[#252525] hover:border-white/20 hover:text-red-400 shadow-lg'
                : 'bg-white/5 border border-white/5 text-white/20 cursor-not-allowed'
            ]"
          >
            Clock Out
          </button>
        </div>
      </div>

      <!-- Bottom Info Row -->
      <div class="grid grid-cols-3 gap-6 shrink-0 h-72">
        <!-- Profile & Designation -->
        <div class="glass-card rounded-2xl p-5 border border-white/5 flex flex-col justify-between relative overflow-hidden group hover:border-white/10 transition-colors">
            <div class="absolute top-0 right-0 p-3 opacity-5 group-hover:opacity-10 transition-opacity">
                <span class="material-symbols-outlined text-6xl">badge</span>
            </div>
            <div>
                <p class="text-[10px] text-white/40 font-bold uppercase tracking-wider mb-1">My Profile</p>
                <div class="flex items-center gap-3 mt-1">
                    <div class="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-orange-500 flex items-center justify-center text-black font-bold text-sm shadow-lg shadow-primary/20">AW</div>
                    <div>
                        <p class="text-sm font-bold text-white leading-tight">Alexander Wright</p>
                        <p class="text-[10px] text-primary mt-0.5">Senior Jeweler</p>
                    </div>
                </div>
            </div>
             <button class="mt-2 py-2 px-3 bg-white/5 hover:bg-white/10 rounded-lg text-[10px] font-bold text-white border border-white/5 flex items-center gap-2 w-full justify-center transition-all group-hover:bg-white/10">
                <span class="material-symbols-outlined text-[14px]">account_box</span>
                View Profile
            </button>
        </div>

        <!-- Reporting Manager -->
        <div class="glass-card rounded-2xl p-5 border border-white/5 flex flex-col justify-between relative overflow-hidden group hover:border-white/10 transition-colors">
             <div class="absolute top-0 right-0 p-3 opacity-5 group-hover:opacity-10 transition-opacity">
                <span class="material-symbols-outlined text-6xl">supervisor_account</span>
            </div>
            <div>
                <p class="text-[10px] text-white/40 font-bold uppercase tracking-wider mb-1">Reporting To</p>
                <div class="flex items-center gap-3 mt-2">
                    <div class="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400 font-bold text-xs ring-1 ring-blue-500/30">RK</div>
                    <div>
                        <p class="text-sm font-bold text-white">Rajesh Kumar</p>
                        <p class="text-[10px] text-white/50">Production Head</p>
                    </div>
                </div>
            </div>
            <button class="mt-auto py-2 px-3 bg-white/5 hover:bg-white/10 rounded-lg text-[10px] font-bold text-white/70 border border-white/5 w-full transition-all">
                View Team
            </button>
        </div>

        <!-- Payslip -->
        <div class="glass-card rounded-2xl p-5 border border-white/5 flex flex-col justify-between relative overflow-hidden group hover:border-white/10 transition-colors">
             <div class="absolute top-0 right-0 p-3 opacity-5 group-hover:opacity-10 transition-opacity">
                <span class="material-symbols-outlined text-6xl">payments</span>
            </div>
            <div>
                <p class="text-[10px] text-white/40 font-bold uppercase tracking-wider mb-1">Payroll</p>
                <p class="text-base font-bold text-white">Oct 2023</p>
                <p class="text-[10px] text-emerald-400 mt-1 flex items-center gap-1 bg-emerald-400/10 w-fit px-1.5 py-0.5 rounded">
                    <span class="material-symbols-outlined text-[10px]">check_circle</span> Paid
                </p>
            </div>
            <button class="mt-4 py-2 px-3 bg-primary/10 hover:bg-primary/20 rounded-lg text-[10px] font-bold text-primary border border-primary/20 flex items-center justify-center gap-2 w-full transition-all">
                <span class="material-symbols-outlined text-[14px]">visibility</span>
                View Slip
            </button>
        </div>
      </div>
    </div>

    <!-- Right Column: Split Activity & Todos -->
    <div class="col-span-12 lg:col-span-4 flex flex-col gap-6 h-full">
      
      <!-- Top: Notifications / Activity -->
      <div class="glass-card rounded-[2rem] p-6 h-1/2 border border-white/10 flex flex-col">
        <div class="flex items-center justify-between mb-4">
            <h3 class="font-bold text-lg text-white font-display">Activity & Alerts</h3>
             <span class="w-2 h-2 bg-primary rounded-full animate-pulse shadow-[0_0_8px_#FCD34D]"></span>
        </div>
        
        <div class="flex-1 overflow-y-auto custom-scrollbar space-y-4 pr-2">
            <!-- Static Notifications for Demo -->
             <div class="flex gap-3 relative group">
                <div class="w-8 h-8 rounded-full bg-blue-500/10 flex items-center justify-center shrink-0 border border-blue-500/20 text-blue-400">
                     <span class="material-symbols-outlined text-[16px]">assignment_turned_in</span>
                </div>
                <div>
                    <p class="text-xs font-bold text-white leading-snug group-hover:text-blue-400 transition-colors">New Task Assigned</p>
                    <p class="text-[10px] text-white/40 mt-0.5">"Gemstone Inventory Check" assigned by Rajesh K.</p>
                    <p class="text-[9px] text-white/20 mt-1">2 mins ago</p>
                </div>
            </div>

            <div class="flex gap-3 relative group">
                <div class="w-8 h-8 rounded-full bg-emerald-500/10 flex items-center justify-center shrink-0 border border-emerald-500/20 text-emerald-400">
                     <span class="material-symbols-outlined text-[16px]">check_circle</span>
                </div>
                <div>
                    <p class="text-xs font-bold text-white leading-snug group-hover:text-emerald-400 transition-colors">Leave Approved</p>
                    <p class="text-[10px] text-white/40 mt-0.5">Your leave for Nov 14th has been approved.</p>
                    <p class="text-[9px] text-white/20 mt-1">1 hour ago</p>
                </div>
            </div>

            <!-- Recent Clock Logs -->
             <div v-for="log in recentLogs" :key="log.id" class="flex gap-3 relative group opacity-60 hover:opacity-100 transition-opacity">
                <div class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 border bg-[#0a0c1a]"
                     :class="log.type === 'clock-out' ? 'border-primary/50 text-primary' : 'border-white/10 text-white/40'">
                  <span class="material-symbols-outlined text-[16px]">{{ log.icon }}</span>
                </div>
                <div>
                  <p class="text-xs font-bold text-white transition-colors group-hover:text-primary leading-snug">{{ log.title }}</p>
                  <p class="text-[9px] text-white/30 mt-0.5">{{ log.time }}</p>
                </div>
              </div>
        </div>
      </div>

      <!-- Bottom: Todos -->
      <div class="glass-card rounded-[2rem] p-6 h-1/2 border border-white/10 flex flex-col">
        <div class="flex items-center justify-between mb-4">
            <h3 class="font-bold text-lg text-white font-display">My Tasks</h3>
            <button class="w-6 h-6 rounded-full bg-white/5 hover:bg-white/10 flex items-center justify-center text-white/50 hover:text-white transition-all border border-white/5">
                <span class="material-symbols-outlined text-[16px]">add</span>
            </button>
        </div>
        
        <div class="flex-1 overflow-y-auto custom-scrollbar space-y-2 pr-2">
            <div v-for="todo in todos" :key="todo.id" class="group flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-all border border-transparent hover:border-white/5 cursor-pointer">
                <div class="w-4 h-4 rounded border border-white/20 flex items-center justify-center group-hover:border-primary transition-colors text-transparent group-hover:text-white/20">
                    <span class="material-symbols-outlined text-[12px]">check</span>
                </div>
                <div class="flex-1 min-w-0">
                    <p class="text-xs font-medium text-white group-hover:text-primary/90 transition-colors truncate">{{ todo.text }}</p>
                    <div class="flex items-center gap-2 mt-0.5">
                        <span class="text-[9px] text-white/30">{{ todo.due }}</span>
                        <span v-if="todo.urgent" class="w-1.5 h-1.5 rounded-full bg-red-400"></span>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const clockedIn = ref(false)
const elapsedTime = ref('00:00:00')
const loading = ref(false)
const shiftSeconds = ref(0)
let shiftTimerInterval

const recentLogs = ref([
  { id: 1, title: 'Clock Out', time: 'Yesterday, 6:00 PM', icon: 'check_circle', type: 'clock-out' },
  { id: 3, title: 'Clocked In', time: 'Yesterday, 9:02 AM', icon: 'login', type: 'info' },
])

const todos = ref([
    { id: 1, text: 'Review diamond inventory', due: 'Today, 2:00 PM', urgent: true },
    { id: 2, text: 'Submit weekly report', due: 'Tomorrow', urgent: false },
    { id: 3, text: 'Call with design team', due: 'Oct 25', urgent: false },
    { id: 4, text: 'Approve pending leaves', due: 'Oct 26', urgent: false },
    { id: 5, text: 'Check safety gear', due: 'Oct 27', urgent: false },
])

const getTimerColor = computed(() => {
    if (!clockedIn.value) return 'text-white/20'
    return shiftSeconds.value >= 28800 ? 'text-green-500' : 'text-red-500' // Red < 8h, Green > 8h
})

const getDotColor = computed(() => {
    return shiftSeconds.value >= 28800 ? 'bg-green-500' : 'bg-red-500'
})

function handleClockIn() {
  loading.value = true
  setTimeout(() => {
    clockedIn.value = true
    shiftSeconds.value = 0 
    loading.value = false
    recentLogs.value.unshift({ 
      id: Date.now(), 
      title: 'Clocked In', 
      time: 'Just now', 
      icon: 'login',
      type: 'info'
    })
    startShiftTimer()
  }, 800)
}

function handleClockOut() {
  loading.value = true
  setTimeout(() => {
    clockedIn.value = false
    loading.value = false
    recentLogs.value.unshift({ 
      id: Date.now(), 
      title: 'Clocked Out', 
      time: 'Just now', 
      icon: 'logout',
      type: 'clock-out'
    })
    stopShiftTimer()
  }, 800)
}

function startShiftTimer() {
  shiftTimerInterval = setInterval(() => {
    shiftSeconds.value++
    const h = Math.floor(shiftSeconds.value / 3600).toString().padStart(2, '0')
    const m = Math.floor((shiftSeconds.value % 3600) / 60).toString().padStart(2, '0')
    const s = (shiftSeconds.value % 60).toString().padStart(2, '0')
    elapsedTime.value = `${h}:${m}:${s}`
  }, 1000)
}

function stopShiftTimer() {
  clearInterval(shiftTimerInterval)
}

onUnmounted(() => {
  clearInterval(shiftTimerInterval)
})
</script>

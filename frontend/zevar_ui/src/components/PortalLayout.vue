<template>
	<div
		class="h-[100dvh] w-full flex overflow-hidden bg-portal-bg-dark text-white selection:bg-portal-primary/30 mesh-gradient-bg font-portal"
	>
		<!-- Desktop Sidebar - Hidden on mobile/tablet -->
		<aside
		 class="hidden lg:flex w-72 bg-black/20 backdrop-blur-3xl border-r border-white/5 flex-col transition-all duration-300"
            :class="sidebarCollapsed ? 'items-center' : ''"
        >
            <div
                class="flex items-center gap-4 mb-10 h-12"
                :class="sidebarCollapsed ? 'px-0 justify-center' : 'px-4'"
            >
                <!-- Toggle Button (Desktop) -->
                <button
                    v-show="!sidebarCollapsed"
                    @click="sidebarCollapsed = !sidebarCollapsed"
                    class="hidden lg:flex items-center justify-center w-8 h-8 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 transition-all text-gray-400 hover:text-white"
                >
                    <span class="material-symbols-outlined text-[20px]">menu_open</span>
                </button>

                <div class="flex items-center gap-3 overflow-hidden" v-show="!sidebarCollapsed">
                    <div
                        class="size-10 rounded-xl bg-gradient-to-br from-portal-primary to-portal-accent-indigo flex items-center justify-center shadow-lg shadow-portal-primary/20 shrink-0"
                    >
                        <span class="material-symbols-outlined text-white text-2xl"
                            >rocket_launch</span
                        >
                    </div>
                    <div>
                        <h1 class="text-xl font-bold tracking-tight">Zevar</h1>
                    </div>
                </div>

                <!-- Collapsed View (Only Toggle) -->
                <div v-show="sidebarCollapsed" class="w-full flex justify-center">
                    <button
                        @click="sidebarCollapsed = !sidebarCollapsed"
                        class="hidden lg:flex items-center justify-center w-10 h-10 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all text-gray-400 hover:text-white shrink-0"
                    >
                        <span class="material-symbols-outlined text-[20px] rotate-180">menu_open</span>
                    </button>
                </div>
            </div>
            <nav class="flex-1 flex flex-col gap-2">
                <router-link
                    to="/"
                    class="group flex items-center gap-4 py-4 rounded-full transition-all duration-300"
                    :class="sidebarCollapsed ? 'px-0 justify-center' : 'px-6'"
                    active-class="bg-portal-primary/15 border border-portal-primary/30 shadow-[0_0_15px_rgba(37,192,244,0.1)]"
                    v-slot="{ isActive }"
                >
                    <span
                        class="material-symbols-outlined shrink-0"
                        :class="
                            isActive
                                ? 'text-portal-primary'
                                : 'text-white/60 group-hover:text-portal-primary transition-colors'
                        "
                        >dashboard</span
                    >
                    <span
                        v-show="!sidebarCollapsed"
                        :class="
                            isActive
                                ? 'font-semibold text-white'
                                : 'font-medium text-white/60 group-hover:text-white transition-colors'
                        "
                        >Dashboard</span
                    >
                </router-link>

                <router-link
                    to="/tasks"
                    class="group flex items-center gap-4 py-4 rounded-full transition-all duration-300"
                    :class="sidebarCollapsed ? 'px-0 justify-center' : 'px-6'"
                    active-class="bg-portal-primary/15 border border-portal-primary/30 shadow-[0_0_15px_rgba(37,192,244,0.1)]"
                    v-slot="{ isActive }"
                >
                    <span
                        class="material-symbols-outlined shrink-0"
                        :class="
                            isActive
                                ? 'text-portal-primary'
                                : 'text-white/60 group-hover:text-portal-primary transition-colors'
                        "
                        >task_alt</span
                    >
                    <span
                        v-show="!sidebarCollapsed"
                        :class="
                            isActive
                                ? 'font-semibold text-white'
                                : 'font-medium text-white/60 group-hover:text-white transition-colors'
                        "
                        >Tasks</span
                    >
                </router-link>

                <router-link
                    to="/attendance"
                    class="group flex items-center gap-4 py-4 rounded-full transition-all duration-300"
                    :class="sidebarCollapsed ? 'px-0 justify-center' : 'px-6'"
                    active-class="bg-portal-primary/15 border border-portal-primary/30 shadow-[0_0_15px_rgba(37,192,244,0.1)]"
                    v-slot="{ isActive }"
                >
                    <span
                        class="material-symbols-outlined shrink-0"
                        :class="
                            isActive
                                ? 'text-portal-primary'
                                : 'text-white/60 group-hover:text-portal-primary transition-colors'
                        "
                        >calendar_today</span
                    >
                    <span
                        v-show="!sidebarCollapsed"
                        :class="
                            isActive
                                ? 'font-semibold text-white'
                                : 'font-medium text-white/60 group-hover:text-white transition-colors'
                        "
                        >Attendance</span
                    >
                </router-link>

                <router-link
                    to="/leave"
                    class="group flex items-center gap-4 py-4 rounded-full transition-all duration-300"
                    :class="sidebarCollapsed ? 'px-0 justify-center' : 'px-6'"
                    active-class="bg-portal-primary/15 border border-portal-primary/30 shadow-[0_0_15px_rgba(37,192,244,0.1)]"
                    v-slot="{ isActive }"
                >
                    <span
                        class="material-symbols-outlined shrink-0"
                        :class="
                            isActive
                                ? 'text-portal-primary'
                                : 'text-white/60 group-hover:text-portal-primary transition-colors'
                        "
                        >beach_access</span
                    >
                    <span
                        v-show="!sidebarCollapsed"
                        :class="
                            isActive
                                ? 'font-semibold text-white'
                                : 'font-medium text-white/60 group-hover:text-white transition-colors'
                        "
                        >Leave</span
                    >
                </router-link>

                <router-link
                    to="/payroll"
                    class="group flex items-center gap-4 py-4 rounded-full transition-all duration-300"
                    :class="sidebarCollapsed ? 'px-0 justify-center' : 'px-6'"
                    active-class="bg-portal-primary/15 border border-portal-primary/30 shadow-[0_0_15px_rgba(37,192,244,0.1)]"
                    v-slot="{ isActive }"
                >
                    <span
                        class="material-symbols-outlined shrink-0"
                        :class="
                            isActive
                                ? 'text-portal-primary'
                                : 'text-white/60 group-hover:text-portal-primary transition-colors'
                        "
                        >payments</span
                    >
                    <span
                        v-show="!sidebarCollapsed"
                        :class="
                            isActive
                                ? 'font-semibold text-white'
                                : 'font-medium text-white/60 group-hover:text-white transition-colors'
                        "
                        >Payroll</span
                    >
                </router-link>

                <router-link
                    to="/pos"
                    class="group flex items-center gap-4 py-4 rounded-full transition-all duration-300"
                    :class="sidebarCollapsed ? 'px-0 justify-center' : 'px-6'"
                    active-class="bg-portal-primary/15 border border-portal-primary/30 shadow-[0_0_15px_rgba(37,192,244,0.1)]"
                    v-slot="{ isActive }"
                >
                    <span
                        class="material-symbols-outlined shrink-0"
                        :class="
                            isActive
                                ? 'text-portal-primary'
                                : 'text-white/60 group-hover:text-portal-primary transition-colors'
                        "
                        >point_of_sale</span
                    >
                    <span
                        v-show="!sidebarCollapsed"
                        :class="
                            isActive
                                ? 'font-semibold text-white'
                                : 'font-medium text-white/60 group-hover:text-white transition-colors'
                        "
                        >POS Terminal</span
                    >
                </router-link>
            </nav>

            <div class="mt-auto flex flex-col gap-4">
                <div
                    v-show="!sidebarCollapsed"
                    class="glass-card p-5 rounded-xl border-portal-primary/20 bg-portal-primary/5 relative overflow-hidden group"
                >
                    <div
                        class="absolute -top-4 -right-4 size-16 bg-portal-primary/20 blur-2xl rounded-full"
                    ></div>
                    <p
                        class="text-xs font-bold text-portal-primary uppercase mb-2 tracking-tighter"
                    >
                        Support Desk
                    </p>
                    <p class="text-sm text-white/70 mb-4 leading-relaxed">
                        Need help? Our team is available 24/7.
                    </p>
                    <button
                        class="w-full py-3 bg-portal-primary text-portal-bg-dark font-bold rounded-full text-sm hover:scale-105 transition-transform"
                    >
                        Chat Now
                    </button>
                </div>
                <button
                    v-show="sidebarCollapsed"
                    class="size-12 rounded-full glass-card hover:bg-portal-primary/20 flex items-center justify-center transition-colors"
                >
                    <span class="material-symbols-outlined text-portal-primary"
                        >support_agent</span
                    >
                </button>

                <button
                    @click="sidebarCollapsed = !sidebarCollapsed"
                    class="w-full py-3 glass-card rounded-full text-white/60 hover:text-white hover:bg-white/10 transition-colors flex items-center justify-center gap-2"
                >
                    <span
                        class="material-symbols-outlined transition-transform duration-300"
                        :class="sidebarCollapsed ? 'rotate-180' : ''"
                        >chevron_left</span
                    >
                    <span v-show="!sidebarCollapsed" class="text-sm font-bold">Collapse</span>
                </button>
            </div>
        </aside>

        <!-- Main Content -->
        <div class="flex-1 flex flex-col overflow-hidden min-w-0 min-h-0">
            <!-- Header -->
            <header
                class="flex items-center justify-between px-4 md:px-10 py-4 md:py-6 flex-shrink-0 backdrop-blur-md bg-portal-bg-dark/30 z-10"
            >
                <!-- Mobile: Hamburger Menu -->
                <button
                    @click="isMobileDrawerOpen = true"
                    class="lg:hidden p-2 rounded-lg hover:bg-white/10 transition-colors mr-2"
                >
                    <span class="material-symbols-outlined text-white/70">menu</span>
                </button>

                <!-- Search - hidden on mobile, shown on tablet/desktop -->
                <div class="flex-1 max-w-md hidden md:block">
                    <div class="relative group">
                        <span
                            class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-white/40 group-focus-within:text-portal-primary transition-colors"
                            >search</span
                        >
                        <input
                            class="w-full bg-white/5 border-none rounded-full py-3 pl-12 pr-6 text-sm text-white placeholder:text-white/30 focus:ring-2 focus:ring-portal-primary/40 transition-all outline-none"
                            placeholder="Search resources, tasks..."
                            type="text"
                        />
                    </div>
                </div>

                <!-- Mobile: Logo -->
                <div class="flex items-center gap-2 md:hidden">
                    <div
                        class="size-10 rounded-xl bg-gradient-to-br from-portal-primary to-portal-accent-indigo flex items-center justify-center shadow-lg shadow-portal-primary/20"
                    >
                        <span class="material-symbols-outlined text-white text-2xl">rocket_launch</span>
                    </div>
                    <span class="text-lg font-bold">Zevar</span>
                </div>

                <div class="flex items-center gap-4 md:gap-6">
                    <button
                        class="size-10 flex items-center justify-center rounded-full glass-card hover:bg-white/10 transition-colors relative"
                    >
                        <span class="material-symbols-outlined text-white/70">notifications</span>
                        <span
                            class="absolute top-2 right-2.5 size-2 bg-red-500 rounded-full"
                        ></span>
                    </button>
                    <div class="h-8 w-px bg-white/10 hidden sm:block"></div>
                    <div class="relative">
                        <!-- Overlay for clicking outside -->
                        <div
                            v-if="userMenuOpen"
                            class="fixed inset-0 z-40"
                            @click="userMenuOpen = false"
                        ></div>

                        <!-- Profile Button -->
                        <button
                            class="relative z-50 flex items-center gap-3 glass-card pl-2 pr-4 py-1.5 rounded-full border-white/10 hover:bg-white/10 transition-colors"
                            @click="userMenuOpen = !userMenuOpen"
                        >
                            <div
                                class="size-8 rounded-full bg-cover bg-center border border-white/20 bg-[url('https://lh3.googleusercontent.com/aida-public/AB6AXuDnQJq8q1gAPlq-d17pt8MWUZvSZ-e3HtdAvxGssLOU8lP369oHj2hjrlSKn5zUOiEAwvP9W0P1XiABRXa5ntNhm7dqXwiT16MPKqAPxUZ3VNRyhbr-yj9fVvuw72k5PVeMYKtjqw2Zf9SCMVzoPcLmnoC58TZkv0DC2UenKxK1hYlyrNpI2X0GOLluWjgWcCgajvIfT1ImVoxHB_73JFVPYDPzZdFPOmHoVmqHP46qkc1k9XQCPoyTCfR7RYLkhmct1yAAN7Rn2dTG')]"
                            ></div>
                            <span class="text-sm font-semibold hidden sm:block">Alex Rivera</span>
                            <span
                                class="material-symbols-outlined text-white/50 text-sm ml-1"
                                :class="{ 'rotate-180': userMenuOpen }"
                                >expand_more</span
                            >
                        </button>

                        <!-- Dropdown Menu -->
                        <div
                            v-show="userMenuOpen"
                            class="absolute right-0 top-full mt-2 w-56 glass-card border border-white/10 rounded-xl shadow-2xl py-2 z-50 flex flex-col font-medium text-sm"
                        >
                            <div class="px-4 py-3 border-b border-white/5 mb-1">
                                <p class="text-white font-bold tracking-tight">Alex Rivera</p>
                                <p class="text-xs text-white/50 mt-0.5">alex.rivera@zevar.com</p>
                            </div>

                            <button
                                class="w-full text-left px-4 py-2.5 text-white/70 hover:text-white hover:bg-white/5 transition-colors flex items-center gap-3"
                            >
                                <span class="material-symbols-outlined text-[18px]">person</span>
                                Employee Detail
                            </button>

                            <button
                                class="w-full text-left px-4 py-2.5 text-white/70 hover:text-white hover:bg-white/5 transition-colors flex items-center justify-between"
                            >
                                <div class="flex items-center gap-3">
                                        <span class="material-symbols-outlined text-[18px]">dark_mode</span>
                                        Dark Mode
                                    </div>
                                <!-- Simple toggle visualization -->
                                <div
                                    class="w-8 h-4 bg-portal-primary/30 rounded-full relative flex items-center"
                                >
                                    <div
                                        class="size-3 bg-portal-primary rounded-full absolute right-0.5"
                                    ></div>
                                </div>
                            </button>

                            <button
                                class="w-full text-left px-4 py-2.5 text-white/70 hover:text-white hover:bg-white/5 transition-colors flex items-center gap-3"
                            >
                                <span class="material-symbols-outlined text-[18px]">lock</span>
                                Change Password
                            </button>

                            <div class="h-px w-full bg-white/5 my-1"></div>

                            <button
                                class="w-full text-left px-4 py-2.5 text-red-400 hover:text-red-300 hover:bg-red-400/10 transition-colors flex items-center gap-3"
                            >
                                <span class="material-symbols-outlined text-[18px]">logout</span>
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            <!-- Scrollable Content -->
            <main class="flex-1 overflow-y-auto custom-scrollbar min-h-0">
                <slot />
            </main>
        </div>

        <!-- Mobile Drawer -->
        <Teleport to="body">
            <div
                v-if="isMobileDrawerOpen"
                @click="isMobileDrawerOpen = false"
                class="fixed inset-0 bg-black/50 backdrop-blur-sm z-[60] lg:hidden"
            ></div>
            <div
                class="fixed top-0 left-0 h-full w-80 max-w-[85vw] bg-portal-bg-dark z-[61] transform transition-transform duration-300 ease-in-out lg:hidden overflow-y-auto"
                :class="isMobileDrawerOpen ? 'translate-x-0' : '-translate-x-full'"
            >
                <!-- Drawer Header -->
                <div class="p-4 border-b border-white/5 flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div
                            class="size-10 rounded-xl bg-gradient-to-br from-portal-primary to-portal-accent-indigo flex items-center justify-center"
                        >
                            <span class="material-symbols-outlined text-white text-2xl">rocket_launch</span>
                        </div>
                        <div>
                            <h1 class="text-lg font-bold text-white">Zevar</h1>
                            <p class="text-[10px] text-white/50">Employee Portal</p>
                        </div>
                    </div>
                    <button
                        @click="isMobileDrawerOpen = false"
                        class="p-2 hover:bg-white/10 rounded-full transition-colors text-white/50"
                    >
                        <span class="material-symbols-outlined">close</span>
                    </button>
                </div>

                <!-- Search in Drawer -->
                <div class="p-4 border-b border-white/5">
                    <div class="relative">
                        <span
                            class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-white/40"
                            >search</span
                        >
                        <input
                            class="w-full bg-white/5 border-none rounded-full py-3 pl-12 pr-6 text-sm text-white placeholder:text-white/30 outline-none"
                            placeholder="Search..."
                            type="text"
                        />
                    </div>
                </div>

                <!-- Navigation in Drawer -->
                <nav class="p-4 space-y-1">
                    <router-link
                        to="/"
                        @click="isMobileDrawerOpen = false"
                        class="flex items-center gap-4 py-3 px-4 rounded-xl transition-all"
                        active-class="bg-portal-primary/15 text-portal-primary"
                        :class="$route.path === '/' ? '' : 'text-white/60 hover:text-white hover:bg-white/5'"
                    >
                        <span class="material-symbols-outlined">dashboard</span>
                        <span class="font-medium text-sm">Dashboard</span>
                    </router-link>

                    <router-link
                        to="/tasks"
                        @click="isMobileDrawerOpen = false"
                        class="flex items-center gap-4 py-3 px-4 rounded-xl transition-all"
                        active-class="bg-portal-primary/15 text-portal-primary"
                        :class="$route.path === '/tasks' ? '' : 'text-white/60 hover:text-white hover:bg-white/5'"
                    >
                        <span class="material-symbols-outlined">task_alt</span>
                        <span class="font-medium text-sm">Tasks</span>
                    </router-link>

                    <router-link
                        to="/attendance"
                        @click="isMobileDrawerOpen = false"
                        class="flex items-center gap-4 py-3 px-4 rounded-xl transition-all"
                        active-class="bg-portal-primary/15 text-portal-primary"
                        :class="$route.path === '/attendance' ? '' : 'text-white/60 hover:text-white hover:bg-white/5'"
                    >
                        <span class="material-symbols-outlined">calendar_today</span>
                        <span class="font-medium text-sm">Attendance</span>
                    </router-link>

                    <router-link
                        to="/leave"
                        @click="isMobileDrawerOpen = false"
                        class="flex items-center gap-4 py-3 px-4 rounded-xl transition-all"
                        active-class="bg-portal-primary/15 text-portal-primary"
                        :class="$route.path === '/leave' ? '' : 'text-white/60 hover:text-white hover:bg-white/5'"
                    >
                        <span class="material-symbols-outlined">beach_access</span>
                        <span class="font-medium text-sm">Leave</span>
                    </router-link>

                    <router-link
                        to="/pos"
                        @click="isMobileDrawerOpen = false"
                        class="flex items-center gap-4 py-3 px-4 rounded-xl transition-all"
                        active-class="bg-portal-primary/15 text-portal-primary"
                        :class="$route.path === '/pos' ? '' : 'text-white/60 hover:text-white hover:bg-white/5'"
                    >
                        <span class="material-symbols-outlined">point_of_sale</span>
                        <span class="font-medium text-sm">POS Terminal</span>
                    </router-link>
                </nav>
            </div>
        </Teleport>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const sidebarCollapsed = ref(false)
const userMenuOpen = ref(false)
const isMobileDrawerOpen = ref(false)
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: rgba(37, 192, 244, 0.3);
}
</style>

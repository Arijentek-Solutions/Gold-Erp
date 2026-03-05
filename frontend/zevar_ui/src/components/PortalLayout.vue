<template>
	<div
		class="flex h-screen w-full overflow-hidden bg-portal-bg-dark text-white selection:bg-portal-primary/30 mesh-gradient-bg font-portal"
	>
		<aside
			class="flex flex-col p-6 border-r border-white/5 bg-black/20 backdrop-blur-3xl transition-all duration-300"
			:class="sidebarCollapsed ? 'w-24 items-center' : 'w-72'"
		>
			<div
				class="flex items-center gap-3 mb-10"
				:class="sidebarCollapsed ? 'px-0 justify-center' : 'px-4'"
			>
				<div
					class="size-12 rounded-2xl bg-gradient-to-br from-portal-primary to-portal-accent-indigo flex items-center justify-center shadow-lg shadow-portal-primary/20 shrink-0"
				>
					<span class="material-symbols-outlined text-white text-3xl"
						>rocket_launch</span
					>
				</div>
				<div v-show="!sidebarCollapsed">
					<h1 class="text-xl font-bold tracking-tight">Zevar</h1>
					<p
						class="text-xs text-white/50 font-medium uppercase tracking-widest whitespace-nowrap"
					>
						Employee Portal
					</p>
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
					class="group flex items-center gap-4 py-4 rounded-full hover:bg-white/5 transition-all duration-300"
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
					class="group flex items-center gap-4 py-4 rounded-full hover:bg-white/5 transition-all duration-300"
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
					class="group flex items-center gap-4 py-4 rounded-full hover:bg-white/5 transition-all duration-300"
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
		<div class="flex-1 flex flex-col overflow-hidden">
			<!-- Header -->
			<header
				class="flex items-center justify-between px-10 py-6 sticky top-0 z-10 backdrop-blur-md bg-portal-bg-dark/30"
			>
				<div class="flex-1 max-w-md">
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
				<div class="flex items-center gap-6">
					<button
						class="size-10 flex items-center justify-center rounded-full glass-card hover:bg-white/10 transition-colors relative"
					>
						<span class="material-symbols-outlined text-white/70">notifications</span>
						<span
							class="absolute top-2 right-2.5 size-2 bg-red-500 rounded-full"
						></span>
					</button>
					<div class="h-8 w-px bg-white/10"></div>
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
							<span class="text-sm font-semibold">Alex Rivera</span>
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
									<span class="material-symbols-outlined text-[18px]"
										>dark_mode</span
									>
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
			<main class="flex-1 overflow-y-auto custom-scrollbar">
				<slot />
			</main>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue'

const sidebarCollapsed = ref(false)
const userMenuOpen = ref(false)
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

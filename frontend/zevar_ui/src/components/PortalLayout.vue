<template>
	<div
		class="flex h-screen w-full overflow-hidden bg-portal-bg-dark text-white selection:bg-portal-primary/30 mesh-gradient-bg font-portal"
	>
		<!-- Sidebar -->
		<aside
			class="w-72 flex flex-col p-6 border-r border-white/5 bg-black/20 backdrop-blur-3xl"
		>
			<div class="flex items-center gap-3 px-4 mb-10">
				<div
					class="size-12 rounded-2xl bg-gradient-to-br from-portal-primary to-portal-accent-indigo flex items-center justify-center shadow-lg shadow-portal-primary/20"
				>
					<span class="material-symbols-outlined text-white text-3xl"
						>rocket_launch</span
					>
				</div>
				<div>
					<h1 class="text-xl font-bold tracking-tight">Zevar</h1>
					<p class="text-xs text-white/50 font-medium uppercase tracking-widest">
						Employee Portal
					</p>
				</div>
			</div>
			<nav class="flex-1 flex flex-col gap-2">
				<router-link
					to="/"
					class="group flex items-center gap-4 px-6 py-4 rounded-full transition-all duration-300"
					active-class="bg-portal-primary/15 border border-portal-primary/30 shadow-[0_0_15px_rgba(37,192,244,0.1)]"
					v-slot="{ isActive }"
				>
					<span
						class="material-symbols-outlined"
						:class="
							isActive
								? 'text-portal-primary'
								: 'text-white/60 group-hover:text-portal-primary transition-colors'
						"
						>dashboard</span
					>
					<span
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
					class="group flex items-center gap-4 px-6 py-4 rounded-full transition-all duration-300"
					active-class="bg-portal-primary/15 border border-portal-primary/30 shadow-[0_0_15px_rgba(37,192,244,0.1)]"
					v-slot="{ isActive }"
				>
					<span
						class="material-symbols-outlined"
						:class="
							isActive
								? 'text-portal-primary'
								: 'text-white/60 group-hover:text-portal-primary transition-colors'
						"
						>task_alt</span
					>
					<span
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
					class="group flex items-center gap-4 px-6 py-4 rounded-full hover:bg-white/5 transition-all duration-300"
					active-class="bg-portal-primary/15 border border-portal-primary/30 shadow-[0_0_15px_rgba(37,192,244,0.1)]"
					v-slot="{ isActive }"
				>
					<span
						class="material-symbols-outlined"
						:class="
							isActive
								? 'text-portal-primary'
								: 'text-white/60 group-hover:text-portal-primary transition-colors'
						"
						>calendar_today</span
					>
					<span
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
					class="group flex items-center gap-4 px-6 py-4 rounded-full transition-all duration-300"
					active-class="bg-portal-primary/15 border border-portal-primary/30 shadow-[0_0_15px_rgba(37,192,244,0.1)]"
					v-slot="{ isActive }"
				>
					<span
						class="material-symbols-outlined"
						:class="
							isActive
								? 'text-portal-primary'
								: 'text-white/60 group-hover:text-portal-primary transition-colors'
						"
						>beach_access</span
					>
					<span
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
					class="group flex items-center gap-4 px-6 py-4 rounded-full hover:bg-white/5 transition-all duration-300"
					active-class="bg-portal-primary/15 border border-portal-primary/30 shadow-[0_0_15px_rgba(37,192,244,0.1)]"
					v-slot="{ isActive }"
				>
					<span
						class="material-symbols-outlined"
						:class="
							isActive
								? 'text-portal-primary'
								: 'text-white/60 group-hover:text-portal-primary transition-colors'
						"
						>payments</span
					>
					<span
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
					class="group flex items-center gap-4 px-6 py-4 rounded-full hover:bg-white/5 transition-all duration-300"
					active-class="bg-portal-primary/15 border border-portal-primary/30 shadow-[0_0_15px_rgba(37,192,244,0.1)]"
					v-slot="{ isActive }"
				>
					<span
						class="material-symbols-outlined"
						:class="
							isActive
								? 'text-portal-primary'
								: 'text-white/60 group-hover:text-portal-primary transition-colors'
						"
						>point_of_sale</span
					>
					<span
						:class="
							isActive
								? 'font-semibold text-white'
								: 'font-medium text-white/60 group-hover:text-white transition-colors'
						"
						>POS Terminal</span
					>
				</router-link>
			</nav>

			<div class="mt-auto">
				<div
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
					<div
						class="flex items-center gap-3 glass-card pl-2 pr-4 py-1.5 rounded-full border-white/10"
					>
						<div
							class="size-8 rounded-full bg-cover bg-center border border-white/20 bg-[url('https://lh3.googleusercontent.com/aida-public/AB6AXuDnQJq8q1gAPlq-d17pt8MWUZvSZ-e3HtdAvxGssLOU8lP369oHj2hjrlSKn5zUOiEAwvP9W0P1XiABRXa5ntNhm7dqXwiT16MPKqAPxUZ3VNRyhbr-yj9fVvuw72k5PVeMYKtjqw2Zf9SCMVzoPcLmnoC58TZkv0DC2UenKxK1hYlyrNpI2X0GOLluWjgWcCgajvIfT1ImVoxHB_73JFVPYDPzZdFPOmHoVmqHP46qkc1k9XQCPoyTCfR7RYLkhmct1yAAN7Rn2dTG')]"
						></div>
						<span class="text-sm font-semibold">Alex Rivera</span>
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

<script setup></script>

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

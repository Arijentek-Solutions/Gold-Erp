<template>
	<div
		class="h-[100dvh] w-full flex overflow-hidden bg-white dark:bg-[#0b0f19] font-display text-gray-900 dark:text-white selection:bg-primary/30 relative transition-colors duration-700"
		:style="{ '--primary-color': routeColor }"
	>
		<!-- Ambient Glows -->
		<div
			class="fixed top-[-10%] left-[-10%] w-[50%] h-[50%] bg-primary/5 blur-[120px] rounded-full -z-10"
		></div>
		<div
			class="fixed bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-blue-500/5 blur-[120px] rounded-full -z-10"
		></div>

		<!-- Mobile Sidebar Overlay -->
		<div
			v-if="mobileMenuOpen"
			class="fixed inset-0 bg-black/60 z-40 lg:hidden"
			@click="mobileMenuOpen = false"
		></div>

		<!-- Sidebar -->
		<aside
			class="shrink-0 flex flex-col sidebar-standard z-20 transition-all duration-300 fixed lg:relative h-full"
			:class="[
				sidebarCollapsed ? 'lg:w-20 lg:items-center' : 'lg:w-64',
				mobileMenuOpen ? 'w-64 translate-x-0' : '-translate-x-full lg:translate-x-0',
			]"
		>
			<!-- Branding & Toggle -->
			<div
				class="h-20 flex items-center px-6 gap-4 border-b border-black/5 dark:border-white/5"
				:class="sidebarCollapsed ? 'lg:px-4 justify-center' : 'justify-between'"
			>
				<div
					v-if="!sidebarCollapsed"
					class="flex items-center gap-2 overflow-hidden transition-all duration-300"
				>
					<img :src="logoUrl" alt="Zevar" class="w-8 h-8 rounded shrink-0" />
					<span
						class="font-bold text-gray-900 dark:text-white tracking-wide text-sm whitespace-nowrap"
						>Zevar</span
					>
				</div>

				<button
					@click="sidebarCollapsed = !sidebarCollapsed"
					class="hidden lg:flex items-center justify-center w-8 h-8 rounded-lg bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/10 hover:bg-black/5 dark:hover:bg-white/10 transition-all text-gray-500 hover:text-gray-900 dark:text-white/60 dark:hover:text-white"
					:aria-label="sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
				>
					<span
						class="material-symbols-outlined text-[20px] transition-transform"
						:class="sidebarCollapsed ? 'rotate-180' : ''"
						>menu_open</span
					>
				</button>
			</div>

			<!-- Nav Items -->
			<nav class="flex-1 px-4 space-y-1 overflow-y-auto custom-scrollbar pb-6">
				<router-link
					v-for="item in navItems"
					:key="item.to"
					:to="item.to"
					@click="mobileMenuOpen = false"
					class="flex items-center rounded-xl transition-all group"
					:class="[
						route.path === item.to
							? 'bg-primary/10 text-primary shadow-sm'
							: 'text-gray-500 dark:text-white/60 hover:text-gray-900 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5',
						sidebarCollapsed
							? 'lg:justify-center lg:px-2 lg:py-3'
							: 'justify-between px-4 py-3',
					]"
				>
					<div class="flex items-center gap-3">
						<span class="material-symbols-outlined text-[20px] shrink-0">{{
							item.icon
						}}</span>
						<span v-show="!sidebarCollapsed" class="text-sm font-medium">{{
							item.label
						}}</span>
					</div>
					<span
						v-if="route.path === item.to && !sidebarCollapsed"
						class="material-symbols-outlined text-[16px]"
						>chevron_right</span
					>
				</router-link>

				<!-- Desk Link (External Handle) -->
				<a
					href="/app"
					target="_blank"
					class="flex items-center rounded-xl transition-all group text-gray-500 dark:text-white/60 hover:text-gray-900 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 mt-4"
					:class="
						sidebarCollapsed
							? 'lg:justify-center lg:px-2 lg:py-3'
							: 'justify-between px-4 py-3'
					"
				>
					<div class="flex items-center gap-3">
						<span class="material-symbols-outlined text-[20px] shrink-0"
							>open_in_new</span
						>
						<span v-show="!sidebarCollapsed" class="text-sm font-medium"
							>Open Desk</span
						>
					</div>
				</a>
			</nav>
		</aside>

		<!-- Main Content -->
		<main
			class="flex-1 flex flex-col h-full min-w-0 overflow-hidden bg-white dark:bg-[#0b0f19]"
		>
			<!-- Header -->
			<header
				class="flex items-center px-4 md:px-8 py-4 border-b border-black/5 dark:border-white/5 shrink-0"
			>
				<!-- Left Side: Header Actions -->
				<div class="flex items-center gap-4">
					<!-- Mobile Hamburger (inline in header, only for mobile) -->
					<button
						@click="mobileMenuOpen = !mobileMenuOpen"
						class="lg:hidden w-10 h-10 rounded-xl bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/10 flex items-center justify-center text-gray-500 dark:text-white/60 hover:text-gray-900 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/10 transition-all"
					>
						<span class="material-symbols-outlined text-[20px]">{{
							mobileMenuOpen ? "close" : "menu"
						}}</span>
					</button>
				</div>

				<div class="relative ml-auto flex items-center gap-4">
					<!-- Overlay for clicking outside -->
					<div
						v-if="userMenuOpen"
						class="fixed inset-0 z-40"
						@click="userMenuOpen = false"
					></div>

					<!-- Profile Button -->
					<button
						class="relative z-50 flex items-center gap-2 md:gap-3 bg-gray-50 dark:bg-white/5 hover:bg-black/5 dark:hover:bg-white/10 pl-2 pr-3 md:pr-4 py-1.5 rounded-full border border-gray-200 dark:border-white/10 transition-colors"
						@click="userMenuOpen = !userMenuOpen"
					>
						<div
							class="w-7 h-7 md:w-8 md:h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold text-[10px] md:text-xs"
						>
							{{ userInitials }}
						</div>
						<span
							class="text-xs md:text-sm font-semibold text-gray-900 dark:text-white hidden sm:block"
							>{{ auth.user?.full_name || "User" }}</span
						>
						<span
							class="material-symbols-outlined text-gray-400 dark:text-white/50 text-sm ml-1 transition-transform"
							:class="{ 'rotate-180': userMenuOpen }"
							>expand_more</span
						>
					</button>

					<!-- Dropdown Menu -->
					<div
						v-show="userMenuOpen"
						class="absolute right-0 top-full mt-2 w-56 bg-white dark:bg-[#111420] border border-gray-200 dark:border-white/10 rounded-xl shadow-2xl py-2 z-50 flex flex-col font-medium text-sm"
					>
						<div class="px-4 py-3 border-b border-gray-100 dark:border-white/5 mb-1">
							<p class="text-gray-900 dark:text-white font-bold">
								{{ auth.user?.full_name || "User" }}
							</p>
							<p class="text-xs text-gray-500 mt-0.5">
								{{ auth.user?.email || "user@zevar.com" }}
							</p>
						</div>

						<button
							@click="
								showComingSoon = true;
								userMenuOpen = false;
							"
							class="w-full text-left px-4 py-2.5 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-50 dark:hover:bg-white/5 transition-colors flex items-center gap-3"
						>
							<span class="material-symbols-outlined text-[18px]">person</span>
							Employee Detail
						</button>

						<button
							@click="toggleDarkMode"
							class="w-full text-left px-4 py-2.5 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-50 dark:hover:bg-white/5 transition-colors flex items-center justify-between"
						>
							<div class="flex items-center gap-3">
								<span class="material-symbols-outlined text-[18px]">{{
									isDark ? "light_mode" : "dark_mode"
								}}</span>
								{{ isDark ? "Light Mode" : "Dark Mode" }}
							</div>
							<div
								class="w-8 h-4 bg-primary/30 rounded-full relative flex items-center transition-colors"
							>
								<div
									class="w-3 h-3 bg-primary rounded-full absolute transition-all duration-300"
									:class="isDark ? 'right-0.5' : 'left-0.5'"
								></div>
							</div>
						</button>

						<button
							@click="
								showComingSoon = true;
								userMenuOpen = false;
							"
							class="w-full text-left px-4 py-2.5 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-50 dark:hover:bg-white/5 transition-colors flex items-center gap-3"
						>
							<span class="material-symbols-outlined text-[18px]">lock</span>
							Change Password
						</button>

						<div class="h-px w-full bg-gray-100 dark:bg-white/5 my-1"></div>

						<button
							@click="auth.logout()"
							class="w-full text-left px-4 py-2.5 text-red-400 hover:text-red-300 hover:bg-red-400/10 transition-colors flex items-center gap-3"
						>
							<span class="material-symbols-outlined text-[18px]">logout</span>
							Logout
						</button>
					</div>
				</div>
			</header>

			<!-- Page Content Container -->
			<div
				class="flex-1 overflow-y-auto overflow-x-hidden p-4 md:p-6 custom-scrollbar relative"
			>
				<slot />
			</div>
		</main>

		<!-- Coming Soon Modal for generic actions mapped to buttons temporarily -->
		<Teleport to="body">
			<Transition name="fade">
				<div
					v-if="showComingSoon"
					class="fixed inset-0 z-[100] flex items-center justify-center p-4 backdrop-blur-sm"
					@click.self="showComingSoon = false"
				>
					<div class="absolute inset-0 bg-black/60"></div>
					<div
						class="relative bg-white dark:bg-[#15161a] rounded-3xl p-8 w-full max-w-sm border border-gray-200 dark:border-white/10 shadow-2xl text-center transform transition-all"
					>
						<div
							class="w-16 h-16 mx-auto bg-primary/10 rounded-full flex items-center justify-center text-primary mb-4 border border-primary/20"
						>
							<span class="material-symbols-outlined text-3xl">build</span>
						</div>
						<h3
							class="font-display font-bold text-gray-900 dark:text-white text-xl mb-2"
						>
							Feature Incoming
						</h3>
						<p class="text-sm text-gray-500 dark:text-white/50 mb-6 font-medium">
							This module is currently being built and will unlock shortly.
						</p>

						<button
							@click="showComingSoon = false"
							class="w-full py-3 bg-gray-50 dark:bg-white/5 hover:bg-black/5 dark:hover:bg-white/10 border border-gray-200 dark:border-white/5 rounded-xl text-gray-900 dark:text-white text-sm font-bold transition-all"
						>
							Understood
						</button>
					</div>
				</div>
			</Transition>
		</Teleport>
	</div>
</template>

<script setup>
import { computed, ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRoute } from "vue-router";

const auth = useAuthStore();
const route = useRoute();

const sidebarCollapsed = ref(false);
const mobileMenuOpen = ref(false);
const userMenuOpen = ref(false);
const showComingSoon = ref(false);
const isDark = ref(true); // Default to dark theme as per Zevar design language

// Logo URL
const logoUrl = "/assets/zevar_core/images/employee_portal_logo.svg";

const navItems = [
	{ to: "/", icon: "dashboard", label: "Dashboard" },
	{ to: "/tasks", icon: "check_circle", label: "Tasks" },
	{ to: "/attendance", icon: "calendar_month", label: "Attendance" },
	{ to: "/roster", icon: "schedule", label: "Roster" },
	{ to: "/leave", icon: "beach_access", label: "Leave" },
	{ to: "/expense", icon: "attach_money", label: "Expense" },
	{ to: "/payroll", icon: "account_balance_wallet", label: "Payroll" },
	{ to: "/team", icon: "groups", label: "Team" },
	{ to: "/issues", icon: "support_agent", label: "Issues" },
];

const routeColor = computed(() => {
	const colors = {
		"/": "#FCD34D", // Gold
		"/tasks": "#60A5FA", // Sky
		"/attendance": "#34D399", // Emerald
		"/roster": "#A78BFA", // Violet
		"/leave": "#F87171", // Coral
		"/expense": "#FB923C", // Amber
		"/payroll": "#818CF8", // Indigo
		"/team": "#2DD4BF", // Teal
		"/issues": "#F472B6", // Pink
	};
	return colors[route.path] || "#FCD34D";
});

const userInitials = computed(() => {
	const name = auth.user?.full_name || "User";
	return name
		.split(" ")
		.map((n) => n[0])
		.join("")
		.substring(0, 2)
		.toUpperCase();
});

const toggleDarkMode = () => {
	isDark.value = !isDark.value;
	if (isDark.value) {
		document.documentElement.classList.add("dark");
		localStorage.setItem("portal_theme", "dark");
	} else {
		document.documentElement.classList.remove("dark");
		localStorage.setItem("portal_theme", "light");
	}
	userMenuOpen.value = false;
};

onMounted(() => {
	const savedTheme = localStorage.getItem("portal_theme");
	if (savedTheme === "light") {
		isDark.value = false;
		document.documentElement.classList.remove("dark");
	} else {
		document.documentElement.classList.add("dark");
	}
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
	opacity: 0;
	transform: scale(0.95);
}
</style>

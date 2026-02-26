<template>
	<div
		class="flex h-screen w-full overflow-hidden bg-background-dark font-display text-white selection:bg-primary/30 relative"
	>
		<!-- Ambient Glows -->
		<div
			class="fixed top-[-10%] left-[-10%] w-[50%] h-[50%] bg-primary/5 blur-[120px] rounded-full -z-10"
		></div>
		<div
			class="fixed bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-blue-500/5 blur-[120px] rounded-full -z-10"
		></div>

		<!-- Sidebar -->
		<aside class="w-64 shrink-0 flex flex-col bg-[#0a0c1a] border-r border-white/5 z-20">
			<!-- Header -->
			<div class="p-6">
				<div
					class="flex items-center gap-3 bg-[#111420] p-2 rounded-lg border border-white/5"
				>
					<img :src="logoUrl" alt="Zevar" class="w-8 h-8 rounded" />
					<span class="font-bold text-white tracking-wide">Zevar</span>
				</div>
			</div>

			<!-- Nav Items -->
			<nav class="flex-1 px-4 space-y-1 overflow-y-auto custom-scrollbar">
				<router-link
					v-for="item in navItems"
					:key="item.to"
					:to="item.to"
					class="flex items-center justify-between px-4 py-3 rounded-xl transition-all group"
					:class="[
						route.path === item.to
							? 'bg-[#111822] text-primary'
							: 'text-gray-400 hover:text-white hover:bg-white/5',
					]"
				>
					<div class="flex items-center gap-3">
						<span class="material-symbols-outlined text-[20px]">{{ item.icon }}</span>
						<span class="text-sm font-medium">{{ item.label }}</span>
					</div>
					<span
						v-if="route.path === item.to"
						class="material-symbols-outlined text-[16px]"
						>chevron_right</span
					>
				</router-link>
			</nav>

			<!-- Bottom Actions -->
			<div class="p-4 space-y-1">
				<!-- Dark Mode -->
				<button
					class="w-full flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-white/5 rounded-xl transition-all"
				>
					<span class="material-symbols-outlined text-[20px]">dark_mode</span>
					<span class="text-sm font-medium">Dark Mode</span>
				</button>

				<!-- Profile -->
				<div class="flex items-center gap-3 px-4 py-3 mt-2">
					<div
						class="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold text-sm"
					>
						{{ userInitials }}
					</div>
					<div class="flex-1 overflow-hidden">
						<p class="text-sm font-bold text-white truncate">
							{{ auth.user?.full_name || "User" }}
						</p>
						<p class="text-xs text-gray-500 truncate">
							{{ auth.user?.email || "user@zevar.com" }}
						</p>
					</div>
				</div>

				<!-- Change Password -->
				<button
					class="w-full flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-white/5 rounded-xl transition-all"
				>
					<span class="material-symbols-outlined text-[20px]">lock</span>
					<span class="text-sm font-medium">Change Password</span>
				</button>

				<!-- Sign Out -->
				<button
					@click="auth.logout()"
					class="w-full flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-white/5 rounded-xl transition-all"
				>
					<span class="material-symbols-outlined text-[20px]">logout</span>
					<span class="text-sm font-medium">Sign out</span>
				</button>
			</div>
		</aside>

		<!-- Main Content -->
		<main class="flex-1 flex flex-col relative overflow-hidden bg-background-dark">
			<!-- Dashboard Content -->
			<div class="flex-1 overflow-y-auto p-8 custom-scrollbar relative">
				<slot />
			</div>
		</main>
	</div>
</template>

<script setup>
import { computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRoute } from "vue-router";

const auth = useAuthStore();
const route = useRoute();

// Logo URL - uses the golden logo from zevar_core public images folder
const logoUrl = "/assets/zevar_core/images/employee_portal_logo.svg";

const navItems = [
	{ to: "/", icon: "dashboard", label: "Dashboard" },
	{ to: "/tasks", icon: "check_circle", label: "Tasks" },
	{ to: "/attendance", icon: "calendar_month", label: "Attendance" },
	{ to: "/leave", icon: "beach_access", label: "Leave" },
	{ to: "/expense", icon: "attach_money", label: "Expense" },
	{ to: "/payroll", icon: "account_balance_wallet", label: "Payroll" },
	{ to: "/open-desk", icon: "open_in_new", label: "Open Desk" },
];

const userInitials = computed(() => {
	const name = auth.user?.full_name || "User";
	return name
		.split(" ")
		.map((n) => n[0])
		.join("")
		.substring(0, 2)
		.toUpperCase();
});
</script>

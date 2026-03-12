<template>
	<div
		class="h-screen w-screen flex items-center justify-center mesh-gradient-bg bg-portal-bg-dark"
	>
		<div class="w-full max-w-md p-8">
			<!-- Logo -->
			<div class="flex items-center gap-3 justify-center mb-10">
				<div
					class="size-14 rounded-2xl bg-gradient-to-br from-portal-primary to-portal-accent-indigo flex items-center justify-center shadow-lg shadow-portal-primary/30"
				>
					<span class="material-symbols-outlined text-white text-4xl"
						>rocket_launch</span
					>
				</div>
				<div>
					<h1 class="text-2xl font-bold text-white tracking-tight">Zevar</h1>
					<p class="text-xs text-white/50 font-medium uppercase tracking-widest">
						Employee Portal
					</p>
				</div>
			</div>

			<!-- Login Form -->
			<div class="premium-card !p-8">
				<h2 class="text-xl font-bold text-white mb-1">Welcome back</h2>
				<p class="text-sm text-white/40 mb-6">Sign in with your Frappe credentials</p>

				<form @submit.prevent="handleLogin">
					<div class="space-y-4">
						<div>
							<label
								class="text-xs text-white/50 font-semibold uppercase tracking-wider mb-1 block"
								>Email</label
							>
							<input
								v-model="email"
								type="text"
								required
								class="w-full bg-white/5 border border-white/10 rounded-xl py-3 px-4 text-sm text-white placeholder:text-white/20 focus:ring-2 focus:ring-portal-primary/40 focus:border-portal-primary/40 transition-all outline-none"
								placeholder="Enter your email"
							/>
						</div>
						<div>
							<label
								class="text-xs text-white/50 font-semibold uppercase tracking-wider mb-1 block"
								>Password</label
							>
							<input
								v-model="password"
								type="password"
								required
								class="w-full bg-white/5 border border-white/10 rounded-xl py-3 px-4 text-sm text-white placeholder:text-white/20 focus:ring-2 focus:ring-portal-primary/40 focus:border-portal-primary/40 transition-all outline-none"
								placeholder="Enter your password"
							/>
						</div>
					</div>

					<p v-if="errorMsg" class="mt-3 text-xs text-red-400">{{ errorMsg }}</p>

					<button
						type="submit"
						:disabled="loading"
						class="w-full mt-6 py-3.5 bg-gradient-to-r from-portal-primary to-portal-accent-indigo text-white font-bold rounded-xl text-sm hover:shadow-lg hover:shadow-portal-primary/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
					>
						<span v-if="loading">Signing in...</span>
						<span v-else>Sign In</span>
					</button>
				</form>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue";
import { createResource } from "frappe-ui";
import { useRouter } from "vue-router";

const router = useRouter();
const email = ref("");
const password = ref("");
const loading = ref(false);
const errorMsg = ref("");

const loginResource = createResource({
	url: "login",
	makeParams() {
		return { usr: email.value, pwd: password.value };
	},
	onSuccess() {
		window.location.reload();
	},
	onError(err) {
		loading.value = false;
		errorMsg.value = err?.messages?.[0] || "Invalid credentials";
	},
});

function handleLogin() {
	errorMsg.value = "";
	loading.value = true;
	loginResource.submit();
}
</script>

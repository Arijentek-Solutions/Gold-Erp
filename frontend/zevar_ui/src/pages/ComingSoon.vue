<template>
	<PortalLayout>
		<div
			class="px-10 pb-10 flex flex-col items-center justify-center min-h-[60vh] font-portal text-center"
		>
			<div
				class="size-24 rounded-full bg-portal-primary/10 flex items-center justify-center mb-6 neon-glow"
			>
				<span class="material-symbols-outlined text-portal-primary text-5xl"
					>engineering</span
				>
			</div>
			<h1 class="text-4xl font-800 tracking-tight mb-4 text-white">Work in Progress</h1>
			<p class="text-white/50 text-lg max-w-md">
				This feature is currently under development. Check back soon!
			</p>
		</div>
	</PortalLayout>
</template>

<script setup>
import PortalLayout from '@/components/PortalLayout.vue'
</script>

<template>
  <PortalLayout v-if="!route.meta.guest">
    <router-view />
  </PortalLayout>
  <router-view v-else />
</template>

<script setup>
import { useRoute } from 'vue-router'
import PortalLayout from '@/components/PortalLayout.vue'

const route = useRoute()
</script>

<script setup lang="ts">
import { components } from "ui-core";
import Demo from "./Demo.vue";
</script>

<template>
  <div>
    <div v-for="(component, name) in components" :key="name">
      <h2>{{ name }}</h2>
      <Demo :component="component" />
    </div>
  </div>
</template>

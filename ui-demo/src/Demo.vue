<script setup lang="ts">
import { createVueComponent, resultToText } from "ui-core";
import { ref } from "vue";

const Comp = createVueComponent("Choose", {
  options: ["a", "b", "c"],
});

const result = ref();
</script>

<template>
  <div v-if="!result">
    <Comp @complete="result = $event" />
  </div>
  <div v-else>
    <p>Result:</p>
    <pre v-text="resultToText(result)"></pre>
  </div>
</template>

<style scoped></style>

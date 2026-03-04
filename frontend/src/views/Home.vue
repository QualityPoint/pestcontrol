<template>
  <div>
	<h1>Home Page</h1>
	<button @click="ping.fetch()">Ping</button>
  </div>
</template>

<script setup>
import { createResource } from 'frappe-ui';

const ping = createResource({
  url: 'frappe.ping',
  onSuccess(d) {
	alert(d);
  },
});
</script>

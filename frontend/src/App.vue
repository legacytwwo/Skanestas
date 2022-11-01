<template>
  <div class="main-app">
      <div class="app-container">
        <div class="ticker-container">
          <div class="text-[20px]">
            Please Select Ticker
          </div>
          <div class="w-[70%]">
            <v-select v-model="selected" :options=tickers ></v-select>
          </div>
        </div>
        <div class="chart-container">
          <Chart :ticker="selected" v-if="selected" />
          <div class="text-[20px]" v-if="!selected"> Waiting For Ticker... </div>
        </div>
    </div>
  </div>
</template>

<script setup>
  import Chart from './Chart.vue'
  import vSelect from 'vue-select'
  import { onMounted, ref } from 'vue'
  import 'vue-select/dist/vue-select.css';

  const tickers = ref()

  const selected = ref()

  onMounted( async () => {
    let url = 'http://localhost:8000/api/tickers';
    await fetch(url)
    .then(response => response.json())
    .then((response) => {
      tickers.value = response['response']
  })})
</script>

<style lang="scss" scoped>
  @import "./App.scss";
</style>
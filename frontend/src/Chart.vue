<template>
    <Line
        :chart-data="chartData"
        :width="800"
        :height="400"
    />
</template>

<script>
    import { Line } from 'vue-chartjs'
    import { onMounted, onUnmounted, ref, computed } from 'vue';
    import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js'

    ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement)

    export default ({
        name: 'Chart',
        components: { Line },
        props: {
            ticker: String
        },
        setup(props) {

            let pooling

            const data = ref([])

            const time = ref([])

            const ws = new WebSocket('ws://localhost:8000/api/service')

            const chartData = computed(() => ({
                labels: time.value,
                datasets: [{
                    label: 'Price',
                    data: data.value,
                    fill: false,
                    borderColor: 'rgb(184, 25, 25)',
                    tension: 0.3
                }]
            }));

            ws.onmessage = function(e) {
                data.value = JSON.parse(e.data).data
                time.value = Array.from(Array(data.value.length).keys())
            }

            onMounted( async () => {
                pooling = setInterval(() => {
                    ws.send(props.ticker)
                }, 1000)
            })

            onUnmounted( async () => {
                clearInterval(pooling)
                ws.close()
            })
            
            return { chartData }
        }
    })
</script>
<template>
  <div class="example">
    <b-alert show variant="secondary">Monitoring System</b-alert>
    <div>
      <b-button variant="primary">Primary</b-button>
      <b-button variant="secondary">Secondary</b-button>
      <b-button variant="success">Success</b-button>
      <b-button variant="danger">Danger</b-button>
      <b-button variant="warning">Warning</b-button>
      <b-button variant="info">Info</b-button>
      <b-button variant="light">Light</b-button>
      <b-button variant="dark">Dark</b-button>
      <b-dropdown right text="Menu">
        <b-dropdown-item>Item 1</b-dropdown-item>
        <b-dropdown-item>Item 2</b-dropdown-item>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-item>Item 3</b-dropdown-item>
      </b-dropdown>
    </div>

    <apexcharts
      width="100%"
      height="350"
      type="line"
      :options="chartOptions"
      :series="series"
    />
    <apexchart
      type="radialBar"
      height="350"
      :options="chartOptionsTemp"
      :series="temp"
      width="100%"
    >TEMP</apexchart>
    <apexchart
      type="radialBar"
      height="350"
      :options="chartOptions"
      :series="humi"
      width="100%"
    ></apexchart>

    <div>
      <b-button v-b-toggle.collapse-1 variant="primary"
        >Toggle Collapse</b-button
      >
      <b-collapse id="collapse-1" class="mt-2">
        <b-card>
          <p class="card-text">Collapse contents Here</p>
          <b-button v-b-toggle.collapse-1-inner size="sm"
            >Toggle Inner Collapse</b-button
          >
          <b-collapse id="collapse-1-inner" class="mt-2">
            <b-card>Hello!</b-card>
          </b-collapse>
        </b-card>
      </b-collapse>
    </div>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts";

export default {
  name: "chart",
  components: {
    apexcharts: VueApexCharts,
  },
  created() {
    this.$socket.on("temp", (dt) => {
      //this.series = [{ name: "temp", data }];
      
      if(this.series.length == 0){
        this.series = [{ name: "temp", data:dt }];
      }
      else
      {
        this.series[0]['data'].push(dt[0])
        const data = this.series[0]['data']
        this.series = [{name:"temp", data}]
      }
      this.temp = [dt[dt.length - 1]];
      
      console.log(this.series)
    });
    this.$socket.on("humi", (data) => {
      this.humi = [data[data.length - 1]];
    });
    
  },
  data: function () {
    return {
      chartOptions: {
        chart: { id: "basic-bar" },
        xaxis: { categories: [1] },
      },
      chartOptionsTemp: {
        chart: { id: "basic-bar" },
        xaxis: { categories: ["TEMP"] },
      },
      series: [],
      humi: [],
      temp: [],
    };
  },
  updated() {},
};
</script>
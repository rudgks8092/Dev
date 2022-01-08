<template>
  <div id="app">
    <Chart></Chart>
  </div>
</template>

<script>
import Chart from "./components/Chart";

export default {
  name: "App",
  components: {
    Chart,
  },
  created(){
    this.$socket.on("temp",(data)=>{
      //console.log(data)
    })
  }
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>

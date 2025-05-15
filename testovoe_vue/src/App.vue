<script setup>
import {ref} from 'vue'
var balance = ref(0)
var rolling = ref(false)
var dices = ref([0,0,0,0,0,0])
var activecombo = ref({'pair':false, 'full house': false, 'yahtzee': false, 'three pairs':false,'other':false})
console.log(activecombo.value)
var response
async function getBalance() {
  response = await fetch('http://localhost:8000/balance')
  balance.value = await response.json()
}
getBalance()
async function roll(bet) {
  rolling.value=true
  setTimeout(async () => {
  var response_bet= await fetch('http://localhost:8000/bet/'+bet)
  var response_roll = await fetch('http://localhost:8000/roll')
  let tmp =0
  tmp = await response_roll.json()
  dices.value = tmp['dices']
  activecombo = tmp['comb']
  console.log(activecombo['pair'])
  getBalance()
  rolling.value=false
  }, 1000)
}
</script>


<template>
<div style="border:solid; width:425px; height:100px; text-align:center;margin:10px">DICE <br>
  <div style="display: flex;flex-direction:row;margin-left:50px" v-if='dices'>
    <div style="border:solid;text-align:center;margin: 20px;width:10px">{{dices[0]}}</div>
    <div style="border:solid;text-align:center;margin: 20px;width:10px">{{dices[1]}}</div>
    <div style="border:solid;text-align:center;margin: 20px;width:10px">{{dices[2]}}</div>
    <div style="border:solid;text-align:center;margin: 20px;width:10px">{{dices[3]}}</div>
    <div style="border:solid;text-align:center;margin: 20px;width:10px">{{dices[4]}}</div>
    <div style="border:solid;text-align:center;margin: 20px;width:10px">{{dices[5]}}</div>
  </div>
  <h2 v-if='rolling'>ROLLING</h2>
</div>
<div style="display: flex;">
  <div style="border:solid; width:200px; height:215px; text-align:center;margin:10px">Prices
    <ul v-if="activecombo">
      <li :style="{color: activecombo['pair']? 'red':'black'}">Pair x1</li>
      <li :style="{color: activecombo['full house']==true ? 'red':'black'}">Full house x2</li>
      <li :style="{color: activecombo['yahtzee']==true ? 'red':'black'}">Yahtzee x3</li>
      <li :style="{color: activecombo['three pairs']==true ? 'red':'black'}">Three pairs x4</li>
      <li :style="{color: activecombo['other']==true ? 'red':'black'}">Other x0</li>
    </ul>
  </div>
    <div style="flex-direction:column">
      <div style="border:solid; width:200px; height:100px; text-align:center;margin:10px">BET
        <br>
        <input style='width:70px'v-model="bet" placeholder="BET">
        <button style='width:90px'@click="roll(bet)">ROLL</button>
    </div>
<div style="border:solid; width:200px; height:100px; text-align:center;margin:10px">Your balance <br>{{ balance }}</div>
    </div>
</div>
</template>

<style scoped>
ul {
  text-align: left;
  list-style-type: "";
}
</style>

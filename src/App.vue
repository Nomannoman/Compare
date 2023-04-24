<template>
  <div class="main" 
  style=""
>
  <div class="intro">
    Compare products on different websites
  </div>
    <div class="url" v-show="!disp[0]">
        <label class="label" >Enter item : </label>
        <b-form-input size="md"
        v-on:keyup.enter="getFromBackend(text)" class='input' v-model="text" placeholder="Enter the item to compare"></b-form-input>
        <b-button @click="getFromBackend(text)" class='button' variant="success">Go!</b-button>
    </div>

    <div class="amazon-bar">
    <div class="amazon-price" v-show = !disp[0]> {{ amazonPrice }}</div>
    <div class="amazon-title" v-show = !disp[0]>{{ amazonTitle }}</div>
    <img class="amazon-image" :src="amazonImageURL" v-show = toShowImage[0]>
    <div class="amazon-time" v-show = !disp[0]>{{ amazonTime }}</div>
    <div class="amazon-delivery" v-show = !disp[0]>{{ AmazonDelivery }}</div>
  </div>
  <div class="flipkart-bar">
    <div class="flipkart-price" v-show = !disp[0]> {{ flipkartPrice }}</div>
    <div class="flipkart-title" v-show = !disp[0]>{{ flipkartTitle }}</div>
    <img class="flipkart-image" :src="flipkartImageURL" v-show = toShowImage[0]>
    <div class="flipkart-specification" v-show = !disp[0]>{{ flipkartSpecification }}</div>
    <div class="flipkart-brand" v-show = !disp[0]>{{ flipkartBrand }}</div>
    <div class="flipkart-delivery" v-show = !disp[0]>{{ flipkartDelivery }}</div>
  </div>
    <div v-show="disp[0]" class="timer"> Results arriving in {{ timerCount }} seconds...</div>
  </div>
</template>

<script>
import {getAmazonHTML} from './frontend/index';
export default {
  name: 'App',
  data(){
    return{
    text:'',
    image:'',
    gg:"<div>hello</div>",
    timerCount: 20,
    disp:[false],
    toShowImage : [false],
    amazonImageURL: '',
    amazonTitle : '',
    amazonPrice : undefined,
    amazonTime : undefined,
    AmazonDelivery : undefined,
    flipkartTitle:'',
    flipkartPrice : undefined,
    flipkartImageURL : '',
    flipkartSpecification : undefined,
    flipkartBrand:undefined,
    flipkartDelivery:undefined,
    }
  },
  methods:{
    async getFromBackend(url){
      this.timerCount = 20;
      this.$set(this.disp,0,true); 
      this.$set(this.toShowImage,0,false); 
      this.reducer();
      var replaced = url;
      const x = await getAmazonHTML(replaced);
      const data = x.data.html;

      const re = /data-asin="[a-zA-Z0-9]*" data-index="[0-9]+"/g;

      const indices=[];
      var match;
      while ((match = re.exec(data)) != null) {
        indices.push(match.index);
      }

      var i = 0;

      var finalString ;
      while(i<indices.length-1){
        var start = indices[i]-5;
        var end = indices[i+1]-5;

        var get = data.slice(start,end);
        if(get.indexOf('sponsored') === -1 && get.indexOf('Sponsored')=== -1 && get.indexOf('messaging-widget')===-1 && get.indexOf('₹')!==-1){
          this.gg=get;
          finalString = get;
          break;
        }
        i++;
      }
      let index = finalString.indexOf('src="')+5;
      const lastindex = finalString.indexOf('"',index);

      const imageURL = finalString.slice(index,lastindex);
      this.amazonImageURL = imageURL;

      // Putting Title
      this.amazonTitle='';

      index = finalString.indexOf('<span class="a-size-base-plus a-color-base a-text-normal">');
      if (index===-1){
        index = finalString.indexOf('<span class="a-size-medium a-color-base a-text-normal">');
      }
      let index2 = finalString.indexOf('</a>',index)+3;

      let a = finalString.indexOf('>',index);
      while(a<index2){
        let a = finalString.indexOf('>',index);
        const b = finalString.indexOf('<',a);
        if(a===-1 || b===-1) break;
        this.amazonTitle+=finalString.slice(a+1,b);
        index = a+1;
        if(a>=index2) break;
      }
      this.amazonTitle = this.amazonTitle.replaceAll('&amp; ','');
      // Getting Price
      index = finalString.indexOf('price-whole">')+13;
      index2 = finalString.indexOf('<',index);

      this.amazonPrice = 'Rs. '+finalString.slice(index,index2);
      


      // Getting delivery time

      index = finalString.indexOf('Get it by');
      index2 = finalString.indexOf('"',index);

      this.amazonTime = finalString.slice(index,index2);


      // Getting free delivery

      let finalTaking;
      index = finalString.indexOf("FREE Delivery");
      if(index!==-1){
        index2 = finalString.indexOf('<',index);
        let index3 = finalString.indexOf('"',index);

        finalTaking = index2;
        if(index2!==-1 && index2<index3) finalTaking = index2;
        else if(index2===-1) finalTaking = index3;
        else if(index3!==-1 && index3<index2) finalTaking = index3;
      }
      this.AmazonDelivery = finalString.slice(index,finalTaking);

      // Flipkart starts here
      const flipkart = x.data.html2;

      console.log(flipkart);

      index = flipkart.indexOf('<div class="_13oc-S">')+21;
      index2 = flipkart.indexOf('<div class="_13oc-S">',index);

      this.gg = flipkart.slice(index,index2);

      while(this.gg.indexOf('<div class="_2I5qvP"><span>Ad</span></div>')!==-1){
        index = flipkart.indexOf('<div class="_13oc-S">',index)+21;
        index2 = flipkart.indexOf('<div class="_13oc-S">',index);
        this.gg = flipkart.slice(index,index2);
      }

      finalString = this.gg;
      console.log(finalString);

      //Flipkart Setting title
      
      index = finalString.indexOf('"_4rR01T"');
      if(index!==-1){
        index+=10;
        index2 = finalString.indexOf('<',index);
      }else{
        index = finalString.indexOf('title="')+7;
        index2 = finalString.indexOf('"',index);
      }
      this.flipkartTitle = finalString.slice(index,index2);

      //Flipkart Setting Price
      index = finalString.indexOf('₹')+1;
      index2 = finalString.indexOf('<',index);

      this.flipkartPrice= 'Rs. ' + finalString.slice(index,index2);
      
      // Flipkart Image
      index = finalString.indexOf('src')+5;
      index2 = finalString.indexOf('"',index);

      this.flipkartImageURL = finalString.slice(index,index2);

      console.log(finalString);
      // flipkart Specificattion

      this.flipkartSpecification = undefined;
      index = finalString.indexOf('"_3eWWd-"');
      index2 = finalString.indexOf('<',index+10);
      if(index!==-1 )
      this.flipkartSpecification = 'Specification : '+ finalString.slice(index+10,index2);

      // Flipkart Brand

      this.flipkartBrand = undefined;
      index = finalString.indexOf('"_2WkVRV"');
      index2 = finalString.indexOf('<',index+10);
      if(index!==-1)
      this.flipkartBrand = 'Brand : '+finalString.slice(index+10,index2);

      // Flipkart Delivery
      this.flipkartDelivery = undefined;
      index = finalString.indexOf('Free delivery')
      if(index!==-1){
        this.flipkartDelivery = 'Free Delivery'
      }

      this.timerCount = 0;
      this.$set(this.toShowImage,0,true); 
      this.$set(this.disp,0,false);
    },
    reducer(){
    let interval = setInterval(() => {
      if (this.timerCount === 0) {
        clearInterval(interval);              
      } else {
        this.timerCount--;
      }             
    }, 1000);
  },
  },
}
</script>

<style>
html, body {
 height: 100%;
 background: linear-gradient(to right, #2E86C1, #9B59B6);
}
.intro{
  width: fit-content;
  margin-left:30% !important;
  font-size:1.2rem !important;
  background-color: azure;
  padding-left: 2rem;
  padding-right: 2rem;
}
.url{
  margin : 3rem 5rem auto 5rem ;
}
.input{
  width:60% !important;
  display: inline !important;
  margin-top:-0.5rem !important;
}
.label{
  width: 9% !important;
  font-size:1.2rem !important;
  background-color: rgb(129, 109, 109);
  margin-right:1.5rem;
  padding-left:0.8rem;
}
.button{
  margin-left: 1.5rem !important;
  margin-top:-0.2rem !important;
}
.timer{
  background-color: white;
  margin-top : 3rem;
  text-align: center;
  height: 20%;
  font-size:2rem;
}
.flipkart-title , .amazon-title{
  font-size: 1.35rem !important;
  margin-left:3rem !important;
  color : cornsilk !important;
}
.flipkart-price, .amazon-price{
  font-size:2.5rem;
  color : red;
}
.amazon-bar{
  width: 40%;
  margin-left:5rem;
  margin-top:2rem;
  display: inline-flex;
  align-items: center;
  flex-direction: column;
}
.amazon-time{
  color: cyan;
}
.amazon-delivery{
  color: fuchsia;
}
.amazon-time , .amazon-delivery{
  font-size:1.5rem;
}
.flipkart-image , .amazon-image{
  margin-top:1.5rem !important;
   width: 13rem !important;
  height: 20rem !important;
}
.flipkart-bar{
  width: 40%;
  margin-left:5rem;
  margin-right:5rem;
  margin-top:2rem;
  display: inline-flex;
  align-items: center;
  flex-direction: column;
  float: right;
}

.flipkart-specification , .flipkart-brand , .flipkart-delivery{
  font-size: 1.5rem;
}
.flipkart-delivery{
  color: fuchsia;
}
</style>

import{U as a}from"./index-DnmX-5Vw.js";const o=a("tab",{state:()=>({tabData:"test1"}),getters:{tabDataGet(t){return t.tabData}},actions:{tabDataChange(t){this.tabData=t}},persist:{enable:!0}}),n=a("menu",{state:()=>({menuData:{tab:"test1",title:"",icon:"home",link:"/",routerTo:"/"},homeData:{tab:"test1",title:"",icon:"home",link:"/",routerTo:"/"}}),getters:{menuDataGet(t){return t.menuData},homePageGet(t){return t.homeData}},actions:{menuDataChange(t){this.menuData=t},homePage(t){this.homeData=t}}});export{n as a,o as u};

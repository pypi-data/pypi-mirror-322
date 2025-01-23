import{g as l,u as c,c as u,a as e,w as d,b as s,o as m,d as a}from"./index-D02h7Qn5.js";import{_}from"./VContainers-B6XCNh9U.js";import{_ as f,a as g}from"./VHeader-487PXF2Z.js";import{_ as o}from"./VStat-B55_we8R.js";import"./VWarningAlert-C3K3v3kq.js";const p=l`
  query getDashboard {
    version
    dockerVersion
    stackCount
    containers(stopped: false) {
      id
      name
      image
      service
      state
    }
  }
`,k={class:"mx-auto max-w-7xl"},v={class:"grid grid-cols-1 gap-4 sm:grid-cols-3"},C={__name:"DashboardView",setup(h){const{result:t,loading:r,error:i}=c(p);return(x,n)=>(m(),u("div",null,[e(g,{title:"Dashboard"}),e(f,{loading:s(r),error:s(i),result:s(t),"result-key":"version"},{default:d(()=>[a("section",null,[a("div",k,[a("div",v,[e(o,{name:"Odooghost version",stat:s(t).version},null,8,["stat"]),e(o,{name:"Docker version",stat:s(t).dockerVersion},null,8,["stat"]),e(o,{name:"Stacks count",stat:s(t).stackCount},null,8,["stat"])])])]),a("section",null,[n[0]||(n[0]=a("h3",null,"Running Containers",-1)),e(_,{containers:s(t).containers},null,8,["containers"])])]),_:1},8,["loading","error","result"])]))}};export{C as default};

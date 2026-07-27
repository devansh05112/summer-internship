document.addEventListener("DOMContentLoaded",()=>{

const copyBtn=document.getElementById("copyBtn");

const summary=document.getElementById("summaryText");

if(copyBtn){

copyBtn.onclick=()=>{

navigator.clipboard.writeText(summary.innerText);

copyBtn.innerHTML="<i class='fas fa-check'></i> Copied!";

setTimeout(()=>{

copyBtn.innerHTML="<i class='fas fa-copy'></i> Copy";

},2000);

};

}

});
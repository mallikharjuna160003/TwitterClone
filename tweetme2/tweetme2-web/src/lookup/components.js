import React,{useEffect,useState}  from "react"
import {apiTweetList} from "../tweets/lookup"

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export function backendLookup(method, endpoint, myCallback, data){
    let jsonData;
    console.log(data)
    if(data){
        jsonData = JSON.stringify(data)
    }
    const xhr = new XMLHttpRequest()
    const url = `http://127.0.0.1:8000/api${endpoint}`
    const csrftoken = getCookie('csrftoken')
    xhr.responseType = "json"
    xhr.open(method,url)
    xhr.setRequestHeader("Content-Type","application/json")
    
    if(csrftoken){
        xhr.setRequestHeader("HTTP_X_REQUESTED_WITH","XMLHttpRequest")
        xhr.setRequestHeader("x-requested-with","XMLHttpRequest")
        xhr.setRequestHeader("X-CSRFToken",csrftoken)
    }
   
    xhr.onload = function(){
       console.log(xhr.response)
       myCallback(xhr.response,xhr.status)
  
    }
    console.log(jsonData)
    xhr.onerror = function(){
      myCallback({"message":"Error occurred"},400)
    }
    xhr.send(jsonData); 
}


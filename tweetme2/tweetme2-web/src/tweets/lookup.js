import { backendLookup } from "../lookup/components"
export function apiTweetCreate(newTweet, callback){
    backendLookup("POST","/tweets/create/",callback,{content:newTweet})
}
export function apiTweetAction(tweetId,action, callback){
    const data = {id: tweetId,action:action}
    backendLookup("POST","/tweets/action/",callback,data)
    
}

export function apiTweetList(myCallback){
    const method="GET"
    const endpoint = "/tweets/"
    backendLookup(method,endpoint,myCallback)
}

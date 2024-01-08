import React,{useEffect,useState}  from "react"
import { apiTweetCreate,apiTweetList,apiTweetAction } from "./lookup"

export function TweetsComponent(props){

    const textAreaRef = React.createRef()
    const [newTweets, setNewTweets] = useState([])
    
    // backend response 
    const handleBackedUpdate = (response,status)=>{
        const tempNewTweets = [...newTweets]
        if(status===201){
            console.log(response)
            tempNewTweets.unshift(response)
            setNewTweets(tempNewTweets)
        }
        else{
            console.log(response)
            alert(
                "Error Occurred!!"
            )
        }
    }
    // backend request
    const handleSubmit = (event)=>{
        event.preventDefault()
        const newVal = textAreaRef.current.value
        console.log("NwVal",newVal)
        apiTweetCreate(newVal,handleBackedUpdate)
        textAreaRef.current.value=""
    }
    
    return(
        <div className={props.className}>
            <div className="col-12 mx-30 px-30">
                <form onSubmit={handleSubmit}>
                <textarea ref={textAreaRef} required={true} className="form-control">
                </textarea>
                <button type="submit" className="btn btn-primary my-3">Tweet</button>
                </form>
            </div>
            <TweetList newTweets={newTweets}/>
        </div>
        
    )
}

export function ActionBtn(props){

    const {tweet,action} = props
    const [likes,setLikes] = useState(tweet.likes ? tweet.likes:0)
    const [userLike, setUserLike] = useState(tweet.userLike ===true?true:false)
    const className=tweet.className?tweet.className:'btn btn-primary btn-sm mt-3'
    const actionDisplay = action.display?action.display:"Action"
    const handleActionBackendEvent = (response,status)=>{
        console.log(response,status)
        if(status===200){
            setLikes(response.likes)
            //setUserLike(true)
        }
    }
    const handleClick =(e)=>{
      e.preventDefault()
      apiTweetAction(tweet.id,action.type,handleActionBackendEvent)
     
    }
    const display = action.type==="like" ? `${likes} ${action.type}`: actionDisplay
    return <button onClick={handleClick} className={className}>{display}</button>
}

function ParentTweet(props){
    const {tweet} = props
    return tweet.parent ?
    <div className="row">
        <div className="col-11 mx-auto p-3 border rounded">
            <div>
            <p className="mb-0 small text-white font-weight-bold">Retweet</p>
            </div>
                <Tweet tweet={tweet.parent} />  
        </div>
    </div>:null  
}
export function Tweet(props){
    const {tweet} = props  
    const className = props.className?props.className:'col-10 mx-auto col-md-6';
    return(
      <div className={className}>
        <div>
           <p>
              {tweet.id} - {tweet.content}
            </p>
           <ParentTweet tweet={tweet}/>
        </div>
          <div className='btn btn-group'>
          <ActionBtn tweet={tweet} action={{type:"like",display:"Like"}} />
          <ActionBtn tweet={tweet} action={{type:"unlike",display:"UnLike"}} />
          <ActionBtn tweet={tweet} action={{type:"retweet",display:"Retweet"}} />
          </div>
      </div>
    )
}

export function TweetList(props){
  const [tweetsInit,setTweetsInit] = useState([])
  const [tweets,setTweets] = useState([])
  const [tweetsDidSet, setTweetsDidSet] = useState(false)
  //setTweetsInit(props.newTweets)
  //console.log(props.newTweets)
  const handleTweetListLookup = (response, status) =>{
    if(status===200){
      setTweetsInit(response)
      setTweetsDidSet(true)
    }
    else{
      alert("There is an eeror")
    }
  }
  // do my lookup
  useEffect(()=>{
    const final = [...props.newTweets].concat(tweetsInit)
    if(final.length!== tweets.length){
        setTweets(final)
        apiTweetList(handleTweetListLookup)  
    }
  },[props.newTweets,tweets,tweetsInit])


  useEffect(()=>{
    if(tweetsDidSet===false){
        apiTweetList(handleTweetListLookup)  
    }
    
  },[tweetsInit,tweetsDidSet,setTweetsDidSet])

  return(
    tweets.map((tweet,index)=>(
    <Tweet tweet={tweet} key={index} className="my-5 py-5 bg-dark text-white"/>
    ))
  )
}


export function Button({text,color,func,msg}){

    return (
        <button onClick={()=> func(msg)} style={{backgroundColor:color}}>
            <p>{text}</p>
        </button>
    )
}
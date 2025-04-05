//holds the upload functions as well as the text that SAYS to upload a a file.
const UploadForm = () => {
    const header = "Upload an image:";
    
    const onClickEvent = () =>{
        alert("Clicking works!")
    }

    return(
        <div>
            <h1>{header}</h1>
            <button onClick={onClickEvent}>Upload Image</button>
        </div>
    )
  };
  
  export default UploadForm;
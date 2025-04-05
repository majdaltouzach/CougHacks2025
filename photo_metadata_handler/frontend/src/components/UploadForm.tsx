//holds the upload functions as well as the text that SAYS to upload a a file.
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import "./UploadForm.css";

const UploadForm = () => {
  const [file, setFile] = useState<File | null>(null);
  const navigate = useNavigate();
  const askInput = "Upload an Image";
  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post("http://localhost:8000/upload/", formData);
    localStorage.setItem("metadata", JSON.stringify(res.data.metadata));
    localStorage.setItem("filename", res.data.filename);
    navigate("/metadata");
  };

  return (
    <div className="uploadContainer">
      <img src="/stockImgIcon.png" alt="logo192.png" className="uploadImage" />
      <h1 className="header"> {askInput} </h1>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
};

export default UploadForm;

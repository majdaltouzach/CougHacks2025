// UploadForm.tsx
import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const UploadForm = () => {
  const [file, setFile] = useState<File | null>(null);
  const navigate = useNavigate();

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
    <div>
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

// MetadataEditor.tsx
import { useState } from "react";
import axios from "axios";
import "./MetadataEditor.css";

const MetadataEditor = () => {
  const [metadata, setMetadata] = useState<Record<string, string>>(() =>
    JSON.parse(localStorage.getItem("metadata") || "{}")
  );
  const filename = localStorage.getItem("filename");

  const imageUrl = `http://localhost:8000/image/${filename}`;

  const handleAdd = () => {
    const tag = prompt("Tag name?");
    const value = prompt("Tag value?");
    if (tag && value) {
      axios.post("/update-metadata", { filename, action: "add", tag, value });
      setMetadata({ ...metadata, [tag]: value });
    }
  };

  const handleDelete = (tag: string) => {
    axios.post("/update-metadata", { filename, action: "delete", tag });
    const copy = { ...metadata };
    delete copy[tag];
    setMetadata(copy);
  };

  const handleEraseAll = () => {
    axios.post("/update-metadata", { filename, action: "erase" });
    setMetadata({});
  };

  const handleDownload = () => {
    window.open(`http://localhost:8000/image/${filename}`, "_blank");
  };

  return (
    <div className="metadata-editor-container">
      <h3>Preview</h3>
      <img src={imageUrl} alt="Uploaded" className="preview-image" />

      <ul className="metadata-list">
        {Object.entries(metadata).map(([k, v]) => (
          <li key={k} className="metadata-item">
            <span>
              {k}: {v}
            </span>
            <button onClick={() => handleDelete(k)} className="button-danger">
              Delete
            </button>
          </li>
        ))}
      </ul>

      <div className="metadata-actions">
        <button onClick={handleAdd} className="button">
          Add Tag-Value
        </button>
        <button onClick={handleEraseAll} className="button">
          Delete All Tag-Values
        </button>
        <button onClick={handleDownload} className="button">
          Download Image
        </button>
      </div>
    </div>
  );
};

export default MetadataEditor;

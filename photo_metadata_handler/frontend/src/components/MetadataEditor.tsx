// MetadataEditor.tsx
import { useState } from "react";
import axios from "axios";

const MetadataEditor = () => {
  const [metadata, setMetadata] = useState<Record<string, string>>(() =>
    JSON.parse(localStorage.getItem("metadata") || "{}")
  );
  const filename = localStorage.getItem("filename");

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
    <div>
      <ul>
        {Object.entries(metadata).map(([k, v]) => (
          <li key={k} className="flex justify-between">
            <span>
              {k}: {v}
            </span>
            <button onClick={() => handleDelete(k)}>Delete</button>
          </li>
        ))}
      </ul>
      <div className="mt-4">
        <button onClick={handleAdd}>Add Tag-Value</button>
        <button onClick={handleEraseAll}>Delete All Tag-Values</button>
        <button onClick={handleDownload}>Download Image</button>
      </div>
    </div>
  );
};

export default MetadataEditor;

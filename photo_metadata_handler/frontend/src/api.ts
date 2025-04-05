import axios from "axios";

const BASE_URL = "http://localhost:8000"; // or use env: import.meta.env.VITE_API_URL

export const uploadImage = (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  return axios.post(`${BASE_URL}/upload/`, formData);
};

export const updateMetadata = (
  filename: string,
  action: "add" | "edit" | "delete" | "erase",
  tag?: string,
  value?: string
) => {
  return axios.post(`${BASE_URL}/update-metadata/`, {
    filename,
    action,
    tag,
    value,
  });
};

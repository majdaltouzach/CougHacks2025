import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import UploadPage from "./pages/UploadPage";
import MetadataPage from "./pages/MetadataPage";

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<UploadPage />} />
          <Route path="/metadata" element={<MetadataPage />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
